# -*- coding: utf-8 -*-
"""User views."""
import datetime as dt
import os
import socket

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
from flask_login import current_user, login_required, login_user

from opencert.admin.forms import OpencertLogger
from opencert.email.forms import generate_confirmation_token, send_email
from opencert.extensions import db
from opencert.public.forms import ForgetPasswordForm, LoginForm
from opencert.recaptcha.forms import recaptcha
from opencert.user.forms import RegisterForm, UpdateForm
from opencert.user.models import LoginAttempt, User
from opencert.utils import flash_errors

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/home", methods=["GET"])
@login_required
def member_home():
    """Members Service page."""
    return render_template("users/members.html")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    """User login route."""
    # if user is logged in we get out of here
    if current_user.is_authenticated:
        return redirect(url_for("user.member_home"))

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
        return redirect(url_for("user.member_home"))

    else:
        if form.errors.items():
            if attempt <= 0:
                minutes = round(time_since_last_attempt.seconds / 60)
                flash(
                    f"You have exceeded the number of login attempts! Please try again in {15 - minutes} minutes.",
                    "danger",
                )
                return redirect(url_for("user.login"))
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


@blueprint.route("/update", methods=["GET", "POST"])
@login_required
def update():
    """Update user information."""
    form = UpdateForm(request.form)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    # Load values to display to user
    if request.method == "GET":
        form.wallet_add.data = user.wallet_add
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name

    if request.method == "POST":
        if form.validate_on_submit():
            user.wallet_add = form.wallet_add.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data

            # If users does not want to update password they can leave it blank.
            if form.curr_password.data != "":
                user.password = form.password.data

            User.update(user)
            flash("Account has successfully been updated.", "success")
            return redirect(url_for("user.members"))
        else:
            flash_errors(form)

    return render_template(
        "users/updateuser.html",
        form=form,
        site_key=os.environ.get("RECAPTCHA_SITE_KEY"),
    )


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
        return redirect(url_for("auth.two_factor_setup"))
    else:
        flash_errors(form)
    return render_template(
        "users/register.html", form=form, site_key=os.environ.get("RECAPTCHA_SITE_KEY")
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
        "users/forget_password.html",
        form=form,
        site_key=os.environ.get("RECAPTCHA_SITE_KEY"),
    )
