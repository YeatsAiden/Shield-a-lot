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
        self.min_radius = 0.5

        self.relative_position = pg.Vector2(4, 0) 
        self.velocity = pg.Vector2(60, 0) 

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
        self.pos = pos
        self.angle = self.angle_to_mouse()
        temp_rotated_vel = self.velocity.rotate(-self.angle)
        self.relative_position += temp_rotated_vel * common.DT
        self.relative_position = self.relative_position.clamp_magnitude(self.min_radius, self.max_radius + math.sin(self.frame * 20) * 2000 * common.DT)
        self.pos = pos + self.relative_position

    def flip_image(self):
        if self.angle > 90 or self.angle < -90:
            self.flip_vertical = True
        else:
            self.flip_vertical = False
        
        self.image = pg.transform.flip(self.original_image, False, self.flip_vertical)

    def angle_to_mouse(self):
        return -math.degrees(math.atan2(common.MOUSE_POSITION[1] - self.pos[1], common.MOUSE_POSITION[0] - self.pos[0]))

    def slap(self):
        mouse_pressed = pg.mouse.get_pressed()

        if mouse_pressed[0] and self.charge == 0:
            self.swing = True

        ocillating_var = self.frame * 20

        if self.swing:
            self.frame += common.DT

        if ocillating_var > math.pi:
            self.swing = False
            self.frame = 0

    def charge_shield(self):
        mouse_pressed = pg.mouse.get_pressed()

        if mouse_pressed[0] and self.charge == 100:
            self.charge = 0
        else:
            self.charge += 200 * common.DT
            self.charge = 100 if self.charge > 100 else self.charge

