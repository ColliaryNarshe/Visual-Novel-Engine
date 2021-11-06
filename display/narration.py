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
        self.change_font(narration_settings['font_name'], narration_settings['font_size'], narration_settings['font_color'])

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
        self.game.create_menu('narration', choices, x_pos, y_pos, 'white', self.text_size, 30, align='horizontal-center')


    def display_narration_box(self):
        self.surface.display_surface()


    def parse_narration(self, text, choices=[], set_disabled=[]):
        """Called from scene. set_disabled to set which choices are disabled"""

        # Convert choices into lists with T/F:
        choices = self._convert_choices(choices, set_disabled)

        # Wrap text lines to proper width:
        full_text = self._format_text_wrap(text)

        # Clear text at start rather than end to not clear last loop in case box is kept up:
        self.surface.clear_text()

        # Check if number of text lines are more than max_lines:
        display_times = int(math.ceil(len(full_text) / self.max_lines)) # Number of boxes needed

        partial_text = ''

        for idx in range(display_times):
            partial_text = full_text[:self.max_lines]
            full_text = full_text[self.max_lines:]

            # Only add menu to last full_text:
            if idx + 1 == len(range(display_times)):
                self._render_dialog_txt(partial_text, narration_menu=choices)
            else:
                self._render_dialog_txt(partial_text)

            # Game loop:
            self.surface.triangle = True
            self.game.game_loop_input()
            self.surface.triangle = False
            # Don't clear last one in case window kept up
            if idx + 1 != display_times:
                self.surface.clear_text()


    def remove_narration_box(self):
        self.game.toggle_narration = False
        self.game.toggle_menu = False


    def config_surface(self, x=None, y=None, width=None, height=None, background_color=None, border_color=None, border_width=None, transparency=None, max_lines=None, txt_wrap=None):
        self.surface.configure(x, y, width, height, background_color, border_color, border_width, transparency)

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
