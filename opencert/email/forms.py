# -*- coding: utf-8 -*-
"""Email forms."""

from flask_mail import Message
import os
from itsdangerous import URLSafeTimedSerializer
from opencert import app

def generate_confirmation_token(email): 
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY")) 
    return serializer.dumps(email, salt=os.environ.get('SECURITY_PASSWORD_SALT')) 
    
def confirm_token(token, expiration=3600): 
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY")) 
    try: 
        email = serializer.loads(  token,  salt=os.environ.get('SECURITY_PASSWORD_SALT'),  max_age=expiration ) 
    except: 
        return False 
        
    return email

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=os.environ.get('MAIL_DEFAULT_SENDER')
    )
    mail = app.Mail()
    mail.send(msg)
    