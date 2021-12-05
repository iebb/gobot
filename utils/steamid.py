offset_pos = [
    0, 9, 8, 7, 19, 18, 3, 2,
    14, 13, 12, 11, 23, 22, 21, 20,
    32, 17, 16, 15, 27, 26, 25, 34,
    36, 35, 44, 29, 31, 30, 39, 38
]
alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'


def friend_code_to_steamid(friend_code):
    val = 0
    for x in friend_code.replace("-", ""):
        val <<= 5
        val += alphabet.find(x)

    steamid = 0
    for x in offset_pos:
        steamid <<= 1
        if val & 1 << x:
            steamid |= 1

    return steamid


def steam_id_32_to_64(steamid32):
    return 76561197960265728 + steamid32


def steam_id_64_to_32(steamid64):
    return steamid64 & 0xffffffff
