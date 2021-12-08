import pygame

from src.engine.data import SCREEN_SIZE


class Camera:
    def __init__(self, entities, world_border):
        self.entities = entities

        self.world_border = pygame.Rect(0, 0, 0, 0)
        self.world_border.size = world_border
        self.world_aspect = world_border[0] / world_border[1]

        self.screen_aspect_ratio = SCREEN_SIZE[0] / SCREEN_SIZE[1]
        self.screen_size = SCREEN_SIZE

        self.screen_border_thickness = 50
        sbp_width = (SCREEN_SIZE[0] - 2 * self.screen_border_thickness) / SCREEN_SIZE[0]   # screenborderpercentage
        sbp_height = (SCREEN_SIZE[1] - 2 * self.screen_border_thickness) / SCREEN_SIZE[1]  # screenborderpercentage

        msm = 1  # min screen multiplier
        self.min_rect_size = SCREEN_SIZE[0] * sbp_width * msm, SCREEN_SIZE[1] * sbp_height * msm
        self.rect_aspect_ratio = self.min_rect_size[0] / self.min_rect_size[1]

        if self.world_aspect < self.screen_aspect_ratio:
            self.max_rect_size = world_border[0]*sbp_width, (world_border[0]/self.screen_aspect_ratio)*sbp_height
        else:
            self.max_rect_size = world_border[1]*self.screen_aspect_ratio*sbp_width, world_border[1]*sbp_height

        if self.min_rect_size[0] > self.max_rect_size[0]:
            self.min_rect_size = self.max_rect_size

        self.number_of_rects = 120
        self.last_left = []
        self.last_top = []
        self.last_width = []
        self.last_height = []
        self.initialize_lists()

    def initialize_lists(self):
        x = (self.world_border.width - self.max_rect_size[0])/2
        y = (self.world_border.height - self.max_rect_size[1])/2
        for i in range(self.number_of_rects):
            self.last_left.append(x)
            self.last_top.append(y)
            self.last_width.append(self.max_rect_size[0])
            self.last_height.append(self.max_rect_size[1])

    def get_average_rect(self, rect):
        self.last_left.insert(0, rect.left)
        self.last_top.insert(0, rect.top)
        self.last_width.insert(0, rect.width)
        self.last_height.insert(0, rect.height)
        self.last_left.pop(-1)
        self.last_top.pop(-1)
        self.last_width.pop(-1)
        self.last_height.pop(-1)

        avg_left = sum(self.last_left)/self.number_of_rects
        avg_top = sum(self.last_top)/self.number_of_rects
        avg_width = sum(self.last_width)/self.number_of_rects
        avg_height = sum(self.last_height)/self.number_of_rects

        return pygame.Rect(avg_left, avg_top, avg_width, avg_height)

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
        rect_aspect_ratio = width / height
        rect = pygame.Rect(left, top, width, height)
        rect_center = rect.center

        if width > self.max_rect_size[0] or height > self.max_rect_size[1]:
            rect.size = self.max_rect_size
        elif width < self.min_rect_size[0] and height < self.min_rect_size[1]:
            rect.size = self.min_rect_size
        elif rect_aspect_ratio < self.rect_aspect_ratio:
            rect.size = height * self.rect_aspect_ratio, height
        else:
            rect.size = width, width / self.rect_aspect_ratio

        width, height = rect.size

        margin = width * 2 * self.screen_border_thickness / self.min_rect_size[0]
        rect.inflate_ip(margin, margin)

        rect.center = rect_center

        if rect.top < self.world_border.top:
            rect.top = self.world_border.top
        elif rect.bottom > self.world_border.bottom:
            rect.bottom = self.world_border.bottom
        if rect.left < self.world_border.left:
            rect.left = self.world_border.left
        elif rect.right > self.world_border.right:
            rect.right = self.world_border.right

        return self.get_average_rect(rect)
