# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm


class MintingForm(FlaskForm):
    """Minting form."""

    def __init__(self, *args, **kwargs):
        """Create instance."""
        # super(MintingForm, self).__init__(*args, **kwargs)
        self.user = None
