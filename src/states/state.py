import pygame as pg
import sys
from ..display import Display


class State:
    def __init__(self, window: pg.Surface, display: Display, previous_state = None, show_cursor: bool = False) -> None:
        self.previous_state = previous_state
        self.window = window
        self.display = display

        self.cursor_visible = show_cursor
        self.next_state = None

        self.done = False

    def exit_state(self, *args, **kwargs):
        self.next_state = None

    def enter_state(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass
