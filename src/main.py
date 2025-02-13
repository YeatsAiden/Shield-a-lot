import pygame as pg

import sys

from .states import MainMenu
from . import settings, common, assets, ui


class StateManager:
    def __init__(self) -> None:
        self.window = pg.display.set_mode(settings.WINDOW_SIZE, common.FLAGS) 
        self.display = pg.Surface(settings.DISPLAY_SIZE)
        self.clock = pg.Clock()

        assets.load_assets()

        self.state = MainMenu(self.window, self.display)

        self.fps = ui.Font(assets.images["smol_font"], [1, 2, 3], 1)

    def update(self):
        self.state.update() 

    def swap_state(self):
        if self.state.next_state:
            self.state.exit_state()
            self.state = self.state.next_state(self.window, self.display, self.state)
            self.state.enter_state()
    
    def run(self):
        while True:
            # Global vars
            common.EVENTS = pg.event.get()
            common.SCALE = min(self.window.height / self.display.height, self.window.width / self.display.height)
            common.TO_CENTRE = pg.Vector2((self.window.width - self.display.width * common.SCALE) / 2, (self.window.height - self.display.height * common.SCALE) / 2)
            x, y = pg.mouse.get_pos()
            common.MOUSE_POSITION = [(x - common.TO_CENTRE.x) / common.SCALE, (y - common.TO_CENTRE.y) / common.SCALE]

            # Actual state stuff
            self.update()
            self.swap_state()
            self.event_loop()
            self.fps.render(self.window, f"{self.clock.get_fps()}", 60, 10, 1, 1)
            pg.display.update((common.TO_CENTRE.x, common.TO_CENTRE.y, self.display.width * common.SCALE, self.display.height * common.SCALE))
            common.DT = self.clock.tick(common.FPS)/1000

    def event_loop(self):
        for event in common.EVENTS:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
