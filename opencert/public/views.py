# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from io import BytesIO
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    session,
    abort,
)
from flask_login import login_required, login_user, logout_user, current_user
import os, requests
from opencert.extensions import login_manager
from opencert.public.forms import LoginForm
from opencert.user.forms import RegisterForm
from opencert.user.models import User
from opencert.utils import flash_errors
import pyqrcode
from opencert.email.forms import generate_confirmation_token, send_email


blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    """User login route."""
    if current_user.is_authenticated:
        # if user is logged in we get out of here
        return redirect(url_for("public.home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():  # this is where the form is validated
        user = User.query.filter_by(username=form.username.data).first()
        # log user in
        login_user(user)
        flash("You are now logged in!")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
        
    return render_template("public/login.html", form=form)


@blueprint.route("/about/")
def about():
    """About page."""
    return render_template("public/about.html")


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""

    form = RegisterForm(request.form)
    
    if form.validate_on_submit():
        #get recaptcha response
        secret_response = request.form['g-recaptcha-response']
        #get key from env
        SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
        RECAPTCHA_URL =os.environ.get("RECAPTCHA_VERIFY_URL")
        #verify its not a bot
        verify_response = requests.post(url=f'{RECAPTCHA_URL}?secret={SECRET_KEY}&response={secret_response}').json()
        if verify_response['success'] == False or verify_response['score'] < 0.5:
            abort(401)
        new_user_email = form.email.data
        User.create(
            username=form.username.data,
            email=form.email.data,
            email_confirmed=False,
            password=form.password.data,
            wallet_add=form.wallet_add.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            active=True,
            role_id = request.form.get("user_type")
        )
        # flash("Thank you for registering. You can now log in.", "success")
        # Log the user in after registering
        user = User.query.filter_by(email=form.email.data).first()
        token = generate_confirmation_token(new_user_email)
        confirm_url = url_for('email.confirm_email', token=token, _external=True)
        html = render_template('email/confirm.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(new_user_email, subject, html)
        flash("Thank you for registering. Please check your email and activate your account.", "success")
        # login_user(user)
        session["username"] = user.username
        return redirect(url_for("public.two_factor_setup"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form, site_key=os.environ.get("RECAPTCHA_SITE_KEY"))


@blueprint.route("/two-factor/")
def two_factor_setup():
    """2FA page."""
    if "username" not in session:
        return redirect(url_for("public.home"))
    user = User.query.filter_by(username=session["username"]).first()
    if user is None:
        return redirect(url_for("public.home"))
    return (
        render_template("public/two_factor_setup.html"),
        200,
        {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@blueprint.route("/qrcode")
def qrcode():
    if "username" not in session:
        abort(404)
    user = User.query.filter_by(username=session["username"]).first()
    if user is None:
        abort(404)

    # for added security, remove username from session
    del session["username"]

    # render qrcode for FreeTOTP
    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=3)
    return (
        stream.getvalue(),
        200,
        {
            "Content-Type": "image/svg+xml",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )
