import pygame as pg

from . import assets, common
from .entity import Entity

class Health(Entity):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0, flags: int = 0) -> None:
        super().__init__(image, pos, spritesheet, angle, flags)
        self.lives = 3
        self.dead = False
        self.cooldown = 1
        self.image = pg.Surface((self.original_image.width * self.lives + 3, self.original_image.height))
        self.image.set_colorkey("black")
        for life in range(self.lives):
            self.image.blit(self.original_image, (life * self.original_image.width + life, 0))

    def update(self, *args, **kwargs):
        self.cooldown -= common.DT

    def decrease_health(self):
        if self.cooldown <= 0:
            self.lives -= 1
            self.cooldown = 1
        if self.lives >= 0:
            self.update_image()
        else:
            self.dead = True

    def update_image(self):
        self.image = pg.Surface((self.original_image.width * self.lives + 3, self.original_image.height))
        self.image.set_colorkey("black")
        for life in range(self.lives):
            self.image.blit(self.original_image, (life * self.original_image.width + life, 0))
