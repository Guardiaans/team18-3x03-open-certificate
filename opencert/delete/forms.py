# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired


class DeleteForm(FlaskForm):
    """Delete form."""

    def __init__(self, *args, **kwargs):
        """Create instance."""
        # super(DeleteForm, self).__init__(*args, **kwargs)
        self.user = None
