from channels.generic.websocket import AsyncWebsocketConsumer
import json




class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print(f"WebSocket connected: {self.channel_name}")
        # Создайте экземпляр игры


    async def disconnect(self, close_code):
        print(f"WebSocket disconnected: {self.channel_name}")

    async def receive(self, text_data):
        # Принимаем данные от клиента (если нужно)
        pass

    async def game_data(self, event):
        # Получите данные игры из метода send_game_data_to_websocket класса Game
        game_data = event["data"]

        await self.send(text_data=game_data)




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
