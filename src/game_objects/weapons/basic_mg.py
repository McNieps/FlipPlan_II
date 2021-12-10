import pygame

from math import radians, cos, sin
from json import load as json_load
from random import randint


class BasicMG:
    def __init__(self, projectile, linked_plane, projectile_handler):
        # Weapon metadata
        self.gunshot_sound = pygame.mixer.Sound("../assets/sounds/basic_shot/basic_shot_1.wav")
        self.gunshot_sound.set_volume(0.1)
        self.min_rate_of_fire = None
        self.max_rate_of_fire = None
        self.min_spread = None
        self.max_spread = None
        self.time_before_overheat = None
        self.cooldown_rate = None
        self.linked_plane = linked_plane

        # Projectile metadata
        self.projectile = projectile
        self.projectile_initial_speed = None
        self.projectile_handler = projectile_handler

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

        self.min_rate_of_fire = 1 / dictionary["BasicMG"]["min_rate_of_fire"]
        self.max_rate_of_fire = 1 / dictionary["BasicMG"]["max_rate_of_fire"]
        self.min_spread = dictionary["BasicMG"]["min_spread"] * 1000
        self.max_spread = dictionary["BasicMG"]["max_spread"] * 1000
        self.time_before_overheat = dictionary["BasicMG"]["time_before_overheat"]
        self.cooldown_rate = dictionary["BasicMG"]["cooldown_rate"]
        self.projectile_initial_speed = dictionary["BasicMG"]["projectile_speed"]

    def trigger(self, delta):
        # TODO ROF dynamique
        actual_rof = self.max_rate_of_fire
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
        self.gunshot_sound.play()
        self.linked_plane.set_speed(-10, 0)     # TODO add weapon knockback
        rad = radians(self.linked_plane.a)
        pvx = self.linked_plane.vx + cos(rad) * self.projectile_initial_speed
        pvy = self.linked_plane.vy + sin(rad) * self.projectile_initial_speed
        spread = self.max_spread                # TODO add spread function of overheat
        rspread = radians(randint(-spread, spread) / 1000)
        sinspread = sin(rspread)
        cosspread = cos(rspread)
        pvx = pvx * cosspread - pvy * sinspread
        pvy = pvy * cosspread + pvx * sinspread
        projectile = self.projectile(self.linked_plane.player_number,
                                     self.linked_plane.x,
                                     self.linked_plane.y,
                                     pvx, pvy)
        self.projectile_handler.add_projectile(projectile)
