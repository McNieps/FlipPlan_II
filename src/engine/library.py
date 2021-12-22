import pygame


def is_surface_empty(surface):
    width, height = surface.get_size()
    if colorkey := surface.get_colorkey():
        for i in range(width):
            for j in range(height):
                if surface.get_at((i, j)) != colorkey:
                    return False
    else:
        for i in range(width):
            for j in range(height):
                if surface.get_at((i, j))[3] != 255:
                    return False
    return True


def set_outline(img, epaisseur=1, couleur=(255, 255, 255)):
    # TODO Optimiser la fonction ptet?
    image = pygame.Surface((img.get_size()[0]+2*epaisseur, img.get_size()[1]+2*epaisseur))
    image.set_colorkey((0, 0, 0))
    mask = pygame.mask.from_surface(img)
    mask_surf = mask.to_surface()
    mask_surf.set_colorkey((255, 255, 255))
    surf_temp = pygame.Surface(mask_surf.get_size())
    surf_temp.fill(couleur)
    surf_temp.blit(mask_surf, (0, 0))
    surf_temp.set_colorkey((0, 0, 0))
    for i in range(epaisseur+1):
        for j in range(epaisseur+1-i):
            image.blit(surf_temp, (epaisseur+i, epaisseur+j))
            image.blit(surf_temp, (epaisseur+i, epaisseur-j))
            image.blit(surf_temp, (epaisseur-i, epaisseur+j))
            image.blit(surf_temp, (epaisseur-i, epaisseur-j))
    image.blit(img, (epaisseur, epaisseur))
    return image
