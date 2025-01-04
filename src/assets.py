import pygame as pg
import json
from . import common

images = {}
data = {}

def load_image(path: str, extention: str = "png"):
    return pg.image.load(f"{common.WORKING_DIRECTORY}assets/images/{path}/{path}.{extention}")

def load_sound(path: str, extention: str = "wav"):
    return pg.image.load(f"{common.WORKING_DIRECTORY}assets/sfx/{path}.{extention}")

def load_json(path: str, extention: str = "json"):
    with open(f"{common.WORKING_DIRECTORY}assets/json/{path}.{extention}", "r") as file:
        data = json.load(file)
        return data


class SpriteSheet:
    def __init__(self, path: str) -> None:
        self.images: dict[str, pg.Surface] = {}
        self.index = 0

        json_file = f"{common.WORKING_DIRECTORY}assets/images/{path}/{path}.json"
        image = load_image(path)

        with open(json_file, "r") as file:
            data = json.load(file)
            for key, frame in data["frames"].items():
                x, y, w, h = frame["frame"].values()
                self.images[f"{key}"] = common.clip_image(image, x, y, w, h)

    def next_image(self):
        self.index += 1
        if self.index == len(self.images):
            self.index = 0

        return self.images[f"{self.index}"]

    def get_image(self, index: int):
        if index >= len(self.images) or index < -len(self.images):
            self.index = 0
        else:
            self.index = index
        return self.images[f"{self.index}"]


def load_assets():
    images.update(
        {
            "arrow": load_image("arrow"),
            "bar": load_image("bar"),
            "charge": load_image("charge"),
            "player": load_image("player"),
            "shield": load_image("shield"),
            "button": SpriteSheet("button"),
            "rocket": SpriteSheet("rocket"),
            "grass": SpriteSheet("grass"),
        }
    )
    data.update(
        {
            "wave_0": load_json("wave_0"),
        }
    )
