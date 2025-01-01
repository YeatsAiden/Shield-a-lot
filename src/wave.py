import pygame as pg
import random, math
from .entity import Entity, Group
from . import common, assets, settings


class Rocket(Entity):
    def __init__(self, image: pg.Surface, pos, angle: int = 0, flags: int = 0) -> None:
        super().__init__(image, pos, angle)
        self.speed = 70 
        self.velocity = pg.Vector2(0, 0)

    def update(self, *args, **kwargs):
        self.move()

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.pos += rotated_velocity


class WaveManager(Group):
    def __init__(self, time_per_wave: int) -> None:
        super().__init__()
        self.time_per_wave = time_per_wave
        self.difficulty = 0
        self.projectiles = [Rocket]
        self.projectile_images = ["rocket"]
        self.spawn_clock = random.random() + random.random()

    def update(self, *args, **kwargs):
        player_pos = kwargs["player_pos"]
        angle_to_player = -math.degrees(math.atan2(player_pos[1], player_pos[0]))

        if self.tick():
            for i in range(random.randint(1, 3)):
                random_projectile = random.randint(0, self.difficulty)
                random_position = common.generate_random_position_out_of_area(settings.DISPLAY_SIZE, 20)
                self.add(self.projectiles[random_projectile](assets.images[self.projectile_images[random_projectile]], random_position))

        for projectile in self.entities:
            projectile.update()

    def tick(self):
        self.spawn_clock -= common.DT
        if self.spawn_clock <= 0:
            self.spawn_clock = random.random() + random.random()
            return True
        else:
            return False
            
