import pygame as pg
import os

EVENTS: list[pg.Event] = []
MOUSE_POSITION: list[int]
SCALE: float = 0
TO_CENTRE: pg.Vector2
FLAGS = pg.RESIZABLE
FPS: int = 360
DT: float = 0
WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__)).split("src")[0]

def clip_image(image: pg.Surface, x: int, y: int, width: int, height: int):
    image.set_clip((x, y, width, height))
    return image.subsurface(image.get_clip())

def rotate(surface: pg.Surface, angle: float, size: float, pivot, offset):
    scaled_image = pg.transform.scale(surface, (surface.width * size, surface.height * size))
    rotated_image = pg.transform.rotate(scaled_image, angle)
    rotated_offset = offset.rotate(-angle)
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect
