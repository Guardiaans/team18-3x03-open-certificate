from flask import (
    Blueprint,
    flash,
    render_template,
)

from opencert.email.forms import confirm_token
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