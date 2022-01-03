from flipplan.game_objects.projectiles.abstract_bullet import AbstractBullet
from math import radians, cos, sin
from random import gauss


# TODO Ajouter wiggle
class Missile(AbstractBullet):
    def __init__(self, arena_handler, player_number, initial_pos, initial_speed, initial_a):
        super().__init__(arena_handler, player_number, initial_pos, initial_speed, initial_a)

        # Projectile image
        self.original_image = self.ressource_handler.images["projectiles"]["missile"]
        self.update_image_rect_mask()

        # Projectile sound
        self.sound_channel = self.ressource_handler.play_sound(["weapons", "missile_launcher"])

        # Projectile data
        self.acceleration = self.ressource_handler.fetch_data(["projectiles", "missile", "acceleration"])

        self.wiggle_period = self.ressource_handler.fetch_data(["projectiles", "missile", "wiggle_period"])
        self.wiggle_amplitude = self.ressource_handler.fetch_data(["projectiles", "missile", "wiggle_amplitude"])
        self.wiggle_acceleration = self.ressource_handler.fetch_data(["projectiles", "missile", "wiggle_acceleration"])
        self.wiggle_friction = self.ressource_handler.fetch_data(["projectiles", "missile", "wiggle_friction"])

        self.wiggle_time = 0
        self.wiggle_angle = 0
        self.wiggle_speed = 0
        self.wiggle_instruction = gauss(0, self.wiggle_amplitude)

    def update_position(self, delta):
        rad = radians(self.a)
        self.vx += cos(rad) * self.acceleration * delta
        self.vy += sin(rad) * self.acceleration * delta
        self.x += self.vx * delta
        self.y += self.vy * delta

    def hit_ground(self, pos):
        dig_radius = self.ressource_handler.fetch_data(["projectiles", "missile", "ground_damage_radius"])
        self.arena_handler.world.dig_ground(pos, dig_radius)
        self.number_of_hit_left = 0

    def on_death_event(self):
        self.ressource_handler.play_sound(["explosion"], self.sound_channel)
