import pygame
from json import load as json_load


class World:
    def __init__(self, level_name="cliffs"):
        file = open(f"../assets/world/{level_name}/world_data.json", "r")
        level_dictionary = json_load(file)
        file.close()

        self.level_name = level_dictionary["level_name"]
        self.level_size = level_dictionary["level_size"]
        self.level_bg_color = level_dictionary["bg_color"]

        self.level_ground_surfaces = {}
        self.level_ground_rects = {}
        self.level_ground_masks = {}
        for i in level_dictionary["ground_parts"]:
            image_file_path = f"../assets/world/{level_name}/{i}"
            surf = pygame.image.load(image_file_path).convert_alpha()
            rect = surf.get_rect()
            rect.move_ip(level_dictionary["ground_parts"][i])
            rect_tuple = tuple(rect)
            mask = pygame.mask.from_surface(surf)
            self.level_ground_surfaces[rect_tuple] = surf
            self.level_ground_rects[rect_tuple] = rect
            self.level_ground_masks[rect_tuple] = mask

        self.ground = pygame.image.load(f"../assets/world/{level_name}.png").convert_alpha()
        self.rect = self.ground.get_rect()
        self.size = self.ground.get_size()
        self.mask = pygame.mask.from_surface(self.ground)

    def dig_ground(self, pos, radius):
        _surface = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(_surface, (123, 123, 123), (radius, radius), radius)
        _surface.set_colorkey((0, 0, 0))
        rect = _surface.get_rect()
        rect.center = pos
        self.ground.blit(_surface, rect.topleft)
        self.ground.set_colorkey((123, 123, 123))
        self.ground = self.ground.convert_alpha()
