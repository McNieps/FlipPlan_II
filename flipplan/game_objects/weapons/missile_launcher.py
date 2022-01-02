import pygame

from json import load as json_load
from math import radians, cos, sin

from flipplan.game_objects.projectiles.missile import Missile


class MissileLauncher:
    def __init__(self, linked_plane, arena_handler):
        self.arena_handler = arena_handler

        # Weapon metadata
        self.gunshot_sound = pygame.mixer.Sound("../assets/sounds/weapons/missile_launcher/missile_launch_1.wav")
        self.gunshot_sound.set_volume(0.05)
        self.missiles_capacity = None
        self.missiles_quantity = None
        self.missiles_recover_time = None
        self.linked_plane = linked_plane

        # Projectile metadata
        self.projectile = Missile
        self.projectile_image = pygame.image.load("../assets/images/projectiles/missile.png").convert()
        self.projectile_sound_launch = pygame.mixer.Sound("../assets/sounds/weapons/missile_launcher/missile_launch_1.wav")
        self.projectile_sound_destroyed = pygame.mixer.Sound("../assets/sounds/explosion/loud_explosion.wav")
        self.projectile_sound_launch.set_volume(0.05)
        self.projectile_sound_destroyed.set_volume(0.05)
        self.projectile_image.set_colorkey((0, 0, 0))
        self.projectile_handler = self.arena_handler.projectile_handler
        self.projectile_initial_speed = None
        self.projectile_acceleration = None
        self.projectile_speed_distribution = None

        # Weapon state
        self.missile_linked = None
        self.has_fired = False
        self.missiles_current_cooldown = 0

        # self.load_values()

    def load_values(self):
        file = open("../game_objects/weapons/weapons.json")
        dictionary = json_load(file)
        file.close()

        self.missiles_capacity = dictionary["missile_launcher"]["capacity"]
        self.missiles_quantity = dictionary["missile_launcher"]["capacity"]
        self.missiles_recover_time = dictionary["missile_launcher"]["recover_time"]

        self.projectile_initial_speed = dictionary["missile_launcher"]["projectile_speed"]
        self.projectile_acceleration = dictionary["missile_launcher"]["projectile_acceleration"]
        self.projectile_speed_distribution = dictionary["missile_launcher"]["projectile_speed_distribution"]

    def trigger_down(self):
        if self.missiles_quantity > 0:
            self.missiles_quantity -= 1
            self.shoot()
            self.has_fired = True

    def trigger_pressed(self, delta):
        if self.missile_linked:
            linked_plane_x = self.linked_plane.x
            linked_plane_y = self.linked_plane.y
            dv = self.projectile_acceleration * self.projectile_speed_distribution * delta
            self.missile_linked.set_position(linked_plane_x, linked_plane_y, False, False)
            self.linked_plane.set_speed(dv, 0)
            self.missile_linked.a = self.linked_plane.a
            self.missile_linked.vx = self.linked_plane.vx
            self.missile_linked.vy = self.linked_plane.vy

    def trigger_up(self):
        self.missile_linked = None

    def reset(self, delta):
        self.has_fired = True
        if not self.has_fired:
            if self.missiles_quantity < self.missiles_capacity:
                self.missiles_current_cooldown += delta
                if self.missiles_current_cooldown > self.missiles_recover_time:
                    self.missiles_quantity += 1
                    if self.missiles_quantity == self.missiles_capacity:
                        self.missiles_current_cooldown = 0
                    else:
                        self.missiles_current_cooldown -= self.missiles_recover_time

        self.has_fired = False

    def shoot(self):
        rad = radians(self.linked_plane.a)
        pvx = self.linked_plane.vx + cos(rad) * self.projectile_initial_speed
        pvy = self.linked_plane.vy + sin(rad) * self.projectile_initial_speed

        projectile = self.projectile(self.arena_handler,
                                     self.linked_plane.player_number,
                                     self.linked_plane.x,
                                     self.linked_plane.y,
                                     pvx, pvy,
                                     self.linked_plane.a,
                                     self.projectile_acceleration,
                                     "ampli", "frequence")

        # projectile.set_position(8, 0, True, True)
        self.projectile_handler.add_projectile(projectile)
        self.missile_linked = projectile
