# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import json
import os
from wsgiref.util import request_uri

import requests
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required
from werkzeug.utils import secure_filename

from opencert.delete.forms import DeleteForm
from opencert.utils import flash_errors

blueprint = Blueprint("delete", __name__, static_folder="../static")


@blueprint.route("/delete", methods=["GET", "POST"])
# @login_required
def delete():
    "Delete NFT Page"
    return render_template("delete/deleteNFT.html")


@blueprint.route("/deletefail", methods=["GET"])
def deletefail():
    """Delete failed page"""
    return render_template("delete/deletefail.html")


@blueprint.route("/deletesuccess", methods=["GET"])
def deletesucces():
    """Delete succeeded page"""
    return render_template("delete/deletesuccess.html")
