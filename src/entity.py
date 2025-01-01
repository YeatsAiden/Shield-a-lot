import pygame as pg


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
        if condition:
            self.outline = True
            self.image = pg.Surface((self.original_image.width + 2, self.original_image.height + 2))
            self.image.set_colorkey((0, 0, 0))
            mask_surf = self.mask.to_surface(setcolor= (255, 255, 255))
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
