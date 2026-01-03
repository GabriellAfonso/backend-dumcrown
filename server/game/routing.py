from django.urls import path

from game.consumers.connection import ConnectionConsumer

websocket_urlpatterns = [
    path("ws/connection/", ConnectionConsumer.as_asgi()),
]
