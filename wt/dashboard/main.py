# -*- coding: utf-8 -*-
"""
API для SmartCat
"""
from flask import Blueprint

from wt.dashboard import route, route_test

bp = Blueprint('main', __name__)


@route_test(bp, '/test', methods=['GET'])
def get_status():
    return 'success', 200


@route(bp, '/', methods=['GET'])
def main_page():
    return 'dashboard/main.html', 200


@route(bp, '/help', methods=['GET'])
def help_page():
    return 'dashboard/help.html', 200