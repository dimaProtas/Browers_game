import asyncio

import pygame as pg
import sys
import json
# sys.path.append('C:\\Users\\dima_protasevich\\Documents\\devTem\\GB_dev_agile_web\\web\\game_src\\doom_game\\')
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
from PIL import Image, ImageFilter
import io




class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        # Установите режим отображения без окна (headless)
        # self.screen = pg.display.set_mode((1, 1), pg.NOFRAME)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()
        self.frame_buffer = None

    async def get_game_data(self):
        game_data = {
            "player_position": (self.player.x, self.player.y),
            "player_health": self.player.health,
            # Другие данные из игры
        }
        return game_data

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    async def update(self):
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
        size_img = (300, 400)
        frame_image = Image.frombytes("RGB", self.screen.get_size(), pg.image.tostring(self.screen, "RGB"))
        frame_image.resize(size_img)
        self.frame_buffer = io.BytesIO()
        frame_image.save(self.frame_buffer, format="PNG")

    async def get_frame_bytes(self):
        if self.frame_buffer:
            return self.frame_buffer.getvalue()
        else:
            return b''

    async def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()




if __name__ == '__main__':
    game = Game()
    game.run()

