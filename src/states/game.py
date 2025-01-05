import pygame as pg
import random, math
from .state import State
from .. import assets
from ..entity import Entity, Group
from ..display import Display
from ..player import Player
from ..shield import Shield 
from ..bar import Bar
from ..wave import WaveManager


class Game(State):
    def __init__(self, window: pg.Surface, display: Display, previous_state) -> None:
        super().__init__(window, display, previous_state)
        self.window = window
        self.display = display

        self.frame = 0

        # Colors
        self.bg_color = pg.Color(16, 20, 31)
        self.alt_bg_color = pg.Color(37, 86, 46)

        # Class initialization
        self.player = Player(assets.images["player"], (display.display.width//2, display.display.height//2))
        self.shield = Shield(assets.images["shield"], self.player.rect.center)

        self.charge_bar = Bar(assets.images["bar"], assets.images["charge"], [8, 4])

        self.wave = WaveManager()

        # All entities
        self.all_entities = Group()

        self.grass = Group()
        for _ in range(random.randint(3, 5)):
            self.grass.add(Entity(assets.images["grass"].images[f"{random.randint(0, 2)}"], (random.randint(10, 54), random.randint(10, 54))))

        self.all_entities.add(self.grass)
        self.all_entities.add(self.charge_bar)
        self.all_entities.add(self.player)
        self.all_entities.add(self.shield)

    def update(self):
        # Resets screen
        self.window.fill("black")
        self.display.display.fill(self.bg_color)

        # Updating player
        self.all_entities.update(player_pos= self.player.pos, charge= self.shield.charge)
        self.wave.update(player_pos= self.player.pos, shield_rect= self.shield.rect, shield_mask= self.shield.mask, swinging= self.shield.swing,)

        # Add entities to display buffer
        self.display.add(self.grass)
        self.display.add(self.player)
        self.display.add(self.shield)
        self.display.add(self.wave)
        self.display.add(self.charge_bar)

        if self.frame == 60:
            self.frame = 0
        else:
            self.frame += 1

        self.display.update()
