import pygame as pg
import math

from .entity import Entity
from . import common, settings

class Player(Entity):
    def __init__(self, image: pg.Surface, pos) -> None:
        super().__init__(image, pos)
        self.image = image
        self.rect = self.image.get_frect(center=pos)

        self.direction = pg.Vector2(0, 0)
        self.velocity = pg.Vector2(0, 0) 
        self.speed = 20

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
        self.pos += self.velocity

    def restrict_pos(self):
        if self.pos[0] > settings.DISPLAY_SIZE[0]:
            self.pos[0] = settings.DISPLAY_SIZE[0]
        elif self.pos[0] < 0:
            self.pos[0] = 0

        if self.pos[1] > settings.DISPLAY_SIZE[1]:
            self.pos[1] = settings.DISPLAY_SIZE[1]
        elif self.pos[1] < 0:
            self.pos[1] = 0

    def oscillate(self):
        if self.velocity.x or self.velocity.y:
            self.wobble = True

        ocillating_angle = self.frame * 20

        if self.wobble:
            self.angle += math.sin(ocillating_angle) * 300 * common.DT
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

