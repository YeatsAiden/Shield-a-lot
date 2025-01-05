import pygame as pg
import random
from .entity import Entity, Group
from . import common, assets, settings


class Projectile(Entity):
    def __init__(self, image: pg.Surface, pos, angle: float = 0, flags: int = 0) -> None:
        super().__init__(image, pos, angle, flags)
        self.is_hit = False
        self.entered_arena = False
        self.speed: int
        self.velocity: pg.Vector2

    def hit(self):
        pass


class Arrow(Projectile):
    def __init__(self, image: pg.Surface, pos, angle: float = 0) -> None:
        super().__init__(image, pos, angle)
        self.speed = 30
        self.velocity = pg.Vector2(0, 0)

        self.is_hit = False

    def update(self, *args, **kwargs):
        self.move()

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
    def __init__(self, image: pg.Surface, pos, angle: float = 0) -> None:
        super().__init__(image, pos, angle)
        self.speed = 30
        self.velocity = pg.Vector2(0, 0)

        self.is_hit = False

    def update(self, *args, **kwargs):
        self.move()

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
    def __init__(self, image: pg.Surface, pos, angle: float = 0) -> None:
        super().__init__(image, pos, angle)
        self.speed = 30
        self.velocity = pg.Vector2(0, 0)

        self.is_hit = False

    def update(self, *args, **kwargs):
        self.move()

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
    def __init__(self, image: pg.Surface, pos, angle: float = 0) -> None:
        super().__init__(image, pos, angle)
        self.speed = 30
        self.velocity = pg.Vector2(0, 0)

        self.is_hit = False

    def update(self, *args, **kwargs):
        self.move()

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
    def __init__(self, image: pg.Surface, pos, angle: float = 0) -> None:
        super().__init__(image, pos, angle)
        self.speed = 60
        self.velocity = pg.Vector2(0, 0)

        self.is_hit = False

    def update(self, *args, **kwargs):
        self.move()

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
    def __init__(self, image: pg.Surface, pos, angle: float = 0) -> None:
        super().__init__(image, pos, angle)
        self.speed = 60
        self.velocity = pg.Vector2(0, 0)

        self.is_hit = False

    def update(self, *args, **kwargs):
        self.move()
        self.animate()

    def move(self):
        self.velocity.x, self.velocity.y = 0, 0 
        self.velocity.x += self.speed * common.DT
        rotated_velocity =  self.velocity.rotate(-self.angle)
        self.rect.topleft += rotated_velocity
        self.pos = self.rect.center

    def animate(self):
        self.image = self.sprite_sheet.next_frame()

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
                "rocket": Rocket
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


    def update(self, *args, **kwargs):
        player_pos = kwargs["player_pos"]
        shield_rect = kwargs["shield_rect"]
        shield_mask = kwargs["shield_mask"]
        swinging = kwargs["swinging"]

        if self.tick():
            self.spawn_projectiles(player_pos)

        for projectile in self.entities:
            projectile.update()
            if projectile.mask.overlap(shield_mask, ((shield_rect.x - projectile.rect.left) * common.SCALE, (shield_rect.y - projectile.rect.top) * common.SCALE)) and swinging:
                projectile.hit()

    def tick(self):
        if not len(self.entities):
            self.spawn_clock -= common.DT
        if self.spawn_clock <= 0 and not len(self.entities):
            return True
        else:
            return False

    def decide_projectile(self, pos, angle):
        projectile_type = random.choice(self.projectile_types)
        return self.projectiles[projectile_type](assets.images[projectile_type], pos, angle)

    def spawn_projectiles(self, player_pos):
        for _ in range(self.amount):
            random_position = common.generate_random_position_out_of_area(settings.DISPLAY_SIZE, random.randint(20, 300))
            angle_to_player = common.angle_to(random_position, player_pos) + random.randint(-self.angle_deviation, self.angle_deviation)
            projectile = self.decide_projectile(random_position, angle_to_player)
            self.add(projectile)

