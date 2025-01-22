import pygame as pg

from .. import assets, common
from .state import State
from .game import Game
from ..entity import Group
from ..ui import Button 


class MainMenu(State):
    def __init__(self, window: pg.Surface, display: pg.Surface, previous_state = None) -> None:
        super().__init__(window, display, previous_state)
        self.window = window
        self.display = display

        self.play = Button(
                assets.images["button"],
                (21, 21),
                lambda: setattr(self, "next_state", Game),
                assets.images["button_spritesheet"]
            )
        self.quit = Button(
                assets.images["button"],
                (21, 42),
                lambda: setattr(self, "done", True),
                assets.images["button_spritesheet"]
            )

        self.buttons = Group() 
        self.buttons.add(self.play, self.quit)

    def exit_state(self):
        pass

    def enter_state(self):
        pass

    def update(self):
        self.window.fill(common.bg_color)
        self.display.fill(common.bg_color)

        self.buttons.update()

        display_copy = pg.transform.scale(self.display, (self.display.width * common.SCALE, self.display.height * common.SCALE))
        self.buttons.draw(display_copy)
        self.window.blit(display_copy, common.TO_CENTRE)
