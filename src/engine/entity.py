import pygame


class BasicEntity(pygame.sprite.Sprite):
    def __init__(self, image, position=(0, 0), vitesse=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.x = position[0]
        self.y = position[1]
        self.vx = vitesse[0]
        self.vy = vitesse[1]
        self.a = 0              # Angle
        self.va = 0             # Vitesse angulaire

        self.image = image.copy()
        self.original_image = image
        self.rect = self.set_rect()
        self.mask = self.set_mask()

    def set_rect(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        return self.rect

    def set_mask(self):
        self.mask = pygame.mask.from_surface(self.image)
        return self.mask

    def update_pos(self, delta=1):
        self.x += self.vx * delta
        self.y += self.vy * delta
        self.a += self.va * delta
        self.set_rect()

    def update_image(self):
        self.image = pygame.transform.rotate(self.original_image, self.a)
        self.set_rect()
        self.set_mask()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


if __name__ == "__main__":
    sursur = pygame.Surface((255, 255)).convert_alpha()
    x = BasicEntity(sursur)
    x.update_image()
