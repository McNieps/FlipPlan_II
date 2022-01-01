import pygame

from math import radians, sin, cos
from numpy import dot

from flipplan.engine.opp import OPP
from flipplan.game_objects.weapons.basic_mg import BasicMG
from flipplan.game_objects.weapons.missile_launcher import MissileLauncher


class Player:
    def __init__(self, number: int, x: float, y: float, a: float, image_dict: dict, arena_handler):
        self.arena_handler = arena_handler

        # position and movement
        self.x = x
        self.y = y
        self.a = a
        self.vx = 0
        self.vy = 0
        self.va = 0
        self.friction = 0.85
        self.catchup_rate = 0.5
        self.catchup_loss = 0.8
        self.catchup_min_speed = 100

        # freefall
        self.free_fall = 0
        self.free_fall_length = 1  # sec

        # surface and masks
        self.opp = OPP(image_dict, 1)
        self.image = None
        self.rect = None
        self.mask = None
        self.mask_affichee = False

        # player meta
        self.player_number = number

        # weapons
        self.weapon_1 = BasicMG(self, self.arena_handler)
        self.weapon_2 = MissileLauncher(self, self.arena_handler)

        # stats
        self.health = 100

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
    # endregion

    # region user inputs
    def up_key(self, kdkpku, delta):        # Accelere
        if kdkpku[1]:   # key_pressed
            self.set_speed(250*delta, 0)

    def left_key(self, kdkpku, delta):      # Tourne
        if kdkpku[1]:   # key_pressed
            self.set_angle(-180 * delta)

    def down_key(self, kdkpku):      # Decroche
        if kdkpku[1]:   # key_pressed
            self.free_fall = self.free_fall_length

    def right_key(self, kdkpku, delta):     # Tourne
        if kdkpku[1]:   # key_pressed
            self.set_angle(180 * delta)

    def use1_key(self, kdkpku, delta):
        if kdkpku[0]:
            self.weapon_1.trigger_down()
        if kdkpku[1]:
            self.weapon_1.trigger_pressed(delta)
        elif kdkpku[2]:
            self.weapon_1.trigger_up()

    def use2_key(self, kdkpku, delta):
        if kdkpku[0]:
            self.weapon_2.trigger_down()
        if kdkpku[1]:
            self.weapon_2.trigger_pressed(delta)
        elif kdkpku[2]:
            self.weapon_2.trigger_up()

    def use3_key(self, kdkpku, delta):
        pass
    # endregion

    # region player update
    def update_position_and_angle(self, delta):
        if delta > 0.1:
            return False

        self.weapon_1.reset(delta)
        self.weapon_2.reset(delta)

        if self.free_fall:
            self.free_fall -= delta
            if self.free_fall <= 0:
                self.free_fall = 0

        self.vy += 275 * delta
        self.a += self.va

        if not self.free_fall and (abs(self.vx) > 0 or abs(self.vy) > 0):
            rad = radians(self.a)
            cosa, sina = cos(rad), sin(rad)
            dir_vec = [cosa, sina]

            speed_vec = [self.vx, self.vy]
            speed = (self.vx**2 + self.vy**2)**0.5

            dot_speed = ((dir_vec[0]*speed_vec[0]+dir_vec[1]*speed_vec[1])/speed)**49
            value = dot_speed

            if abs(dot(speed_vec, dir_vec)) > self.catchup_min_speed:
                new_speed = value * speed * self.catchup_loss**delta
                self.vx *= 1-abs(value)
                self.vy *= 1-abs(value)
                self.set_speed(new_speed, 0)

        self.vx *= self.friction**delta
        self.vy *= self.friction**delta
        self.x += self.vx*delta
        self.y += self.vy*delta
        return True

    def update_surface_and_hitbox(self):
        self.opp.set_angle(360-self.a, False)
        self.image = self.opp.get_surface()
        self.image = pygame.transform.rotate(self.image, -self.a)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        if self.mask_affichee:
            self.image = self.mask.to_surface()
        self.rect.center = self.x, self.y

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.free_fall = 10

    def respawn(self):
        self.free_fall = 0

    # endregion
