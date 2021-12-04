import pygame


class World:
    def __init__(self, world_name="world"):
        self.background = (44, 232, 245)
        self.world_name = world_name
        self.ground = pygame.image.load(f"../assets/{world_name}.png").convert_alpha()
        self.size = self.ground.get_size()
        self.image = pygame.Surface(self.size)
        self.update_image()

    def update_image(self):
        self.image.fill(self.background)
        self.image.blit(self.ground, (0, 0))
        return self.image
