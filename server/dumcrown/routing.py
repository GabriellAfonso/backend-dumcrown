from django.urls import path
from dumcrown.consumer import TestConsumer

websocket_urlpatterns = [
    path("ws/game/", TestConsumer.as_asgi()),
]
