import pygame
from math import radians, degrees, cos, sin, atan2


class AbstractBullet:
    def __init__(self, player_number, x, y, vx, vy):
        # position and movement
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.a = degrees(atan2(self.vy, self.vx))

        # surface and mask
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # meta
        self.player_number = player_number

        # behaviour
        self.number_of_hit_left = 1
        self.death_function = self.on_death_event

    def update_position(self, delta):
        self.x += self.vx * delta
        self.y += self.vy * delta
        self.rect.center = self.x, self.y

    def update(self, delta):
        self.update_position(delta)

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
