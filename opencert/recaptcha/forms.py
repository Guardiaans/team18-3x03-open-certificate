"""recaptcha forms."""

import os

import requests
from flask import request


def recaptcha():
    """Validate reCAPTCHA."""
    # get recaptcha response
    secret_response = request.form["g-recaptcha-response"]
    # get key from env
    secrete_key = os.environ.get("RECAPTCHA_SECRET_KEY")
    recaptcha_url = os.environ.get("RECAPTCHA_VERIFY_URL")
    # verify its not a bot
    verify_response = requests.post(
        url=f"{recaptcha_url}?secret={secrete_key}&response={secret_response}"
    ).json()

    if verify_response["success"] is False or verify_response["score"] < 0.5:
        return False
    return True
