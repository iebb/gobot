import os

import requests
from graia.application.message.elements.internal import Plain, Image

from utils.imagen import create_signature
from utils.consts import bindMessage, convertTimeStamp
from utils.db import get_db_cur
from utils.wmpvp import get_csgo_history


async def perfectWorldMatches(app, message, reply, data_source=0):

    db, cur = get_db_cur()
    cur.execute("SELECT steamid64 FROM accounts WHERE qq = ?", (message.sender.id, ))
    row = cur.fetchone()
    if row:
        wanmei_data = get_csgo_history(row[0], 8, data_source)

        response = [
            Plain("Steam 用户名：" + wanmei_data["user-info"]["name"]),
            Plain(f"\n国服：\n"
                  f"{wanmei_data['basic-data']['totalMatch']} 场 / "
                  f"Rtg {wanmei_data['basic-data']['rating']} / "
                  f"KD {wanmei_data['basic-data']['kd']} / "
                  f"MVP {wanmei_data['basic-data']['mvpCount']}"),
        ]

        response += [Plain("\n-------------------")]

        for row in wanmei_data["match"]:
            team1 = ("[%d]" if row["team"] == 1 else "%d") % row["score1"]
            team2 = ("[%d]" if row["team"] == 2 else "%d") % row["score2"]
            win = (
                row["team"] == 1 and row["score1"] > row["score2"]
            ) or (
                row["team"] == 2 and row["score1"] < row["score2"]
            )
            if row["score1"] == row["score2"]:
                symbol = '💛'
            elif win:
                symbol = '💚'
            else:
                symbol = '💔'
            ty = ' [' + row['mode'].replace("竞技", "") + ']'
            msg = f"\n{symbol} {convertTimeStamp(row['timeStamp'])} {row['mapName']}{ty}\n" \
                  f"{team1} - {team2} / {row['kill']}-{row['assist']}-{row['death']} / Rating {row['rating']}"
            response += [Plain(msg)]
    else:
        response = [bindMessage]

    return response


async def perfectWorldSignature(app, message, reply, data_source=0):
    db, cur = get_db_cur()
    cur.execute("SELECT steamid64 FROM accounts WHERE qq = ?", (message.sender.id, ))
    row = cur.fetchone()
    if not row:
        return [bindMessage]

    wanmei_data = get_csgo_history(row[0], 10, data_source)
    basename = "avatars/" + os.path.basename(wanmei_data["user-info"]['avatar'])
    if not os.path.isfile(basename):
        open(basename, "wb+").write(requests.get(wanmei_data["user-info"]['avatar']).content)

    user_info = {
        'platform_icon': [
            'data/cs.ico', 'data/steamchina_101.ico',
            'data/steamchina_102.ico', 'data/wmpvp.ico'
        ][data_source],
        'name': wanmei_data["user-info"]['name'],
        'code': wanmei_data["basic-data"]['friendCode'],
        'avatar': basename,
    }

    results = []
    for row in wanmei_data["match"]:
        basename = "images/" + os.path.basename(row['mapLogo'])
        if not os.path.isfile(basename):
            open(basename, "wb+").write(requests.get(row['mapLogo']).content)
        results.append({
            'map': basename,
            'timestamp': row['timeStamp'],
            'score1': row['score1'] if row['team'] == 1 else row['score2'],
            'score2': row['score2'] if row['team'] == 1 else row['score1'],
            'rating': row['rating'],
            'elo': row['pvpScore'],
            'elo_change': row['pvpScoreChange'],
        })

    return [
        Image.fromUnsafeBytes(create_signature(user_info, results)),
    ]
