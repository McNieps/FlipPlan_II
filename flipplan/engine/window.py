import pygame
from .data import game_dict


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.set_num_channels(game_dict["audio"]["number_of_channels"])

if game_dict["window"]["scaled"]:
    window = pygame.display.set_mode(game_dict["window"]["size"], pygame.SCALED)
else:
    window = pygame.display.set_mode(game_dict["window"]["size"])

pygame.display.set_caption(game_dict["window"]["name"])

if game_dict["window"]["icon"]:
    icon = pygame.image.load("../assets/images/icon.png").convert()
    pygame.display.set_icon(icon)


if __name__ == "__main__":
    marche = True
    while marche:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                marche = False

    pygame.quit()
