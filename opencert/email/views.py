from flask import Blueprint, flash, redirect, render_template, request, url_for

from opencert.email.forms import (
    ResendConfirmationForm,
    ResetPasswordForm,
    confirm_token,
    generate_confirmation_token,
    send_email,
)
from opencert.user.models import User
from opencert.utils import flash_errors
blueprint = Blueprint("email", __name__, url_prefix="/email", static_folder="../static")


@blueprint.route("/confirm/<token>")
def confirm_email(token):

    email = confirm_token(token)
    if email == False:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for("email.unconfirmed"))

    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash("Account already confirmed. Please login.", "success")
        return redirect(url_for("public.login"))
    else:
        user.email_confirmed = True
        User.update(user)
        flash("You have confirmed your account. Thanks!", "success")
    return redirect(url_for("public.login"))


@blueprint.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = confirm_token(token)
    except:
        flash("The confirmation link is invalid or has expired.", "danger")
    form = ResetPasswordForm(request.form)
    if request.method == "POST":
        user = User.query.filter_by(email=email).first_or_404()
        if user and form.validate_on_submit():
            user.password = form.password.data
            User.update(user)
            flash("You have successfully udpated", "success")
            return redirect(url_for("public.home"))
    flash_errors(form)
    return render_template("email/reset_password.html", form=form)


@blueprint.route("/unconfirmed", methods=["GET", "POST"])
def unconfirmed():
    """Resend confirmation email page"""
    form = ResendConfirmationForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user.email_confirmed == True:
                flash(
                    "If your email exists, we will send a confirmation email to you.",
                    "success",
                )
                return redirect(url_for("public.login"))
            else:
                token = generate_confirmation_token(form.email.data)
                confirm_url = url_for(
                    "email.confirm_email", token=token, _external=True
                )
                html = render_template("email/confirm.html", confirm_url=confirm_url)
                subject = "Please confirm your email"
                send_email(form.email.data, subject, html)
                flash(
                    "If your email exists, we will send a confirmation email to you.",
                    "success",
                )
                return redirect(url_for("public.login"))
        else:
            flash(
                "If your email exists, we will send a confirmation email to you.",
                "success",
            )
            return redirect(url_for("public.login"))
    return render_template("email/unconfirmed.html", form=form)
