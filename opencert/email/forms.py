# -*- coding: utf-8 -*-
"""Email forms."""

from flask_mail import Message
import os
from itsdangerous import URLSafeTimedSerializer
from opencert import app
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

def generate_confirmation_token(email): 
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY")) 
    return serializer.dumps(email, salt=os.environ.get('SECURITY_PASSWORD_SALT')) 
    
def confirm_token(token, expiration=180): 
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
    
class ResetPasswordForm(FlaskForm):
    "Forget password form"
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(ResetPasswordForm, self).validate()
        if not initial_validation:
            return False
        return True
