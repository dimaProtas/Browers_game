# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path

from authapp import consumers

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        re_path(r'ws/game_stream/$', consumers.GameConsumer.as_asgi()),
    ]),
})
