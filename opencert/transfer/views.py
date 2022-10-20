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


blueprint = Blueprint("transfer", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/transfer", methods=["GET", "POST"])
def transfer():
    """Transfer certificate page"""
    return render_template("transfer/transfer.html")
