import pygame
from math import radians, cos, sin

from src.game_objects.projectiles import AbstractBullet


class RayBullet(AbstractBullet):
    def __init__(self, player_number, x, y, vx, vy, angle=0):
        super().__init__(player_number, x, y, vx, vy, angle)

        # surface and mask
        self.original_image = pygame.image.load("../assets/projectiles/simple_bullet.png").convert_alpha()
        self.image = pygame.transform.rotate(self.original_image, -self.a)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
