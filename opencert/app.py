# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template
from flask_mail import Mail

from opencert import (
    auth,
    commands,
    delete,
    email,
    minting,
    public,
    transfer,
    user,
    verify,
)
from opencert.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
)

from opencert.user.models import Role


def create_app(config_object="opencert.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    Mail(app)

    with app.app_context():
        # Insert Admin role into Role table
        admin_role = Role.query.filter_by(name="admin").first()
        if admin_role is None:
            admin_role = Role(name="admin")
            db.session.add(admin_role)
            db.session.commit()
        # Insert Buyer and seller roles into Role table
        buyer_role = Role.query.filter_by(name="buyer").first()
        if buyer_role is None:
            buyer_role = Role(name="buyer")
            db.session.add(buyer_role)
            db.session.commit()
        seller_role = Role.query.filter_by(name="seller").first()
        if seller_role is None:
            seller_role = Role(name="seller")
            db.session.add(seller_role)
            db.session.commit()

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


# Register blueprints here
def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(minting.views.blueprint)
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(email.views.blueprint)
    app.register_blueprint(transfer.views.blueprint)
    app.register_blueprint(verify.views.blueprint)
    app.register_blueprint(delete.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
