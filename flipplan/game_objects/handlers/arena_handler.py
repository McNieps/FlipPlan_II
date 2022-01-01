import pygame

from flipplan.engine.camera import Camera
from flipplan.engine.library import set_outline
from flipplan.engine.handlers.ressource_handler import RessourceHandler

from flipplan.game_objects.handlers.player_handler import PlayerHandler
from flipplan.game_objects.handlers.projectile_handler import ProjectileHandler
from flipplan.game_objects.world import World

# TODO RETIRER CES IMPORTS DE POUDZOUF
from flipplan.game_objects.projectiles.ray_bullet import RayBullet
from flipplan.game_objects.projectiles.missile import Missile


class ArenaHandler:
    def __init__(self, window: pygame.Surface, ressource_handler: RessourceHandler,
                 number_of_players: int, level_name: str = "mountains"):

        self.window = window
        self.ressource_handler = ressource_handler

        self.projectile_handler = ProjectileHandler()
        self.player_handler = PlayerHandler(self)
        self.player_handler.add_players(number_of_players)

        screen_size = self.ressource_handler.fetch_data(["system", "window", "size"])
        self.world = World(screen_size, level_name)
        self.camera = Camera(screen_size, self.player_handler.players, self.world.level_size)

    def update_event(self, event):
        self.player_handler.update_event(event)

    def update(self, delta):
        self.player_handler.handle_input(delta)
        self.player_handler.handle_movements(delta)
        self.player_handler.update_surface_and_mask()
        self.player_handler.reset_keys()

        self.projectile_handler.handle_movements(delta)

        for projectile in self.projectile_handler.projectile_list:
            if not self.world.rect_in_level(projectile.rect):
                projectile.leave_level()
            elif pos := self.world.collide_ground_mask_mask(projectile.mask, projectile.rect):
                projectile.hit_ground()
                if type(projectile) == RayBullet:
                    self.world.dig_ground(pos, 2)
                if type(projectile) == Missile:
                    self.world.dig_ground(pos, 20)
            else:
                for player in self.player_handler.players:
                    if player.player_number != projectile.player_number:
                        diff_pos = -player.rect[0] + projectile.rect[0], -player.rect[1] + projectile.rect[1]
                        if player.mask.overlap(projectile.mask, diff_pos):
                            projectile.hit_player()
                            player.hit(20)  # TODO Gerer ça c'est naze là
        self.projectile_handler.check_and_remove_projectile()

        for player in self.player_handler.players:
            if not self.world.level_rect.collidepoint(player.rect.center):
                # Ajouter player respawn
                print("Sorti du terrain")
                player.set_position(50, 50, False)
                player.set_speed(0, 0, False)

            if self.world.collide_ground_point_mask(player.rect.center):
                # Ajouter player respawn
                print("crash dans le terrain")
                player.set_position(50, 50, False)
                player.set_speed(0, 0, False)

                self.world.dig_ground(player.rect.center, 20)

    def render(self):
        screen_rect = self.camera.compute_screen_size()
        offsetx, offsety = -screen_rect.left, -screen_rect.top

        self.window.fill(self.world.level_bg_color)

        self.world.blit_background_to_surface(self.window, screen_rect)
        self.world.blit_ground_to_surface(self.window, screen_rect)

        for projectile in self.projectile_handler.projectile_list:
            projectile_pos = projectile.rect[0] + offsetx, projectile.rect[1] + offsety
            self.window.blit(projectile.image, projectile_pos)

        for player in self.player_handler.players:
            # -1 sur x et -1 sur y pour prendre en compte le set_outline
            player_pos = player.rect[0] + offsetx - 1, player.rect[1] + offsety - 1
            self.window.blit(set_outline(player.image, 1, (70, 14, 43)), player_pos)
