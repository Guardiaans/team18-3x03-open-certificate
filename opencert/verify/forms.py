# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm


class VerifyForm(FlaskForm):
    """Verify form."""

    def __init__(self, *args, **kwargs):
        """Create instance."""
        # super(VerifyForm, self).__init__(*args, **kwargs)
        self.user = None
