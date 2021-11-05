import pygame
from configuration import pygame_colors
import textwrap

class Text_Box:
    """Some functions to be shared between Dialog and narration boxes"""

    def _render_dialog_txt(self, text:list, narration_menu=[]):
        """Add text to self.text one char at a time and display to screen.
           Loops here until text is finished being displayed."""

        # Write Text:
        if self.gradual_typing:
            typing = True
            while typing:
                # To make sure screen is loaded already, some kind of lag before writing characters one at a time.
                self.game.game_loop_input(2, tick=False)

                for num, line in enumerate(text):
                    rendering = ''  # The characters of incomplete line to render
                    y = self.y_txt_padding + (self.text_height * num)  # new lines

                    color, line = self._check_color_change(line)
                    line = line.strip()

                    for char in line:
                        pygame.time.delay(self.typing_speed)

                        # If pressing enter during typing, display entire text at once
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    text_rect = self._display_without_typing(text)
                                    typing = False

                            elif event.type == pygame.MOUSEBUTTONUP:
                                text_rect = self._display_without_typing(text)
                                typing = False

                        if not typing:
                            break

                        pygame.event.clear()  # stackoverflow: This is very important if your event queue is not handled properly elsewhere. Alternativly pygame.event.pump() would work.

                        # Prepare the partial text to blit with rect:
                        rendering = rendering + char
                        rendered_text = self.font.render(rendering, 1, color)
                        if self.image_surface_on:
                            text_rect = rendered_text.get_rect(topleft=(self.x_txt_padding + self.surface.surface_rect.height, y))
                        else:  # If dialog box has no image:
                            text_rect = rendered_text.get_rect(topleft=(self.x_txt_padding, y + 10))

                        # Add the text to surface
                        self.surface.display_text_list.append((rendered_text, text_rect))

                        self.game.game_loop_input(1, tick=False)

                        self.surface.display_text_list.pop() # Remove incomplete text line

                    # With completed line, add to be rendered and short pause before next line
                    else:
                        self.surface.display_text_list.append((rendered_text, text_rect))
                        delay = self.typing_speed + 70
                        pygame.time.delay(delay)

                typing = False

        # Display text without typing (entire surface at once)
        else:
            text_rect = self._display_without_typing(text)

        # Need to create narration choice surface here to get last text y coordinate
        if narration_menu:
            self.game.toggle_menu = True
            self.text_y = text_rect.bottom
            self._create_narration_question(narration_menu)
            self.game.current_menu = 'narration'


    def _display_without_typing(self, text):
        """Displays text in box all at once"""
        for num, line in enumerate(text):
            line = line.strip()
            y = self.y_txt_padding + (self.text_height * num)  # new lines

            color, line = self._check_color_change(line)

            rendered_text = self.font.render(line, 1, color)
            if self.image_surface_on:
                text_rect = rendered_text.get_rect(topleft=(self.x_txt_padding + self.surface.surface_rect.height, y))
            else:  # If dialog box has no image:
                text_rect = rendered_text.get_rect(topleft=(self.x_txt_padding, y + 10))

            self.surface.display_text_list.append((rendered_text, text_rect))

        return text_rect


    def _format_text_wrap(self, text) -> list:
        """Shorten length of line to wrap length"""

        # Calculate wrap by using width of text and box:
        if self.image_surface_on:  # For Dialog Box with character image
            wrap_num = int((self.surface.width - self.img_surface.width - (self.x_txt_padding * 2)) / self.text_width)
        else:
            wrap_num = int((self.surface.width - (self.x_txt_padding * 2)) / self.text_width)

        # Prepare indent for Narration surface:
        if self.game.toggle_narration:
            ind = "     "
        else:
            ind = ''

        # First split along any \n
        split_text = []
        split_text += text.splitlines()

        wrapped_text = []
        new_color = ''
        # Split by width:
        for line in split_text:

            # This allows multiple newlines, otherwise textwrap will remove it
            if not line:
                line = " "

            # Check for color marker at start of string:
            for name in pygame_colors:
                if line.lower().startswith(name+':'):
                    new_color = name
                    color_len = len(name) + 1

            if new_color:
                colored = textwrap.wrap(line[color_len:], wrap_num, drop_whitespace=True, initial_indent=ind)
                for line in colored:
                    wrapped_text.append(new_color+':' + line.strip())

            else:
                wrapped_text += textwrap.wrap(line, wrap_num, drop_whitespace=False, initial_indent=ind)

        return wrapped_text


    def _convert_choices(self, choices, set_disabled):
        """If given a list of ["one", "two"]
           Converts into: [["one", True], ["two", True]]
           which can be used by Menu class"""

        if choices:
            if not isinstance(choices[-1], list):
                new_list = []
                if not set_disabled:
                    for choice in choices:
                        new_list.append([choice, 'True'])
                else:
                    for choice, disabled in zip(choices, set_disabled):
                        new_list.append([choice, disabled])

                return new_list

            else:
                return choices


    def _check_color_change(self, line):
        """Used for color specification within text ('RED:')"""

        color = None

        for name in pygame_colors:
            if line.lower().startswith(name+':'):
                color = name
                num = len(name) + 1
                line = line[num:]

        if not color:
            color = self.color

        return color, line


    def change_font(self, font_name=None, text_size=None, color=None, name_tag=False):
        """Renders new font to reset height and width"""
        # Check if arguments given, and create the variables
        if not name_tag:
            if not font_name:
                font_name = self.font_name
            else:
                self.font_name = font_name

            if not text_size:
                text_size = self.text_size
            else:
                self.text_size = text_size

            if not color:
                color = self.color
            else:
                self.color = color


            self.font = pygame.font.SysFont(font_name, text_size, 0)

        # Check name tag data
        else:
            if not font_name:
                font_name = self.name_tag_font_name
            else:
                self.name_tag_font_name = font_name

            if not text_size:
                text_size = self.name_tag_size
            else:
                self.name_tag_size = text_size

            if not color:
                color = self.name_tag_color
            else:
                self.name_tag_color = color

            self.name_tag_font = pygame.font.SysFont(font_name, text_size, 1)

        # Get height of text and sample width for auto-wrap (don't change text example)
        any_text = self.font.render("see how it works. The text runs on then continues in a new dialog", 1, "White")
        self.text_height = any_text.get_height()
        self.text_width = any_text.get_width() / 65
