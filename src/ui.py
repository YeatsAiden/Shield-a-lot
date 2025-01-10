import pygame as pg

import typing

from .entity import Entity
from . import common, assets


class Button(Entity):
    command: typing.Callable = staticmethod(lambda: None)

    def __init__(self, image: pg.Surface, pos, command: typing.Callable, spritesheet: assets.SpriteSheet | None = None, angle: float = 0, flags: int = 0) -> None:
        super().__init__(image, pos, spritesheet, angle, flags)
        self.rect = self.image.get_frect(center=pos)

        self.command: typing.Callable = command

        self.focused: bool = False
        self.clicked: bool = False
        
    def update(self):
        self.focused = True if self.rect.collidepoint(common.MOUSE_POSITION) else False

        for event in common.EVENTS:
            if event.type == pg.MOUSEBUTTONDOWN and self.focused and event.button == 1:
                self.clicked = True
            if event.type == pg.MOUSEBUTTONUP and self.focused and self.clicked:
                self.clicked = False
                self.command()
        
        if self.focused:
            self.image = self.spritesheet.get_image(1)
        else:
            self.image = self.spritesheet.get_image(0)
        if self.clicked:
            self.image = self.spritesheet.get_image(2)


class Font:
    def __init__(self, path: str, include: list[int], step: int) -> None:
        self.characters = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", "0123456789", "!@#$%^&*()`~-_=+\\|[]}{';:/?.>,<"]

        self.font = self.load_font(path, include, step)
    
    def load_font(self, path: str, include: list[int], step: int):
        font_img = pg.image.load(path).convert()
        font_img.set_colorkey((0, 0, 0))
        
        characters = []
        font = {}

        x_pos = 0

        for x in range(font_img.get_width()):
            for y in range(font_img.get_height()):
                color = font_img.get_at((x, y))

                if color == (255, 0, 0, 255):
                    character = common.clip_image(font_img, x_pos, 0, x - x_pos, font_img.get_height())
                    x_pos = x + 1

                    if y == 1:
                        cp_surface = character.copy()
                        character = pg.Surface((cp_surface.get_width(), cp_surface.get_height() + step))
                        character.blit(cp_surface, (0, step))
                    characters.append(character)
        
        for i in include:
            for character in self.characters[i]:
                font[character] = characters[len(font)]
        
        return font
    
    def render(self, surface: pg.Surface, text: str, x: int, y: int, space: int, size: int):
        x_pos = 0
        for letter in text:
            if letter == " ":
                x_pos += space * size
            else:
                character_img = pg.transform.scale_by(self.font[letter], size)
                surface.blit(character_img, (x + x_pos, y))
                x_pos += character_img.get_width() + size
