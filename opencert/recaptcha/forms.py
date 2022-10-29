import os
from unittest import result

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
    result = [verify_response["success"], verify_response["score"]]
    return result
