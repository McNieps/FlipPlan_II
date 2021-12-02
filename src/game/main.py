import pygame

from src.engine.window import window

from src.game.menu import menu


def main():
    menu(window)
    pygame.quit()


if __name__ == "__main__":
    main()
