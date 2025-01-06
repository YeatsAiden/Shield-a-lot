import pygame as pg

from . import common
from .entity import Entity


class Bar(Entity):
    def __init__(self, image: pg.Surface, charge_image: pg.Surface, pos) -> None:
        super().__init__(image, pos)
        self.charge_image = charge_image

    def update(self, *args, **kwargs):
        self.update_charge(kwargs["charge"])

    def update_charge(self, charge: float):
        x, y, w, h = 0, 0, round(charge/10), self.charge_image.height
        _charge_image = common.clip_image(self.charge_image, x, y, w, h)
        self.image = self.original_image.copy()
        self.image.blit(_charge_image, (2, 1))
