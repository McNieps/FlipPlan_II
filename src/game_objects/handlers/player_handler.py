from pygame.locals import *

from src.game_objects.handlers.projectile_handler import ProjectileHandler
from src.game_objects.player import Player


class PlayerHandler:
    def __init__(self, projectile_handler: ProjectileHandler):
        self.players = []
        self.number_of_players = 0

        # KEYS
        self.players_keys = [K_z, K_q, K_s, K_d, K_i, K_o, K_p,
                             K_t, K_f, K_g, K_h, K_KP_7, K_KP_8, K_KP_9]

        self.player_1_keys = {"up": K_z, "left": K_q, "down": K_s, "right": K_d,
                              "use_1": K_i, "use_2": K_o, "use_3": K_p}

        self.player_2_keys = {"up": K_t, "left": K_f, "down": K_g, "right": K_h,
                              "use_1": K_KP_7, "use_2": K_KP_8, "use_3": K_KP_9}

        self.player_dict_keys = [self.player_1_keys, self.player_2_keys]

        self.key_state = {}
        for key in self.players_keys:
            self.key_state[key] = [False, False, False]

        self.projectile_handler = projectile_handler

    def add_player(self):
        player_number = len(self.players) + 1
        self.number_of_players += 1
        player_x = 50
        player_y = 50
        player = Player(player_number, player_x, player_y, "fat_player", self.projectile_handler)

        self.players.append(player)

    def add_players(self, number_of_players):
        for i in range(number_of_players):
            self.add_player()

    def reset_keys(self):
        for key in self.players_keys:
            self.key_state[key][0] = False
            self.key_state[key][2] = False

    def update_event(self, event):
        if event.type == KEYDOWN:
            self.update_keydown(event.key)
        elif event.type == KEYUP:
            self.update_keyup(event.key)

    def update_keydown(self, key):
        if key in self.players_keys:
            self.key_state[key][0] = True
            self.key_state[key][1] = True

    def update_keyup(self, key):
        if key in self.players_keys:
            self.key_state[key][1] = False
            self.key_state[key][2] = True

    def handle_input(self, delta):
        for i in range(self.number_of_players):
            if i < 2:
                dictio = self.player_dict_keys[i]
                self.players[i].up_key(self.key_state[dictio["up"]], delta)
                self.players[i].left_key(self.key_state[dictio["left"]], delta)
                self.players[i].down_key(self.key_state[dictio["down"]])
                self.players[i].right_key(self.key_state[dictio["right"]], delta)
                self.players[i].use1_key(self.key_state[dictio["use_1"]], delta)
                self.players[i].use2_key(self.key_state[dictio["use_2"]], delta)
                self.players[i].use3_key(self.key_state[dictio["use_3"]], delta)

    def handle_movements(self, delta):
        for i in range(self.number_of_players):
            self.players[i].update_position_and_angle(delta)

    def update_surface_and_mask(self):
        for i in range(self.number_of_players):
            self.players[i].update_surface_and_hitbox()
