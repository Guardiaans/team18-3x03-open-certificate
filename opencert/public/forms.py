# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask import flash

from opencert.user.models import User


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    token = PasswordField("Token", validators=[DataRequired(), Length(6, 6)])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append("Invalid username or password")
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append("Invalid username or password")
            return False

        if not self.user.verify_totp(self.token.data):
            self.token.errors.append("Invalid token")
            return False

        if not self.user.active:
            self.username.errors.append("User not activated")
            return False
        return True
