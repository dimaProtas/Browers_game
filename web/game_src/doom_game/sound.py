import pygame as pg
import os

# Абсолютный путь к корневой директории игры
GAME_ROOT = os.path.abspath(os.path.dirname(__file__))

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = os.path.join(GAME_ROOT, 'resources', 'sound')  # Используйте os.path.join для объединения путей
        self.shotgun = pg.mixer.Sound(os.path.join(self.path, 'shotgun.wav'))  # Обновите путь
        self.npc_pain = pg.mixer.Sound(os.path.join(self.path, 'npc_pain.wav'))  # Обновите путь
        self.npc_death = pg.mixer.Sound(os.path.join(self.path, 'npc_death.wav'))  # Обновите путь
        self.npc_shot = pg.mixer.Sound(os.path.join(self.path, 'npc_attack.wav'))  # Обновите путь
        self.npc_shot.set_volume(0.2)
        self.player_pain = pg.mixer.Sound(os.path.join(self.path, 'player_pain.wav'))  # Обновите путь
        self.theme = pg.mixer.music.load(os.path.join(self.path, 'theme.mp3'))  # Обновите путь
        pg.mixer.music.set_volume(0.3)