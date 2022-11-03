"""auth views."""
import pyqrcode
from io import BytesIO

from flask import Blueprint, render_template, session, redirect, url_for, abort
from opencert.user.models import User

blueprint = Blueprint("auth", __name__, static_folder="../static")


@blueprint.route("/two-factor/")
def two_factor_setup():
    """2FA page."""
    if "username" not in session:
        return redirect(url_for("public.home"))
    user = User.query.filter_by(username=session["username"]).first()
    if user is None:
        return redirect(url_for("public.home"))
    return (
        render_template("auth/two_factor_setup.html"),
        200,
        {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@blueprint.route("/qrcode")
def qrcode():
    if "username" not in session:
        abort(404)
    user = User.query.filter_by(username=session["username"]).first()
    if user is None:
        abort(404)

    # for added security, remove username from session
    del session["username"]

    # render qrcode for FreeTOTP
    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=3)
    return (
        stream.getvalue(),
        200,
        {
            "Content-Type": "image/svg+xml",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )
