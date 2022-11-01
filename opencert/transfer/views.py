# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, render_template
from flask_login import login_required
from opencert.extensions import login_manager
from opencert.user.models import User
from flask_login import login_required

blueprint = Blueprint("transfer", __name__, static_folder="../static")

@blueprint.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    """Transfer certificate page."""
    return render_template("transfer/transfer.html")


@blueprint.route("/transferfail", methods=["GET"])
@login_required
def transferfail():
    """Transfer failed page."""
    return render_template("transfer/transferfail.html")


@blueprint.route("/transfersuccess", methods=["GET"])
@login_required
def transfersucces():
    """Transfer succeeded page."""
    return render_template("transfer/transfersuccess.html")
