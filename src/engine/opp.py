import pygame
from math import floor, cos, sin, radians


class OPP:
    """
    Un super objet super malin permettant donner l'illusion de 3D à partir de 8 images.
    ça signifie Objet Pas Plat.
    J'aurais pu mettre Image Pas Plate mais ça reveille des traumatismes.
    """

    def __init__(self, opp_name, scale=1):
        self.images = []
        self.angle = 0
        self.load_images(opp_name)
        self.visible = [(3, 6, 1, 0), (5, 0, 3, 2), (7, 2, 5, 4),
                        (1, 4, 7, 6)]  # Face visible dans les intervalles 0,90 90,180 180,270 et 270,360
        self.width = round(self.images[0].get_size()[0] * scale)
        self.height = round(self.images[0].get_size()[1] * scale)
        self.pdv = 0
        self.cosx = None
        self.sinx = None
        self.compute_cos_sin()

    def load_images(self, opp_name):
        self.images = []
        for i in range(8):
            self.images.append(pygame.image.load(f"../assets/{opp_name}/{i}.png"))

    def set_angle(self, angle, increment=True):
        if increment:
            self.angle += angle
        else:
            self.angle = angle
        self.angle = self.angle % 360

        self.pdv = floor(self.angle / 90)
        if self.pdv == 4:
            self.pdv = 3
        self.compute_cos_sin()

    def compute_cos_sin(self):
        rad = radians(self.angle % 90)
        self.cosx = abs(cos(rad))
        self.sinx = abs(sin(rad))

    def rescale_height(self, index, ratio):
        return pygame.transform.scale(self.images[index], (self.width, round(self.height * ratio)))

    def get_surface(self):
        surface = pygame.Surface((self.width, self.height * 2))
        surface.fill((1, 1, 1))
        surface.set_colorkey((1, 1, 1))
        surface.blit(self.rescale_height(self.visible[self.pdv][0], self.sinx),
                     (0, self.height - round(self.height * self.sinx)))
        surface.blit(self.rescale_height(self.visible[self.pdv][1], self.cosx), (0, self.height))
        surface.blit(self.rescale_height(self.visible[self.pdv][2], self.cosx),
                     (0, self.height - round(self.height * self.cosx)))
        surface.blit(self.rescale_height(self.visible[self.pdv][3], self.sinx), (0, self.height))
        return surface


if __name__ == "__main__":
    import pygame

    marche = True
    fenetre = pygame.display.set_mode((800, 600))
    opp = OPP("player", 2)
    clock = pygame.time.Clock()

    while marche:
        clock.tick(2400)
        print(clock.get_fps())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                marche = False
        tp = pygame.key.get_pressed()

        if tp[pygame.K_q]:
            opp.set_angle(0.093)
        if tp[pygame.K_d]:
            opp.set_angle(-0.092)

        fenetre.fill((255, 255, 255))
        fenetre.blit(opp.get_surface(), (20, 20))

        pygame.display.flip()
    pygame.quit()



