import pygame
from configuration import portrait_settings

class Portrait_Image:
    # Can be used to add any images to the screen, and some options for moving them.
    def __init__(self, game, name, image: str):
        self.game = game
        self.WIN = self.game.WIN
        self.name = name
        self.image = pygame.image.load(image).convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = 0
        self.y = 0
        # To the sides of screen but note all the way to edge
        self.left_in = int(self.game.win_width * .1)
        self.right_in = int(self.game.win_width * .9) - self.width
        # To place the image right above dialog
        self.dialog_height = int(self.game.win_height * .75) - self.height

        # These four used in/out animation without a pause (animated in main loop)
        self.in_left_animating = False
        self.in_right_animating = False
        self.out_left_animating = False
        self.out_right_animating = False
        self.portrait_animating = False

        self.speed = portrait_settings['animation_speed']


    def blit_image(self, x=0, y=0, dialog=None):
        """Add image to game dictionary to be blit in loop.
           Possible coordinates to use besides int are:
           'bottom' 'right' 'center' 'left' 'top'
           dialog can be: 'left' 'right' or 'center' (to put above dialog box)
           """
        self.game.portraits_to_blit[self.name] = self

        if dialog:
            self.y = self.dialog_height
            if dialog == 'left':
                self.x = self.left_in
                return
            elif dialog == 'center':
                self.x = (self.game.win_width // 2) - (self.width // 2)
                return
            elif dialog == 'right':
                self.x = self.right_in
                return

        self.x, self.y = self._convert_x_y_keywords(x, y)


    def move_in_left(self, y='default', pause=True):
        if y == 'default':
            y = self.dialog_height

        self.blit_image(-self.width - self.speed, y)

        if pause:
            while True:
                self.x += self.speed
                self.game.game_loop_input(1)

                if self.x >= self.left_in:
                    pygame.event.clear()  # Clear input made during animation
                    break

        else:
            self.in_left_animating = True


    def move_out_left(self, pause=True):
        if pause:
            while True:
                self.x -= self.speed
                self.game.game_loop_input(1)

                if self.x + self.width < 0:
                    pygame.event.clear()  # Clear input made during animation
                    break

            self.remove()

        else:
            self.out_left_animating = True


    def move_in_right(self, y='default', pause=True):
        if y == 'default':
            y = self.dialog_height

        # Put the image off screen
        self.blit_image(self.game.win_width + self.speed, y)

        if pause:
            while True:
                self.x -= self.speed
                self.game.game_loop_input(1)

                if self.x <= self.right_in:
                    pygame.event.clear()
                    break
        else:
            self.in_right_animating = True


    def move_out_right(self, pause=True):
        if pause:
            while True:
                self.x += self.speed
                self.game.game_loop_input(1)

                if self.x > self.game.win_width:
                    pygame.event.clear()
                    break

            self.remove()

        else:
            self.out_right_animating = True


    def animate(self, start: tuple, end: tuple, pause=True, speed=None):
        """
        Blit and animate an image from given position to given position.
        Possible coordinates to use besides int are:
        'bottom' 'right' 'center' 'left' 'top'
        """
        if speed:
            self.speed = speed

        if start == 'current':
            # Add to dict to blit, but don't change x,y
            self.game.portraits_to_blit[self.name] = self
        else:
            self.blit_image(start[0], start[1])

        # Calculate the distance to move:
        x_end, y_end = self._convert_x_y_keywords(end[0], end[1])
        x_distance = self.x - x_end
        y_distance = self.y - y_end

        longest = max(abs(x_distance), abs(y_distance))
        if x_distance:
                                # 770
            x_move = self.speed / (longest / x_distance)
        else: x_move = 0
        if y_distance:
            # -44  = 770      / -350      * 20
            y_move = self.speed / (longest / y_distance)
            print(y_move, longest, y_distance, self.speed, x_move)
        else: y_move = 0

        # Fix for when x_y are different lengths
        # Start: (770, 0)
        # End: (0, 350)
        # x_move, y_move: (20, -44)
        if pause:
            new_x = self.x
            new_y = self.y
            for num in range(longest // self.speed):
                new_x -= x_move
                new_y -= y_move
                self.x = int(new_x)
                self.y = int(new_y)
                self.game.game_loop_input(1)
            else:
                pygame.event.clear()
                self.x, self.y = x_end, y_end

        else:
            self.animation_count = longest // self.speed
            self.longest = longest
            self.x_end = x_end
            self.y_end = y_end
            self.x_move = x_move
            self.y_move = y_move
            self.new_x = self.x
            self.new_y = self.y
            self.portrait_animating = True


    def upscale(self, percent: int):
        """Change the image size by a percentage"""
        self.width = int(self.width + (self.width * (percent / 100)))
        self.height = int(self.height + (self.height * (percent / 100)))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


    def remove(self):
        del self.game.portraits_to_blit[self.name]


    def switch_sides(self):
        center = (self.game.win_width // 2) - (self.width // 2)

        # If image is on left, move to right:
        if self.x < center:
            while True:
                self.x += self.speed
                self.game.game_loop_input(1)
                if self.x > self.right_in:
                    pygame.event.clear()
                    break

        # If image is on right, move to left
        elif self.x > center:
            while True:
                self.x -= self.speed
                self.game.game_loop_input(1)
                if self.x < self.left_in:
                    pygame.event.clear()
                    break


    def _convert_x_y_keywords(self, x=None, y=None):
        if x != None:
            if x == 'right':
                x = self.game.win_width - self.width
            elif x == 'center':
                x = (self.game.win_width // 2) - (self.width // 2)
            elif x == 'left':
                x = 0

        if y != None:
            if y == 'bottom':
                y = self.game.win_height - self.height
            elif y == 'center':
                y = (self.game.win_height // 2) - (self.height // 2)
            elif y == 'top':
                y = 0

        if y != None and x != None:
            return x, y
        elif y != None:
            return y
        elif x != None:
            return x
