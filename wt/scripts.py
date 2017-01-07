# -*- coding: utf-8 -*-
import random
import re
import string

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


def get_chain(input_text, next_state, no_stop="false"):
    """
    Create chain from input phrase
    :param input_text:
    :param next_state:
    :param no_stop:
    :return: chain states
    """
    states = list()
    chain_tag = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))

    words = input_text.split()

    # Process words in phrase
    for i in xrange(1, len(words)):
        state = etree.Element('state')
        state.attrib['name'] = chain_tag + str(i)
        state_tr = etree.Element('transition')
        state_tr.attrib['input'] = words[i]
        if i != len(words)-1:
            state_tr.attrib['no_stop'] = 'true'
            state_tr.attrib['next'] = chain_tag + str(i+1)
        else:
            # Transition from last state of chain to target state
            state_tr.attrib['no_stop'] = no_stop
            state_tr.attrib['next'] = next_state

        state.append(state_tr)
        states.append(state)

    # Prepare start transition
    tr = etree.Element('transition')
    tr.attrib["no_stop"] = "true"
    tr.attrib["input"] = words[0]
    if len(states) > 0:
        tr.attrib["next"] = states[0].attrib['name']
    else:
        tr.attrib["next"] = next_state

    return states, tr


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
        passages = root.findall(".//tw-passagedata")
    else:
        r = root.findall("body/div[@id='storeArea']")
        passages = r[0].getchildren()

    for passage in passages:
        name = passage.attrib["name"] if not old else passage.attrib["tiddler"]
        text = passage.text

        actions = list()
        keys = list()

        # Find special data
        if text:
            keys_re = r"\[\[[^\[\]]*\]\]"
            keys_matches = re.findall(keys_re, passage.text)
            keys = [x[2:-2].split("->") for x in keys_matches]
            imgs_re = r"\(open-url:\s*\"[^\(\)]*\"\s*\)"
            imgs = re.findall(imgs_re, passage.text)
            action_re = r"\(action:\s*\"[^\(\)]*\"\s*\)"
            actions = [x[10:-2] for x in re.findall(action_re, passage.text)]

            ## Remove used matches
            # Remove keys
            for i in xrange(len(keys_matches)):
                text = text.replace(keys_matches[i], keys[i][0])

            # Remove actions
            text = re.sub(action_re, "", text)

            # Remove images
            for img in imgs:
                # [12:-2]
                text = text.replace(img, " ===" + img[12:-2] + "=== ")

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

        # Prepare states
        state_intro.attrib['name'] = state_intro_name
        state_menu.attrib['name'] = state_menu_name

        # Prepare transitions
        tr = etree.Element('transition')
        tr.attrib['input'] = "*"
        tr.attrib['next'] = state_menu_name
        for action in actions:
            tr.attrib['action'] = action
        tr.attrib["pending_keyboard"] = ','.join([x[0] for x in keys])
        tr.text = text
        state_intro.append(tr)

        # Process keys
        for key in keys:
            if len(key) != 2:
                raise Exception("Illegal key text: {key}".format(key=str(key)))
            chain_states, first_tr = get_chain(key[0], get_state_intro_name(key[1]), no_stop="true")
            state_menu.append(first_tr)
            for state in chain_states:
                res_xml.append(state)

        # Process *
        tr = etree.Element('transition')
        tr.attrib["input"] = "*"
        tr.attrib["next"] = state_menu_name
        tr.text = "Please, use buttons"
        state_menu.append(tr)

        res_xml.append(state_intro)
        res_xml.append(state_menu)

    start_state.append(start_tr)

    #res = '<states><state name="Start"><transition input="start" next="start">It works better!</transition></state></states>'
    res = tostring(res_xml)
    return res


def create_bot(scenario, name):
    bot = Bot()
    bot.name = name
    bot.language = 1
    bot.fancy_name = name

    bot.scenario = '<fsm name="{name}">'.format(name=bot.name) + scenario + '</fsm>'

    client = Chatfirst(token=current_app.config["CHATFIRST_TOKEN"])
    return client.bots_update(bot)
