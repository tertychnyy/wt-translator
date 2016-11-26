# -*- coding: utf-8 -*-
from functools import wraps
import traceback

from chatfirst.models import ActionResponse
from flask import make_response
from flask import jsonify

from wt import factory
from wt.core import log, InvalidUsage
from wt.helpers import JSONEncoder


def create_app(settings_override=None, config_name=None):
    """Returns the Project api application instance"""
    app = factory.create_app(__name__, __path__, settings_override, config_name=config_name)
    app.debug = True

    # Set the default JSON encoder
    app.json_encoder = JSONEncoder

    # Register custom error handlers

    app.register_error_handler(InvalidUsage, on_c1_error)
    app.register_error_handler(404, on_404)
    app.register_error_handler(Exception, on_5xx_error)

    return app


def handle_error(e):
    return make_response(jsonify(dict(error='server error')))


def route(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            rv = f(*args, **kwargs)
            if isinstance(rv, tuple):
                sc = rv[1]
                rv = rv[0]
            if isinstance(rv, ActionResponse):
                return make_response(jsonify(rv.to_json()), sc)
            if isinstance(rv, str) or isinstance(rv, unicode):
                robj = ActionResponse()
                robj.messages = [rv]
                return make_response(jsonify(robj.to_json()), sc)
            raise InvalidUsage("Bad return")
        return f

    return decorator


def on_c1_error(e):
    log.error("ChatFirstError {ec}: {msg}".format(ec=e.status_code, msg=str(e.to_dict())))

    robj = ActionResponse()
    robj.messages = ["Adapter error"]
    return make_response(jsonify(robj.to_json()), 400)


def on_5xx_error(e):
    tb = traceback.format_exc()
    log.critical("InternalError: {msg}".format(msg=tb))

    robj = ActionResponse()
    robj.messages = ["Adapter error"]
    return make_response(jsonify(robj.to_json()), 400)


def on_404(e):
    return jsonify(dict(error='Not found')), 404
