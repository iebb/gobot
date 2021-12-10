import os

import requests
from graia.application.message.elements.internal import Plain, Image

from utils.imagen import create_signature
from utils.consts import bindMessage, convertTimeStamp, noPlatformMessage
from utils.db import get_db_cur, get_sender_account
from utils.fivee import get_five_e_data


async def fiveEMatches(app, message, reply, index=0):

    account = get_sender_account(message.sender.id, '5e_id', index)
    if account == "ACCOUNT_NOT_EXIST":
        return [noPlatformMessage]
    if not account:
        return [bindMessage]

    five_e_data = get_five_e_data(account)
    response = [
        Plain("5e 用户名：" + five_e_data["user"]["username"]),
    ]
    try:
        response += [
            Plain(f"\n本赛季 "
                  f"{five_e_data['data']['match_total']} 场 / "
                  f"Elo {five_e_data['data']['elo']} / "
                  f"Rtg {five_e_data['data']['rating']} / "
                  f"KD {five_e_data['data']['kill_death']} / "
                  f"MVP {five_e_data['data']['mvp_total']} / "
                  f"Ace {five_e_data['data']['kill_5']}"),
        ]
    except:
        pass

    response += [Plain("\n-------------------")]
    if five_e_data["match"]:
        for row in five_e_data["match"][:8]:
            s1 = int(row["group1_all_score"])
            s2 = int(row["group2_all_score"])
            is_team1 = row["group_id"] == "1"
            team1_score = ("[%d]" if is_team1 else "%d") % s1
            team2_score = ("[%d]" if not is_team1 else "%d") % s2
            win = (
                is_team1 and s1 > s2
            ) or (
                not is_team1 and s1 < s2
            )
            if s1 == s2:
                symbol = '💛'
            elif win:
                symbol = '💚'
            else:
                symbol = '💔'
            change_elo_text = row['change_elo']
            change_elo = float(row['change_elo'])
            base_elo = float(row['origin_elo'])
            if float(change_elo_text) > 0:
                change_elo_text = "+" + change_elo_text

            final_elo = round(base_elo + change_elo, 2)

            msg = f"\n{symbol} {convertTimeStamp(int(row['start_time']))} {row['map']}\n" \
                  f"{team1_score} - {team2_score} / {row['kill']}-{row['death']} / Rating {row['rating']}"
            if base_elo > 0:
                msg += f" Elo: {final_elo} ({change_elo_text})"
            response += [Plain(msg)]

    return response


async def fiveESignature(app, message, reply, index=0):

    account = get_sender_account(message.sender.id, '5e_id', index)
    if account == "ACCOUNT_NOT_EXIST":
        return [noPlatformMessage]
    if not account:
        return [bindMessage]

    five_e_data = get_five_e_data(account)
    avatar_link = five_e_data["user"]["avatar_url"]

    basename = "avatars/" + os.path.basename(avatar_link)
    if not os.path.isfile(basename):
        open(basename, "wb+").write(requests.get(avatar_link).content)

    user_info = {
        'platform_icon': 'data/5e.ico',
        'name': five_e_data["user"]["username"],
        'code': "Rating %.2f | Elo %.2f" % (
            float(five_e_data['data']['rating']),
            float(five_e_data['data']['elo']),
        ),
        'avatar': basename,
    }

    results = []
    if five_e_data["match"]:
        for row in five_e_data["match"][:10]:
            map = row["map"].split("_")[-1]
            mapLogo = "https://www.csgo.com.cn/images/maps/logo/%s.png" % map

            basename = "images/" + os.path.basename(mapLogo)
            if not os.path.isfile(basename):
                open(basename, "wb+").write(requests.get(mapLogo).content)

            results.append({
                'map': basename,
                'timestamp': int(row['end_time']),
                'score1': int(row['group1_all_score'] if row['group_id'] == "1" else row['group2_all_score']),
                'score2': int(row['group2_all_score'] if row['group_id'] == "1" else row['group1_all_score']),
                'rating': float(row['rating']),
                'elo': float(row['origin_elo']) + float(row['change_elo']),
                'elo_change': float(row['change_elo']),
            })

    return [
        Image.fromUnsafeBytes(create_signature(user_info, results)),
    ]
