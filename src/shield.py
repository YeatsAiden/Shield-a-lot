import pygame as pg

import math
from . import common
from .entity import Entity


class Shield(Entity):
    def __init__(self, image: pg.Surface, pos) -> None:
        super().__init__(image, pos)
        self.image = image
        self.rect = self.image.get_frect(center=pos)

        self.pos = self.rect.center

        self.angle = 0
        self.max_radius = 2.5
        self.min_radius = 0

        self.relative_position = pg.Vector2(4, 0) 
        self.velocity = pg.Vector2(70, 0) 

        self.flip_vertical = False

        self.swing = False
        self.frame = 0

        self.charge = 0

    def update(self, *args, **kwargs):
        self.follow(kwargs["player_pos"])
        self.flip_image()
        self.slap()
        self.charge_shield()

    def follow(self, pos):
        self.angle = common.angle_to(pos, common.MOUSE_POSITION)
        temp_rotated_vel = self.velocity.rotate(-self.angle)
        self.relative_position += temp_rotated_vel * common.DT
        self.relative_position = self.relative_position.clamp_magnitude(self.min_radius, self.max_radius + math.sin(self.frame) * 200)
        self.rect.center = pos + self.relative_position
        self.pos = self.rect.center

    def flip_image(self):
        if self.angle > 90 or self.angle < -90:
            self.flip_vertical = True
        else:
            self.flip_vertical = False
        
        self.image = pg.transform.flip(self.original_image, False, self.flip_vertical)

    def slap(self):
        mouse_pressed = pg.mouse.get_pressed()

        if mouse_pressed[0] and self.charge == 0:
            self.swing = True

        if self.swing:
            self.frame += common.DT * 20

        if self.frame > math.pi:
            self.swing = False
            self.frame = 0

    def charge_shield(self):
        mouse_pressed = pg.mouse.get_pressed()

        if mouse_pressed[0] and self.charge == 100:
            self.charge = 0
        else:
            self.charge += 200 * common.DT
            self.charge = 100 if self.charge > 100 else self.charge

