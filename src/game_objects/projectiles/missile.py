import pygame

from src.game_objects.projectiles.abstract_bullet import AbstractBullet
from math import radians, atan2, cos, sin


class Missile(AbstractBullet):
    def __init__(self, player_number, x, y, vx, vy, a, dvx, dva, fva, img, sound_launch, sound_destroyed):
        super().__init__(player_number, x, y, vx, vy)
        self.a = a
        self.original_image = img
        self.acceleration = dvx
        self.angle_variation_amplitude = dva
        self.angle_variation_frequency = fva
        self.sound_channel = sound_launch.play()
        self.sound_destroyed = sound_destroyed

    def update(self, delta):
        rad = radians(self.a)
        self.vx += cos(rad) * self.acceleration * delta
        self.vy += sin(rad) * self.acceleration * delta

        self.image = pygame.transform.rotate(self.original_image, -self.a)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.mask = pygame.mask.from_surface(self.image)
        self.update_position(delta)

    def on_death_event(self):
        self.sound_destroyed.play()