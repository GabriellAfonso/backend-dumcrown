from django.urls import path

from game.consumers.connection import ConnectionConsumer
from game.consumers.matchmaking import MatchmakingConsumer
from game.consumers.match import MatchConsumer

websocket_urlpatterns = [
    path("ws/connection/", ConnectionConsumer.as_asgi()),
    path("ws/matchmaking/", MatchmakingConsumer.as_asgi()),
    path("ws/match/", MatchConsumer.as_asgi()),
]
