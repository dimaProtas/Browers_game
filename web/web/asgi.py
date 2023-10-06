"""
ASGI config for web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
from django.core.asgi import get_asgi_application
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path

from authapp import consumers
import sys

sds = sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(sds)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
            URLRouter([
                # re_path(r'ws/game_stream/$', consumers.GameConsumer.as_asgi()),
                re_path(r'ws/messages/$', consumers.ChatConsumer.as_asgi()),
            ])
    ),
})


