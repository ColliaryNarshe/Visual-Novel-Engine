import pygame
import math
# import time

from display.surfaces import Surface
from display.text_boxes import Text_Box
from configuration import dialog_settings


class Dialog_Box(Text_Box):
    def __init__(self, game, box_name):
        self.game = game
        self.WIN = game.WIN
        self.box_name = box_name

        # These used with move_dialog_up/down
        self.bottom_x = dialog_settings['bottom_x']
        self.bottom_y = dialog_settings['bottom_y']

        self.color = dialog_settings['font_color']
        self.surface = Surface(
            self.WIN, self.game,
            dialog_settings['bottom_x'], dialog_settings['bottom_y'],
            dialog_settings['width'], dialog_settings['height'],
            dialog_settings['bg_color'], dialog_settings['border_color'],
            dialog_settings['border_width'], dialog_settings['box_transparency']
        )

        # Image Surface
        if dialog_settings['image_size'] == 'auto':
            _, self.image_size = self.game._convert_percents_into_ints(None, dialog_settings['height'])
        else:
            _, self.image_size = self.game._convert_percents_into_ints(None, dialog_settings['image_size'])
        self.img_surface = Surface(self.WIN, self.game, self.surface.x, self.surface.y, self.image_size, self.image_size, 0, dialog_settings['border_color'], dialog_settings['image_border_width'], dialog_settings['box_transparency'])
        self.image_surface_on = True


        # Name tag
        self.name_tag_y = dialog_settings['name_tag_y']
        self.name_tag_x = self.surface.surface_rect.height * dialog_settings['name_tag_x_multiplier']
        self.name = None  # Name tag
        self.name_on = True  # To not draw nametag

        # Create choice menu:
        self.choice_menu_x = self.surface.surface_rect.right + dialog_settings['choice_menu_x'] + 20  # 20 is padding (hardcoded in menu add_bg below)
        self.choice_menu_y = self.surface.surface_rect.top + int(self.surface.surface_rect.height * dialog_settings['choice_menu_y']) + 20  # 20 is padding
        self.game.create_menu(self.box_name, [['temp', True]], self.choice_menu_x, self.choice_menu_y, color='white', size=dialog_settings['font_size'], spacing=5)
        self.game.menus[self.box_name].add_bg(padding=20, bg_color ='darkblue', border_color='Grey', border_width=self.surface.border_width, transparency=dialog_settings['box_transparency'])

        # Fonts for main window & name tag:
        self.change_font(dialog_settings['font_name'], dialog_settings['font_size'], self.color, dialog_settings['bold'])
        self.change_font(dialog_settings['font_name'], dialog_settings['name_tag_font_size'], self.color, True, name_tag=True)

        self.highlight_color = dialog_settings['highlight_color']
        self.typing_speed = dialog_settings['typing_speed']
        self.gradual_typing = dialog_settings['gradual_typing']

        # Spacing:
        self.x_txt_padding = dialog_settings['x_txt_padding']
        self.y_txt_padding = dialog_settings['y_txt_padding']

        # Max lines: 'auto' uses height of dialog box, text, and spacing:
        self.max_lines = dialog_settings['max_lines']
        if self.max_lines == 'auto':
            self.max_lines = int((self.surface.height - (self.y_txt_padding * 1.5)) / self.text_height)
            if not self.max_lines:
                self.max_lines = 1

        # Text wrap
        self.wrap_num = dialog_settings['txt_wrap_length']
        if self.wrap_num == 'auto':
            self.wrap_num = int((self.surface.width - (self.x_txt_padding * 2)) / self.text_width)


    def parse_quote(self, dialog: list, set_disabled):
        """Called from scene -> Game.display_dialog()
           Dialog example: ['Arjen', 0, "Dialog text"]
           With question: ['Arjen', 0, "Question?", ['Yes', 'No']]"""

        # Clear the text at the start of each dialog, not at end in case chosen to keep dialog up
        self.surface.clear_text()

        # Set the name and create nametag surface
        self.name = dialog[0]
        if not self.name:
            self.name_on = False
        else:
            self.name_on = True

        # Check if name in images, if not create name with no images:
        if self.name and not self.name in self.game.dialog_images:
            self.game.dialog_images[self.name] = ''

        self._create_nametag()

        # Made a copy to not edit original, which can be reused for repeating dialog
        dialog_copy = dialog[:]

        # If choices menu:
        if len(dialog) == 4:
            # Separate dialog from list of menu items:
            dialog_copy = dialog[:-1]

            # Make the choice menu with menu items
            self._update_dialog_choices(dialog[-1], set_disabled)

        # Check if no image or no name given in parameters
        if type(dialog_copy[1]) == int and self.name and self.game.dialog_images[self.name]:
            # Check if there's a name but no picture in dictionary, and existing index given
            try:
                # Get chosen image, resize, and add to surface:
                img = self.game.dialog_images[dialog_copy[0]][dialog_copy[1]]
                img = pygame.transform.scale(img, (self.img_surface.surface_rect.width, self.img_surface.surface_rect.height))
                self.img_surface.image = img
            except IndexError:
                self.img_surface.image = ''
                self.image_surface_on = False
                print("IndexError loading dialog character image", dialog_copy[0])

        else:
            self.img_surface.image = ''
            self.image_surface_on = False

        # Wrap text lines to proper width:
        full_text = self._format_text_wrap(dialog_copy[2])
        partial_text = ''

        # Check if text is longer than max_lines:
        display_times = int(math.ceil(len(full_text) / self.max_lines)) # Number of boxes needed

        # Create the dialog box, multiple boxes if text is long:
        for idx in range(display_times):
            partial_text = full_text[:self.max_lines]
            full_text = full_text[self.max_lines:]
            self._render_dialog_txt(partial_text)
            self.surface.triangle = True

            # Show the dialog option box only after last text box is displayed
            if idx + 1 == display_times:
                if len(dialog) == 4:
                    self.game.toggle_menu = True
                    self.game.current_menu = self.box_name
                    self.game.menus[self.box_name].bg_surface.hide_surface = False
                    self.surface.triangle = False

            # Wait for input:
            self.game.game_loop_input()
            self.game.toggle_menu = False
            self.surface.triangle = False
            # Clear the text from character's surface, but not if last one (for keeping txt on screen)
            if idx + 1 != display_times:
                self.surface.clear_text()

        self.image_surface_on = True


    def remove_dialog_box(self):
        self.game.toggle_dialog = False
        self.game.toggle_menu = False


    def _create_nametag(self):
        # Render text and rect:
        name_render = self.name_tag_font.render(self.name, 1, self.name_tag_color)
        name_render_rect = name_render.get_rect(topleft=(10, 5))
        # Create new surface based on text size:
        self.name_surface = Surface(self.WIN, self.game, self.surface.x + self.name_tag_x, self.surface.y + self.name_tag_y, name_render_rect.width + 20, name_render_rect.height + 10, self.surface.background_color, self.surface.border_color, self.surface.border_width, self.surface.transparency)
        # Add text to new surface:
        self.name_surface.display_text_list = [(name_render, name_render_rect)]


    def _update_dialog_choices(self, choices: list, set_disabled):
        """Create the surface and text for dialog choices"""

        # Convert to usable menu format (with T/F)
        choices = self._convert_choices(choices, set_disabled)

        self.game.menus[self.box_name].update_text(choices)
        self.game.menus[self.box_name].add_bg(padding=20, bg_color=self.surface.background_color, border_color='Grey', border_width=self.surface.border_width, transparency=self.surface.transparency)

        self.game.menus[self.box_name].bg_surface.hide_surface = True


    def display_dialog_box(self):
        """Called from game loop"""
        # Box:
        self.surface.display_surface()

        # Picture:
        if self.img_surface.image:
            self.img_surface.display_surface()

        # Name tag:
        if self.name_on:
            self.name_surface.display_surface()


