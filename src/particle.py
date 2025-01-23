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


class ParticleProcess:
    layer = 0
    def __init__(self, spritesheet: assets.SpriteSheet | None = None, entity: None | Entity = None) -> None:
        self.spritesheet = spritesheet
        self.entity = entity 

        self.particles: list[Particle] = []

        self.started = False
        self.done = False

    def update(self, *args, **kwargs):
        if len(self.particles):
            self.started = True

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

    def check_done(self):
        return not len(self.particles) and self.done and self.started

    def draw(self, surface: pg.Surface):
        for particle in self.particles:
            image, rect = common.rotate(self.spritesheet.get_image(particle.image_index), particle.angle, common.SCALE, (particle.pos[0] * common.SCALE, particle.pos[1] * common.SCALE), pg.Vector2(0, 0))
            surface.blit(image, rect)


class Trail(ParticleProcess):
    def __init__(self, spritesheet: assets.SpriteSheet | None = None, entity: None | Entity = None) -> None:
        super().__init__(spritesheet, entity)
        self.cooldown = 0.04

    def update(self, *args, **kwargs):
        if self.entity.dead:
            self.done = True

        self.cooldown -= common.DT
        if not self.done and self.cooldown <= 0:
            self.cooldown = 0.04
            for _ in range(random.randint(0, 2)):
                random_relative_pos = pg.Vector2(0, random.randint(-1, 1)).rotate(-self.entity.angle)
                pos = [self.entity.pos[0] + random_relative_pos.x, self.entity.pos[1] + random_relative_pos.y] 
                random_vec = pg.Vector2(random.randint(5, 10), 0).rotate(-self.entity.angle + random.randint(-15, 15) + 180)
                self.spawn(pos, random_vec, [random.random(), random.random()], 0)

        return super().update(*args, **kwargs)


class Flash(ParticleProcess):
    def __init__(self, spritesheet: assets.SpriteSheet | None = None, entity: None | Entity = None) -> None:
        super().__init__(spritesheet, entity)

    def update(self, *args, **kwargs):
        if self.entity.dead and not self.done and self.entity.explode:
            for _ in range(random.randint(5, 10)):
                random_relative_pos = pg.Vector2(random.gauss(0, 6), random.gauss(0, 6))
                pos = [self.entity.pos[0] + random_relative_pos.x, self.entity.pos[1] + random_relative_pos.y] 
                random_vec = pg.Vector2(random.randint(1, 5), 0).rotate(-common.angle_to(self.entity.pos, pos))
                self.spawn(pos, random_vec, [random.gauss(1/3, 1/2), random.gauss(1/2, 1/2), random.gauss(1/3, 1/2)], 0)
            self.done = True

        return super().update(*args, **kwargs)


class ShockWave(ParticleProcess):
    def __init__(self, spritesheet: assets.SpriteSheet | None = None, entity: None | Entity = None) -> None:
        super().__init__(spritesheet, entity)

    def update(self, *args, **kwargs):
        if self.entity.dead and not self.done and self.entity.explode:
            pos = self.entity.pos 
            random_vec = pg.Vector2(0, 0)
            self.spawn(pos, random_vec, [*[0.001 for _ in range(10)], 0.05, 0.05, 0.1], 0)
            self.done = True

        return super().update(*args, **kwargs)
