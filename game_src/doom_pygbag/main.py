import socket

from map import *
from player import *
from raycasting import *
from object_renderer import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
import asyncio


dir = os.path.abspath(os.curdir)


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()

        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                # pg.quit()
                # sys.exit()
                pass
            elif event.type == self.global_event:
                self.global_trigger = True
            elif event.type == 768:  # enter k_button
                print('enter button')
                self.try_socket()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.player.single_fire_event(event)

    def try_socket(self):  # сокеты не работают в pygbag?
        # Создаем сокет UDP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # SOCK_DGRAM вроде работает
        host = '185.165.160.158'
        port = 8080
        print(client_socket)
        client_socket.bind(('', 0))
        print(client_socket)
        # client_socket.bind((host, port))
        # print(client_socket.getsockname())
        # Отправляем данные серверу
        try:
            client_socket.sendto('Hello, server! from pygbag!'.encode('utf-8'), (host, port))
            print('host', host, 'port: ', port)
            print(client_socket.getsockname())
            print('OK OK OK OK OK')
        except Exception as e:
            print(f'cant sendto socket: ----{e}')
        # Закрываем сокет
        client_socket.close()

        # # Создаем сокет TCP
        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #
        # # Подключаемся к серверу
        # client_socket.connect(('localhost', 12345))
        #
        # # Отправляем данные серверу
        # client_socket.sendall(b'Hello, server!')
        #
        # # Закрываем соединение
        # client_socket.close()

    # def send_file(self):
    #     # целевой URL-адрес
    #     url = 'http://127.0.0.1:8888/pygbag/'
    #     # открываем файл на чтение в
    #     # бинарном режиме ('rb')
    #     fp = open('C:\\Users\\vanka\\PycharmProjects\\game_project\\game\\text_data.txt', 'rb')
    #     # помещаем объект файла в словарь
    #     # в качестве значения с ключом 'file'
    #     files = {'file': fp}
    #     # передаем созданный словарь аргументу `files`
    #     resp = requests.post(url, files=files)
    #     fp.close()

    def send_data(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", 80))
        print(s.getsockname()[0])
        s.close()

    async def run(self):
        while True:
            # f = open(f'{dir}/text_data.txt', 'rb')
            # try:
            #     print(f.readlines())
            # finally:
            #     f.close()

            self.check_events()
            self.update()
            self.draw()
            # self.try_socket()
            await asyncio.sleep(0)


if __name__ == '__main__':

    game = Game()
    asyncio.run(game.run())
