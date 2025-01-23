import pygame as pg

from . import entity, particle


class Group:
    def __init__(self) -> None:
        self.entities: list["entity.Entity"] = []
        self.particles: list["particle.ParticleProcess"] = []

    def update(self, *args, **kwargs):
        for entities in self.entities:
            entities.update(*args, **kwargs)

    def add(self, *args):
        for entity in args: 
            if isinstance(entity, Group):
                self.entities.extend(entity.entities)
            else:
                self.entities.append(entity)

    def remove(self, entity: "entity.Entity"):
        self.entities.remove(entity)

    def draw(self, surface: pg.Surface):
        for entity in self.entities:
            entity.draw(surface)

    def draw_particles(self, surface):
        for process in self.particles:
            process.draw(surface)
