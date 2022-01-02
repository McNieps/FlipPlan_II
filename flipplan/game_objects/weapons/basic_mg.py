from math import degrees, radians, cos, sin, atan2
from random import gauss

from flipplan.game_objects.projectiles.ray_bullet import RayBullet


class BasicMG:
    def __init__(self, linked_plane, arena_handler):
        self.arena_handler = arena_handler
        self.ressource_handler = self.arena_handler.ressource_handler

        # Weapon metadata
        self.linked_plane = linked_plane

        self.start_rate_of_fire = 1 / self.ressource_handler.fetch_data(["weapons", "basic_mg", "start_rate_of_fire"])
        self.end_rate_of_fire = 1 / self.ressource_handler.fetch_data(["weapons", "basic_mg", "end_rate_of_fire"])
        self.diff_rate_of_fire = self.end_rate_of_fire - self.start_rate_of_fire

        self.start_spread = self.ressource_handler.fetch_data(["weapons", "basic_mg", "start_spread"]) * 1000
        self.end_spread = self.ressource_handler.fetch_data(["weapons", "basic_mg", "end_spread"]) * 1000
        self.diff_spread = self.end_spread - self.start_spread

        self.time_before_overheat = self.ressource_handler.fetch_data(["weapons", "basic_mg", "time_before_overheat"])
        self.overheat_severity_exponent = self.ressource_handler.fetch_data(["weapons", "basic_mg", "overheat_severity_exponent"])
        self.cooldown_rate = self.ressource_handler.fetch_data(["weapons", "basic_mg", "cooldown_rate"])

        self.recoil = self.ressource_handler.fetch_data(["weapons", "basic_mg", "recoil"])

        # Projectile metadata
        self.projectile = RayBullet
        self.projectile_initial_speed = self.ressource_handler.fetch_data(["weapons", "basic_mg", "projectile_speed"])
        self.projectile_handler = self.arena_handler.projectile_handler

        # Weapon state
        self.have_been_triggered = False
        self.weapon_time_spend_shooting = 0
        self.time_since_fired = 0
        self.time_excess = 0

    def get_overheat_coef(self):
        return (self.weapon_time_spend_shooting/self.time_before_overheat)**self.overheat_severity_exponent

    def trigger_down(self):
        pass

    def trigger_pressed(self, delta):
        actual_rof = self.start_rate_of_fire + self.get_overheat_coef() * self.diff_rate_of_fire
        self.time_since_fired += self.time_excess

        if self.time_since_fired > actual_rof:
            self.time_excess = self.time_since_fired - actual_rof
            self.time_since_fired = 0
            self.shoot()

        else:
            self.time_excess = self.time_since_fired
            self.time_since_fired = 0

        # Gestion surchauffe
        self.weapon_time_spend_shooting += delta
        if self.weapon_time_spend_shooting > self.time_before_overheat:
            self.weapon_time_spend_shooting = self.time_before_overheat

    def trigger_up(self):
        pass

    def reset(self, delta):
        if self.time_since_fired:
            self.time_since_fired = 0
            self.time_excess = 0

            # Gestion surchauffe
            if self.weapon_time_spend_shooting:
                self.weapon_time_spend_shooting -= delta * self.cooldown_rate
                if self.weapon_time_spend_shooting <= 0:
                    self.weapon_time_spend_shooting = 0
        self.time_since_fired += delta

    def shoot(self):
        self.arena_handler.ressource_handler.play_sound(["weapons", "basic_mg"])
        self.linked_plane.set_speed(-self.recoil, 0)

        rad = radians(self.linked_plane.a)
        pvx = self.linked_plane.vx + cos(rad) * self.projectile_initial_speed
        pvy = self.linked_plane.vy + sin(rad) * self.projectile_initial_speed

        spread = self.start_spread + round(self.get_overheat_coef() * self.diff_spread)
        rspread = radians(gauss(0, spread) / 1000)
        sinspread = sin(rspread)
        cosspread = cos(rspread)

        pvx = pvx * cosspread - pvy * sinspread
        pvy = pvy * cosspread + pvx * sinspread

        dvx = pvx - self.linked_plane.vx
        dvy = pvy - self.linked_plane.vy

        initial_pos = (self.linked_plane.x, self.linked_plane.y)
        initial_speed = (pvx, pvy)
        initial_a = degrees(atan2(dvy, dvx))

        projectile = self.projectile(self.arena_handler,
                                     self.linked_plane.player_number,
                                     initial_pos, initial_speed, initial_a)

        projectile.set_position(8, 0, True, True)

        self.projectile_handler.add_projectile(projectile)
