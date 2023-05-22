import pygame
from pygame.sprite import Sprite


class Tiefighter(Sprite):  # NOQA
    def __init__(self, ai_game):
        # initialise tiefighter and set its starting position  # noqa
        super().__init__()
        self.screen = ai_game.screen
        # access tiefighter settings  # noqa
        self.settings = ai_game.settings

        # load the tiefighter image and set its rect attribute  # noqa
        self.image = pygame.image.load('sw_images/tiefighter.png')  # noqa
        self.rect = self.image.get_rect()

        # start each new tf near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the tf exact horizontal position
        self.x = float(self.rect.x)

    # check if tiefighter hit edges of screen
    def check_edges(self):
        # return true if tiefighter is at edge of screen
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    # update function to move tiefighters  # noqa
    def update(self):
        # every time update is run, we move the tiefighter to the right using assigned speed
        self.x += self.settings.tiefighter_speed * self.settings.fleet_direction
        # then update position of rect.x
        self.rect.x = self.x
