# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import os
from io import BytesIO

import pyqrcode
import requests
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

from opencert.email.forms import generate_confirmation_token, send_email
from opencert.extensions import login_manager
from opencert.public.forms import LoginForm
from opencert.user.forms import RegisterForm
from opencert.user.models import User
from opencert.utils import flash_errors

blueprint = Blueprint("transfer", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/transfer", methods=["GET", "POST"])
def transfer():
    """Transfer certificate page"""
    return render_template("transfer/transfer.html")


@blueprint.route("/transferfail", methods=["GET"])
def transferfail():
    """Transfer failed page"""
    return render_template("transfer/transferfail.html")


@blueprint.route("/transfersuccess", methods=["GET"])
def transfersucces():
    """Transfer succeeded page"""
    return render_template("transfer/transfersuccess.html")
