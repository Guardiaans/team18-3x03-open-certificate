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

from opencert.delete.forms import DeleteForm
from opencert.utils import flash_errors
from flask import Blueprint, render_template
from flask_login import login_required


import os
import json
from werkzeug.utils import secure_filename
import requests


blueprint = Blueprint("delete", __name__, static_folder="../static")


@blueprint.route("/delete",methods=["GET", "POST"])
#@login_required
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
         

