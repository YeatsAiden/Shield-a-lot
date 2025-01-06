import pygame as pg

from . import assets


class Entity:
    def __init__(self, image: pg.Surface | assets.SpriteSheet, pos, angle: float = 0, flags: int = 0) -> None:
        if isinstance(image, assets.SpriteSheet):
            self.sprite_sheet = image
            self.image = image.images[f"{image.index}"]
            self.original_image = self.image
        else:
            self.image = image
            self.original_image = self.image

        self.mask: pg.Mask = pg.mask.from_surface(self.image)

        self.pos = pos
        self.rect: pg.FRect | pg.Rect = self.image.get_frect(center = self.pos)

        self.angle = angle
        self.flags = flags
        self.outline = False

        self.group: list["Group"] = []

    def update(self, *args, **kwargs):
        pass

    def add_outline(self, condition: bool, color):
        if condition and not self.outline:
            self.outline = True
            self.image = pg.Surface((self.original_image.width + 2, self.original_image.height + 2))
            self.image.set_colorkey((0, 0, 0))
            mask_surf = self.mask.to_surface(setcolor=color)
            mask_surf.set_colorkey((0, 0, 0))
            self.image.blit(mask_surf, (1, 0))
            self.image.blit(mask_surf, (1, 2))
            self.image.blit(mask_surf, (0, 1))
            self.image.blit(mask_surf, (2, 1))
            self.image.blit(self.original_image, (1, 1))
        elif not condition:
            self.outline = False
            self.image = self.original_image


class Group:
    def __init__(self) -> None:
        self.entities: list["Entity"] = []

    def update(self, *args, **kwargs):
        for entities in self.entities:
            entities.update(*args, **kwargs)

    def add(self, entity: "Entity | Group"):
        if isinstance(entity, Group):
            self.entities.extend(entity.entities)
            [e.group.append(self) for e in entity.entities]
        else:
            self.entities.append(entity)
            entity.group.append(self)

    def remove(self, entity: "Entity"):
        entity.group.remove(self)
        self.entities.remove(entity)
