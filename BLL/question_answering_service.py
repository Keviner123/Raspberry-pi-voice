import json
import requests
import asyncio
import websockets
from getmac import get_mac_address as gma

class QuestionAnsweringService:
    def __init__(self, url, macaddress):
        self.websocket = None
        self.url = url
        self.macaddress = macaddress
        self.token = None

    async def connect(self):
        self.websocket = await websockets.connect(self.url)

    async def authenticate(self):
        if not self.websocket:
            await self.connect()
        await self.websocket.send('{"Type": "mac","Message": "'+self.macaddress+'"}')
        response = await self.websocket.recv()

        repsonse_json = json.loads(response)
        self.token = repsonse_json["Message"]

    def get_answer(self, question: str) -> str:

        url = "https://api.xn--prve-hra.xn--svendeprven-ngb.dk/api/question/device?question="+question

        payload={}
        headers = {
        'Authorization': 'Bearer '+self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=60)
        response = json.loads(response.text)

        return response["answer"]
