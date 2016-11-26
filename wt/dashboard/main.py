# -*- coding: utf-8 -*-
"""
API для SmartCat
"""
from flask import Blueprint

from wt.dashboard import route

bp = Blueprint('main', __name__)


@route(bp, '/', methods=['GET'])
def get_status():
    return 'success', 200
