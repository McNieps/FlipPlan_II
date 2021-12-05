import pygame
from engine.data import SCREEN_SIZE, SCREEN_NAME, SCALED  # , SCREEN_ICON_PATH

pygame.mixer.pre_init(44100, -16, 1, 512)

pygame.init()

pygame.mixer.set_num_channels(16)

if SCALED:
    window = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED)
else:
    window = pygame.display.set_mode(SCREEN_SIZE)

pygame.display.set_caption(SCREEN_NAME)

# icon = pygame.image.load(SCREEN_ICON_PATH).convert_alpha()
# pygame.display.set_icon(icon)


if __name__ == "__main__":
    marche = True
    while marche:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                marche = False

    pygame.quit()
