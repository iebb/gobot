import datetime
import sqlite3

import pytz
import requests
from graia.application.message.elements.internal import Plain, Image

from utils.consts import bindMessage, convertTimeStamp, tz
from utils.db import get_db_cur
from utils.wmpvp import get_csgo_history


async def hltvMatches(app, message, reply):

    url = "https://www.hltv.org/mobile/matches"
    data = requests.get(url).json()
    response = []
    data.sort(
        key=lambda x: x["startDateTime"] if "startDateTime" in x else "|"
    )

    prev_event = ""

    for match in list(filter(lambda x: not x["postMatch"], data))[:15]:

        msg = ""
        if prev_event != match["eventName"]:
            msg += '--------------\n'
            msg += match["eventName"] + "\n"
            prev_event = match["eventName"]

        dt = pytz.utc.localize(datetime.datetime.fromisoformat(
            match["startDateTime"].replace("Z", "")
        )).astimezone(tz).strftime("%m-%d %H:%M")

        tm = dt + " "
        if match["live"]:
            tm = "*LIVE* "

        msg += tm + \
               f'{match["team1"]["name"] if match["team1"] else match["placeholderText"]} - ' \
               f'{match["team2"]["name"] if match["team2"] else match["team2PlaceholderText"]}' \
               f' ({match["mapShort"]})\n'

        response += [Plain(msg)]

    return response
