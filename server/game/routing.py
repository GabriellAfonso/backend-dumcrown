from django.urls import path
from game.consumer import TestConsumer

websocket_urlpatterns = [
    path("ws/game/", TestConsumer.as_asgi()),
]
