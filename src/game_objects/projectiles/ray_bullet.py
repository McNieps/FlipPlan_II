import pygame
from math import degrees, atan2

from src.game_objects.projectiles.abstract_bullet import AbstractBullet


class RayBullet(AbstractBullet):
    def __init__(self, player_number, x, y, vx, vy, img):
        super().__init__(player_number, x, y, vx, vy)

        # surface and mask
        self.original_image = img
        self.image = pygame.transform.rotate(self.original_image, -self.a)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta):
        self.a = degrees(atan2(self.vy, self.vx))  # TODO faire ça tout les x temps
        self.image = pygame.transform.rotate(self.original_image, -self.a)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.mask = pygame.mask.from_surface(self.image)
        self.update_position(delta)
