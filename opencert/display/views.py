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

from opencert.utils import flash_errors
from opencert.display.forms import DisplayForm

blueprint = Blueprint("display", __name__, static_folder="../static")


@blueprint.route("/display", methods=["GET", "POST"])
# @login_required
def display():
    "display NFT Page"
    return render_template("display/displayNFT.html")


@blueprint.route("/displayfail", methods=["GET"])
def displayfail():
    """display failed page"""
    return render_template("display/displayfail.html")


@blueprint.route("/displaysuccess", methods=["GET"])
def displaysucces():
    """display succeeded page"""
    return render_template("display/displaysuccess.html")
