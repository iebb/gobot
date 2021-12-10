from graia.application.message.elements.internal import Plain
from utils.b5csgo import get_b5csgo_account
from utils.consts import bindMessage, convertTimeStamp, noPlatformMessage
from utils.db import get_db_cur, get_sender_account


async def B5Matches(app, message, reply, index=0):

    account = get_sender_account(message.sender.id, 'b5_id', index)
    print(account)
    if account == "ACCOUNT_NOT_EXIST":
        return [noPlatformMessage]
    if not account:
        return [bindMessage]

    b5 = get_b5csgo_account(account)
    response = [
        Plain("B5 用户名：" + b5["player_info"]["nickname"]),
        Plain(f" Elo {b5['career']['header'][0]['value']} / 排名 {b5['career']['header'][1]['value']}"),
    ]

    for row in b5["matches"][:5]:
        print(row)
        result = row["win"]
        if result == 0:
            symbol = '💔'
        elif result == 1:
            symbol = '💚'
        else:
            symbol = '💛'

        row['updateTime'] = convertTimeStamp(row['time'])

        msg = f"\n{symbol} {row['updateTime']} {row['class_name']} {row['map_name']}\n" \
              f"{row['score']} / {row['kill']}K {row['assist']}A {row['death']}D"

        try:
            if row["elo_change"] == "定级赛":
                msg += f" ({row['elo_change']})"
            elif row["elo_change"] != "--":
                msg += f" Elo {round(row['elo'], 2)} ({row['elo_change']})"
        except:
            pass

        response += [Plain(msg)]

    return response
