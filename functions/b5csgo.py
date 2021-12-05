from graia.application.message.elements.internal import Plain
from utils.b5csgo import get_b5csgo_account
from utils.consts import bindMessage, convertTimeStamp
from utils.db import get_db_cur


async def B5Matches(app, message, reply):

    db, cur = get_db_cur()
    cur.execute("SELECT `b5_id` FROM accounts WHERE qq = ?", (message.sender.id, ))
    row = cur.fetchone()
    if row and row[0]:
        b5 = get_b5csgo_account(row[0])
        response = [
            Plain("B5 用户名：" + b5["player_info"]["nickname"]),
            Plain(f" Elo {b5['career']['header'][0]['value']} / 排名 {b5['career']['header'][1]['value']}"),
        ]

        for row in b5["matches"][:5]:
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
    else:
        response = [bindMessage]

    return response
