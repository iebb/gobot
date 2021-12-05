import requests


def get_b5csgo_account(steamid_32):
    try:
        b5_userinfo_url = f"https://www.b5csgo.com.cn/personalCenterV2Controller/user_info.do?steamId={steamid_32}"
        resp = requests.get(b5_userinfo_url).json()
        if resp["success"]:
            data = {
                "user": resp["data"],
            }
            power_url = f"https://www.b5csgo.com.cn/personalCenterV2Controller/power.do?steamId={steamid_32}"
            resp = requests.get(power_url).json()
            data["power"] = resp["data"]
            return data
    except:
        pass
    return None


def get_b5csgo_five_matches(steamid_32):
    resp = requests.get(
        f"https://www.b5csgo.com.cn/personalCenterV2Controller/recent_five_match.do?steamId={steamid_32}"
    ).json()
    if resp["success"]:
        return resp["data"]
    return None


def get_b5csgo_matches(steamid_32):
    resp = requests.get(
        f"https://www.b5csgo.com.cn/personalCenterV2Controller/match.do?pageNum=1&pageSize=20&steamId={steamid_32}"
    ).json()
    if resp["success"]:
        return resp["data"]
    return None
