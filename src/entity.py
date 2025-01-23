import pygame as pg

from . import assets, common


class Entity:
    layer = 0
    def __init__(self, image: pg.Surface,  pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0) -> None:
        self.image = image
        self.original_image = image

        self.pos = pos
        self.rect = self.image.get_frect(center=self.pos)

        if spritesheet:
            self.spritesheet = spritesheet
            self.rect = self.spritesheet.get_image(0).get_frect(center=self.pos)

        self.mask: pg.Mask = pg.mask.from_surface(self.image)
        self.mask_rect = self.rect

        self.angle = angle
        self.outline = False

    def update(self, *args, **kwargs):
        pass

    def draw(self, surface: pg.Surface):
        image, rect = common.rotate(self.image, self.angle, common.SCALE, (self.pos[0] * common.SCALE, self.pos[1] * common.SCALE), pg.Vector2(0, 0))
        self.mask = pg.mask.from_surface(image)
        self.mask_rect = rect
        surface.blit(image, rect)

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
