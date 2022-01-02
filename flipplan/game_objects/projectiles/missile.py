from flipplan.game_objects.projectiles.abstract_bullet import AbstractBullet
from math import radians, cos, sin


class Missile(AbstractBullet):
    def __init__(self, arena_handler, player_number, initial_pos, initial_speed, initial_a):
        super().__init__(arena_handler, player_number, initial_pos, initial_speed, initial_a)

        # Projectile image
        self.original_image = self.arena_handler.ressource_handler.images["projectiles"]["missile"]
        self.update_image_rect_mask()

        # Projectile sound
        self.sound_channel = self.arena_handler.ressource_handler.play_sound(["weapons", "missile_launcher"])

        # Projectile data
        self.acceleration = self.arena_handler.ressource_handler.fetch_data(["projectile", "missile", "acceleration"])

    def update_position(self, delta):
        rad = radians(self.a)
        self.vx += cos(rad) * self.acceleration * delta
        self.vy += sin(rad) * self.acceleration * delta
        self.x += self.vx
        self.y += self.vy

    def on_death_event(self):
        self.arena_handler.ressource_handler.play_sound(["explosion"], self.sound_channel)
