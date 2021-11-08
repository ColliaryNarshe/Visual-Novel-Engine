import pygame
from configuration import narration_settings
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
                for num, line in enumerate(text):
                    rendering = ''  # The characters of incomplete line to render
                    y = self.y_txt_padding + (self.text_height * num)  # new lines
                    color, line = self._check_color_change(line)

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
                            text_rect = rendered_text.get_rect(topleft=(self.x_txt_padding, y))

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
            y = self.y_txt_padding + (self.text_height * num)  # new lines

            color, line = self._check_color_change(line)

            rendered_text = self.font.render(line, 1, color)
            if self.image_surface_on:
                text_rect = rendered_text.get_rect(topleft=(self.x_txt_padding + self.surface.surface_rect.height, y))
            else:  # If dialog box has no image:
                text_rect = rendered_text.get_rect(topleft=(self.x_txt_padding, y))

            self.surface.display_text_list.append((rendered_text, text_rect))

        return text_rect


    def _format_text_wrap(self, text) -> list:
        """Shorten length of line to wrap length"""

        # Calculate wrap by using width of text and box:
        if self.image_surface_on:  # For Dialog Box with character image
            wrap_num = self.wrap_num - int(self.img_surface.width / self.text_width)
        else:
            wrap_num = self.wrap_num

        # Prepare indent for Narration surface:
        if self.game.toggle_narration:
            ind = ' ' * narration_settings['txt_indentation']
        else:
            ind = ''

        # First split along any newlines (paragraphs)
        split_text = text.splitlines()

        wrapped_text = []  # List of lines
        new_color = None  # Escape character color

        for paragraph in split_text:

            # This allows multiple newlines, otherwise textwrap will remove it
            if not paragraph:
                paragraph = " "

            # Check for color marker at start of string:
            for color in pygame.color.THECOLORS.keys():
                if paragraph.startswith('<') and paragraph.lower().startswith(f'<{color}>'):
                    new_color = color
                    color_len = len(color) + 2

            if new_color:
                colored = textwrap.wrap(paragraph[color_len:], wrap_num, drop_whitespace=True, initial_indent=ind)
                for paragraph in colored:
                    wrapped_text.append(f'<{new_color}>' + paragraph)
                new_color = None

            else:
                wrapped_text += textwrap.wrap(paragraph, wrap_num, drop_whitespace=True, initial_indent=ind)

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
        """Used for color specification within text ('<Red>')"""

        color = None

        for color_name in pygame.color.THECOLORS.keys():
            if line.startswith('<') and line.lower().startswith(f'<{color_name}>'):
                color = color_name
                num = len(color) + 2
                line = line[num:]


        if not color:
            color = self.color

        return color, line


    def change_font(self, font_name=None, text_size=None, color=None, name_tag=False):
        """Renders new font to reset height and width"""

        # Check if arguments given, and create the variables
        if not name_tag:
            if font_name: self.font_name = font_name
            if text_size: self.text_size = text_size
            if color: self.color = color

            self.font = pygame.font.SysFont(self.font_name, self.text_size, 0)

        # Check name tag data
        else:
            if font_name: self.name_tag_font_name = font_name
            if text_size: self.name_tag_size = text_size
            if color: self.name_tag_color = color

            self.name_tag_font = pygame.font.SysFont(font_name, text_size, 1)

        # Get height of text and sample width for auto-wrap (don't change text example)
        any_text = self.font.render("see how it works. The text runs on then continues in a new dialog", 1, "White")
        self.text_height = any_text.get_height()
        self.text_width = any_text.get_width() / 65
