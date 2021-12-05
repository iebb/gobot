import requests


def get_five_e_account(steamid64):
    five_e_username_url = f"http://app.5ewin.com/api/user/steam_username/{steamid64}"
    resp = requests.get(five_e_username_url).json()
    if resp["success"]:
        five_e_username = resp["data"]["username"]
        five_e_data_url = f"http://app.5eplay.com/api/csgo/data/search_player_data?username={five_e_username}"
        resp = requests.get(five_e_data_url).json()
        return resp["data"][0]
    return None


def get_five_e_data(five_e_id):
    resp = requests.get(f"http://app.5eplay.com/api/csgo/data/player_data/{five_e_id}").json()
    if resp["success"]:
        return resp["data"][0]
    return None


'''
resp = requests.get(f"http://app2.5eplay.com/api/csgo/data/player_match/{five_e_id}").json()
player["match"] = resp["data"]
return player
'''