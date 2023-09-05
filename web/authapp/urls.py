from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from authapp import consumers, views


websocket_urlpatterns = [
    path("ws/game_stream/", consumers.GameConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)

urlpatterns = [
    path('game/', views.game, name='game'),
    path('game/doom_game/', views.start_game, name='start_game'),
]


