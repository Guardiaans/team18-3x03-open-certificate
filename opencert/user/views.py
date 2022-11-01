# -*- coding: utf-8 -*-
"""User views."""
import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from opencert.user.forms import UpdateForm
from opencert.user.models import User
from opencert.utils import flash_errors

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")


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

    return render_template("users/updateuser.html", form=form, site_key=os.environ.get("RECAPTCHA_SITE_KEY"))
