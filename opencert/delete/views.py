# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, render_template

blueprint = Blueprint("delete", __name__, static_folder="../static")


@blueprint.route("/delete", methods=["GET", "POST"])
# @login_required
def delete():
    """Delete NFT Page."""
    return render_template("delete/deleteNFT.html")


@blueprint.route("/deletefail", methods=["GET"])
def deletefail():
    """Delete failed page."""
    return render_template("delete/deletefail.html")


@blueprint.route("/deletesuccess", methods=["GET"])
def deletesucces():
    """Delete succeeded page."""
    return render_template("delete/deletesuccess.html")
