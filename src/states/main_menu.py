import pygame as pg
from .state import State
from .game import Game
from .. import assets
from ..ui import Button 
from ..entity import Group
from ..display import Display, common


class MainMenu(State):
    def __init__(self, window: pg.Surface, display: Display, previous_state = None) -> None:
        super().__init__(window, display, previous_state)
        self.window = window
        self.display = display

        self.play = Button(
                assets.images["button"][0],
                assets.images["button"][1],
                assets.images["button"][2],
                (21, 21),
                lambda: setattr(self, "next_state", Game)
            )
        self.quit = Button(
                assets.images["button"][0],
                assets.images["button"][1],
                assets.images["button"][2],
                (21, 42),
                lambda: setattr(self, "done", True)
            )

        self.buttons = Group() 
        self.buttons.add(self.play)
        self.buttons.add(self.quit)

        # Entities
        self.all_entities = Group()
        self.all_entities.add(self.buttons)

        # Colors
        self.bg_color = pg.Color(16, 20, 31)

    def exit_state(self):
        pass

    def enter_state(self):
        pass

    def update(self):
        self.window.fill("black")
        self.display.display.fill(self.bg_color)
        self.buttons.update()
        self.display.add(self.all_entities)
        self.display.update()
