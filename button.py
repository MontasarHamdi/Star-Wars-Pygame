import pygame.font


# create button class to create a filled rectangle with a label

class Button:
    def __init__(self, ai_game, msg):
        # initialize button attributes
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # set dimensions and properties of the button
        self.width, self.height = 500, 50
        self.button_color = (60, 40, 40, 100)
        self.text_color = (255, 232, 31)
        self.font = pygame.font.SysFont(None, 48)

        # build the buttons rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # the button message needs to be prepped only once
        self._prep_msg(msg)

    # turn msg into rendered img and center text on the button
    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    # draw blank button and then draw message
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

