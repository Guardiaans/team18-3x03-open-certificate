# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import socket

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user

from opencert.admin.forms import sendlogs
from opencert.extensions import login_manager
from opencert.public.forms import LoginForm
from opencert.user.models import User
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


@blueprint.route("/logout/")
@login_required
async def logout():
    """Logout."""
    await sendlogs()
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/about/")
def about():
    """About page."""
    return render_template("public/about.html")
