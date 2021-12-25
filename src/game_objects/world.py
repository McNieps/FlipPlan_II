import pygame
from json import load as json_load

from src.engine.library import is_surface_empty


class World:
    def __init__(self, level_folder_name="isles"):
        file = open(f"../assets/world/{level_folder_name}/world_data.json", "r")
        level_dictionary = json_load(file)
        file.close()

        self.level_name = level_dictionary["level_name"]
        self.level_size = level_dictionary["level_size"]
        self.level_bg_color = level_dictionary["bg_color"]

        self.cluster_size = (50, 50)      # TODO ajouter une config pour regler ça
        self.level_ground_surfaces = {}
        self.level_ground_rects = {}
        self.level_ground_masks = {}
        self.level_rect = pygame.Rect(0, 0, self.level_size[0], self.level_size[1])

        # self.load_surfaces_rects_masks_old(level_dictionary, level_folder_name)
        self.load_surfaces_rects_masks(level_folder_name)

    def load_surfaces_rects_masks(self, level_folder_name):
        ground_surf = pygame.image.load(f"../assets/world/{level_folder_name}/ground.png").convert()
        ground_width, ground_height = ground_surf.get_size()
        width_cluster_number = ground_width // self.cluster_size[0]
        height_cluster_number = ground_height // self.cluster_size[1]
        remainings = ground_width % self.cluster_size[0] + ground_height % self.cluster_size[1]
        if remainings:
            raise Exception("Level size and cluster size do not match")

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
                    self.level_ground_rects[cluster_coords] = sub_rect
                    self.level_ground_surfaces[cluster_coords] = sub_surf
                    self.level_ground_masks[cluster_coords] = sub_mask

    def old_blit_ground_to_surface(self, surface, camera_rect):
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

    def blit_ground_to_surface(self, surface, camera_rect):
        visible_clusters = self.clusters_in_rect(camera_rect)
        for cluster in visible_clusters:
            pos = (self.level_ground_rects[cluster].topleft[0] - camera_rect[0],
                   self.level_ground_rects[cluster].topleft[1] - camera_rect[1])

            surface.blit(self.level_ground_surfaces[cluster], pos)

    def dig_ground(self, pos, radius):
        rect = pygame.Rect(pos[0]-radius, pos[1]-radius, 2*radius, 2*radius)

        for tuple_rect in self.level_ground_rects:
            if self.level_ground_rects[tuple_rect].colliderect(rect):
                ground_rect = self.level_ground_rects[tuple_rect]
                new_center = pos[0] - ground_rect.left, pos[1] - ground_rect.top
                pygame.draw.circle(self.level_ground_surfaces[tuple_rect], (0, 0, 0), new_center, radius)
                self.level_ground_masks[tuple_rect] = pygame.mask.from_surface(self.level_ground_surfaces[tuple_rect])

    def rect_in_level(self, rect):
        return self.level_rect.colliderect(rect)

    def clusters_in_rect(self, rect):
        clusters = []
        left_indice = rect.left // self.cluster_size[0]
        right_indice = rect.right // self.cluster_size[0]
        top_indice = rect.top // self.cluster_size[1]
        bottom_indice = rect.bottom // self.cluster_size[1]
        for i in range(left_indice, right_indice+1):
            for j in range(top_indice, bottom_indice+1):
                if (i, j) in self.level_ground_rects:       # Si le cluster existe
                    clusters.append((i, j))
        return clusters

    def collide_ground_point_mask(self, point):
        point_cluster_coords = point[0]//self.cluster_size[0], point[1]//self.cluster_size[1]
        local_point_coords = point[0] % self.cluster_size[0], point[1] % self.cluster_size[1]
        if point_cluster_coords in self.level_ground_masks:
            if self.level_ground_masks[point_cluster_coords].get_at(local_point_coords):
                return True
        return False

    def collide_ground_rect_rect(self, rect):
        print("TESTESTETS")
        for tuple_rect in self.level_ground_rects:
            if self.level_ground_rects[tuple_rect].colliderect(rect):
                return True
        return False

    def collide_ground_mask_mask(self, mask, offset):
        mask_rect = mask.get_rect()
        mask_rect.move_ip(offset[0], offset[1])

        intersecting_clusters = self.clusters_in_rect(mask_rect)

        for cluster in intersecting_clusters:
            if cluster in self.level_ground_masks:
                mask_relative_offset = (offset[0] - cluster[0] * self.cluster_size[0],
                                        offset[1] - cluster[1] * self.cluster_size[1])
                if pos := self.level_ground_masks[cluster].overlap(mask, mask_relative_offset):
                    impact_pos = (pos[0] + cluster[0] * self.cluster_size[0],
                                  pos[1] + cluster[1] * self.cluster_size[1])
                    return impact_pos
        return False
