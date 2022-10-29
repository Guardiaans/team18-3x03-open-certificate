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
from opencert.verify.forms import VerifyForm

blueprint = Blueprint("verify", __name__, static_folder="../static")


@blueprint.route("/verify", methods=["GET", "POST"])
# @login_required
def verify():
    "verify NFT Page"
    return render_template("verify/verifyNFT.html")


@blueprint.route("/verifyfail", methods=["GET"])
def verifyfail():
    """verify failed page"""
    return render_template("verify/verifyfail.html")


@blueprint.route("/verifysuccess", methods=["GET"])
def verifysucces():
    """verify succeeded page"""
    return render_template("verify/verifysuccess.html")
