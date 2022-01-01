import pygame

from flipplan.engine.window import window

# from src.game.menu import menu


def main():
    marche = True
    test_rect = pygame.Rect(100, 100, 20, 20)

    while marche:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                marche = False
            if event.type == pygame.KEYDOWN:
                test_rect.width += 5

            window.fill((255, 255, 255))
            pygame.draw.rect(window,(0, 0, 0), test_rect)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
