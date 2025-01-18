import pygame as pg

from . import assets, common


class Entity:
    layer = 0
    def __init__(self, image: pg.Surface,  pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0, flags: int = 0) -> None:
        self.image = image
        self.original_image = image

        if spritesheet:
            self.spritesheet = spritesheet

        self.pos = pos
        self.rect: pg.FRect | pg.Rect = self.image.get_frect(center = self.pos)

        self.mask: pg.Mask = pg.mask.from_surface(self.image)
        self.mask_rect = self.rect

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

    def add(self, *args):
        for entity in args: 
            if isinstance(entity, Group):
                self.entities.extend(entity.entities)
                [e.group.append(self) for e in entity.entities]
            else:
                self.entities.append(entity)
                entity.group.append(self)

    def remove(self, entity: "Entity"):
        entity.group.remove(self)
        self.entities.remove(entity)

    def draw(self, surface: pg.Surface):
        for entity in self.entities:
            image, rect = common.rotate(entity.image, entity.angle, common.SCALE, (entity.pos[0] * common.SCALE, entity.pos[1] * common.SCALE), pg.Vector2(0, 0))
            entity.mask = pg.mask.from_surface(image)
            entity.mask_rect = rect
            surface.blit(image, rect)
