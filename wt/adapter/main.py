# -*- coding: utf-8 -*-
"""
API для SmartCat
"""
from flask import Blueprint
from flask import request

from wt.adapter import route
from wt.adapter.scripts import check_user, new_session

bp = Blueprint('main', __name__)


@route(bp, '/test', methods=['GET'])
def test_page():
    return 'success', 200


@route(bp, '/start', methods=['GET'])
def start_bot():
    id_ = request.args.get('id', None)

    # Регистрирует игрока
    player_id = check_user(id_, "skype")

    # Стартует новую сессию
    session_id = new_session("eced7582-4acd-46ec-9c78-42df56175dc1", player_id)
    # Устанавливает
    # Обнуляет параметры(?)
    return 'success', 200


@route(bp, '/good', methods=['GET'])
def good_bot():
    id_ = request.args.get('id', None)
    return 'success', 200


@route(bp, '/bad', methods=['GET'])
def bad_bot():
    id_ = request.args.get('id', None)
    return 'success', 200
