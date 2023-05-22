import pygame
from pygame.sprite import Sprite


# create class to manage bullets fired from xwing
class Bullet(Sprite):
    def __init__(self, ai_game):
        # create a bullet object at the xwing's current position
        # call super to inherent from Sprite
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # create a bullet rect at (0, 0) and then set correct position
        # we have to create image rect from scratch using pygame.Rect() class
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        # match the xwing's midtop attribute, making the bullet emerge from the top of the ship.  # NOQA
        self.rect.midtop = ai_game.xwing.rect.midtop  # NOQA

        # store bullets position as a float
        self.y = float(self.rect.y)

    # When bullet is fired it moves up the screen which corresponds to a decreasing y-coordinate value.
    # To update position we subtract the amount stored in settings.bullet_speed from self.y
    # We then use the value of self.y to set the value of self.rect.y
    def update(self):
        # === move bullet up the screen === #
        # update the exact position of the bullet
        self.y -= self.settings.bullet_speed
        # update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
