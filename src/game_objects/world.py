import pygame
from json import load as json_load
from math import ceil, floor

from src.engine.library import is_surface_empty
from src.engine.data import SCREEN_SIZE


class World:
    def __init__(self, level_folder_name):
        file = open(f"../assets/world/{level_folder_name}/world_data.json", "r")
        level_dictionary = json_load(file)
        file.close()

        self.level_name = level_dictionary["level_name"]
        self.level_size = level_dictionary["level_size"]
        self.level_bg_color = level_dictionary["bg_color"]
        self.cluster_size = level_dictionary["cluster_size"]

        self.level_ground_surfaces = {}
        self.level_background_surfaces = []
        self.level_rect = pygame.Rect(0, 0, self.level_size[0], self.level_size[1])

        self.load_ground(level_folder_name)
        self.load_background(level_folder_name, level_dictionary)

    def load_ground(self, level_folder_name):
        ground_surf = pygame.image.load(f"../assets/world/{level_folder_name}/ground.png").convert()
        ground_width, ground_height = ground_surf.get_size()
        width_cluster_number = ground_width // self.cluster_size[0]
        height_cluster_number = ground_height // self.cluster_size[1]
        remainings = ground_width % self.cluster_size[0] + ground_height % self.cluster_size[1]
        if remainings:
            raise Exception("Level size and cluster size do not match")

        self.level_ground_surfaces["size"] = ground_surf.get_size()

        for i in range(width_cluster_number):
            for j in range(height_cluster_number):
                cluster_coords = (i, j)
                tuple_rect = (i*self.cluster_size[0],
                              j*self.cluster_size[1],
                              self.cluster_size[0],
                              self.cluster_size[1])

                sub_rect = pygame.Rect(tuple_rect)
                sub_surf = ground_surf.subsurface(sub_rect)
                if not is_surface_empty(sub_surf):
                    sub_mask = pygame.mask.from_surface(sub_surf)
                    self.level_ground_surfaces[cluster_coords] = {}
                    self.level_ground_surfaces[cluster_coords]["rect"] = sub_rect
                    self.level_ground_surfaces[cluster_coords]["surf"] = sub_surf
                    self.level_ground_surfaces[cluster_coords]["mask"] = sub_mask

    def load_background(self, level_folder_name, level_dictionary):
        bg_surfaces_names = level_dictionary["background"]

        for surf_name in bg_surfaces_names:
            bg_dict = {}
            bg_surf = pygame.image.load(f"../assets/world/{level_folder_name}/{surf_name}").convert()
            bg_dict["size"] = bg_surf.get_size()
            marge_x = bg_dict["size"][0] - SCREEN_SIZE[0]
            marge_y = bg_dict["size"][1] - SCREEN_SIZE[1]
            max_travel_x = self.level_ground_surfaces["size"][0] - SCREEN_SIZE[0]
            max_travel_y = self.level_ground_surfaces["size"][1] - SCREEN_SIZE[1]
            d_max_x = self.level_ground_surfaces["size"][0] - bg_dict["size"][0]
            d_max_y = self.level_ground_surfaces["size"][1] - bg_dict["size"][1]
            x_mult = marge_x / max_travel_x
            y_mult = marge_y / max_travel_y
            print(x_mult, y_mult)
            bg_dict["x_mult"] = x_mult
            bg_dict["y_mult"] = y_mult
            bg_dict["surf"] = bg_surf

            self.level_background_surfaces.append(bg_dict)

    def blit_ground_to_surface(self, surface, camera_rect):
        visible_clusters = self.clusters_in_rect(camera_rect)
        for cluster in visible_clusters:
            if cluster in self.level_ground_surfaces:
                pos = (self.level_ground_surfaces[cluster]["rect"].topleft[0] - camera_rect[0],
                       self.level_ground_surfaces[cluster]["rect"].topleft[1] - camera_rect[1])
                surface.blit(self.level_ground_surfaces[cluster]["surf"], pos)

    def blit_background_to_surface(self, surface, camera_rect):
        for layer in range(len(self.level_background_surfaces)):
            pos = [camera_rect[0] * -self.level_background_surfaces[layer]["x_mult"],
                   camera_rect[1] * -self.level_background_surfaces[layer]["y_mult"]]

            surface.blit(self.level_background_surfaces[layer]["surf"], pos)

    def dig_ground(self, pos, radius):
        rect = pygame.Rect(pos[0]-radius, pos[1]-radius, 2*radius, 2*radius)

        for cluster in self.clusters_in_rect(rect):
            if cluster in self.level_ground_surfaces:
                ground_rect = self.level_ground_surfaces[cluster]["rect"]
                new_center = pos[0] - ground_rect.left, pos[1] - ground_rect.top
                pygame.draw.circle(self.level_ground_surfaces[cluster]["surf"], (0, 0, 0), new_center, radius)
                self.level_ground_surfaces[cluster]["mask"] = pygame.mask.from_surface(self.level_ground_surfaces[cluster]["surf"])

    def rect_in_level(self, rect):
        return self.level_rect.colliderect(rect)

    def clusters_in_rect(self, rect, layer_coefs=(1, 1)):
        clusters = []

        left_indice = rect.left // self.cluster_size[0]
        right_indice = rect.right // self.cluster_size[0]
        top_indice = rect.top // self.cluster_size[1]
        bottom_indice = rect.bottom // self.cluster_size[1]

        for i in range(left_indice, right_indice+1):
            for j in range(top_indice, bottom_indice+1):
                clusters.append((i, j))
        return clusters

    def collide_ground_point_mask(self, point):
        point_cluster_coords = point[0]//self.cluster_size[0], point[1]//self.cluster_size[1]
        local_point_coords = point[0] % self.cluster_size[0], point[1] % self.cluster_size[1]
        if point_cluster_coords in self.level_ground_surfaces:
            if self.level_ground_surfaces[point_cluster_coords]["mask"].get_at(local_point_coords):
                return True
        return False

    def collide_ground_rect_rect(self, rect):
        for tuple_rect in self.level_ground_surfaces:
            if self.level_ground_surfaces[tuple_rect]["rect"].colliderect(rect):
                return True
        return False

    def collide_ground_mask_mask(self, mask, offset):
        mask_rect = mask.get_rect()
        mask_rect.move_ip(offset[0], offset[1])

        intersecting_clusters = self.clusters_in_rect(mask_rect)

        for cluster in intersecting_clusters:
            if cluster in self.level_ground_surfaces:
                mask_relative_offset = (offset[0] - cluster[0] * self.cluster_size[0],
                                        offset[1] - cluster[1] * self.cluster_size[1])
                if pos := self.level_ground_surfaces[cluster]["mask"].overlap(mask, mask_relative_offset):
                    impact_pos = (pos[0] + cluster[0] * self.cluster_size[0],
                                  pos[1] + cluster[1] * self.cluster_size[1])
                    return impact_pos
        return False
