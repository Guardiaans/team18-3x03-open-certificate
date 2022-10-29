import flask
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_security import login_required, two_factor_verify_code_form

# Write a two_factor_verify_code_form that inherits from LoginForm
# and adds a field for the two factor code.
#
# The form should be named TwoFactorVerifyCodeForm
# and should have a field named two_factor_code
# that is a StringField with a DataRequired validator.
#
# The form should have a validate method that calls
# the validate method of the parent class and then
# checks that the two factor code is valid.
# If the code is not valid, the form should have an
# error added to the two_factor_code field.
#

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
