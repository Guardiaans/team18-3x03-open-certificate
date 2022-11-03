# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import datetime as dt
import os
import socket
from io import BytesIO

import pyqrcode
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from opencert.admin.forms import OpencertLogger, sendlogs
from opencert.email.forms import generate_confirmation_token, send_email
from opencert.extensions import db, login_manager
from opencert.public.forms import ForgetPasswordForm, LoginForm
from opencert.recaptcha.forms import recaptcha
from opencert.user.forms import RegisterForm
from opencert.user.models import LoginAttempt, User
from opencert.utils import flash_errors

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""

    # Get the client IP address
    IPAddr = socket.gethostbyname(socket.gethostname())
    current_app.logger.info("Visiting from IP address: %s", IPAddr)

    form = LoginForm(request.form)
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


@blueprint.route("/home", methods=["GET"])
@login_required
def member_home():
    """Members Service page."""
    return render_template("users/members.html")


@blueprint.route("/logout/")
@login_required
async def logout():
    """Logout."""
    await sendlogs()
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    """User login route."""
    # if user is logged in we get out of here
    if current_user.is_authenticated:
        return redirect(url_for("public.home"))

    time_now = dt.datetime.now()
    IPAddr = socket.gethostbyname(socket.gethostname())  # Get the client IP address
    login_user_ip = LoginAttempt.query.filter_by(
        ip=IPAddr
    ).first()  # Who is the current user?

    # If first time visitor, create a new record
    if login_user_ip is None:
        login_user_ip = LoginAttempt(ip=IPAddr, attempted_at=time_now)
        db.session.add(login_user_ip)
        db.session.commit()

    attempt = login_user_ip.login_attempt_count
    time_since_last_attempt = 0

    current_app.logger.info(
        f"Login attempt: {attempt} from IP address: {IPAddr}, last attempted at: {login_user_ip.attempted_at}"
    )

    # Check if the time difference is more than 15 minutes, if more than 15 minutes, reset the login attempt count
    if login_user_ip.attempted_at is not None:
        # current_app.logger.info(f"Current time: {time_now}")
        last_attempt = login_user_ip.attempted_at
        time_since_last_attempt = time_now - last_attempt
        # current_app.logger.info(
        #     f"Time since last attempt: {time_since_last_attempt.seconds} seconds"
        # )

        if time_since_last_attempt.seconds > 900:
            login_user_ip.login_attempt_count = 5
            db.session.commit()

    # this is where the form is validated
    form = LoginForm(request.form)
    if form.validate_on_submit() and login_user_ip.login_attempt_count > 0:
        if recaptcha() is not True:
            abort(401)
        user = User.query.filter_by(username=form.username.data).first()
        # log user in
        login_user(user)
        OpencertLogger()
        flash("You are now logged in!", "success")
        # reset login attempt
        return redirect(url_for("public.member_home"))

    else:
        if form.errors.items():
            if attempt <= 0:
                minutes = round(time_since_last_attempt.seconds / 60)
                flash(
                    f"You have exceeded the number of login attempts! Please try again in {15 - minutes} minutes.",
                    "danger",
                )
                return redirect(url_for("public.login"))
            elif attempt == 1:
                # get client ip address
                flash(
                    f"Invalid username, password, token or account unactivated! You have {attempt} login attempt remaining before being locked out.",
                    "warning",
                )
                # update login attempt
                attempt -= 1
                login_user_ip.login_attempt_count = attempt
                login_user_ip.attempted_at = time_now
                db.session.commit()
            else:
                flash(
                    f"Invalid username, password, token or account unactivated! You have {attempt} login attempts remaining.",
                    "warning",
                )
                # update login attempt
                attempt -= 1
                login_user_ip.login_attempt_count = attempt
                login_user_ip.attempted_at = time_now
                db.session.commit()
    return render_template(
        "public/login.html", form=form, site_key=os.environ.get("RECAPTCHA_SITE_KEY")
    )


@blueprint.route("/about/")
def about():
    """About page."""
    return render_template("public/about.html")


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""

    form = RegisterForm(request.form)

    if form.validate_on_submit():
        if recaptcha() is not True:
            abort(401)
        User.create(
            username=form.username.data,
            email=form.email.data,
            email_confirmed=False,
            password=form.password.data,
            wallet_add=form.wallet_add.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            active=True,
            role_id=2,
        )
        # flash("Thank you for registering. You can now log in.", "success")
        # Log the user in after registering
        user = User.query.filter_by(email=form.email.data).first()
        token = generate_confirmation_token(form.email.data)
        confirm_url = url_for("email.confirm_email", token=token, _external=True)
        html = render_template("email/confirm.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(form.email.data, subject, html)
        flash(
            "Thank you for registering. Please check your email and activate your account.",
            "success",
        )
        # login_user(user)
        session["username"] = user.username
        return redirect(url_for("public.two_factor_setup"))
    else:
        flash_errors(form)
    return render_template(
        "public/register.html", form=form, site_key=os.environ.get("RECAPTCHA_SITE_KEY")
    )


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


@blueprint.route("/forget_password", methods=["GET", "POST"])
def forget_password():
    form = ForgetPasswordForm(request.form)

    if form.validate_on_submit():
        if recaptcha() is not True:
            abort(401)
        email = form.email.data
        token = generate_confirmation_token(email)
        html = render_template("email/link_reset_password.html", token=token)
        subject = "Password Reset"
        send_email(email, subject, html)

        flash("We have send instruction to your email ", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template(
        "public/forget_password.html",
        form=form,
        site_key=os.environ.get("RECAPTCHA_SITE_KEY"),
    )
