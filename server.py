# import socket
# # UDP-сервер
# # Создаем сокет
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# # Привязываем сокет к IP-адресу и порту
# server_socket.bind(('', 12345))
# print(server_socket)
#
# print("Сервер запущен и ожидает входящих данных...")
#
# # Получаем данные от клиента
# data, client_address = server_socket.recvfrom(1024)
# print(f"Получены данные от {client_address}: {data}")
#
# # Закрываем сокет
# server_socket.close()


import socket

UDP_IP = "185.165.160.158"
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print(data)
    print(addr)
    print("received message: %s" % data)


# import asyncio
# from websockets.server import serve
#
# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send(message)
#
# async def main():
#     async with serve(echo, "localhost", 8765):
#         await asyncio.Future()  # run forever
#
# asyncio.run(main())



# # TCP-сервер
# # Создаем сокет
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # Привязываем сокет к IP-адресу и порту
# server_socket.bind(('localhost', 12345))
#
# # Слушаем входящие соединения
# server_socket.listen(1)
#
# print("Сервер запущен и ожидает подключений...")
#
# # Принимаем входящее соединение
# client_socket, client_address = server_socket.accept()
# print(f"Подключение установлено с {client_address}")
#
# # Получаем данные от клиента
# data = client_socket.recv(1024)
# print(f"Получены данные: {data}")
#
# # Закрываем соединения
# client_socket.close()
# server_socket.close()