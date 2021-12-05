import requests


def get_b5csgo_account(steamid_32):
    try:
        b5_userinfo_url = f"https://api.xiaoheihe.cn/game/csgo/b5/get_player_overview/?hkey=d&account_id={steamid_32}"
        resp = requests.get(b5_userinfo_url, headers={
            'Content-Type': "application/json",
            'User-Agent': "xiaoheihe/1.3.114 (iPhone; iOS 13.1.2; Scale/3.00)",
        }).json()
        if resp["result"]["player_info"]["nickname"] != "匿名玩家":
            return resp["result"]
    except:
        pass
    return None

