import pygame as pg

from dataclasses import dataclass
from . import common, assets

# I swear this isn't stolen ;]

@dataclass
class Particle:
    pos: pg.Vector2
    velocity: pg.Vector2
    angle: int
    time: float

class ParticleManager:
    def __init__(self, spritesheet: assets.SpriteSheet) -> None:
        self.spritesheet = spritesheet
        self.particles: list[Particle] = []

    def update(self, *args, **kwargs):
        for particle in self.particles:
            particle.pos += particle.velocity * common.DT
            particle.time -= common.DT
        self.particles = [particle for particle in self.particles if particle.time >= 0]

    def spawn(self, pos, velocity: pg.Vector2, time: int, angle: int = 0, amount: int = 1):
        for _ in range(amount):
            self.particles.append(Particle(pos = pos, velocity = velocity, angle = angle, time = time))
