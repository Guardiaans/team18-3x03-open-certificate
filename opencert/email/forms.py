# -*- coding: utf-8 -*-
"""Email forms."""

import os
from threading import Thread

from flask import copy_current_request_context, current_app
from flask_mail import Message
from flask_wtf import FlaskForm
from itsdangerous import URLSafeTimedSerializer, exc
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from opencert import app
from opencert.user.models import User


def generate_confirmation_token(email):
    """Generate confirmation token."""
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))
    return serializer.dumps(email, salt=os.environ.get("SECURITY_PASSWORD_SALT"))


def confirm_token(token, expiration=180):
    """Confirm token function."""
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))
    try:
        
        email = serializer.loads(
            token, salt=os.environ.get("SECURITY_PASSWORD_SALT"), max_age=expiration
        )
        return email

    except exc.SignatureExpired as e:
        current_app.logger.error(e)
        return False


def send_email(to, subject, template):
    """Send email function."""
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=os.environ.get("MAIL_DEFAULT_SENDER"),
    )

    @copy_current_request_context
    def async_send_message(message):
        mail = app.Mail()
        mail.send(message)

    Thread(target=async_send_message, args=[msg]).start()


class ResetPasswordForm(FlaskForm):
    """Forget password form."""

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,40}$",
                message="Need 1 upper and lower, 1 special",
            ),
            Length(min=8, max=40),
        ],
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(ResetPasswordForm, self).validate()
        if not initial_validation:
            return False
        return True


class ResendConfirmationForm(FlaskForm):
    """Form for resending of confirmation email."""

    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(ResendConfirmationForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(ResendConfirmationForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(email=self.email.data).first()
        if self.user is None:
            return False

        return True
