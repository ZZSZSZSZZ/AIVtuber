import asyncio
import json

import websockets
from websockets import ConnectionClosed

from collections import namedtuple

# Blivedm 配置
BlivedmServer = "ws://localhost:12450/api/chat"  # 服务器地址
BlivedmRoomId = "22195814"  # 房间ID
blivedmHeartbeatMessage = '{"cmd": 0, "data": {}}'  # 心跳包消息
blivedmHeartbeatInterval = 20  # 心跳包发送间隔时间

# Blivedm Cmd 常量
blivedmCmdText = 2  # 文本消息
blivedmCmdGift = 3  # 礼物
blivedmCmdMember = 4  # 上舰
blivedmCmdSuperChat = 5  # SC

# 结构体定义
blivedmMessage = namedtuple('blivedmMessage', ['cmd', 'data'])  # 消息结构体
# textMessageDatatest = namedtuple('textMessageDatatest', ['AvatarUrl', 'Timestamp', 'AuthorName', 'AuthorType',
# 'Content', 'PrivilegeType', 'IsGiftDanmaku', 'AuthorLevel', 'IsNewbie', 'IsMobileVerified', 'MedalLevel'])
textMessageData = namedtuple('textMessageData', ['AuthorType', 'Content'])  # 文本消息结构体
giftMessageData = namedtuple('giftMessageData', ['AuthorName', 'GiftName'])  # 礼物结构体
superChatMessageData = namedtuple('superChatMessageData', ['AuthorName', 'Content'])  # SC结构体

# 用于发送心跳包
async def KeepAlive(websocket):
    while True:
        try:
            await websocket.send(blivedmHeartbeatMessage)
            await asyncio.sleep(blivedmHeartbeatInterval)
        except:
            break


# 获取消息
async def GetMessage(blivedmServer, blivedmRoomId):
    while True:  # 用于断线重连
        try:
            async with websockets.connect(blivedmServer) as websocket:
                await websocket.send(json.dumps({"cmd": 1, "data": {"roomId": blivedmRoomId}}))
                asyncio.create_task(KeepAlive(websocket))

                while True:  # 获取消息
                    try:
                        message = await websocket.recv()
                        print(message)
                        MessageHandle(message)

                    except ConnectionClosed as e:
                        print(e.code)
                        if e.code == 1006 or e.code == 1005:
                            break
        except Exception as e:
            print(e)
            await asyncio.sleep(1)


# 消息处理
def MessageHandle(message):
    message = json.loads(message)
    message = blivedmMessage(message['cmd'], message['data'])  # 把读取到的消息写入消息结构体

    if message.cmd == blivedmCmdText:
        textMessage = textMessageData(message.data[3], message.data[4])
        print(textMessage.Content)
    elif message.cmd == blivedmCmdGift:
        giftMessage = giftMessageData(message.data['authorName'], message.data['giftName'])
        # print("礼物 - " + giftMessage.GiftName)
        # giftList.append(message['data']['giftName'])
    elif message.cmd == blivedmCmdSuperChat:
        superChatMessage = superChatMessageData(message.data['authorName'], message.data['Content'])
        print("sc")


if __name__ == '__main__':
    print("-----开始接收直播间消息-----")
    asyncio.run(GetMessage(BlivedmServer, BlivedmRoomId))
