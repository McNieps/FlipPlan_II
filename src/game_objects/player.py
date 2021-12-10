import pygame

from math import radians, sin, cos
from numpy import dot
from random import randint
from src.engine.opp import OPP
from src.game_objects.projectiles import SimpleBullet
from src.game_objects.weapons.basic_mg import BasicMG


class Player:
    def __init__(self, number, x, y, image_type, projectile_handler):
        # position and movement
        self.x = x
        self.y = y
        self.a = 0
        self.vx = 0
        self.vy = 0
        self.va = 0
        self.friction = 0.85
        self.catchup_rate = 0.5
        self.catchup_loss = 0.8
        self.catchup_min_speed = 100
        self.mg = BasicMG(SimpleBullet, self, projectile_handler)

        # freefall
        self.free_fall = 0
        self.free_fall_length = 1  # sec

        # surface and masks
        self.opp = OPP(image_type, 0.4)
        self.image = None
        self.rect = None
        self.mask = None
        self.mask_affichee = False

        # player meta
        self.player_number = number

        # weapons
        self.weapon_1_projectile_surface = pygame.image.load("../assets/projectiles/simple_bullet.png").convert_alpha()
        self.weapon_1_shot_sound = pygame.mixer.Sound("../assets/sounds/basic_shot/basic_shot_1.wav")
        self.weapon_1_shot_sound.set_volume(0.1)
        self.weapon_1_rof = 1/35  # duree pour un tir
        self.weapon_1_projectile_speed = 800
        self.weapon_1_sec_pressed = 0
        self.weapon_1_spread = int(radians(5)*1000)     # 5 degrees de spread
        self.projectile_handler = projectile_handler

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

    def use1_key(self, kdkpku, delta):      # Useless pour le moment
        if kdkpku[1]:
            self.weapon_1_sec_pressed += delta
            added_projectile = []
            number_of_new_bullets = round(self.weapon_1_sec_pressed//self.weapon_1_rof)
            for i in range(number_of_new_bullets):
                self.weapon_1_shot_sound.play()
                self.set_speed(-10, 0)
                rad = radians(self.a)
                spread = randint(-self.weapon_1_spread, self.weapon_1_spread)/1000
                pvx = self.vx + cos(rad) * self.weapon_1_projectile_speed
                pvy = self.vy + sin(rad) * self.weapon_1_projectile_speed
                sinspread = sin(spread)
                cosspread = cos(spread)
                pvx = pvx * cosspread - pvy * sinspread
                pvy = pvy * cosspread + pvx * sinspread
                projectile = SimpleBullet(self.player_number, self.x, self.y, pvx, pvy)
                self.projectile_handler.add_projectile(projectile)
                # todo creer bcp de balle en fonction du cooldown et a la fin faire move delta pour eviter qu'elles soient stacké
            self.weapon_1_sec_pressed %= self.weapon_1_rof

    def use2_key(self, kdkpku, delta):      # Useless pour le moment
        if kdkpku[0]:
            self.mask_affichee = True
        if kdkpku[2]:
            self.mask_affichee = False

    def use3_key(self, kdkpku, delta):      # Useless pour le moment
        if kdkpku[1]:
            self.mg.trigger(delta)
    # endregion

    # region player update
    def update_position_and_angle(self, delta):
        # TODO retirer la merde qui suit
        self.mg.reset(delta)

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

    def update_surface_and_hitbox(self):
        self.opp.set_angle(360-self.a, False)
        self.image = self.opp.get_surface()
        self.image = pygame.transform.rotate(self.image, -self.a)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        if self.mask_affichee:
            self.image = self.mask.to_surface()
        self.rect.center = self.x, self.y

    # endregion
