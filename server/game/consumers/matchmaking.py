from .base import BaseConsumer
from django.core.cache import cache
import uuid


MATCHMAKING_QUEUE_KEY = "matchmaking_queue"


class MatchmakingConsumer(BaseConsumer):

    async def connect(self):
        await super().connect()
        print('conectou ao matchmaking')
        await self.join_queue()

    async def disconnect(self, code):
        await self.leave_queue()
        await super().disconnect(code)

    async def join_queue(self):
        """Adiciona o jogador à fila e tenta criar um match"""
        queue = cache.get(MATCHMAKING_QUEUE_KEY, [])
        queue.append(self.user.id)
        cache.set(MATCHMAKING_QUEUE_KEY, queue, timeout=None)

        # se houver pelo menos 2 jogadores, cria um match
        if len(queue) >= 2:
            player1 = queue.pop(0)
            player2 = queue.pop(0)
            cache.set(MATCHMAKING_QUEUE_KEY, queue, timeout=None)

            # Cria um ID de match aleatório (ou qualquer lógica)
            match_id = str(uuid.uuid4())

            # Envia evento para os dois jogadores conectarem ao MatchConsumer
            for player_id in [player1, player2]:
                await self.send_event(
                    type="match_found",
                    payload={
                        "match_id": match_id,
                        "players": [player1, player2],
                    }
                )

            print(f'id da partida{match_id}')

    async def leave_queue(self):
        """Remove o jogador da fila caso desconecte antes de parear"""
        queue = cache.get(MATCHMAKING_QUEUE_KEY, [])
        if self.user.id in queue:
            queue.remove(self.user.id)
            cache.set(MATCHMAKING_QUEUE_KEY, queue, timeout=None)
