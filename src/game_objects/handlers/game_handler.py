import pygame

from src.game_objects.handlers.player_handler import PlayerHandler
from src.game_objects.handlers.projectile_handler import ProjectileHandler
from src.game_objects.world import World
from src.engine.library import set_outline

from src.engine.camera import Camera

from time import time as time


class GameHandler:
    def __init__(self, window: pygame.Surface, number_of_players: int, level_name: str = "mountains"):
        self.projectile_handler = ProjectileHandler()
        self.player_handler = PlayerHandler(self.projectile_handler)
        self.player_handler.add_players(number_of_players)
        self.world = World(level_name)

        self.window = window
        self.camera = Camera(self.player_handler.players, self.world.level_size)
        self.snd = pygame.mixer.Sound("../assets/sounds/explosion/loud_explosion.wav")
        self.snd.set_volume(0.2)

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
                self.world.dig_ground(pos, 2)  # TODO remettre normal
            else:
                for player in self.player_handler.players:
                    if player.player_number != projectile.player_number:
                        diff_pos = -player.rect[0] + projectile.rect[0], -player.rect[1] + projectile.rect[1]
                        if player.mask.overlap(projectile.mask, diff_pos):
                            projectile.hit_player()
                            player.hit(20)

        self.projectile_handler.check_and_remove_projectile()

    def render(self):

        screen_rect = self.camera.compute_screen_size()
        offsetx, offsety = -screen_rect.left, -screen_rect.top

        # TODO Retirer cette surface temporaraire de merde, ça fait rammer
        temporary_surface = pygame.Surface(screen_rect.size).convert_alpha()
        temporary_surface.set_colorkey((0, 0, 0))
        self.window.fill(self.world.level_bg_color)

        self.world.blit_ground_to_surface(self.window, screen_rect)

        for projectile in self.projectile_handler.projectile_list:
            projectile_pos = projectile.rect[0] + offsetx, projectile.rect[1] + offsety
            temporary_surface.blit(projectile.image, projectile_pos)

        for player in self.player_handler.players:
            player_pos = player.rect[0] + offsetx - 1, player.rect[1] + offsety - 1

            temporary_surface.blit(set_outline(player.image, 1, (70, 14, 43)), player_pos)

            if not self.world.level_rect.collidepoint(player.rect.center) or self.world.collide_ground_point_mask(
                    player.rect.center):
                self.world.dig_ground(player.rect.center, 20)

                player.set_position(50, 50, False)
                player.set_speed(0, 0, False)
                self.snd.play()

        if screen_rect.size != self.window.get_rect().size:
            temporary_surface = pygame.transform.scale(temporary_surface, self.window.get_rect().size).convert_alpha()

        self.window.blit(temporary_surface, (0, 0))
