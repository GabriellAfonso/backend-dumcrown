from .base import BaseConsumer
from django.core.cache import cache


class ConnectionConsumer(BaseConsumer):
    location = "global"

    async def connect(self):
        await super().connect()

        await self.channel_layer.group_add(
            "online_players",
            self.channel_name,
        )

        await self.set_heartbeat()
        await self.send_ok(event="connected")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            "online_players",
            self.channel_name,
        )

        await super().disconnect(code)

    # ---------- Handlers ----------

    async def handle_ping(self, content):
        await self.set_heartbeat()
        await self.send_ok(event="pong")

    async def handle_set_location(self, content):
        location = content.get("location")

        if not location:
            await self.send_error("location is required")
            return

        self.location = location

        cache.set(
            f"player_location:{self.user.id}",
            location,
            timeout=60,
        )

        await self.send_ok(event="location_updated", location=location)
