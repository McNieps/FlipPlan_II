import pygame

from src.game_objects.handlers.player_handler import PlayerHandler
from src.game_objects.world import World

from src.engine.camera import Camera

from time import time


class GameHandler:
    def __init__(self, world: World, player_handler: PlayerHandler, window: pygame.Surface):
        self.world = world
        self.player_handler = player_handler
        self.window = window
        self.camera = Camera(self.player_handler.players)
        self.snd = pygame.mixer.Sound("../assets/sounds/explosion/loud_explosion.wav")

    def update_position(self, delta):
        self.player_handler.handle_input(delta)
        self.player_handler.handle_movements(delta)
        self.player_handler.update_surface_and_mask()
        self.player_handler.reset_keys()

    def render(self):
        screen_rect = self.camera.compute_screen_size()
        offsetx, offsety = -screen_rect.left, -screen_rect.top

        temporary_surface = pygame.Surface(screen_rect.size).convert_alpha()
        temporary_surface.fill(self.world.background)
        print(temporary_surface.blit(self.world.ground, (0, 0), screen_rect))

        for player in self.player_handler.players:
            player_pos = player.rect[0] + offsetx, player.rect[1] + offsety
            temporary_surface.blit(player.image, player_pos)

            if not self.world.rect.collidepoint(player.rect.center) or self.world.mask.get_at(player.rect.center):
                self.world.dig_ground(player.rect.center, 30)

                player.set_position(50, 50, False)
                player.set_speed(0, 0, False)
                self.snd.play()

        if screen_rect.size != self.window.get_rect().size:
            temporary_surface = pygame.transform.scale(temporary_surface, self.window.get_rect().size)

        self.window.blit(temporary_surface, (0, 0))
