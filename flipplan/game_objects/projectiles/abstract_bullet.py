import pygame

from math import radians, degrees, cos, sin, atan2
from numpy import sign


class AbstractBullet:
    def __init__(self, arena_handler, player_number, initial_pos, initial_speed, initial_a):
        # meta
        self.arena_handler = arena_handler
        self.ressource_handler = self.arena_handler.ressource_handler
        self.player_number = player_number

        # position and movement
        self.x = initial_pos[0]
        self.y = initial_pos[1]
        self.a = initial_a
        self.vx = initial_speed[0]
        self.vy = initial_speed[1]
        self.va = 0

        # surface and mask
        self.original_image = None
        self.image = None
        self.rect = None
        self.mask = None

        # behaviour
        self.number_of_hit_left = 1
        self.death_function = self.on_death_event

    def update_position(self, delta):
        self.x += self.vx * delta
        self.y += self.vy * delta

    def update_angle(self, delta):
        print("aaaa")
        final_angle = degrees(atan2(self.vy, self.vx))
        diff_angle = final_angle - self.a
        BASE_ANGLE_SPEED = 90
        gain_angle = BASE_ANGLE_SPEED * delta * sign(diff_angle)

        if abs(gain_angle) > abs(diff_angle):
            self.a = final_angle
        else:
            self.a += gain_angle

    def update_image_rect_mask(self):
        self.update_image()
        self.update_rect()
        self.update_mask()

    def update_image(self):
        self.image = pygame.transform.rotate(self.original_image, -self.a)

    def update_rect(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta):
        self.update_position(delta)
        # self.update_angle(delta)
        self.update_image_rect_mask()

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

    def hit_ground(self, pos):
        self.arena_handler.world.dig_ground(pos, 2)        # TODO AJOUTER RAYON CREUSAGE
        self.number_of_hit_left = 0

    def leave_level(self):
        self.death_function = self.null_function
        self.number_of_hit_left = 0

    def on_death_event(self):
        print("ABSTRACT_BULLET_DEATH_EVENT")

    def null_function(self):
        pass
