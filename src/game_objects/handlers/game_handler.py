import pygame

from src.game_objects.handlers.player_handler import PlayerHandler
from src.game_objects.world import World

from src.engine.camera import Camera


class GameHandler:
    def __init__(self, world: World, player_handler: PlayerHandler, window: pygame.Surface):
        self.world_handler = world
        self.player_handler = player_handler
        self.window = window
        self.camera = Camera(self.player_handler.players)

    def render(self):
        screen_rect = self.camera.compute_screen_size()
        offsetx, offsety = -screen_rect.left, -screen_rect.top

        tempsurf = pygame.Surface(screen_rect.size)
        tempsurf.fill(self.world_handler.background)
        tempsurf.blit(self.world_handler.ground, (0, 0), screen_rect)

        for i in range(len(self.player_handler.players)):
            player_pos = self.player_handler.players[i].rect[0]+offsetx, self.player_handler.players[i].rect[1]+offsety
            tempsurf.blit(self.player_handler.players[i].image, player_pos)

        if screen_rect.size != self.window.get_rect().size:
            tempsurf = pygame.transform.scale(tempsurf, self.window.get_rect().size)
        self.window.blit(tempsurf, (0, 0))
