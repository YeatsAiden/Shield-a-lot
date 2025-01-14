import pygame as pg

import random

from .entity import Entity, Group
from . import common, assets, settings, particle


class Projectile(Entity):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0, flags: int = 0) -> None:
        super().__init__(image, pos, spritesheet, angle, flags)
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
        if -50 < self.pos[0] < settings.DISPLAY_SIZE[0] + 50 and -50 < self.pos[1] < settings.DISPLAY_SIZE[1] + 50:
            self.entered_arena = True
        elif self.entered_arena:
            self.suicide()

    def hit(self):
        pass

    def suicide(self):
        # I dare you to tell me another way to do this
        for group in self.group:
            group.remove(self)

        self.dead = True


class Arrow(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0, flags: int = 0) -> None:
        super().__init__(image, pos, spritesheet, angle, flags)
        self.speed = 40
        self.velocity = pg.Vector2(0, 0)

        self.is_hit = False

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center

    def hit(self):
        if not self.is_hit:
            self.is_hit = True
            self.angle += 180


class Boomerang(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0, flags: int = 0) -> None:
        super().__init__(image, pos, spritesheet, angle, flags)
        self.speed = 30
        self.velocity = pg.Vector2(0, 0)

        self.is_hit = False

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center

    def hit(self):
        if not self.is_hit:
            self.is_hit = True
            self.angle += 180


class SmallBanana(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0, flags: int = 0) -> None:
        super().__init__(image, pos, spritesheet, angle, flags)
        self.speed = 30
        self.velocity = pg.Vector2(0, 0)

        self.is_hit = False

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center

    def hit(self):
        if not self.is_hit:
            self.is_hit = True
            self.angle += 180


class LargeBanana(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0, flags: int = 0) -> None:
        super().__init__(image, pos, spritesheet, angle, flags)
        self.speed = 30
        self.velocity = pg.Vector2(0, 0)

        self.is_hit = False

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center

    def hit(self):
        if not self.is_hit:
            self.is_hit = True
            self.angle += 180


class Spike(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0, flags: int = 0) -> None:
        super().__init__(image, pos, spritesheet, angle, flags)
        self.speed = 30
        self.velocity = pg.Vector2(0, 0)

        self.is_hit = False

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center

    def hit(self):
        if not self.is_hit:
            self.is_hit = True
            self.angle += 180

class SawBlade(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0, flags: int = 0) -> None:
        super().__init__(image, pos, spritesheet, angle, flags)
        self.speed = 60
        self.velocity = pg.Vector2(0, 0)

        self.is_hit = False

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center

    def hit(self):
        if not self.is_hit:
            self.is_hit = True
            self.angle += 180


class Rocket(Projectile):
    def __init__(self, image: pg.Surface, pos, spritesheet: assets.SpriteSheet | None = None, angle: float = 0, flags: int = 0) -> None:
        super().__init__(image, pos, spritesheet, angle, flags)
        self.speed = 60
        self.velocity = pg.Vector2(0, 0)

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center

    def animate(self):
        self.image = self.spritesheet.next_frame()

    def hit(self):
        if not self.is_hit:
            self.is_hit = True
            self.angle += 180


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

        self.particles: list[particle.ParticleProccess] = []

    def update(self, **kwargs):
        player_pos = kwargs["player_pos"]
        shield_rect = kwargs["shield_rect"]
        shield_mask = kwargs["shield_mask"]
        swinging = kwargs["swinging"]

        if self.tick():
            self.spawn_projectiles(player_pos)
            
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

        for projectile in self.entities:
            projectile.update()

            if projectile.mask.overlap(shield_mask, ((shield_rect.x - projectile.rect.left) * common.SCALE, (shield_rect.y - projectile.rect.top) * common.SCALE)) and swinging:
                projectile.hit()

        for process in self.particles:
            process.update()

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
                self.particles.append(particle.Fire(assets.images["fire_spritesheet"], projectile))

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

    def draw_particles(self, surface):
        for process in self.particles:
            process.draw(surface)

