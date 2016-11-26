from chatfirst.client import Chatfirst
from chatfirst.models import Bot
from flask import current_app

from wt.core import InvalidUsage


def check_file_pre(f):
    return True


def check_file_post(scenario):
    return True


def read_scenarion_file(r):
    # Fetch file
    file_tag = "raw"
    f = r.files[file_tag]

    # Check file
    if not check_file_pre(f):
        raise InvalidUsage("Bad file")

    # Read file
    scenario = f.read()

    # Check data
    if not check_file_post(scenario):
        raise InvalidUsage("Bad file")

    return scenario


def translate_raw_scenario(raw):
    res = '<states><state name="Start"><transition input="start" next="start">It works better!</transition></state></states>'
    return res


def create_bot(scenario):
    bot = Bot()
    bot.name = "Junction2016"
    bot.language = 1
    bot.fancy_name = "Junction2016"

    bot.scenario = '<fsm name="{name}">'.format(name=bot.name) + scenario + '</fsm>'

    client = Chatfirst(token=current_app.config["CHATFIRST_TOKEN"])
    return client.bots_update(bot)
