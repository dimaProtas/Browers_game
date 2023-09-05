import os
import subprocess
import asyncio
from channels.layers import get_channel_layer
import json

def run_game_and_send_data():
    current_directory = os.getcwd()  # Сохраняем текущую директорию
    try:
        game_directory = "C:\\Users\\dima_protasevich\\Documents\\devTem\\GB_dev_agile_web\\web\\game_src\\doom_game"
        os.chdir(game_directory)
        subprocess.run(["python", "main.py"], cwd=game_directory, shell=True)

        # Получите данные из игры (замените это на вашу логику)
        # game_data = {"message": "Game started!"}

        # Отправьте данные в WebSocket
        # channel_layer = get_channel_layer()
        # asyncio.get_event_loop().run_until_complete(channel_layer.group_add("game_group", "game_stream"))  # Подставьте сюда правильное имя consumer
        # asyncio.get_event_loop().run_until_complete(channel_layer.group_send(
        #     "game_group",
        #     {
        #         "type": "game_data",
        #         "data": json.dumps(game_data),
        #     },
        # ))

    finally:
        os.chdir(current_directory)  # Восстанавливаем текущую директорию

if __name__ == '__main__':
    run_game_and_send_data()
