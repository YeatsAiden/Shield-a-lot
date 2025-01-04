import pygame as pg
from .entity import Entity, Group
from . import common

class Display:
    def __init__(self, size: list[int], window: pg.Surface) -> None:
        self.display: pg.Surface = pg.Surface(size)
        self.window = window

        self.entities: list["Entity"] = [] 
    
    def update(self):
        display_copy = pg.transform.scale(self.display, (self.display.width * common.SCALE, self.display.height * common.SCALE))
        self.render(display_copy, self.entities)
        self.window.blit(display_copy, (common.TO_CENTRE.x, common.TO_CENTRE.y))
        self.entities = []

    def add(self, entity: "Entity | Group"):
        if isinstance(entity, Group):
            self.entities.extend(entity.entities)
        else:
            self.entities.append(entity)

    def render(self, surface: pg.Surface, entities: list["Entity"]):
        for entity in entities:
            image, rect = common.rotate(entity.image, entity.angle, common.SCALE, (entity.pos[0] * common.SCALE, entity.pos[1] * common.SCALE), pg.Vector2(0, 0))
            entity.mask = pg.mask.from_surface(image)
            surface.blit(image, rect)

