import sys

sys.path.append('/game_src')
import asyncio
import threading

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from game_src.doom_game.main import Game


class GameConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_thread = None

    async def send_game_data_to_websocket(self, game):
        while True:
            game_data = await game.get_game_data()
            game_display = await game.get_frame_bytes()
            print(game_display)
            await self.send(json.dumps(game_data))
            await self.send(bytes_data=game_display)
            await asyncio.sleep(1)

    async def connect(self):
        await self.accept()
        print(f"WebSocket connected: {self.channel_name}")
        self.game = Game()  # Создайте экземпляр игры
        self.game_thread = threading.Thread(target=self.game.run)
        self.game_thread.start()
        asyncio.create_task(self.send_game_data_to_websocket(self.game))

            # def run_game(self):
    #     game = Game()
    #     game.run()
    #     while True:
    #         game_data = game.get_game_data()
    #         asyncio.run_coroutine_threadsafe(self.send(json.dumps(game_data)), asyncio.get_event_loop())

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected: {self.channel_name}")
        if self.game_thread:
            self.game_thread.join()




# class GameConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#
#         # Пример тестовых данных
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
