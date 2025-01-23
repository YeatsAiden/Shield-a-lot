import pygame as pg

import random

from .. import assets, common
from .state import State
from ..entity import Entity
from ..group import Group
from ..player import Player
from ..health import Health
from ..shield import Shield 
from ..bar import Bar
from ..wave import WaveManager


class Game(State):
    def __init__(self, window: pg.Surface, display: pg.Surface, previous_state) -> None:
        super().__init__(window, display, previous_state)
        self.window = window
        self.display = display

        # Class initialization
        self.health = Health(assets.images["heart"], [54, 4])
        self.player = Player(assets.images["player"], (display.width//2, display.height//2))
        self.shield = Shield(assets.images["shield"], self.player.rect.center)

        self.charge_bar = Bar(assets.images["bar"], assets.images["charge"], [8, 4])

        self.wave = WaveManager()

        # All entities
        self.entities = Group()
        
        self.entities.add(*[Entity(assets.images["grass_spritesheet"].images[f"{random.randint(0, 2)}"], (random.randint(10, 54), random.randint(10, 54))) for _ in range(random.randint(3, 5))])
        self.entities.add(self.player, self.shield, self.charge_bar, self.health)

    def update(self):
        self.window.fill(common.bg_color)
        self.display.fill(common.bg_color)

        self.entities.update(player_pos=self.player.pos, charge=self.shield.charge)
        self.wave.update(player=self.player, health=self.health, shield=self.shield, swinging=self.shield.swing,)

        display_copy = pg.transform.scale(self.display, (self.display.width * common.SCALE, self.display.height * common.SCALE))

        self.entities.draw(display_copy)
        self.wave.draw_particles(display_copy)
        self.wave.draw(display_copy)

        self.window.blit(display_copy, common.TO_CENTRE)
