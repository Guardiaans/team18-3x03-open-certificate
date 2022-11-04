# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm


class TransferForm(FlaskForm):
    """Minting form."""

    def __init__(self, *args, **kwargs):
        """Create instance."""
        # super(TransferForm, self).__init__(*args, **kwargs)
        self.user = None
