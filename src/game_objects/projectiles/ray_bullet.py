import pygame
from math import radians, cos, sin


class RayBullet:
    def __init__(self, player_number, x, y, vx, vy, angle=0):
        # position and movement
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.a = angle

        # surface and mask
        self.original_image = pygame.image.load("../assets/projectiles/simple_bullet.png").convert_alpha()
        self.image = pygame.transform.rotate(self.original_image, -self.a)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # meta
        self.player_number = player_number

        # behaviour
        self.number_of_hit_left = 1
        self.death_function = self.on_death_event

    def update_position(self, delta):
        self.vy += 275*delta
        self.x += self.vx * delta
        self.y += self.vy * delta
        self.rect.center = self.x, self.y

    def set_position(self, x, y, increment=True, relative=False):
        if relative:
            rad = radians(self.a)
            cosa, sina = cos(rad), sin(rad)
            x, y = cosa * x - sina * y, sina * x + cosa * y

        if increment:
            self.x += x
            self.y += y
        else:
            self.x = x
            self.y = y

    def hit_player(self):
        self.number_of_hit_left -= 1

    def hit_ground(self):
        self.number_of_hit_left = 0

    def leave_level(self):
        self.death_function = self.null_function
        self.number_of_hit_left = 0

    def on_death_event(self):
        pass

    def null_function(self):
        pass
