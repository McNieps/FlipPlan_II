import pygame
from numpy import array, dot
from numpy.linalg import norm

from math import radians, sin, cos
from src.engine.opp import OPP


class Player:
    def __init__(self, number, x, y, image_type):
        self.x = x
        self.y = y
        self.a = 0
        self.vx = 0
        self.vy = 0
        self.va = 0
        self.directional_speed = 0
        self.friction = 0.80
        self.catchup_coef = 0.5

        # freefall
        self.free_fall = 0
        self.free_fall_length = 1  # sec

        self.opp = OPP(image_type, 0.5)
        self.image = None
        self.rect = None
        self.mask = None

        self.player_number = number

    # region position and angle control
    def set_angle(self, angle, increment=True):
        if increment:
            self.a += angle
        else:
            self.a = angle
        self.a = self.a % 360

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

    def set_speed(self, vx, vy, increment=True, relative=True):
        if relative:
            rad = radians(self.a)
            cosa, sina = cos(rad), sin(rad)
            vx, vy = cosa * vx - sina * vy, sina * vx + cosa * vy

        if increment:
            self.vx += vx
            self.vy += vy
        else:
            self.vx = vx
            self.vy = vy

    def set_directional_speed(self, speed, increment=False):
        if increment:
            self.directional_speed += speed
        else:
            self.directional_speed = speed
    # endregion

    # region user inputs
    def up_key(self, kdkpku, delta):        # Accelere
        if kdkpku[1]:   # key_pressed
            self.directional_speed += 100 * delta

    def left_key(self, kdkpku, delta):      # Tourne
        if kdkpku[1]:   # key_pressed
            self.set_angle(-180 * delta)

    def down_key(self, kdkpku):      # Decroche
        if kdkpku[0]:   # key_down
            self.set_speed(self.directional_speed, 0)
            self.directional_speed = 0

        if kdkpku[1]:   # key_pressed
            self.free_fall = self.free_fall_length

    def right_key(self, kdkpku, delta):     # Tourne
        if kdkpku[1]:   # key_pressed
            self.set_angle(180 * delta)

    def use1_key(self, kdkpku, delta):      # Useless pour le moment
        if kdkpku[1]:
            self.directional_speed -= 10

    def use2_key(self, kdkpku, delta):      # Useless pour le moment
        pass

    def use3_key(self, kdkpku, delta):      # Useless pour le moment
        pass
    # endregion

    # region player update
    def update_position_and_angle(self, delta):
        self.vy += 40*delta
        if self.free_fall:
            self.free_fall -= delta
            if self.free_fall <= 0:
                self.free_fall = 0

        self.a += self.va
        rad = radians(self.a)
        cosa = cos(rad)
        sina = sin(rad)
        dir_speed_x = cosa*self.directional_speed
        dir_speed_y = sina*self.directional_speed
        self.x += (self.vx + dir_speed_x) * delta
        self.y += (self.vy + dir_speed_y) * delta

        if not self.free_fall and (abs(self.vx) > 1 or abs(self.vy) > 1):
            dir_speed_vec = array([cosa, sina])
            abs_speed_vec = array([self.vx, self.vy])
            abs_speed_norm = norm(abs_speed_vec)

            dot_speed = dot(dir_speed_vec, abs_speed_vec/abs_speed_norm)**9
            value = self.catchup_coef**delta * dot_speed

            self.directional_speed += abs_speed_norm*value
            self.vx *= abs(1-abs(value))
            self.vy *= abs(1-abs(value))
            print(dot_speed)

        self.directional_speed *= self.friction**delta
        self.vx *= self.friction**delta
        self.vy *= self.friction**delta

    def update_surface_and_hitbox(self):
        self.opp.set_angle(-self.a, False)
        self.image = self.opp.get_surface()
        self.image = pygame.transform.rotate(self.image, -self.a)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = self.x, self.y

    # endregion
