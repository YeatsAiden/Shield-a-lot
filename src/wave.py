import pygame as pg

import random

from .health import Health
from .player import Player
from .shield import Shield
from .entity import Entity
from .group import Group
from . import common, assets, settings, particle


class Projectile(Entity):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0) -> None:
        super().__init__(image, pos, spritesheet, angle)
        self.is_hit = False
        self.entered_arena = False
        self.dead = False

    def update(self):
        self.move()
        self.animate()
        self.entrance_check()

    def move(self):
        pass

    def animate(self):
        pass

    def entrance_check(self):
        # if 0 < self.pos[0] < settings.DISPLAY_SIZE[0] and 0 < self.pos[1] < settings.DISPLAY_SIZE[1]:
        if -50 < self.pos[0] < settings.DISPLAY_SIZE[0] + 50 and -50 < self.pos[1] < settings.DISPLAY_SIZE[1] + 50:
            self.entered_arena = True
        elif self.entered_arena:
            self.dead = True

    def hit(self):
        self.dead = True

    def reflect(self):
        if not self.is_hit:
            self.is_hit = True
            self.angle += 180



class Arrow(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0) -> None:
        super().__init__(image, pos, spritesheet, angle)
        self.speed = 40
        self.velocity = pg.Vector2(0, 0)

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center


class Boomerang(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0) -> None:
        super().__init__(image, pos, spritesheet, angle)
        self.speed = 30
        self.velocity = pg.Vector2(0, 0)

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center


class SmallBanana(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0) -> None:
        super().__init__(image, pos, spritesheet, angle)
        self.speed = 30
        self.velocity = pg.Vector2(0, 0)

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center


class LargeBanana(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0) -> None:
        super().__init__(image, pos, spritesheet, angle)
        self.speed = 30
        self.velocity = pg.Vector2(0, 0)

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center


class Spike(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0) -> None:
        super().__init__(image, pos, spritesheet, angle)
        self.speed = 30
        self.velocity = pg.Vector2(0, 0)

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center


class SawBlade(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0) -> None:
        super().__init__(image, pos, spritesheet, angle)
        self.speed = 60
        self.velocity = pg.Vector2(0, 0)
        self.explode = False

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center


class Rocket(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0) -> None:
        super().__init__(image, pos, spritesheet, angle)
        self.speed = 60
        self.velocity = pg.Vector2(0, 0)
        self.explode = False

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center

    def animate(self):
        self.image = self.spritesheet.next_frame()

    def hit(self):
        self.dead = True
        self.explode = True


class WaveManager(Group):
    def __init__(self) -> None:
        super().__init__()

        self.projectiles = {
                "arrow": Arrow,
                "spike": Spike,
                "sawblade": SawBlade,
                "rocket": Rocket,
                "boomerang": Boomerang,
                "large_banana": LargeBanana
                }

        # Wave specific information
        self.wave_id = 0
        self.current_wave = assets.data[f"wave_{self.wave_id}"]
        self.angle_deviation = self.current_wave["angle_deviation"]

        # Sub_wave specific info
        self.sub_wave_index = 0
        self.current_sub_wave = self.current_wave["sub_waves"][self.sub_wave_index]
        self.spawn_clock = self.current_sub_wave["spawn_clock"]
        self.projectile_types = self.current_sub_wave["types"]
        self.amount = self.current_sub_wave["amount"]

    def update(self, **kwargs):
        player: Player = kwargs["player"]
        health: Health = kwargs["health"]
        shield: Shield = kwargs["shield"]
        swinging = kwargs["swinging"]

        # Wave related shinanigans
        if self.tick():
            self.spawn_projectiles(player.pos)
            
            if self.sub_wave_index < len(self.current_wave["sub_waves"]) - 1:
                self.sub_wave_index += 1
                self.next_sub_wave()
            else:
                self.sub_wave_index = 0
                if f"wave_{self.wave_id + 1}" in assets.data:
                    self.wave_id += 1
                    self.next_wave()
                else:
                    # This needs to be removed in end product, will be replaced with an endless difficulty :\
                    self.wave_id = 0
                    self.next_wave()

        # entities update + particle update
        for projectile in self.entities:
            projectile.update()

            if projectile.mask.overlap(shield.mask, (shield.mask_rect.x - projectile.mask_rect.x, shield.mask_rect.y - projectile.mask_rect.y)) and swinging:
                projectile.reflect()
            if projectile.mask.overlap(player.mask, (player.mask_rect.x - projectile.mask_rect.x, player.mask_rect.y - projectile.mask_rect.y)):
                projectile.hit()
                health.decrease_health()

        for process in self.particles:
            process.update()

            if process.check_done():
                self.particles.remove(process)

    def tick(self):
        if not len(self.entities):
            self.spawn_clock -= common.DT
        if self.spawn_clock <= 0 and not len(self.entities):
            return True
        else:
            return False

    def decide_projectile(self, pos, angle):
        projectile_type = random.choice(self.projectile_types)
        spritesheet = assets.images[projectile_type + "_spritesheet"] if projectile_type + "_spritesheet" in assets.images else None
        return self.projectiles[projectile_type](assets.images[projectile_type], pos, spritesheet, angle)

    def spawn_projectiles(self, player_pos):
        for _ in range(self.amount):
            random_position = common.generate_random_position_out_of_area(settings.DISPLAY_SIZE, random.randint(20, 300))
            angle_to_player = common.angle_to(random_position, player_pos) + random.randint(-self.angle_deviation, self.angle_deviation)
            projectile = self.decide_projectile(random_position, angle_to_player)

            if isinstance(projectile, Rocket):
                trail = particle.Trail(assets.images["smoke_spritesheet"], projectile)
                flash = particle.Flash(assets.images["flash_spritesheet"], projectile)
                alt_flash = particle.Flash(assets.images["alt_flash_spritesheet"], projectile)
                shock_wave = particle.ShockWave(assets.images["shockwave_spritesheet"], projectile)
                self.particles.extend([trail, flash, alt_flash, shock_wave])

            self.add(projectile)

    def next_sub_wave(self):
        self.current_sub_wave = self.current_wave["sub_waves"][self.sub_wave_index]
        self.spawn_clock = self.current_sub_wave["spawn_clock"]
        self.projectile_types = self.current_sub_wave["types"]
        self.amount = self.current_sub_wave["amount"]

    def next_wave(self):
        self.current_wave = assets.data[f"wave_{self.wave_id}"]
        self.angle_deviation = self.current_wave["angle_deviation"]
        self.next_sub_wave()
