import requests

from wt.core import InvalidUsage


def check_user(id_, channel):
    """
    http://localhost:3000/players/create?name=Super User&channel=skype&uid=22211
    :param id_:
    :param channel:
    :return:
    """
    url = "https://walkie-talkie-api.herokuapp.com/players/create"
    params = dict()
    params["channel"] = channel
    params["uid"] = id_

    res = requests.get(url, params=params)
    if not res.status_code == 200:
        raise InvalidUsage("Bad https://walkie-talkie-api.herokuapp.com/players/create response: bad error code")
    try:
        data = res.json()
        return data["id"]
    except:
        raise InvalidUsage("Bad https://walkie-talkie-api.herokuapp.com/players/create response: cannot parse json")


def new_session(game_id, player_id):
    """
    curl -X "GET" "http://localhost:3000/games/ff3f5cab-c3d1-4648-a8d2-2d8ad97976e0/start?player_id=029f98b8-37a1-4e45-94a2-18ca3b4ce513"
    :param game_id:
    :param player_id:
    :return:
    """
    url = "https://walkie-talkie-api.herokuapp.com/games/{game_id}/start".format(game_id=game_id)
    params = dict()
    params["player_id"] = player_id

    res = requests.get(url, params=params)
    if not res.status_code == 200:
        raise InvalidUsage("Bad https://walkie-talkie-api.herokuapp.com/games/{game_id}/start response: bad error code")
    try:
        data = res.json()
        return data["id"]
    except:
        raise InvalidUsage("Bad https://walkie-talkie-api.herokuapp.com/games/{game_id}/start response: cannot parse json")


def get_sessions(game_id, player_id):
    """
    curl -X "GET" "http://localhost:3000/games/ff3f5cab-c3d1-4648-a8d2-2d8ad97976e0/start?player_id=029f98b8-37a1-4e45-94a2-18ca3b4ce513"
    :param game_id:
    :param player_id:
    :return:
    """
    url = "http://localhost:3000/players/029f98b8-37a1-4e45-94a2-18ca3b4ce513/sessions".format(game_id=game_id)
    # params = dict()
    # params["player_id"] = player_id
    #
    # res = requests.get(url, params=params)
    # if not res.status_code == 200:
    #     raise InvalidUsage("Bad https://walkie-talkie-api.herokuapp.com/games/{game_id}/start response: bad error code")
    # try:
    #     data = res.json()
    #     return data["id"]
    # except:
    #     raise InvalidUsage("Bad https://walkie-talkie-api.herokuapp.com/games/{game_id}/start response: cannot parse json")
