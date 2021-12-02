import pygame
from engine.data import MAX_FPS


class LoopHandler:
    def __init__(self, stop=False):
        self.clock = pygame.time.Clock()
        self.run = not stop
        self.stop = stop
        self.max_fps = MAX_FPS
        self.delta = 1/self.max_fps

    def is_running(self):
        return self.run

    def stop_loop(self):
        self.run = False

    def stop_game(self):
        self.run = False
        self.stop = True

    def end_of_loop_return(self):
        return self.stop

    def limit_and_get_delta(self):
        self.delta = self.clock.tick(self.max_fps) / 1000
        return self.delta

    def print_fps(self):
        print(self.clock.get_fps())
