import pygame
from json import load as json_load


class World:
    def __init__(self, level_folder_name="cliffs"):
        file = open(f"../assets/world/{level_folder_name}/world_data.json", "r")
        level_dictionary = json_load(file)
        file.close()

        self.level_name = level_dictionary["level_name"]
        self.level_size = level_dictionary["level_size"]
        self.level_bg_color = level_dictionary["bg_color"]

        self.level_ground_surfaces = {}
        self.level_ground_rects = {}
        self.level_ground_masks = {}
        self.level_rect = pygame.Rect(0, 0, self.level_size[0], self.level_size[1])

        self.load_surfaces_rects_masks(level_dictionary, level_folder_name)

    def load_surfaces_rects_masks(self, level_dictionary, level_folder_name):
        for i in level_dictionary["ground_parts"]:
            image_file_path = f"../assets/world/{level_folder_name}/{i}"
            surf = pygame.image.load(image_file_path).convert_alpha()
            rect = surf.get_rect()
            rect.move_ip(level_dictionary["ground_parts"][i])
            rect_tuple = tuple(rect)
            mask = pygame.mask.from_surface(surf)
            self.level_ground_surfaces[rect_tuple] = surf
            self.level_ground_rects[rect_tuple] = rect
            self.level_ground_masks[rect_tuple] = mask

    def blit_ground_to_surface(self, surface, camera_rect):
        zoom_x = camera_rect.width / surface.get_rect().width
        zoom_y = camera_rect.height / surface.get_rect().height

        for tuple_rect in self.level_ground_rects:
            if camera_rect.colliderect(self.level_ground_rects[tuple_rect]):
                # isolate surface
                clipping_rect = camera_rect.clip(self.level_ground_rects[tuple_rect])
                sub_surf_rect = clipping_rect.move(-tuple_rect[0], -tuple_rect[1])
                sub_surf = self.level_ground_surfaces[tuple_rect].subsurface(sub_surf_rect)

                # surface mapping
                screen_rect = clipping_rect.move(-camera_rect[0], -camera_rect[1])
                new_x = round(screen_rect.left / zoom_x)
                new_y = round(screen_rect.top / zoom_y)
                new_width = round(screen_rect.width / zoom_x)
                new_height = round(screen_rect.height / zoom_y)
                screen_rect = pygame.Rect(new_x, new_y, new_width, new_height)
                # pygame.draw.rect(surface, (255, 0, 0), screen_rect)
                surface.blit(pygame.transform.scale(sub_surf, screen_rect.size), screen_rect)

    def dig_ground(self, pos, radius):
        surface = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(surface, (123, 123, 123), (radius, radius), radius)
        surface.set_colorkey((0, 0, 0))
        rect = surface.get_rect()
        rect.center = pos

        for tuple_rect in self.level_ground_rects:
            if self.level_ground_rects[tuple_rect].colliderect(rect):
                ground_rect = self.level_ground_rects[tuple_rect]
                new_rect = rect.move(-ground_rect.left, -ground_rect.top)
                self.level_ground_surfaces[tuple_rect].blit(surface, new_rect)
                self.level_ground_surfaces[tuple_rect].set_colorkey((123, 123, 123))
                self.level_ground_surfaces[tuple_rect] = self.level_ground_surfaces[tuple_rect].convert_alpha()
                self.level_ground_masks[tuple_rect] = pygame.mask.from_surface(self.level_ground_surfaces[tuple_rect])

    def collide_ground_point_mask(self, point):
        for tuple_rect in self.level_ground_rects:
            if self.level_ground_rects[tuple_rect].collidepoint(point):
                local_point_coords = point[0]-tuple_rect[0], point[1]-tuple_rect[1]
                if ans := self.level_ground_masks[tuple_rect].get_at(local_point_coords):
                    return ans
        return False

    def collide_ground_rect_rect(self, rect):
        pass

    def collide_ground_mask_mask(self, mask, offset):
        pass
