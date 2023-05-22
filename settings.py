import pygame


# store all settings for Star wars game
class Settings:
    def __init__(self):
        # screen settings
        self.screen_width = 1500
        self.screen_height = 750

        # x-wing settings
        self.xwing_speed = 1.5  # NOQA - position adjusted to x pixels on each pass through the loop
        self.xwing_limit = 3 # NOQA

        # bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3

        # tiefighter settings  # noqa
        self.fleet_drop_speed = 30

        # how quickly the game speeds up
        self.speedup_scale = 1.1
        # how quickly point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # initialize settings that change as the game progresses
        self.xwing_speed = 1.5
        self.bullet_speed = 2.5
        self.tiefighter_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # scoring settings
        self.xwing_points = 50

    def increase_speed(self):
        # increase speed settings and xwing point values
        self.xwing_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.tiefighter_speed *= self.speedup_scale
        self.xwing_points = int(self.xwing_points * self.score_scale)





