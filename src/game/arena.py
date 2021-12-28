import pygame

from src.engine.loop_handler import LoopHandler
from src.engine.data import IFI
from src.game_objects.handlers.game_handler import GameHandler


def arena(window, level_name="mountains"):
    loop_handler = LoopHandler()
    game_handler = GameHandler(window, 1, level_name)

    while loop_handler.is_running():
        # loop_handler.print_fps()
        delta = loop_handler.limit_and_get_delta()

        for event in pygame.event.get():
            game_handler.update_event(event)
            if event.type == pygame.QUIT:
                loop_handler.stop_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop_handler.stop_loop()

        for i in range(IFI):
            game_handler.update(delta/IFI)

        game_handler.render()
        pygame.display.flip()

    return loop_handler.end_of_loop_return()


if __name__ == "__main__":
    from src.engine.window import window as _window
    pygame.init()
    arena(_window)
    pygame.quit()
