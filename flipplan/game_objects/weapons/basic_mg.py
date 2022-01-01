import pygame

from math import radians, cos, sin
from json import load as json_load
from random import gauss

from flipplan.game_objects.projectiles.ray_bullet import RayBullet


class BasicMG:
    def __init__(self, linked_plane, arena_handler):
        self.arena_handler = arena_handler

        # Weapon metadata
        self.start_rate_of_fire = None
        self.end_rate_of_fire = None
        self.diff_rate_of_fire = None
        self.start_spread = None
        self.end_spread = None
        self.diff_spread = None
        self.time_before_overheat = None
        self.overheat_severity_exponent = None
        self.cooldown_rate = None
        self.linked_plane = linked_plane
        self.recoil = None

        # Projectile metadata
        self.projectile = RayBullet
        self.projectile_image = self.arena_handler.ressource_handler.images["projectiles"]["ray_bullet"]
        self.projectile_initial_speed = None
        self.projectile_handler = self.arena_handler.projectile_handler

        # Weapon state
        self.have_been_triggered = False
        self.weapon_time_spend_shooting = 0
        self.time_since_fired = 0
        self.time_excess = 0

        self.load_values()

    def load_values(self):
        file = open("../game_objects/weapons/weapons.json")
        dictionary = json_load(file)
        file.close()

        self.start_rate_of_fire = 1 / dictionary["basic_mg"]["start_rate_of_fire"]
        self.end_rate_of_fire = 1 / dictionary["basic_mg"]["end_rate_of_fire"]
        self.diff_rate_of_fire = self.end_rate_of_fire - self.start_rate_of_fire
        self.start_spread = dictionary["basic_mg"]["start_spread"] * 1000
        self.end_spread = dictionary["basic_mg"]["end_spread"] * 1000
        self.diff_spread = self.end_spread - self.start_spread
        self.time_before_overheat = dictionary["basic_mg"]["time_before_overheat"]
        self.overheat_severity_exponent = dictionary["basic_mg"]["overheat_severity_exponent"]
        self.cooldown_rate = dictionary["basic_mg"]["cooldown_rate"]
        self.projectile_initial_speed = dictionary["basic_mg"]["projectile_speed"]
        self.recoil = dictionary["basic_mg"]["recoil"]

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
        projectile = self.projectile(self.linked_plane.player_number,
                                     self.linked_plane.x,
                                     self.linked_plane.y,
                                     pvx, pvy, self.projectile_image)
        projectile.set_position(8, 0, True, True)
        self.projectile_handler.add_projectile(projectile)