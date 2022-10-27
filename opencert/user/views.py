# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from opencert.user.models import User
from opencert.user.forms import UpdateForm

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")

@blueprint.route("/update", methods=["GET", "POST"])
@login_required
def update():
    """Update user information"""
    form = UpdateForm(request.form)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if request.method == "POST":
        if form.validate_on_submit():
            user.wallet_add = form.wallet_add.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.password = form.password.data
            User.update(user)
            flash("Account has successfully been updated.", "success")
            return redirect(url_for("user.members"))
    return render_template("users/updateuser.html", form=form)