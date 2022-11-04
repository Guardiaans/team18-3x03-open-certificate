# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm


class DeleteForm(FlaskForm):
    """Delete form."""

    def __init__(self, *args, **kwargs):
        """Create instance."""
        # super(DeleteForm, self).__init__(*args, **kwargs)
        self.user = None
