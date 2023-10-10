# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import re_path
#
# from authapp import consumers
#
# # application = ProtocolTypeRouter({
# #     "websocket": URLRouter([
# #         re_path(r'ws/game_stream/$', consumers.GameConsumer.as_asgi()),
# #         re_path(r'ws/messages/$', consumers.ChatConsumer.as_asgi())
# #     ]),
# # })
#
#
#  websocket_urlpatterns= [
#     re_path(r'ws/messages/$', consumers.ChatConsumer.as_asgi()),
# ]
# from django.urls import re_path
#
# from authapp import consumers
#
# websocket_urlpatterns = [
#     re_path(r'ws/private_messages/(?P<user_id>\d+)/(?P<recipient_id>\d+)/$', consumers.PrivateMessageConsumer.as_asgi()),
# ]
