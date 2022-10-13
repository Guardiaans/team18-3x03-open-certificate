"""auth views."""
from flask import Blueprint, render_template

blueprint = Blueprint("auth", __name__, static_folder="../static")


@blueprint.route("/authenticate/", methods=["GET"])
def two_auth():
    """List members."""
    return render_template("auth/auth.html")
