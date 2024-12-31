import pygame as pg
import functools


class Entity:
    def __init__(self, image: pg.Surface, pos, angle: float = 0, rotates: bool = False, flags: int = 0) -> None:
        self.image = image
        self.original_image = image

        self.pos = pos
        self.rect: pg.FRect | pg.Rect = self.image.get_frect(center = self.pos)

        self.mask: pg.Mask = pg.mask.from_surface(self.image)

        self.angle = angle
        self.rotates = rotates

        self.flags = flags

        self.outline = False

        self.group: set["Group"] = set()

    def update(self, *args, **kwargs):
        pass

    def add_outline(self, condition: bool):
        if condition and not self.outline:
            self.outline = True
            self.image = pg.Surface((self.original_image.width, self.original_image.height))
        else:
            self.outline = False


class Group:
    def __init__(self) -> None:
        self.entities: set["Entity"] = set()

    def update(self, *args, **kwargs):
        for entities in self.entities:
            entities.update(*args, **kwargs)

    def add(self, entity: "Entity | Group"):
        if isinstance(entity, Group):
            self.entities.update(entity.entities)
            [e.group.add(self) for e in entity.entities]
        else:
            self.entities.add(entity)
            entity.group.add(self)

    def remove(self, entity: "Entity"):
        entity.group.remove(self)
        self.entities.remove(entity)
