import sqlite3

from graia.application.message.elements.internal import Plain, Image, At

from utils.b5csgo import get_b5csgo_account
from utils.db import get_db_cur, get_sender_all_accounts, set_main_account
from utils.faceit import get_faceit_account
from utils.fivee import get_five_e_account
from utils.steamid import friend_code_to_steamid, steam_id_32_to_64, steam_id_64_to_32
from utils.wmpvp import get_csgo_history


async def update_steamid32(steamid32):
    steam_id32 = int(steamid32)
    steam_id64 = steam_id_32_to_64(steam_id32)

    name_wm = ''
    name_steam = ''
    name_5e = ''
    name_b5 = ''
    name_faceit = ''

    wanmei_data = get_csgo_history(steam_id64)
    name_steam = wanmei_data["user-info"]["name"]

    b5 = get_b5csgo_account(wanmei_data['user-info']['steam_id'])
    if b5:
        name_b5 = b5["player_info"]["nickname"]

    five_e = get_five_e_account(wanmei_data['user-info']['steam_id64'])
    if five_e:
        name_5e = five_e["user"]["username"]

    faceit = get_faceit_account(wanmei_data['user-info']['steam_id64'])
    if faceit:
        name_faceit = faceit["nickname"]

    db, cur = get_db_cur()
    # "friendCode = ?, "
    cur.execute(
        "UPDATE accounts SET "
        "`5e_id` = ?, `b5_id` = ?, `faceit_id` = ?, "
        "name_steam = ?, name_wm = ?, name_5e = ?, name_b5 = ?, name_faceit = ? WHERE steamid32 = ?",
        (
            # wanmei_data["basic-data"]["friendCode"],
            five_e["user"]["domain"] if five_e else None,
            steam_id32 if b5 else None,
            faceit["id"] if faceit else None,
            name_steam, name_wm, name_5e, name_b5, name_faceit, steam_id32
        )
    )
    db.commit()



async def bindAccount(app, message, reply=None, friend_code=None, steamid32=None, steamid64=None, need_binding=False):

    if steamid64:
        steam_id64 = int(steamid64)
        steam_id32 = steam_id_64_to_32(steam_id64)
    elif steamid32:
        steam_id32 = int(steamid32)
        steam_id64 = steam_id_32_to_64(steam_id32)
    else:
        steam_id32 = friend_code_to_steamid(friend_code.upper())
        steam_id64 = steam_id_32_to_64(steam_id32)

    name_wm = ''
    name_steam = ''
    name_5e = ''
    name_b5 = ''
    name_faceit = ''

    wanmei_data = get_csgo_history(steam_id64)

    if reply is not None:
        print("replying", wanmei_data["user-info"]["name"])
        await reply([
            Plain("Steam 用户名：" + wanmei_data["user-info"]["name"]),
            Plain("\n正在查询 完美/5E/B5/FACEIT 中")
        ])
        name_steam = wanmei_data["user-info"]["name"]


    await reply([
        Plain(f"国服：\n"
              f"{wanmei_data['basic-data']['totalMatch']} 场 / "
              f"Rtg {wanmei_data['basic-data']['rating']} / "
              f"KD {wanmei_data['basic-data']['kd']} / "
              f"MVP {wanmei_data['basic-data']['mvpCount']}"),
        # await Image.fromRemote(wanmei_data["user-info"]["avatar"]),
    ])

    b5 = get_b5csgo_account(wanmei_data['user-info']['steam_id'])
    if b5:
        try:
            await reply([
                Plain("B5 用户名：" + b5["player_info"]["nickname"]),
                Plain(f"\nElo {b5['career']['header'][0]['value']} / 排名 {b5['career']['header'][1]['value']}"),
            ])
            name_b5 = b5["player_info"]["nickname"]
        except:
            pass

    five_e = get_five_e_account(wanmei_data['user-info']['steam_id64'])
    if five_e:
        try:
            await reply([
                Plain("5e 用户名：" + five_e["user"]["username"]),
                Plain(f"\nElo {five_e['data']['elo']} / Rtg {five_e['data']['rating']} / RWS {five_e['data']['rws']}"),
            ])
            name_5e = five_e["user"]["username"]
        except:
            pass

    faceit = get_faceit_account(wanmei_data['user-info']['steam_id64'])
    if faceit:
        try:
            await reply([
                Plain("Faceit 用户名：" + faceit["nickname"]),
                Plain(f"\n{faceit['stats']['m1']} 场 / Elo {faceit['elo']} / 胜率 {faceit['stats']['k6']}% / KD {faceit['stats']['k5']}"),
            ])
            name_faceit = faceit["nickname"]
        except:
            pass

    if need_binding:
        db, cur = get_db_cur()
        cur.execute(
            "REPLACE INTO accounts ("
            "qq, steamid64, steamid32, friendCode, `5e_id`, `b5_id`, `faceit_id`, "
            "name_steam, name_wm, name_5e, name_b5, name_faceit, is_last_used"
            ") VALUES ("
            "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                message.sender.id,
                steam_id64,
                steam_id32,
                wanmei_data["basic-data"]["friendCode"],
                five_e["user"]["domain"] if five_e else None,
                steam_id32 if b5 else None,
                faceit["id"] if faceit else None,
                name_steam, name_wm, name_5e, name_b5, name_faceit, 0
            )
        )
        db.commit()


async def listAccounts(app, message, reply):
    s = list(get_sender_all_accounts(message.sender.id))
    resp = [At(message.sender.id), Plain(" 绑定了 %d 个账号:" % len(s))]

    for idx, a in s:
        line = "\n#%d:" % idx
        if a['name_steam']:
            line += " Steam: %s" % a['name_steam']
        else:
            await update_steamid32(int(a['steamid32']))
            line += " SteamID: %s" % a['steamid32']
        if a['name_5e']:
            line += " / 5E: %s" % a['name_5e']
        if a['name_b5']:
            line += " / B5: %s" % a['name_b5']
        if a['name_faceit']:
            line += " / Faceit: %s" % a['name_faceit']
        if a['is_last_used']:
            line += " [MAIN]"

        resp.append(Plain(line))
    resp.append(Plain("\n可以用 #主账号#X 设置主账号"))
    return resp


async def setMainAccount(app, message, reply, index=0):
    a = set_main_account(message.sender.id, index)
    if a:
        resp = [At(message.sender.id), Plain("设置主账号成功:")]

        line = "\n#%s:" % index
        if a['name_steam']:
            line += " Steam: %s" % a['name_steam']
        else:
            await update_steamid32(int(a['steamid32']))
            line += " SteamID: %s" % a['steamid32']
        if a['name_5e']:
            line += " / 5E: %s" % a['name_5e']
        if a['name_b5']:
            line += " / B5: %s" % a['name_b5']
        if a['name_faceit']:
            line += " / Faceit: %s" % a['name_faceit']

        resp.append(Plain(line))
    else:
        resp = [At(message.sender.id), Plain("设置主账号失败")]
    return resp

