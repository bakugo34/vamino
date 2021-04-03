from lib import objects, pack
from lib.headers import Headers
import requests
import json

refId = 712543354323901337


class GlobalClient:
    def __init__(self):
        self.deviceId = "019B6133991CBC2428F822E55AEF0499B3E674928B3268072CC9381881024F07047DCB9A82899C91B8"
        self.api = 'https://service.narvii.com/api/v1/'
        self.chat = '/s/chat/thread/'
        self.sid = None

    def login(self, email: str, password: str):
        data = json.dumps({
            "email": email,
            "secret": f"0 {password}",
            "deviceID": self.deviceId,
            "clientType": 100,
            "action": "normal",
        })
        request = requests.post(f"{self.api}/g/s/auth/login", headers={
            "NDCDEVICEID": "019B6133991CBC2428F822E55AEF0499B3E674928B3268072CC9381881024F07047DCB9A82899C91B8"
        }, data=data)
        global Data
        Data = json.loads(request.text)
        if request.status_code != 200: return Data['api:message']

    def send_message(self, chatId: str, message: str, refId: int = pack.timestamp() // 1000, type: int = 0):
        data = {
            'content': message,
            'type': type,
            'clientRefId': refId
        }
        data = json.dumps(data)
        r = requests.post(url=f'{self.api}g{self.chat + chatId}/message', data=data, headers=Headers(Data).headers).text
        request = json.loads(r)
        return objects.ApiMsg(response=request)

    def join_chat(self, chatId: str):
        r = requests.post(url=f'{self.api}g{self.chat + chatId}/member/' + Headers(Data).uid, headers=Headers(Data).headers).text
        request = json.loads(r)
        return objects.ApiMsg(response=request)

    def leave_chat(self, chatId: str):
        r = requests.delete(url=f'{self.api}g{self.chat + chatId}/member/' + Headers(Data).uid, headers=Headers(Data).headers).text
        request = json.loads(r)
        return objects.ApiMsg(response=request)

    def get_from_link(self, link: str):
        r = requests.get(f'{self.api}g/s/link-resolution?q={link}', headers=Headers(Data).headers).text
        request = json.loads(r)
        return objects.LinkInfo(response=request['linkInfoV2'])

    def Data(self):
        return Data

GlobalClient().login('ridahmad20@gmail.com', 'madarahhhh22')
