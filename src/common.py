import pygame as pg

import os, random, math

EVENTS: list[pg.Event] = []
MOUSE_POSITION: list[int]
SCALE: float = 0
TO_CENTRE: pg.Vector2
FLAGS = pg.RESIZABLE
FPS: int = 360
DT: float = 0
WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__)).split("src")[0]

bg_color = pg.Color(16, 20, 31)
alt_bg_color = pg.Color(37, 86, 46)

def clip_image(image: pg.Surface, x: int, y: int, width: int, height: int):
    image.set_clip((x, y, width, height))
    return image.subsurface(image.get_clip())

def rotate(surface: pg.Surface, angle: float, size: float, pivot, offset):
    scaled_image = pg.transform.scale(surface, (surface.width * size, surface.height * size))
    rotated_image = pg.transform.rotate(scaled_image, angle)
    rotated_offset = offset.rotate(-angle)
    rect = rotated_image.get_frect(center=pivot+rotated_offset)
    return rotated_image, rect

def generate_random_position_out_of_area(area: list[int], offset: int):
    random_position = [random.randint(0, area[0]), random.randint(0, area[1])]

    to_right = random_position[0] > area[0]/2
    to_bottom = random_position[1] > area[1]/2

    min_dist_x = area[0] - random_position[0] if to_right else random_position[0]
    min_dist_y = area[1] - random_position[1] if to_bottom else random_position[1]

    if min_dist_x > min_dist_y:
        random_position[1] = -offset if to_bottom else area[1] + offset
    else:
        random_position[0] = -offset if to_right else area[0] + offset
    
    return random_position

def angle_to(pos_1, pos_2):
    return -math.degrees(math.atan2(pos_2[1] - pos_1[1], pos_2[0] - pos_1[0]))

def out_back(time):
    return 1 + 2.70158 * (time - 1) ** 3 + 1.70158 * (time - 1) ** 2
