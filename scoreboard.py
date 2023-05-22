import pygame.font
from pygame.sprite import Group
from xwing import SpaceShip


class Scoreboard:
    # class to report scoring information
    def __init__(self, ai_game):
        # initialize score keeping attributes
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font setting for scoring information
        self.text_color = (255, 255, 0)
        self.font = pygame.font.SysFont(None, 48)
        # prepare initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_xwing()

    # turn score into rendered image
    def prep_score(self):
        # format the score to include comma separators and report in multiples of 10
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color)

        # display score at the top right  of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 200
        self.score_rect.top = 20

    def show_score(self):
        # draw score to screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.xwings.draw(self.screen)

    # turn highscore into rendered image
    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        # highscore at center top of screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx  # noqa
        self.high_score_rect.top = self.score_rect.top

    # check to see if there is new highscore
    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    # turn level into rendered image
    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color)
        # position level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    # render image to show how many ships left
    def prep_xwing(self):
        self.xwings = Group()
        for xwing_number in range(self.stats.xwings_left):  # noqa
            xwing = SpaceShip(self.ai_game)
            xwing.rect.x = 10 + xwing_number * xwing.rect.width
            xwing.rect.y = 10
            self.xwings.add(xwing)

