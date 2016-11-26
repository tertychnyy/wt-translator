# -*- coding: utf-8 -*-
"""
API для SmartCat
"""
from flask import Blueprint
from flask import request

from wt.dashboard import route, route_test
from wt.scripts import read_scenarion_file, translate_raw_scenario, create_bot

bp = Blueprint('main', __name__)


@route_test(bp, '/test', methods=['GET'])
def get_status():
    return 'success', 200


@route(bp, '/', methods=['GET'])
def main_page():
    return 'dashboard/main.html', 200


@route(bp, '/', methods=['POST'])
def main_page_upload():
    raw_scenario = read_scenarion_file(request)

    scenario = translate_raw_scenario(raw_scenario)

    create_bot(scenario)

    return 'dashboard/help.html', 200


@route(bp, '/help', methods=['GET'])
def help_page():
    return 'dashboard/help.html', 200
