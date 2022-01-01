import pygame

from flipplan.engine.handlers.loop_handler import LoopHandler

from flipplan.game.arena import arena


def menu(_window):
    loop_handler = LoopHandler()

    while loop_handler.is_running():

        # Evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_handler.stop_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop_handler.stop_loop()
                if event.key == pygame.K_RETURN:
                    # Call game
                    loop_handler = LoopHandler(arena(_window))

        # Affichage
        _window.fill((255, 255, 255))
        pygame.display.flip()

    return loop_handler.end_of_loop_return()


if __name__ == '__main__':
    from flipplan.engine.window import window

    menu(window)
    pygame.quit()
