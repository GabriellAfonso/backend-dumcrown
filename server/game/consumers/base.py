from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.cache import cache
from django.utils import timezone


class BaseConsumer(AsyncJsonWebsocketConsumer):
    user = None
    heartbeat_key = None

    async def connect(self):
        self.user = self.scope.get('user')

        if not self.user or not self.user.is_authenticated:
            await self.close(code=4001)
            return

        await self.accept()

    async def disconnect(self, code):
        if self.heartbeat_key:
            cache.delete(self.heartbeat_key)

    async def receive_json(self, content, **kwargs):
        msg_type = content.get('type')
        payload = content.get('payload')

        if not msg_type:
            return

        handler = getattr(self, f'handle_{msg_type}', None)
        if handler:
            await handler(payload)

    async def send_event(self, *, type: str, payload: dict | None = None):
        await self.send_json({
            'type': type,
            'payload': payload or {},
        })

    async def send_error(self, type: str, message: str, **extra):
        await self.send_event(
            type=type,
            payload={
                'error': message,
                **extra,
            }
        )

    async def set_heartbeat(self, ttl=30):
        self.heartbeat_key = f'presence:{self.user.id}'
        cache.set(
            self.heartbeat_key,
            {'last_seen': timezone.now().isoformat()},
            timeout=ttl,
        )
