import pygame as pg

import math

from .entity import Entity
from . import common, settings, assets


class Health(Entity):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0, flags: int = 0) -> None:
        super().__init__(image, pos, spritesheet, angle, flags)
        self.lives = 3
        self.image = pg.Surface((self.original_image.width * self.lives + 3, self.original_image.height))
        self.image.set_colorkey("black")
        for life in range(self.lives):
            self.image.blit(self.original_image, (life * self.original_image.width + life, 0))

    def lose_health(self):
        self.lives -= 1
        if self.lives >= 0:
            self.update_image()

    def update_image(self):
        self.image = pg.Surface((self.original_image.width * self.lives + 3, self.original_image.height))
        for life in range(self.lives):
            self.image.blit(self.original_image, (life * self.original_image.width + life, 0))


class Player(Entity):
    def __init__(self, image: pg.Surface, pos, health: Health) -> None:
        super().__init__(image, pos)
        self.image = image
        self.rect = self.image.get_frect(center=pos)

        self.health = health

        self.direction = pg.Vector2(0, 0)
        self.velocity = pg.Vector2(0, 0) 
        self.speed = 10

        self.frame = 0
        self.wobble = False

        self.flip = False

    def update(self, *args, **kwargs):
       self.recieve_input()
       self.move() 
       self.flip_image()
       self.oscillate()
       self.restrict_pos()

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0
        self.velocity += self.speed * self.direction * common.DT
        self.rect.topleft += self.velocity
        self.pos = self.rect.center

    def restrict_pos(self):
        if self.rect.right > settings.DISPLAY_SIZE[0]:
            self.rect.right = settings.DISPLAY_SIZE[0]
        elif self.rect.x < 0:
            self.rect.x = 0

        if self.rect.bottom > settings.DISPLAY_SIZE[1]:
            self.rect.bottom = settings.DISPLAY_SIZE[1]
        elif self.rect.y < 0:
            self.rect.y = 0

    def oscillate(self):
        if self.velocity.x or self.velocity.y:
            self.wobble = True

        ocillating_angle = self.frame * 20

        if self.wobble:
            self.angle += math.sin(ocillating_angle) * 200 * common.DT
            self.frame += common.DT

        if ocillating_angle > 2 * math.pi:
            self.angle = 0
            self.frame = 0
            self.wobble = False
    
    def flip_image(self):
        if self.direction.x < 0:
            self.flip = True
        elif self.direction.x > 0:
            self.flip = False
        
        self.image = pg.transform.flip(self.original_image, self.flip, False)

    def recieve_input(self):
        keys = pg.key.get_pressed()
        self.direction.x = (keys[pg.K_d] or keys[pg.K_RIGHT]) - (keys[pg.K_a] or keys[pg.K_LEFT])
        self.direction.y = (keys[pg.K_s] or keys[pg.K_DOWN]) - (keys[pg.K_w] or keys[pg.K_UP])
