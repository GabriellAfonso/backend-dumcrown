from .base import BaseConsumer
from django.contrib.auth import get_user_model

User = get_user_model()


class MatchConsumer(BaseConsumer):

    async def connect(self):
        await super().connect()
        # opcional: print quando alguém conecta
        print(f"[MatchConsumer] {self.user.username} connected")

    async def disconnect(self, code):
        await super().disconnect(code)
        print(f"[MatchConsumer] {self.user.username} disconnected")

    async def receive_json(self, content, **kwargs):
        """
        Espera receber do cliente algo tipo:
        {
            "type": "join_match",
            "payload": {
                "match_id": "xxxx",
                "players": [1, 2]
            }
        }
        """
        msg_type = content.get("type")
        payload = content.get("payload", {})

        if msg_type == "join_match":
            player_ids = payload.get("players", [])
            players = User.objects.filter(id__in=player_ids)
            nicknames = [p.username for p in players]
            print(
                f"[MatchConsumer] Players in match {payload.get('match_id')}: {nicknames}")

            # opcional: confirmar para o cliente que recebeu
            await self.send_event(type="match_joined", payload={"players": nicknames})
