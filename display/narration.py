import pygame
import math

from display.surfaces import Surface
from display.text_boxes import Text_Box
from configuration import narration_settings

class Narration_Box(Text_Box):
    # Inherits methods but no need for super()
    def __init__(self, game):
        self.game = game
        self.surface = Surface(self.game.WIN, self.game,
            narration_settings['x'], narration_settings['y'],
            narration_settings['width'], narration_settings['height'],
            narration_settings['bg_color'], narration_settings['border_color'],
            narration_settings['border_width'], narration_settings['box_transparency'])

        # Fonts:
        self.change_font(narration_settings['font_name'], narration_settings['font_size'], narration_settings['font_color'], narration_settings['bold'])

        self.highlight_color = narration_settings['highlight_color']
        self.typing_speed = narration_settings['typing_speed']
        self.gradual_typing = narration_settings['gradual_typing']

        # Spacing
        self.x_txt_padding = narration_settings['x_txt_padding']
        self.y_txt_padding = narration_settings['y_txt_padding']
        self.text_y = 0  # Location of last line to use with menu questions

        # Max lines: 'auto' uses' height of dialog box, text, and spacing:
        self.max_lines = narration_settings['max_lines']
        if self.max_lines == 'auto':
            self.max_lines = ((self.surface.height - (self.y_txt_padding * 2)) // self.text_height) - 1
            if not self.max_lines:
                self.max_lines = 1

        # Text wrap:
        self.wrap_num = narration_settings['txt_wrap_length']
        if self.wrap_num == 'auto':
            self.wrap_num = int((self.surface.width - (self.x_txt_padding * 2)) / self.text_width)

        self.image_surface_on = False  # Always False. Only used by text_boxes.py and wrap method for dialog box image. Can use later to add images to narration maybe


    def _create_narration_question(self, choices: list):
        """Create the Menu with text for narration choices"""

        # x y positions based on last line of text (self.text_y):
        x_pos = self.surface.surface_rect.x + (self.surface.surface_rect.width // 2)
        y_pos = self.surface.surface_rect.y + self.text_y + int(self.text_height * .5)

        # Create menu without a surface
        self.game.create_menu('narration', choices, x_pos, y_pos, 'white', self.text_size, 30, align='horizontal-center', bold=self.bold)


    def narration_scroll(self):
        """Called from game loop: adjust y coordinate, render, and blit to screen"""

        y_adjust = False  # True after removing top item from list, need to adjust start_y

        for idx, line in enumerate(self.scroll_text[:]):
            # Maybe first time in game_engine? to rendered list exists
            rendered_text = self.scroll_font.render(line, 1, self.scroll_color)
            text_rect = rendered_text.get_rect(midtop=(self.game.win_width//2, self.start_y + (self.scroll_txt_height * idx)))
            self.game.WIN.blit(rendered_text, text_rect)

            # If top line is above top of screen:
            if text_rect.bottom < self.y_offset:
                self.scroll_text.pop(0)
                y_adjust = True

            # If line is below bottom of screen, stop drawing lines
            if text_rect.bottom > self.end_y:
                break

        # If top line deleted, lower start_y
        if y_adjust:
            self.start_y_float += self.scroll_txt_height

        # Check input for speed scrolling
        if self.speedup_on:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_RETURN] or keys_pressed[pygame.K_SPACE]:
                self.scroll_speed = self.speed_fast
            else:
                self.scroll_speed = self.speed_slow

        pygame.event.clear()

        # Move all text up
        self.start_y_float -= self.scroll_speed # keep track of floats
        self.start_y = int(self.start_y_float)

        if not self.scroll_text:
            self.game.scrolling = False


    def display_narration_box(self):
        self.surface.display_surface()


    def parse_narration(self, text, choices=[], set_disabled=[]):
        """Called from scene. set_disabled to set which choices are disabled"""

        # Convert choices into lists with T/F:
        choices = self._convert_choices(choices, set_disabled)

        # Wrap text lines to proper width:
        if isinstance(text, str):
            full_text = [self._format_text_wrap(text)]
        else:
            full_text = []
            for page in text:
                full_text.append(self._format_text_wrap(page))

        # Clear text at start rather than end to not clear last loop in case box is kept up:
        self.surface.clear_text()

        for pg_idx, new_page in enumerate(full_text):
            # Check if number of text lines are more than max_lines:
            num_of_pages = int(math.ceil(len(new_page) / self.max_lines)) # Number of boxes needed

            partial_text = ''

            for idx in range(num_of_pages):
                partial_text = new_page[:self.max_lines]
                new_page = new_page[self.max_lines:]

                # Only add menu to last new_page:
                if idx + 1 == len(range(num_of_pages)):
                    self._render_dialog_txt(partial_text, narration_menu=choices)
                else:
                    self._render_dialog_txt(partial_text)

                # Game loop:
                self.surface.triangle = True
                self.game.game_loop_input()
                self.surface.triangle = False
                # Don't clear last one in case window kept up
                if idx + 1 == num_of_pages and pg_idx + 1 == len(full_text):
                    pass
                else:
                    self.surface.clear_text()


    def remove_narration_box(self):
        self.game.toggle_narration = False
        self.game.toggle_menu = False


    def config_surface(self, x=None, y=None, width=None, height=None, background_color=None, border_color=None, border_width=None, transparency=None, max_lines=None, txt_wrap=None, x_txt_padding=None, y_txt_padding=None):

        self.surface.configure(x, y, width, height, background_color, border_color, border_width, transparency)

        # Text padding:
        if x_txt_padding != None:
            self.x_txt_padding = x_txt_padding
        if y_txt_padding != None:
            self.y_txt_padding = y_txt_padding

        # Max lines: 'auto' uses' height of dialog box, text, and spacing:
        if narration_settings['max_lines'] == 'auto':
            self.max_lines = ((self.surface.height - (self.y_txt_padding * 2)) // self.text_height) - 1
            if not self.max_lines:
                self.max_lines = 1
        if max_lines:
            self.max_lines = max_lines
            if max_lines == 'auto':
                self.max_lines = ((self.surface.height - (self.y_txt_padding * 2)) // self.text_height) - 1
                if not self.max_lines:
                    self.max_lines = 1
            else:
                self.max_lines = max_lines

        # Text wrap
        if narration_settings['txt_wrap_length'] == 'auto':
            self.wrap_num = int((self.surface.width - (self.x_txt_padding * 2)) / self.text_width)
        if txt_wrap:
            self.wrap_num = txt_wrap
            if txt_wrap == 'auto':
                self.wrap_num = int((self.surface.width - (self.x_txt_padding * 2)) / self.text_width)
