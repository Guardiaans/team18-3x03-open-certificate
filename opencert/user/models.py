# -*- coding: utf-8 -*-
"""User models."""
import base64
import datetime as dt
import os

import onetimepass
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from opencert.database import Column, PkModel, db, reference_col, relationship
from opencert.extensions import bcrypt


class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean(), default=False)
    _password = Column("password", db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(20), nullable=False)
    last_name = Column(db.String(20), nullable=False)
    wallet_add = Column(db.String(500), nullable=False)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    otp_secret = Column(db.String(16))
    role_id = reference_col("roles", nullable=False)
    role = relationship("Role", backref="users")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.otp_secret is None:
            # generate a random secret
            self.otp_secret = base64.b32encode(os.urandom(10)).decode("utf-8")

    def get_totp_uri(self):
        return "otpauth://totp/open-cert:{0}?secret={1}&issuer=open-cert".format(
            self.username, self.otp_secret
        )

    def verify_totp(self, token):
        return onetimepass.valid_totp(token, self.otp_secret)

    @hybrid_property
    def password(self):
        """Hashed password."""
        current_app.logger.info("getting password")
        return self._password

    @password.setter
    def password(self, value):
        """Set password."""
        self._password = bcrypt.generate_password_hash(value)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self._password, value)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"
