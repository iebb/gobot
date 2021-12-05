import requests
import pprint

def get_csgo_history(steam_id_64, page_size=0, data_source=0):
    data = requests.post(
        "https://api.wmpvp.com/api/v1/home/user",
        json={
            "platform": "admin",
            "gameAbbr": "CSGO",
            "steamId": str(steam_id_64),
            "dataSource": data_source,
            "pageSize": page_size
        }
    ).json()
    # pprint.pprint(data)
    result = {}
    for k in data["data"]:
        result[k["group"]] = k["data"]
    return result

