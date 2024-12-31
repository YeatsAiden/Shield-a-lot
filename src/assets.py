from os.path import isfile
import pygame as pg
import os, json

from pygame.cursors import arrow
from . import common

images = {}

def load_image(path: str, extention: str = "png"):
    return pg.image.load(f"{common.WORKING_DIRECTORY}assets/images/{path}/{path}.{extention}")

def load_sound(path: str, extention: str = "wav"):
    return pg.image.load(f"{common.WORKING_DIRECTORY}assets/sfx/{path}.{extention}")

def load_sprite_sheet(path: str, extention: str = "json"):
    json_file = f"{common.WORKING_DIRECTORY}assets/images/{path}/{path}.{extention}"
    image = load_image(path)
    if os.path.isfile(json_file):
        _images: list[pg.Surface] = []
        with open(json_file, "r") as file:
            data = json.load(file)
            for _, frame in data["frames"].items():
                x, y, w, h = frame["frame"].values()
                _images.append(common.clip_image(image, x, y, w, h))
        return _images
    else:
        return image

def load_assets():
    images.update(
        {
            "arrow": load_image("arrow"),
            "bar": load_image("bar"),
            "charge": load_image("charge"),
            "grass": load_sprite_sheet("grass"),
            "button": load_sprite_sheet("button"),
            "player": load_image("player"),
            "rocket": load_sprite_sheet("rocket"),
            "shield": load_image("shield"),
        }
    )