# Functional--------------------------------------
    def config_surface(self, x=None, y=None, width=None, height=None, background_color=None, border_color=None, border_width=None, transparency=None, choice_menu_x=None, choice_menu_y=None, txt_wrap='auto', max_lines='auto', x_txt_padding=None, y_txt_padding=None, image_size='auto', image_border_width=None, name_tag=False, temp=False):
        # Change for name_tag (created with use for name size):
        if name_tag:
            if background_color: self.surface.background_color = background_color
            if border_color: self.surface.border_color = border_color
            if x != None: self.name_tag_x = x
            if y != None: self.name_tag_y = y

        else:
            # These used with move_dialog_up/down
            if not temp:
                if x != None:
                    self.bottom_x = x
                if y != None:
                    self.bottom_y = y

            # Main box:
            self.surface.configure(x, y, width, height, background_color, border_color, border_width, transparency)

            # Image surface:
            if image_size == 'auto':
                self.image_size = self.surface.height
            else:
                _, self.image_size = self.game._convert_percents_into_ints(None, image_size)

            if image_border_width != None:
                bw = image_border_width
            else:
                bw = self.img_surface.border_width

            self.img_surface.configure(x, y, self.image_size, self.image_size, 0, border_color, bw, transparency)

            # Create Menu:
            if choice_menu_x != None:
                self.choice_menu_x = self.surface.surface_rect.right + choice_menu_x + 20  # 20 is padding (hardcoded at menu creation)
            if choice_menu_y != None:
                self.choice_menu_y = self.surface.surface_rect.top + int(self.surface.surface_rect.height * choice_menu_y) + 20  # 20 is padding

            self.game.create_menu(self.box_name, [['temp', True]], self.choice_menu_x, self.choice_menu_y, color=self.color, size=self.text_size, spacing=5)
            self.game.menus[self.box_name].add_bg(padding=20, bg_color=self.surface.background_color, border_color=self.surface.border_color, border_width=self.surface.border_width, transparency=self.surface.transparency)

            # Text padding:
            if x_txt_padding != None:
                self.x_txt_padding = x_txt_padding
            if y_txt_padding != None:
                self.y_txt_padding = y_txt_padding

            # Max lines: 'auto' uses height of dialog box, text, and spacing:
            if max_lines == 'auto':
                self.max_lines = int((self.surface.height - (self.y_txt_padding * 1.5)) / self.text_height)
                if not self.max_lines:
                    self.max_lines = 1
            else:
                self.max_lines = max_lines

            # Text wrap
            if txt_wrap == 'auto':
                self.wrap_num = int((self.surface.width - (self.x_txt_padding * 2)) / self.text_width)
            else:
                self.wrap_num = txt_wrap

# Extra-------------------------------------------
    def move_dialog_up(self, x=None, y=None):
        if x == None:
            x = self.bottom_x
        if y == None:
            y = dialog_settings['top_y']

        new_x, new_y = self.game._convert_percents_into_ints(x, y)

        self.config_surface(new_x, new_y, temp=True)


    def move_dialog_down(self, x=None, y=None):
        if x == None:
            x = self.bottom_x
        if y == None:
            y = self.bottom_y

        new_x, new_y = self.game._convert_percents_into_ints(x, y)

        self.config_surface(new_x, new_y, temp=True)



#
