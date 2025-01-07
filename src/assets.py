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
        self.animation: list[pg.Surface] = []
        self.frame_index = 0
        self.durations = []

        json_file = f"{common.WORKING_DIRECTORY}assets/images/{path}/{path}.json"
        image = load_image(path)
        with open(json_file, "r") as file:
            data = json.load(file)
            for key, frame in data["frames"].items():
                x, y, w, h = frame["frame"].values()
                _image = common.clip_image(image, x, y, w, h)
                _duration = frame["duration"]
                self.images[f"{key}"] = _image
                self.durations.append(_duration)
                self.animation.extend([_image for _ in range(int(_duration/1000*common.FPS))])

    def next_image(self):
        self.index += 1
        if self.index == len(self.images):
            self.index = 0

        return self.images[f"{self.index}"]

    def next_frame(self):
        self.frame_index += 1
        if self.frame_index == len(self.animation):
            self.frame_index = 0

        return self.animation[self.frame_index]

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
            "heart": load_image("heart"),
            "shield": load_image("shield"),
            "spike": load_image("spike"),
            "large_banana": load_image("large_banana"),
            "small_banana": load_image("small_banana"),
            "boomerang": load_image("boomerang"),
            "button": SpriteSheet("button"),
            "smoke": SpriteSheet("smoke"),
            "spark": SpriteSheet("spark"),
            "fire": SpriteSheet("fire"),
            "rocket": SpriteSheet("rocket"),
            "sawblade": SpriteSheet("sawblade"),
            "grass": SpriteSheet("grass"),
        }
    )
    data.update(
        {
            "wave_0": load_json("wave_0"),
        }
    )
