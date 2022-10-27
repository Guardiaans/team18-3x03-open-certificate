# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from wsgiref.util import request_uri
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,

)

from opencert.verify.forms import VerifyForm
from opencert.utils import flash_errors
from flask import Blueprint, render_template
from flask_login import login_required


import os
import json
from werkzeug.utils import secure_filename
import requests


blueprint = Blueprint("verify", __name__, static_folder="../static")


@blueprint.route("/verify",methods=["GET", "POST"])
#@login_required
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
         