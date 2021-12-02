import pygame


class World:
    def __init__(self):
        self.background = (44, 232, 245)
        self.ground = pygame.image.load("../assets/world.png").convert_alpha()
