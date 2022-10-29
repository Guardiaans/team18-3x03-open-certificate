# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import email
import logging
from logging.config import dictConfig
import sys
from opencert.admin.forms import sendlogs
#from opencert.admin import Config
# import BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
from flask_mail import Mail
from opencert import commands, public, user, auth, email, admin
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

# the following is a sample logging done with own settings
# dictConfig(Config.LOGGING)
# LOGGER = logging.getLogger(__name__)


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
    scheduler = BackgroundScheduler()
        # in your case you could change seconds to hours
    scheduler.add_job(sendlogs, trigger='interval', seconds=3600)
    scheduler.start()

    try:
        # To keep the main thread alive
        return app
    except:
        # shutdown if app occurs except 
        scheduler.shutdown()
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
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(email.views.blueprint)
    # app.register_blueprint(admin.views.blueprint)
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
    # # handler = logging.StreamHandler(sys.stdout)
    # if not app.logger.handlers:
    #     # app.logger.addHandler(handler)
    #     app.logger.addHandler(LOGGER)

    # smtp_handler = logging.handlers.SMTPHandler(mailhost=('smtp.gmail.com', 465), fromaddr=["2020projectconfig@gmail.com"], toaddrs=["hidaniel97foo@gmail.com"], subject="Logs", credentials=("2020projectconfig@gmail.com", "oqlozkghaqmclnvu"), secure=())
    # smtp_handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    # smtp_handler.setFormatter(formatter)

    # if not app.logger.handlers:
    #     app.logger.addHandler(smtp_handler)

    # Original
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)

