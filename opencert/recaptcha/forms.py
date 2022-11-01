import os

import requests
from flask import request


def recaptcha():
    # get recaptcha response
    secret_response = request.form["g-recaptcha-response"]
    # get key from env
    SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
    RECAPTCHA_URL = os.environ.get("RECAPTCHA_VERIFY_URL")
    # verify its not a bot
    verify_response = requests.post(
        url=f"{RECAPTCHA_URL}?secret={SECRET_KEY}&response={secret_response}"
    ).json()

    if verify_response["success"] == False or verify_response["score"] < 0.5:
        return False
    return True
