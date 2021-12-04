import pygame

from src.engine.data import SCREEN_SIZE


class Camera:
    def __init__(self, entities):
        self.entities = entities

        self.minimal_screen_size = SCREEN_SIZE
        self.border_width = 80  # px / 2
        self.interior_min_screen_size = SCREEN_SIZE[0]-self.border_width, SCREEN_SIZE[1]-self.border_width
        self.interior_aspect_ratio = self.interior_min_screen_size[0] / self.interior_min_screen_size[1]

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
        return temprect
