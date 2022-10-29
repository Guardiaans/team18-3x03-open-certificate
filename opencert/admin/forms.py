# -*- coding: utf-8 -*-
"""admin forms."""
from logging.config import dictConfig
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask import flash, current_app
import logging
from opencert.user.models import User


logging.basicConfig(filename='record.log', level=logging.DEBUG)
def OpencertLogger():
  # showing different logging levels
  current_app.logger.debug("debug log info")
  current_app.logger.info("Info log information")
  current_app.logger.warning("Warning log info")
  current_app.logger.error("Error log info")
  current_app.logger.critical("Critical log info")
  return "testing logging levels."


import smtplib
from email.message import EmailMessage

def sendlogs():

  email_sender = '2020projectconfig@gmail.com'
  email_password = 'oqlozkghaqmclnvu'
  email_receiver = 'hidaniel97foo@gmail.com'
  subject = 'Logs from website'
  body = """
  This are the logs collected.
  """

  msg = EmailMessage()
  msg['From'] = email_sender
  msg['To'] = email_receiver
  msg['Subject'] = subject
  msg.set_content(body) 
  

  # with open('emailcontent.txt') as myfile:
  #   data = myfile.read()
  #   msg.set_content(data)

  with open("record.log", "rb") as f:
    file_data=f.read()
    print("File data", file_data)
    file_name = f.name
    print("File name is", file_name)
    msg.add_attachment(file_data, maintype="application", subtype="log", filename=file_name)

  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server=smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email_sender, email_password)
    server.send_message(msg)
    print("Email sent")



# class Config:
#     LOGGING = {
#         "version": 1,
#         "filters": {
#             "backend_filter": {
#                 "backend_module": "backend",
#             }
#         },
#         "formatters": {
#             "standard": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
#             "compact": {"format": "%(asctime)s %(message)s"},
#         },
#         "handlers": {
#             "console": {
#                 "class": "logging.StreamHandler",
#                 "level": "DEBUG",
#                 "formatter": "standard",
#                 "stream": "ext://sys.stdout",
#                 "filters": ["backend_filter"],
#             },
#             "file": {
#                 "class": "logging.handlers.TimedRotatingFileHandler",
#                 "level": "DEBUG",
#                 "filename": "backend.log",
#                 "when": "D",
#                 "interval": 1,
#                 "formatter": "standard",
#             },
#         },
#         "loggers": {
#             "": {"handlers": ["console", "z_buffer"], "level": "DEBUG"},
#             "flask": {"level": "WARNING"},
#             "werkzeug": {"level": "WARNING"},
#         },
#         "disable_existing_loggers": False,
#     }