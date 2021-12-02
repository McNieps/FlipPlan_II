import pygame


class Camera:
    def __init__(self, e1, e2):
        self.entity_1 = e1
        self.entity_2 = e2

        self.minimal_screen_size = (600, 450)
        self.current_size = (600, 450)
        self.border_width = 40  # px
        self.interior_min_screen_size = (520, 370)
        self.interior_ratio = self.interior_min_screen_size[0]/self.interior_min_screen_size[1]

        self.rect = None

    def compute_screen_size(self):
        screen_center = (self.entity_1.x + self.entity_2.x)/2, (self.entity_1.y + self.entity_2.y)/2
        x_distance = abs(self.entity_1.x - self.entity_2.x)
        y_distance = abs(self.entity_1.y - self.entity_2.y)
        if x_distance > y_distance * self.interior_ratio:
            if x_distance < self.interior_min_screen_size[0]:
                self.rect = pygame.Rect(0, 0, self.minimal_screen_size[0], self.minimal_screen_size[1])
            else:
                pass

    def render_surface(self):
        pass
