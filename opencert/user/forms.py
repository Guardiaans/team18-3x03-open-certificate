# -*- coding: utf-8 -*-
"""User forms."""
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, Regexp

from .models import User


class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    wallet_add = StringField(
        "Wallet Address", validators=[DataRequired(), Length(min=6, max=40)]
    )
    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Regexp(
                r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$",
                message="First name should only use alphabetical characters!",
            ),
            Length(min=1, max=20),
        ],
    )
    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(),
            Regexp(
                r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$",
                message="Last name should only use alphabetical characters!",
            ),
            Length(min=1, max=20),
        ],
    )
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
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class UpdateForm(FlaskForm):
    """Register form."""

    wallet_add = StringField("Wallet Address", validators=[Length(min=40, max=40)])
    # Use regexp to disallow malicious inputs
    first_name = StringField(
        "First Name",
        validators=[
            Regexp(
                r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$",
                message="First name should only use alphabetical characters!",
            ),
            Length(min=1, max=20),
        ],
    )
    last_name = StringField(
        "Last Name",
        validators=[
            Regexp(
                r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$",
                message="Last name should only use alphabetical characters!",
            ),
            Length(min=1, max=20),
        ],
    )
    curr_password = PasswordField(
        "Current password",
        validators=[
            Optional(),
            Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,40}$$",
                message="Need 1 upper and lower, 1 special",
            ),
            Length(min=8, max=40),
        ],
    )
    password = PasswordField(
        "New password",
        validators=[
            Optional(),
            Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,40}$",
                message="Need 1 upper and lower, 1 special",
            ),
            Length(min=8, max=40),
        ],
    )
    confirm = PasswordField(
        "Verify new password", [EqualTo("password", message="Passwords must match")]
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(UpdateForm, self).validate()
        if not initial_validation:
            return False

        if self.curr_password.data != "":
            self.user = User.query.filter_by(
                username=current_user.username
            ).first_or_404()
            if not self.user.check_password(self.curr_password.data):
                self.curr_password.errors.append("Current password is incorrect!")
                return False

        return True
