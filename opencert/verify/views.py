# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint("verify", __name__, static_folder="../static")


@blueprint.route("/verify", methods=["GET", "POST"])
@login_required
def verify():
    """Verify NFT Page."""
    return render_template("verify/verifyNFT.html")


@blueprint.route("/verifyfail", methods=["GET"])
@login_required
def verifyfail():
    """Verify failed page."""
    return render_template("verify/verifyfail.html")


@blueprint.route("/verifysuccess", methods=["GET"])
@login_required
def verifysucces():
    """Verify succeeded page."""
    return render_template("verify/verifysuccess.html")
