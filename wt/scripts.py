# -*- coding: utf-8 -*-
import re

from chatfirst.client import Chatfirst
from chatfirst.models import Bot
from flask import current_app
from lxml import html, etree
from lxml.etree import tostring

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


def get_state_name(s, sfx):
    return "State" + s + sfx


def get_state_intro_name(s):
    return get_state_name(s, "Intro")


def get_state_menu_name(s):
    return get_state_name(s, "Menu")


def translate_raw_scenario(raw, old=False):
    root = html.fromstring(raw)

    res_xml = etree.Element('states')
    start_state = etree.Element('state')
    start_state.attrib['name'] = 'Start'
    start_tr = etree.Element('transition')
    start_tr.attrib['input'] = '*'
    start_tr.attrib['next'] = 'Start'
    start_tr.text = "Please, add Start passage"

    res_xml.append(start_state)

    if not old:
        passages = root.findall("tw-passagedata")
    else:
        r = root.findall("body/div[@id='storeArea']")
        passages = r[0].getchildren()

    for passage in passages:
        name = passage.attrib["name"] if not old else passage.attrib["tiddler"]
        text = passage.text

        # Find special data
        if text:
            keys_re = r"\[\[[^\[\]]*\]\]"
            keys = [x[2:-2] for x in re.findall(keys_re, passage.text)]
            imgs_re = r"\(open-url:\s*\"[^\(\)]*\"\s*\)"
            imgs = [x[12:-2] for x in re.findall(imgs_re, passage.text)]

            # Remove used matches
            text = re.sub(keys_re, "", text)
            text = re.sub(imgs_re, "", text)

            # Format newlines
            text = text.replace("\n", "\n\n")

        # Prepare states' names
        state_intro = etree.Element('state')
        state_intro_name = 'State' + name + 'Intro'

        state_menu = etree.Element('state')
        state_menu_name = 'State' + name + 'Menu'

        # If name==Start update Start state
        if name == 'Start':
            start_tr.attrib['next'] = state_intro_name
            start_tr.attrib['no_stop'] = 'true'
            start_tr.text = ""


        # Process imgs
        for img in imgs:
            text += " ===" + img + "=== "

        # Prepare states
        state_intro.attrib['name'] = state_intro_name
        state_menu.attrib['name'] = state_menu_name

        # Prepare transitions
        tr = etree.Element('transition')
        tr.attrib['input'] = "*"
        tr.attrib['next'] = state_menu_name
        tr.attrib["pending_keyboard"] = ','.join([x.split(":")[1] if ":" in x else x for x in keys])
        tr.text = text
        state_intro.append(tr)

        # Process keys
        for key in keys:
            tr = etree.Element('transition')
            tr.attrib["no_stop"] = "true"
            tr.attrib["input"] = key.split(":")[1] if ":" in key else key
            tr.attrib["next"] = get_state_intro_name(key)
            state_menu.append(tr)

        res_xml.append(state_intro)
        res_xml.append(state_menu)

    start_state.append(start_tr)

    #res = '<states><state name="Start"><transition input="start" next="start">It works better!</transition></state></states>'
    res = tostring(res_xml)
    return res


def create_bot(scenario):
    bot = Bot()
    bot.name = "Junction2016"
    bot.language = 1
    bot.fancy_name = "Junction2016"

    bot.scenario = '<fsm name="{name}">'.format(name=bot.name) + scenario + '</fsm>'

    client = Chatfirst(token=current_app.config["CHATFIRST_TOKEN"])
    return client.bots_update(bot)
