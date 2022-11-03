# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""

from wsgiref.util import request_uri

from flask import Blueprint, render_template
from flask_cors import cross_origin
from flask_login import login_required

from opencert.display.forms import DisplayForm

blueprint = Blueprint("display", __name__, static_folder="../static")


@blueprint.route("/display", methods=["GET", "POST"])
@cross_origin()
@login_required
def display():
    "display NFT Page"
    return render_template("display/displayNFT.html")


@blueprint.route("/displayfail", methods=["GET"])
@login_required
def displayfail():
    """display failed page"""
    return render_template("display/displayfail.html")


@blueprint.route("/displaysuccess", methods=["GET"])
@login_required
def displaysucces():
    """display succeeded page"""
    return render_template("display/displaysuccess.html")
