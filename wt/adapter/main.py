# -*- coding: utf-8 -*-
"""
API для SmartCat
"""
from flask import Blueprint

from wt.adapter import route
bp = Blueprint('main', __name__)


@route(bp, '/test', methods=['GET'])
def test_page():
    return 'success', 200
