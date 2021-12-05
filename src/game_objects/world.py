import pygame


class World:
    def __init__(self, world_name="world"):
        self.background = (44, 232, 245)
        self.world_name = world_name
        self.ground = pygame.image.load(f"../assets/world/{world_name}.png").convert_alpha()
        self.rect = self.ground.get_rect()
        self.size = self.ground.get_size()
        self.mask = pygame.mask.from_surface(self.ground)

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.ground)
        return self.mask

    def dig_ground(self, pos, radius):
        _surface = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(_surface, (123, 123, 123), (radius, radius), radius)
        _surface.set_colorkey((0, 0, 0))
        rect = _surface.get_rect()
        rect.center = pos
        self.ground.blit(_surface, rect.topleft)
        self.ground.set_colorkey((123, 123, 123))
        self.ground = self.ground.convert_alpha()
        self.update_mask()
