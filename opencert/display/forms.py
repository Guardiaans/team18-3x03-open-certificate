# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm


class DisplayForm(FlaskForm):
    """Display form."""

    def __init__(self, *args, **kwargs):
        """Create instance."""
        # super(DisplayForm, self).__init__(*args, **kwargs)
        self.user = None
