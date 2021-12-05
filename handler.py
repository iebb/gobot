import re
from typing import Union

from graia.application import GraiaMiraiApplication
from graia.application import GroupMessage, TempMessage, FriendMessage

from functions.b5csgo import B5Matches
from functions.bindAccount import bindAccount
from functions.fivee import fiveEMatches, fiveESignature
from functions.hltv import hltvMatches
from functions.perfectworld import perfectWorldMatches, perfectWorldSignature

message_regex = [
    (r'^#绑定\s*'
     r'((?P<friend_code>[A-Za-z0-9]{5}-[A-Za-z0-9]{4})|'
     r'(?P<steamid64>76561\d{12})|'
     r'(?P<steamid32>\d{,10}))\s*$', bindAccount, {
        "need_binding": True
    }),
    (r'^#国服', perfectWorldMatches, {
        'data_source': 1,
    }),
    (r'^#国际服', perfectWorldMatches, {
        'data_source': 2,
    }),
    (r'^#完美', perfectWorldMatches, {
        'data_source': 3,
    }),
    (r'^%国服', perfectWorldSignature, {
        'data_source': 1,
    }),
    (r'^%国际服', perfectWorldSignature, {
        'data_source': 2,
    }),
    (r'^%完美', perfectWorldSignature, {
        'data_source': 3,
    }),
    (r'^#5E', fiveEMatches, {}),
    (r'^%5E', fiveESignature, {}),
    (r'^#B5', B5Matches, {}),
]


async def messageHandler(app: GraiaMiraiApplication, message: Union[GroupMessage, FriendMessage, TempMessage], reply=None):
    message_str = str(message.messageChain.asDisplay())
    message_str = message_str.replace("％", "%")
    for regex, handler, kwargs in message_regex:
        match = re.match(regex, message_str.upper())
        if match:
            print(regex, match.groupdict())
            h = handler(
                app=app,
                message=message,
                reply=reply,
                **match.groupdict(),
                **kwargs
            )
            if h is not None:
                return await h
    return False
