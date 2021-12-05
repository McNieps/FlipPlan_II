import pygame

from src.engine.data import SCREEN_SIZE


class Camera:
    def __init__(self, entities, world_border=(2400, 1350)):
        self.entities = entities

        self.world_border = pygame.Rect(0, 0, 0, 0)
        self.world_border.size = world_border

        self.aspect_ratio = SCREEN_SIZE[0]/SCREEN_SIZE[1]

        if self.world_border.width/self.aspect_ratio < self.world_border.height:
            self.max_screen_size = (self.world_border.width, self.world_border.width/self.aspect_ratio)
        else:
            self.max_screen_size = (self.world_border.height * self.aspect_ratio, self.world_border.height)

        self.border_width = 80  # px / 2
        self.interior_min_screen_size = SCREEN_SIZE[0]-self.border_width, SCREEN_SIZE[1]-self.border_width
        self.interior_aspect_ratio = self.interior_min_screen_size[0] / self.interior_min_screen_size[1]
        interior_max_width = SCREEN_SIZE[0]/(1+self.border_width/self.interior_min_screen_size[0])
        interior_max_height = interior_max_width / self.interior_aspect_ratio
        print(interior_max_width, interior_max_height)

    def compute_screen_size(self):
        left, right = self.entities[0].rect.left, self.entities[0].rect.right
        top, bottom = self.entities[0].rect.top, self.entities[0].rect.bottom

        for i in range(1, len(self.entities)):
            if self.entities[i].rect.left < left:
                left = self.entities[i].rect.left
            if self.entities[i].rect.right > right:
                right = self.entities[i].rect.right
            if self.entities[i].rect.top < top:
                top = self.entities[i].rect.top
            if self.entities[i].rect.bottom > bottom:
                bottom = self.entities[i].rect.bottom

        width = right - left
        height = bottom - top
        aspect = width/height
        temprect = pygame.Rect(left, top, width, height)

        if aspect < self.interior_aspect_ratio:
            new_width = self.interior_aspect_ratio * height
            if new_width < self.interior_min_screen_size[0]:
                dx, dy = self.interior_min_screen_size[0]-width, self.interior_min_screen_size[1]-height
            else:
                dx, dy = new_width-width, 0
        else:
            new_height = width / self.interior_aspect_ratio
            if new_height < self.interior_min_screen_size[1]:
                dx, dy = self.interior_min_screen_size[0]-width, self.interior_min_screen_size[1]-height
            else:
                dx, dy = 0, new_height-height
        temprect.inflate_ip(dx, dy)

        margin = temprect.width*self.border_width/self.interior_min_screen_size[0]
        temprect.inflate_ip(margin, margin)

        if temprect.left < self.world_border.left:
            dx = self.world_border.left-temprect.left
            temprect.move_ip(dx, 0)
        elif temprect.right > self.world_border.right:
            dx = self.world_border.right-temprect.right
            temprect.move_ip(dx, 0)
        if temprect.top < self.world_border.top:
            dy = self.world_border.top-temprect.top
            temprect.move_ip(0, dy)
        elif temprect.bottom > self.world_border.bottom:
            dy = self.world_border.bottom-temprect.bottom
            temprect.move_ip(0, dy)

        return temprect
