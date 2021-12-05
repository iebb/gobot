import asyncio

from graia.application import GraiaMiraiApplication, Session, Friend, FriendMessage, GroupMessage, Member, Group, \
    MessageChain
from graia.application.message.elements.internal import At, Plain
from graia.broadcast import Broadcast

from config import QQ_ACCOUNT, SESSION_AUTHKEY

loop = asyncio.new_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://121.37.254.238:13331",
        authKey=SESSION_AUTHKEY,
        account=QQ_ACCOUNT,
    )
)


from handler import messageHandler


@bcc.receiver("FriendMessage")
async def event(app: GraiaMiraiApplication, friend: Friend, message: FriendMessage):
    print("member", friend.id, "message", message.messageChain)
    result = await messageHandler(app, message, lambda k: app.sendFriendMessage(friend, MessageChain.create(k)))
    if result:
        await app.sendFriendMessage(friend, MessageChain.create(result))


@bcc.receiver("GroupMessage")
async def event(app: GraiaMiraiApplication, group: Group, member: Member, message: GroupMessage):
    print("member", member.id, "message", message.messageChain)
    result = await messageHandler(app, message, lambda k: app.sendGroupMessage(group, MessageChain.create(k)))
    if result:
        # result = [At(member.id), Plain(":\n")] + result
        await app.sendGroupMessage(group, MessageChain.create(result))



app.launch_blocking()

