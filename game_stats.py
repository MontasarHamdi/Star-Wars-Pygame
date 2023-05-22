import pygame
from settings import Settings


# track statistics for star fighter game
class GameStats:
    def __init__(self, ai_game):
        # initialize statistics
        self.settings = ai_game.settings
        self.reset_stats()
        # high score should never be reset
        self.high_score = 0

    def reset_stats(self):
        # initialize statistics that can change during a game
        self.xwings_left = self.settings.xwing_limit
        self.score = 0
        self.level = 1
3
