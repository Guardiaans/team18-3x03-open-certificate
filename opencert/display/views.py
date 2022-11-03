# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""

from flask import Blueprint, render_template
from flask_cors import cross_origin
from flask_login import login_required

blueprint = Blueprint("display", __name__, static_folder="../static")


@blueprint.route("/display", methods=["GET", "POST"])
@cross_origin()
@login_required
def display():
    """Display NFT Page."""
    return render_template("display/displayNFT.html")


@blueprint.route("/displayfail", methods=["GET"])
@login_required
def displayfail():
    """Display failed page."""
    return render_template("display/displayfail.html")


@blueprint.route("/displaysuccess", methods=["GET"])
@login_required
def displaysucces():
    """Display succeeded page."""
    return render_template("display/displaysuccess.html")
