import flask
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_security import login_required

blueprint = Blueprint("auth", __name__, static_folder="../static")


@blueprint.route("/tf-validate/", methods=["GET", "POST"])
@login_required
def two_auth():
    """List members."""
    form = flask.security.two_factor_verify_code_form.TwoFactorVerifyCodeForm()
    if form.validate_on_submit():
        if form.validate():
            return redirect(url_for("public.home"))
        else:
            flash("Invalid two factor code")
    return render_template("auth/auth.html", form=form)
