import datetime

import pytz
from graia.application.message.elements.internal import Plain

bindMessage = Plain("请先绑定 CS:GO 账号 (命令：#绑定 XXXXX-XXXX）")

tz = pytz.timezone("Asia/Shanghai")


def convertTimeStamp(timestamp, format="%Y%m%d %H:%M"):
    return datetime.datetime.fromtimestamp(
        timestamp, tz=tz
    ).strftime(format)
