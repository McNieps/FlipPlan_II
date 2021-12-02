import pygame

from src.engine.loop_handler import LoopHandler
from src.game_objects.player_handler import PlayerHandler


def arena(window):
    # region arena_initialization
    loop_handler = LoopHandler()
    player_handler = PlayerHandler()
    player_handler.add_players(2)
    # endregion

    # region arena_loop
    while loop_handler.is_running():
        # loop_handler.print_fps()
        delta = loop_handler.limit_and_get_delta()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_handler.stop_game()

            if event.type == pygame.KEYDOWN:
                player_handler.update_keydown(event.key)

                if event.key == pygame.K_ESCAPE:
                    loop_handler.stop_loop()

                elif event.key == pygame.K_RETURN:
                    player_handler.players[0].set_position(0, 0, False)
                    player_handler.players[0].set_speed(0, 0, False)
                    player_handler.players[0].set_directional_speed(0, False)

            if event.type == pygame.KEYUP:
                player_handler.update_keyup(event.key)

        player_handler.handle_input(delta)
        player_handler.handle_movements(delta)
        player_handler.players[0].update_surface_and_hitbox()

        window.fill((180, 130, 25))
        window.blit(player_handler.players[0].image, player_handler.players[0].rect)

        player_handler.reset_keys()
        pygame.display.flip()

    return loop_handler.end_of_loop_return()
    # endregion


if __name__ == "__main__":
    from src.engine.window import window as _window
    arena(_window)
    pygame.quit()
