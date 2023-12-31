"""
ASGI config for web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django_asgi_app = get_asgi_application()


from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path

from authapp import consumers



application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
            URLRouter([
                # re_path(r'ws/game_stream/$', consumers.GameConsumer.as_asgi()),
                re_path(r'ws/messages/$', consumers.ChatConsumer.as_asgi()),
                re_path(r'ws/private_messages/$', consumers.PrivateMessageConsumer.as_asgi()),
                re_path(r'ws/notifications_messages/$', consumers.PrivateMessageConsumer.as_asgi()),
            ])
    ),
})


