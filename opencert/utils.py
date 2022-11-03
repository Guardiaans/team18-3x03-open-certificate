# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)


# Access level 1 is admin
# Access level 2 is buyer
# Access level 3 is seller
def requires_access_level(*access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get the current user role_id
            user_role_id = current_user.role_id

            for n in access_level:
                # if the user role_id is not in the access_level list
                if user_role_id != n:
                    # Redirect to the home page
                    flash("You do not have access to this page", "danger")
                    return redirect(
                        url_for(
                            "public.member_home",
                        )
                    )
            return f(*args, **kwargs)

        return decorated_function

    return decorator  # returns the decorator
