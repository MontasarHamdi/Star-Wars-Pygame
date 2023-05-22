import pygame
from pygame.sprite import Sprite


class SpaceShip(Sprite):
    def __init__(self, ai_game):
        # init ship and set its starting position
        # first add sprite to class spaceship so spaceship can inherit from sprite and create a group of ships
        # call super at the beginning
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # load ship image and get its rect
        self.image = pygame.image.load('sw_images/nw-xwing.png')  # NOQA
        self.rect = self.image.get_rect()

        # start each new xwing at bottom centre of screen
        self.rect.midbottom = self.screen_rect.midbottom  # NOQA

        # store a float for the xwing's exact horizontal position
        self.x = float(self.rect.x)

        # movement flag; start with a ship that is not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # update the xwing x value, not rect
        # ==== X-WING WITHIN BOUNDS ==== #
        # check position of xwing. self.rect.right returns the x coord of right edge of the xwing's rect.
        # if this value is less than the value returned by self.screen_rect.right, the ship hasn't reached edge.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.xwing_speed
        # if self.rect.left is greater than 0 then ship hasn't reached right edge of screen.
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.xwing_speed
        # update rect object from self.x
        self.rect.x = self.x


    def blitme(self):  # NOQA
        # draw ship at current location
        self.screen.blit(self.image, self.rect)

    def center_xwing(self):  # noqa
        self.rect.midbottom = self.screen_rect.midbottom  # noqa
        self.x = float(self.rect.x)
