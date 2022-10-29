# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, render_template

from opencert.extensions import login_manager
from opencert.user.models import User

blueprint = Blueprint("transfer", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/transfer", methods=["GET", "POST"])
def transfer():
    """Transfer certificate page."""
    return render_template("transfer/transfer.html")


@blueprint.route("/transferfail", methods=["GET"])
def transferfail():
    """Transfer failed page."""
    return render_template("transfer/transferfail.html")


@blueprint.route("/transfersuccess", methods=["GET"])
def transfersucces():
    """Transfer succeeded page."""
    return render_template("transfer/transfersuccess.html")
