import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.1'
port = 8765
print(client_socket)
client_socket.bind(('', 0))
print(client_socket)
# client_socket.bind((host, port))
# print(client_socket.getsockname())
# Отправляем данные серверу
try:
    client_socket.sendto('Hello111, server! from pygbag!'.encode('utf-8'), (host, port))
    print('host', host, 'port: ', port)
    print(client_socket.getsockname())
    print('OK OK OK OK OK')
except Exception as e:
    print(f'cant sendto socket: ----{e}')
# Закрываем сокет
client_socket.close()