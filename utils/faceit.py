import requests


def get_faceit_account(steamid_64):
    faceit_api = f"https://api.faceit.com/search/v1?limit=3&query={steamid_64}"
    resp = requests.get(faceit_api).json()
    data = resp["payload"]["players"]["results"]
    if len(data):
        faceit_id = data[0]["id"]
        nickname = data[0]["nickname"]
        try:
            stats = requests.get(
                f"https://api.faceit.com/stats/v1/stats/users/{faceit_id}/games/csgo"
            ).json()["lifetime"]
            elo = requests.get(
                f"https://api.faceit.com/stats/v1/stats/time/users/{faceit_id}/games/csgo?page=0&size=1"
            ).json()[0]['elo']
        except:
            stats = {
                'm1': 0,
                'k6': 0,
                'k5': 0,
            }
            elo = "-"
        return {
            "id": faceit_id,
            "nickname": nickname,
            "elo": elo,
            "stats": stats,
        }
    return None
