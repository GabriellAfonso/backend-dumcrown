from channels.generic.websocket import AsyncWebsocketConsumer
import json


class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('conectou')
        await self.accept()
        await self.send_json({"message": "Conexão estabelecida."})

    async def receive(self, text_data=None, bytes_data=None):
        data = text_data or ""
        await self.send_json({"echo": data})

    async def disconnect(self, close_code):
        pass

    async def send_json(self, data):
        await self.send(text_data=json.dumps(data))
