# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired


class MintingForm(FlaskForm):
    """Minting form."""
    def __init__(self, *args, **kwargs):
        """Create instance."""
        #super(MintingForm, self).__init__(*args, **kwargs)
        self.user = None

    



