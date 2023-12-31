import proto
import websockets
import asyncio
import json
import requests
from websockets import ConnectionClosed


# 22195814

class BiliRequest(object):
    def __init__(self, cookie):
        super(BiliRequest, self).__init__()
        self.cookie = cookie

    def get(self, url: str):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Cookie": self.cookie
        }
        return requests.get(url, headers=headers).text

    def get_danmu_info_data(self, room_id: int):
        request = self.get("https://api.live.bilibili.com/room/v1/Room/room_init?id=" + str(room_id))
        room_id = json.loads(request)["data"]["room_id"]
        request = self.get(
            "https://api.live.bilibili.com/xlive/web-room/v1/index/getDanmuInfo?type=0&id=" + str(room_id))
        return json.loads(request)["data"]


class Websocket(object):
    def __init__(self, ws_url, roomid, key):
        self.ws_url = ws_url
        self.roomid = roomid
        self.key = key

    def run(self):
        loop = asyncio.get_event_loop()
        # 建立连接
        websocket = loop.run_until_complete(self.connect())
        tasks = [
            # 读取信息
            asyncio.ensure_future(self.recvLoop(websocket)),
            # 发送心跳
            asyncio.ensure_future(self.heartBeat(websocket)),
        ]
        loop.run_until_complete(asyncio.gather(*tasks))

    # 建立连接
    async def connect(self):
        authbody = {"roomid":str(self.roomid)}
        authbody = '{"roomid":'+str(self.roomid)+'}'
        #authbody = '{"roomid":21652717}'

        #authbody = json.dumps(authbody)
        print(self.ws_url, authbody)
        websocket = await websockets.connect(self.ws_url)
        # 鉴权
        await self.auth(websocket, authbody)
        return websocket

    # 发送鉴权信息
    async def auth(self, websocket, authBody):
        req = proto.Proto()
        req.body = authBody
        req.op = 7
        await websocket.send(req.pack())
        buf = await websocket.recv()
        resp = proto.Proto()
        resp.unpack(buf)
        respBody = json.loads(resp.body)
        if respBody["code"] != 0:
            print("auth 失败")
        else:
            print("auth 成功")

    # 发送心跳
    async def heartBeat(self, websocket):
        while True:
            await asyncio.ensure_future(asyncio.sleep(30))
            req = proto.Proto()
            req.op = 2
            await websocket.send(req.pack())
            print("[BiliClient] send heartBeat success")

    # 读取信息
    async def recvLoop(self, websocket):
        print("[BiliClient] run recv...")
        while True:
            recvBuf = await websocket.recv()
            resp = proto.Proto()
            resp.unpack(recvBuf)



def openLiveRoom(room_id: int, cookie: str):
    bili_request = BiliRequest(cookie)
    danmu_info_data = bili_request.get_danmu_info_data(room_id)
    token = danmu_info_data["token"]
    host_list = danmu_info_data["host_list"]
    host = host_list[0]
    print(host)
    ws_url = "ws://" + str(host["host"]) + ":" + str(host["ws_port"]) + "/sub"
    ws = Websocket(ws_url, room_id, token)
    ws.run()


if __name__ == '__main__':
    cookie = "buvid3=55A7F2B7-B72F-ABE4-DF01-C7DB3AE4595999240infoc; b_nut=1695376399; _uuid=A2B9510CC-5B2B-86EB-CEDF-6EACB10C6995901438infoc; buvid4=5B925282-260C-3383-E6B7-17775B90AFA500142-023092217-YnAnJPmhdopuZQSVIs4HHw%3D%3D; CURRENT_FNVAL=4048; rpdid=|(J|)k)u)||u0J'uYmlJ~Y))k; buvid_fp_plain=undefined; DedeUserID=383048468; DedeUserID__ckMd5=3d16bc6092fca6e8; header_theme_version=CLOSE; is-2022-channel=1; enable_web_push=DISABLE; fingerprint=919b609a93c52df8c3b6ea2654d03d96; LIVE_BUVID=AUTO6916977215216594; CURRENT_QUALITY=116; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTgxNDEyNDQsImlhdCI6MTY5Nzg4MTk4NCwicGx0IjotMX0.5uRCYm2D9QelGpGD1b5bG7bCYWagfi4bKKCspbd6m40; bili_ticket_expires=1698141184; SESSDATA=bfd37e10%2C1713445818%2Cf36b1%2Aa2CjAkBQ0TpNIAltbv-lhYrV2lNtJnJ5XijVoHlHDRlqHzpNG8mBPsfVB84zdn0ueDFvYSVmxDMXVvdlUtc0FqQV9heS0wYV9XUG5uWkFmamNxQVUwQUQyazUwclEwZ0RYMXl3eTJqUVoyUmtrendPNEJ5djlFZmQxOS1oV1ZocW1jQ2ZGd0prRTJRIIEC; bili_jct=25293ee47f2d1a9f13899f8ecd99b4a5; sid=77vj6cbi; PEA_AU=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJiaWQiOjM4MzA0ODQ2OCwicGlkIjoyNDEwMDksImV4cCI6MTcyOTQ4MTAxMywiaXNzIjoidGVzdCJ9.SJ8oE3Ug8c_If2Z8yIa83ZEUVfUTE4GZtDioys5wqL4; bp_video_offset_383048468=855186907019083799; msource=pc_web; deviceFingerprint=9b28edbeaf1af06018920155593481fa; PVID=1; buvid_fp=919b609a93c52df8c3b6ea2654d03d96; bsource=search_baidu; b_lsid=310B9DB94_18B5698DF02; home_feed_column=4; browser_resolution=1006-1291"
    while True:
        try:
            openLiveRoom(22603245, cookie)
        except Exception as e:
            print("err", e)


