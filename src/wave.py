import pygame as pg
import random
from .entity import Entity, Group
from . import common


class Arrow(Entity):
    def __init__(self, image: pg.Surface, pos, angle: int = 0, flags: int = 0) -> None:
        super().__init__(image, pos, angle)
        self.speed = 50
        self.velocity = pg.Vector2(0, 0)

    def update(self):
        self.move()

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(self.angle)
        self.pos[0] += rotated_velocity.x
        self.pos[1] -= rotated_velocity.y


class Rocket(Entity):
    def __init__(self, image: pg.Surface, pos, angle: int = 0, flags: int = 0) -> None:
        super().__init__(image, pos, angle)
        self.speed = 70 
        self.velocity = pg.Vector2(0, 0)

    def update(self, *args, **kwargs):
        self.move()

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(self.angle)
        self.pos[0] += rotated_velocity.x
        self.pos[1] -= rotated_velocity.y


class Boomerang(Entity):
    def __init__(self, image: pg.Surface, pos, angle: int = 0, flags: int = 0) -> None:
        super().__init__(image, pos, angle)
        self.speed = 50
        self.velocity = pg.Vector2(0, 0)

    def update(self):
        self.move()

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(self.angle)
        self.pos[0] += rotated_velocity.x
        self.pos[1] -= rotated_velocity.y


class Spawner:
    def __init__(self) -> None:
        pass


class Wave(Group):
    def __init__(self, time_per_wave: int, difficulty: int) -> None:
        super().__init__()
        self.time_per_wave = time_per_wave
        self.difficulty = difficulty
        self.spawn_clock: int = random.randint(0, difficulty)
