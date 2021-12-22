import pygame

from src.engine.loop_handler import LoopHandler
from src.game_objects.handlers.game_handler import GameHandler


def arena(window):
    # region arena_initialization
    loop_handler = LoopHandler()
    game_handler = GameHandler(window, 1, "mountains")
    player_handler = game_handler.player_handler

    # endregion

    # region arena_loop
    while loop_handler.is_running():
        # print("")
        loop_handler.print_fps()
        delta = loop_handler.limit_and_get_delta()

        for event in pygame.event.get():
            game_handler.update_event(event)
            if event.type == pygame.QUIT:
                loop_handler.stop_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop_handler.stop_loop()

                elif event.key == pygame.K_RETURN:
                    for i in range(len(game_handler.player_handler.players)):
                        game_handler.player_handler.players[i].set_position(0, 0, False)
                        game_handler.player_handler.players[i].set_speed(0, 0, False)

        for i in range(10):
            game_handler.update(delta/10)

        game_handler.render()

        pygame.display.flip()

    return loop_handler.end_of_loop_return()
    # endregion


if __name__ == "__main__":
    from src.engine.window import window as _window
    pygame.init()
    arena(_window)
    pygame.quit()
