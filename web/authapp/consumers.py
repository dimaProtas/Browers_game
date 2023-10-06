import sys
# sys.path.append('/game_src')
import asyncio
import threading
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
import json
# from game_src.doom_game.main import Game
from .models import MessagesModel
from channels.db import database_sync_to_async
import locale


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print(f"WebSocket connected: {self.channel_name}")
        await self.channel_layer.group_add("chat_group", self.channel_name)

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected: {self.channel_name}")
        await self.channel_layer.group_discard("chat_group", self.channel_name)

    @database_sync_to_async
    def save_message(self, sender, message_text):
        message = MessagesModel(sender=sender, message=message_text)
        message.save()

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message_text = data['message']
        sender = self.scope['user']
        await self.save_message(sender=sender, message_text=message_text)
        # Отправляем сообщение обратно всем в группу
        await self.send_message_to_group(sender, message_text)

    async def send_message_to_group(self, sender, message_text):
        locale.setlocale(locale.LC_TIME, 'ru_RU')
        formatted_datetime = timezone.localtime(timezone.now()).strftime('%d %B %Y г. %H:%M')
        locale.setlocale(locale.LC_TIME, '')
        # Отправка сообщения всем клиентам в группе
        await self.channel_layer.group_send(
            "chat_group",
            {
                "type": "chat.message",
                "sender": sender.username,
                "message": message_text,
                "timestamp": formatted_datetime,
            },
        )

    async def chat_message(self, event):
        # Отправка сообщения клиенту через WebSocket
        sender = event["sender"]
        message = event["message"]
        timestamp = event["timestamp"]
        await self.send(text_data=json.dumps({"sender": sender, "message": message, "timestamp": timestamp}))


# class GameConsumer(AsyncWebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.game_thread = None
#
#     async def send_game_data_to_websocket(self, game):
#         while True:
#             game_data = await game.get_game_data()
#             game_display = await game.get_frame_bytes()
#             print(game_display)
#             await self.send(json.dumps(game_data))
#             await self.send(bytes_data=game_display)
#             await asyncio.sleep(1)
#
#     async def connect(self):
#         await self.accept()
#         print(f"WebSocket connected: {self.channel_name}")
#         self.game = Game()
#         self.game_thread = threading.Thread(target=self.game.run)
#         self.game_thread.start()
#         asyncio.create_task(self.send_game_data_to_websocket(self.game))
#
#     async def disconnect(self, close_code):
#         print(f"WebSocket disconnected: {self.channel_name}")
#         if self.game_thread:
#             self.game_thread.join()


class TryMore():
    pass



# class GameConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#
#         #тестовые данные
#         test_data = {
#             "player_position": 100,
#             "player_health": 100
#         }
#
#         # Отправляем данные в WebSocket через заданное количество секунд
#         await asyncio.sleep(2)
#         await self.send(json.dumps(test_data))
#
#     async def disconnect(self, close_code):
#         pass
