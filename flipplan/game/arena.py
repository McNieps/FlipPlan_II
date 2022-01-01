import pygame

from flipplan.engine.handlers.loop_handler import LoopHandler
from flipplan.game_objects.handlers.arena_handler import ArenaHandler


def arena(_window, _ressource_handler, level_name="mountains"):
    loop_handler = LoopHandler(_ressource_handler.fetch_data(["system", "video", "fps"]))
    arena_handler = ArenaHandler(_window, _ressource_handler, 1, level_name)
    ifi = _ressource_handler.fetch_data(["system", "video", "ifi"])

    while loop_handler.is_running():
        # loop_handler.print_fps()
        delta = loop_handler.limit_and_get_delta()

        for event in pygame.event.get():
            arena_handler.update_event(event)
            if event.type == pygame.QUIT:
                loop_handler.stop_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop_handler.stop_loop()

        for i in range(ifi):
            arena_handler.update(delta / ifi)

        arena_handler.render()
        pygame.display.flip()

    return loop_handler.end_of_loop_return()


if __name__ == "__main__":
    from flipplan.engine.window import window, ressource_handler
    arena(window, ressource_handler)
    pygame.quit()
