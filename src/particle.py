import pygame as pg

from dataclasses import dataclass
import random

from .entity import Entity
from . import common, assets

# I swear this isn't stolen ;]

@dataclass
class Particle:
    pos: pg.Vector2
    velocity: pg.Vector2
    angle: float
    durations: list[float]
    image_index: int = 0


class ParticleProccess:
    def __init__(self, spritesheet: assets.SpriteSheet, entity: None | Entity = None) -> None:
        self.spritesheet = spritesheet

        if entity:
            self.entity = entity 

        self.particles: list[Particle] = []
        self.done = False

    def update(self, *args, **kwargs):
        for particle in self.particles:
            particle.pos += particle.velocity * common.DT

            if particle.durations[particle.image_index] >= 0:
                particle.durations[particle.image_index] -= common.DT
            else:
                particle.image_index += 1

        self.particles = [particle for particle in self.particles if particle.image_index < len(particle.durations)]

    def spawn(self, pos, velocity: pg.Vector2, durations: list[float], angle: float = 0, amount: int = 1):
        for _ in range(amount):
            self.particles.append(Particle(pos = pos, velocity = velocity, angle = angle, durations= durations))

    def draw(self, surface: pg.Surface):
        for particle in self.particles:
            image, rect = common.rotate(self.spritesheet.get_image(particle.image_index), particle.angle, common.SCALE, (particle.pos[0] * common.SCALE, particle.pos[1] * common.SCALE), pg.Vector2(0, 0))
            surface.blit(image, rect)


class Fire(ParticleProccess):
    def __init__(self, spritesheet: assets.SpriteSheet, entity: None | Entity = None) -> None:
        super().__init__(spritesheet, entity)

    def update(self, *args, **kwargs):
        if self.entity.dead:
            self.done = True

        if not self.done:
            random_vec = pg.Vector2(0, random.randint(-2, 2)).rotate(-self.entity.angle)
            random_pos = [self.entity.pos[0] + random_vec.x, self.entity.pos[1] + random_vec.y] 
            self.spawn(random_pos, pg.Vector2(1, 0), [random.randint(0, 1), random.randint(0, 1), random.randint(1, 2)], self.entity.angle, random.randint(0, 1))

        return super().update(*args, **kwargs)

