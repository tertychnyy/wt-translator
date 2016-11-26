import traceback
import os

from flask import Flask, jsonify

from wt.config import config
from wt.core import log
from wt.helpers import register_blueprints
from wt.middleware import HTTPMethodOverrideMiddleware


def create_app(package_name, package_path, settings_override=None,
               register_security_blueprint=True, config_name=None):
    """Returns a :class:`Flask` application instance configured with common
    functionality for the OfficialCharts platform.
    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of settings to override
    :param register_security_blueprint: flag to specify if the Flask-Security
                                        Blueprint should be registered. Defaults
                                        to `True`.
    """
    app = Flask(package_name, instance_relative_config=True)

    if config_name is None:
        config_name = os.environ.get('APP_CONFIG', 'development')

    app.config.from_object(config[config_name])
    app.config.from_object(settings_override)

    register_blueprints(app, package_name, package_path)

    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    @app.errorhandler(500)
    def handle_internal_server_error(e):
        log.critical("Internal error: {msg}".format(msg=traceback.format_exc()))
        return jsonify(dict(status="error")), 500

    return app
