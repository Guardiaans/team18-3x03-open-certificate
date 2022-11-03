# -*- coding: utf-8 -*-
"""admin forms."""
import logging
import smtplib

from email.message import EmailMessage
from flask import current_app
from flask_login import current_user

logging.basicConfig(filename="record.log", level=logging.DEBUG)


def opencert_logger():
    """Create a logger for the opencert app."""
    # showing different logging levels
    current_app.logger.debug("debug log info")
    current_app.logger.info("Info log information")
    current_app.logger.warning("Warning log info")
    current_app.logger.error("Error log info")
    current_app.logger.critical("Critical log info")
    return "testing logging levels."


async def sendlogs():
    """Send logs to admin email."""
    email_sender = "2020projectconfig@gmail.com"
    email_password = "oqlozkghaqmclnvu"
    email_receiver = "openseatificate@gmail.com"
    subject = "Logs from website, logs for " + current_user.email
    body = """
  This are the logs collected.
  """

    msg = EmailMessage()
    msg["From"] = email_sender
    msg["To"] = email_receiver
    msg["Subject"] = subject
    msg.set_content(body)

    with open("record.log", "rb") as f:
        file_data = f.read()
        print("File data", file_data)
        file_name = f.name
        print("File name is", file_name)
        msg.add_attachment(
            file_data, maintype="application", subtype="log", filename=file_name
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(email_sender, email_password)
        server.send_message(msg)
