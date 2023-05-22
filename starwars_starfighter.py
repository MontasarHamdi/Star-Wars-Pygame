import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from xwing import SpaceShip
from tiefighter import Tiefighter
from bullet import Bullet
from button import Button
# PAGE 291 ROUNDING THE SCORE

# overall class to manage game assets and behaviour
class StarwarsStarFighter:  # NOQA
    # init game create game resources, background settings
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Star Wars Star Fighter")
        # start game in an inactive state
        self.game_active = False

        # create instance of clas Clock from pygame.time module -> go to run_game()
        self.clock = pygame.time.Clock()
        # import screen settings
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # create instance to store game statistics
        self.stats = GameStats(self)
        # create instance to store game statistics and create scoreboard
        self.sb = Scoreboard(self)
        # import xwing  # NOQA
        self.xwing = SpaceShip(self)  # NOQA
        # create group that holds bullets in init
        self.bullets = pygame.sprite.Group()
        # create group that holds fleet of tiefighters
        self.tiefighters = pygame.sprite.Group()  # noqa
        self._create_fleet()
        # set background image
        self.background = pygame.image.load('sw_images/starwarsbackground.jpg')  # NOQA
        # ==== FULL SCREEN MODE ==== #
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # make the play button - create at bottom as we only need one play button
        self.play_button = Button(self, "This is where the fun begins!")

    # main game loop
    def run_game(self):
        # start mainloop for game
        while True:
            # call check events method
            self._check_events()
            # if loop in case of game over
            if self.game_active:
                # call xwing update from xwing module  # NOQA
                self.xwing.update()
                # update position of bullets on each iteration of while loop and remove old bullets- call bullet.update
                self._update_bullets()
                # update position of tiefighters when moving  # noqa
                self._update_tiefighters()
            # call update screen method
            self._update_screen()
            # create clock tick - tick method takes argument (60fps) so pygame will make loop run exactly 60fps
            self.clock.tick(60)

    # helper method - simplify run_game
    def _check_events(self):
        # keyboard and mouse events - event loop for screen updates during clicks or moving mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # look to key press helper methods #
            # when right key/left is pressed down, moving right/left is set to True
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # when right/left key is released, moving right/left is set to False
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            # respond to key press to start game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    # ==== key press helper methods simplified ==== #

    # helper method for click play to only respond at the beginning of the game
    def _check_play_button(self, mouse_pos):
        # start new game when player clicks play - ensures area where box appears isn't accidentally clicked
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # reset game settings
            self.settings.initialize_dynamic_settings()
            # reset game stats
            self.stats.reset_stats()
            self.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_xwing()
            # get rid of remaining bullets and tiefighters and create new fleet and center xwing
            self.bullets.empty()
            self.tiefighters.empty()
            self._create_fleet()
            self.xwing.center_xwing()

            # hide mouse cursor when game starts
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.xwing.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.xwing.moving_left = True
        # space bar for shooting bullets
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # press q to exit game
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.xwing.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.xwing.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            # add method is like append method but specific to pygame
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # update position of bullets and get rid of old bullets
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_tiefighter_collisions()

    def _check_bullet_tiefighter_collisions(self):  # noqa
        # use sprite.groupcollide() function to compare rects of each bullet to rects of tiefighters
        # return a dict of bullet tiefighter collisions .. key: bullet, value: hit tiefighter
        # True True arguments tell pygame to delete the bullets and tiefighters when they collide
        # If you change first boolean argument to False then bullets become high powered. They dont delete after coll.
        collisions = pygame.sprite.groupcollide(self.bullets, self.tiefighters, True, True)

        # update scoreboard each time tiegfighter is shot
        if collisions:
            for tiefighters in collisions.values():
                self.stats.score += self.settings.xwing_points*len(tiefighters)
            self.sb.prep_score()
            self.sb.check_high_score()

        # check if all tiefighters are deleted. If so call create fleet function to repopulate the fleet
        if not self.tiefighters:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_tiefighters(self):  # noqa
        # update position of tiefighters after every iteration # noqa
        self._check_fleet_edges()
        self.tiefighters.update()
        self._xwing_tiefighter_collisions()
        self._check_tiefighters_bottom()

    # helper method
    def _xwing_tiefighter_collisions(self):  # noqa
        # spritecolllideany() function looks for any collisions between xwing and tiefighters.
        # it loops through and returns first tiefighter that collided with xwing.
        # if no collisions occur, function returns None
        if pygame.sprite.spritecollideany(self.xwing, self.tiefighters):
            self._xwing_hit()

    def _xwing_hit(self):  # noqa
        # if player has more than 1 ship remaining, then every hit resets the game
        # decrement xwings left
        if self.stats.xwings_left > 0:
            self.stats.xwings_left -= 1
            self.sb.prep_xwing()
            # get rid of any remaining bullets and tiefighters
            self.bullets.empty()
            self.tiefighters.empty()
            # create new fleet and centre xwing
            self._create_fleet()
            self.xwing.center_xwing()
            # pause
            sleep(0.5)
        # if remaining ships reach 0, then game active False - game over
        else:
            self.game_active = False
            # have mouse reappear again
            pygame.mouse.set_visible(True)

    # tiefighters reach bottom of screen
    def _check_tiefighters_bottom(self):  # noqa
        for tiefighter in self.tiefighters.sprites():  # noqa
            if tiefighter.rect.bottom >= self.settings.screen_height:
                self._xwing_hit()
                break

    # helper method - simplify run_game
    def _update_screen(self):
        # background image
        self.screen.blit(self.background, (0, 0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # xwing import  # NOQA
        self.xwing.blitme()
        # tiefighter import
        self.tiefighters.draw(self.screen)
        # draw the score information
        self.sb.show_score()
        # draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()
        # make most recently drawn screen visible
        pygame.display.flip()

    # function to create fleet of tiefighters
    # create one instance of Tiefighter and then adding it to a group that will hold the fleet
    def _create_fleet(self):
        tiefighter = Tiefighter(self)  # noqa
        # rect size is a tuple that contains width and height of tiefighter
        tiefighter_width, tiefighter_height = tiefighter.rect.size  # noqa

        # get width from first tiefighter created which will refer to the horizontal position of next tiefighter
        # while loop to fit as many tiefighters in screen boundary
        current_x, current_y = tiefighter_width, tiefighter_height
        while current_y < (self.settings.screen_height - 3 * tiefighter_height):
            while current_x < (self.settings.screen_width - 2 * tiefighter_width):
                # create new tiefighter
                self._create_tiefighter(current_x, current_y)
                # increment - add 2 tiefighter widths to the horizontal position to move past previous ship
                # and leave space between each ship.
                current_x += 2 * tiefighter_width
                # while loop will re-evaluate the condition at the start of the while loop and see if there is more room
            # when row is filled, reset x value and increment y value so first spaceship in next row will be placed
            # at the same position as the one above
            current_x = tiefighter_width
            current_y += 2 * tiefighter_height

    # helper method tiefighter ships
    def _create_tiefighter(self, x_position, y_position):  # noqa
        new_tiefighter = Tiefighter(self)
        new_tiefighter.x = x_position
        new_tiefighter.rect.x = x_position
        new_tiefighter.rect.y = y_position
        self.tiefighters.add(new_tiefighter)

    # check if fleet hits edge then drop down
    def _check_fleet_edges(self):
        for tiefighter in self.tiefighters.sprites():
            if tiefighter.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for tiefighter in self.tiefighters.sprites():
            tiefighter.rect.y += self.settings.fleet_drop_speed
        # once fleet has dropped, change direction to -1, left
        self.settings.fleet_direction *= -1


if __name__ == '__main__':
    # create game instance and run game.
    ai = StarwarsStarFighter()
    ai.run_game()
