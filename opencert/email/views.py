from flask import (
    Blueprint,
    flash,
    render_template,
    request,
    url_for,
    redirect
)

from opencert.email.forms import confirm_token, ResetPasswordForm
from opencert.user.models import User


blueprint = Blueprint("email", __name__, url_prefix="/email", static_folder="../static")

@blueprint.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.email_confirmed = True
        User.update(user)
        flash('You have confirmed your account. Thanks!', 'success')
    return render_template('email/confirm.html')

@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    form = ResetPasswordForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(email=email).first_or_404()
        if user and form.validate_on_submit:
            user.password = form.password.data
            User.update(user)
            flash('You have successfully udpated','success')
            return redirect(url_for("public.home"))

    return render_template('email/reset_password.html', form = form)

