import pygame

from src.engine.loop_handler import LoopHandler
from src.game_objects.handlers.player_handler import PlayerHandler
from src.game_objects.handlers.game_handler import GameHandler
from src.game_objects.world import World


def arena(window):
    # region arena_initialization
    loop_handler = LoopHandler()
    player_handler = PlayerHandler()
    player_handler.add_players(1)
    world = World()
    game_handler = GameHandler(world, player_handler, window)
    sound = pygame.mixer.Sound("../assets/sounds/missile/missile_launch_1.wav")
    sound.set_volume(0.1)

    # endregion

    # region arena_loop
    while loop_handler.is_running():
        print("")
        loop_handler.print_fps()
        delta = loop_handler.limit_and_get_delta()

        for event in pygame.event.get():
            player_handler.update_event(event)
            if event.type == pygame.QUIT:
                loop_handler.stop_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop_handler.stop_loop()

                elif event.key == pygame.K_RETURN:
                    for i in range(len(player_handler.players)):
                        player_handler.players[i].set_position(0, 0, False)
                        player_handler.players[i].set_speed(0, 0, False)
        if player_handler.key_state[pygame.K_o][0]:
            sound.play()

        game_handler.update_position(delta)
        game_handler.render()

        pygame.display.flip()

    return loop_handler.end_of_loop_return()
    # endregion


if __name__ == "__main__":
    from src.engine.window import window as _window
    pygame.init()
    arena(_window)
    pygame.quit()
