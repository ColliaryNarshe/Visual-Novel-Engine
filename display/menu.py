import pygame
from display.surfaces import Surface
from game.input_check import menu_move_down

class Menu:
    def __init__(self, game, name, items: list, x, y, color="Black", font_size=40, spacing=10, align='left', bold=0, font='georgia'):
        self.game = game
        self.bg_surface = None
        self.items = items  # [["One", True], ["Two", True]]
        self.items_rendered = []
        self.name = name
        self.align = align
        self.spacing = spacing
        self.font = pygame.font.SysFont(font, font_size, bold)
        self.color = color
        self.highlight_color = 'Red'
        self.disabled_color = 'Grey'
        # Padding around text when creating surface
        self.pad_left, self.pad_top, self.pad_right, self.pad_bottom = 0,0,0,0
        self.speed = 35  # To move in from off screen

        any_text = self.font.render("Anything", 1, "White")
        self.font_space = any_text.get_height() + self.spacing

        self.x, self.y = self.game._convert_percents_into_ints(x, y)

        self._create_menu()


    def update_text(self, items):
        self.items = items
        self._create_menu()


    def _create_menu(self):
        self.total_width, self.total_height, self.longest_idx = self._get_text_dimensions()

        # Run through list of menu items, and create fonts/rects:
        self.items_rendered = []
        added_width = 0
        for idx, item in enumerate(self.items):
            # Text:
            text = self.font.render(item[0], 1, self.color)
            text_highlight = self.font.render(item[0], 1, self.highlight_color)
            text_disabled = self.font.render(item[0], 1, self.disabled_color)

            if self.align == 'center':
                text_rect = text.get_rect(midtop=(self.x, self.y + (self.font_space * idx)))

            elif self.align == 'right':
                text_rect = text.get_rect(topright=(self.x, self.y + (self.font_space * idx)))

            elif self.align == 'horizontal':
                text_rect = text.get_rect(topleft=(self.x + added_width, self.y))

            elif self.align == 'horizontal-center':
                text_rect = text.get_rect(topleft=(self.x - (self.total_width // 2) + added_width, self.y))

            else: # align=left
                text_rect = text.get_rect(topleft=(self.x, self.y + (self.font_space * idx)))
            # Add the current width to total width
            added_width += (text.get_width() + self.spacing)

            # Used for screen shaking to return to original pos
            x_original = text_rect.x

            self.items_rendered.append([text, text_highlight, text_disabled, text_rect, x_original])


    def _draw_text(self):
        if self.items_rendered:
            for idx, (text, highlight, disabled, rect, x_original) in enumerate(self.items_rendered):
                # If screen shaking, add x_offset
                if self.game.screen_shaking:
                    rect.x = x_original + self.game.x_offset
                else:
                    rect.x = x_original

                if self.items[idx][1]:
                    if idx == self.game.menu_cursor_loc:
                        self.game.WIN.blit(highlight, rect)
                    else:
                        self.game.WIN.blit(text, rect)
                else:
                    # Disabled text and adjust cursor
                    self.game.WIN.blit(disabled, rect)
                    if idx == self.game.menu_cursor_loc:
                        menu_move_down(self.game)


    def disable_enable_menu_item(self, idx):
        self.items[idx][1] = not self.items[idx][1]


    def show_menu(self, remove=True, default=0):
        """Used for sole menu (like title screen) not dialog/narration
           This is used to call from outside (scenes->game->show_menu) to start flag & gameloop
           Can't call display_menu() directly because game_loop_input loops into itself."""

        self.game.toggle_menu = True
        self.game.menu_cursor_loc = default
        self.game.current_menu = self.name
        self.display_menu()
        self.game.game_loop_input()

        if remove:
            self.remove_menu()


    def remove_menu(self):
        self.game.toggle_menu = False
        self.game.current_menu = None
        # To use instead of automatically in input.


    def display_menu(self):
        """Used in mainloop"""
        # display the dialog choice box, but only at end of typing:
        if not self.game.menus[self.game.dialog_box.box_name].bg_surface.hide_surface and self.game.current_menu == self.game.dialog_box.box_name:
            if self.bg_surface:
                self.bg_surface.display_surface()

            self._draw_text()

        # Display Menu (or narration once it's done)
        if self.game.current_menu != self.game.dialog_box.box_name:
            if self.bg_surface:
                self.bg_surface.display_surface()

            self._draw_text()


    def move_in_left(self, remove=True, default=0):
        self.game.toggle_menu = True
        self.game.menu_cursor_loc = default
        self.game.current_menu = self.name

        # Save original position
        x_original = self.x
        if self.bg_surface:
            x_surface_original = self.bg_surface.x

        # Put text off screen, adjusting for alignment: (surface and text blit from different parts of rect [left right etc]):
        if self.align == 'right':
            self.x = 0 - self.pad_right - self.speed
            if self.bg_surface:
                self.bg_surface.x = -self.bg_surface.width - self.speed

        if self.align == 'center' or self.align == 'horizontal-center':
            self.x = -self.total_width // 2 - self.pad_right - self.speed
            if self.bg_surface:
                self.bg_surface.x = -self.bg_surface.width - self.speed

        else: # align='left' or 'horizontal'
            self.x = -self.total_width - self.pad_right - self.speed
            if self.bg_surface:
                self.bg_surface.x = -self.bg_surface.width - self.speed

        while True:
            # Increase text coordinates
            self.x += self.speed
            self._create_menu() # Render the rects and add to list

            if self.bg_surface:
                # Increase bg_surface coordinates
                self.bg_surface.x += self.speed
                self.bg_surface.reset_location()

            if self.x >= x_original:
                self.x = x_original
                self._create_menu()

                if self.bg_surface:
                    self.bg_surface.x = x_surface_original
                    self.bg_surface.reset_location()

                pygame.event.clear()  # In case of input during animation, clear events
                self.game.game_loop_input()
                if remove:
                    self.remove_menu()
                break

            self.game.game_loop_input(1)


    def move_in_right(self, remove=True, default=0):
        self.game.toggle_menu = True
        self.game.menu_cursor_loc = default
        self.game.current_menu = self.name

        # Save original position
        x_original = self.x
        if self.bg_surface:
            x_surface_original = self.bg_surface.x

        # Put text off screen, adjusting for alignment (surface and text blit from different parts of rect [left right etc]):
        if self.align == 'right':
            self.x = self.game.win_width + self.total_width + self.pad_left + self.speed
            if self.bg_surface:
                self.bg_surface.x = self.game.win_width + self.speed

        elif self.align == 'center' or self.align == 'horizontal-center':
            self.x = self.game.win_width + self.total_width // 2 + self.pad_left + self.speed
            if self.bg_surface:
                self.bg_surface.x = self.game.win_width + self.speed

        else: # align='left' or 'horizontal'
            self.x = self.game.win_width + self.pad_left + self.speed
            if self.bg_surface:
                self.bg_surface.x = self.game.win_width + self.speed


        while True:
            # Increase text coordinates
            self.x -= self.speed
            self._create_menu() # Render the rects and add to list

            if self.bg_surface:
                # Increase bg_surface coordinates
                self.bg_surface.x -= self.speed
                self.bg_surface.reset_location()

            if self.x <= x_original:
                self.x = x_original
                self._create_menu()

                if self.bg_surface:
                    self.bg_surface.x = x_surface_original
                    self.bg_surface.reset_location()

                self.game.game_loop_input()
                if remove:
                    self.remove_menu()
                break

            self.game.game_loop_input(1)


    def add_bg(self, padding=20, bg_color='white', border_color='Grey', border_width=0, transparent=0):
        """Add a colored surface behind text for background
           Padding can but an int or a list of ints: [left, top, right, bottom]"""

        if isinstance(padding, list):
            self.pad_left, self.pad_top, self.pad_right, self.pad_bottom = padding
        else:
            self.pad_left, self.pad_top, self.pad_right, self.pad_bottom = padding, padding, padding, padding

        # Text is measured differently depending on how it's aligned
        if self.align == 'right':
            surf_x = self.items_rendered[0][3].right - self.total_width - self.pad_left

        # Measure the longest if text is centered:
        elif self.align == 'center':
            surf_x = self.items_rendered[self.longest_idx][3].left - self.pad_left

        elif self.align == 'horizontal-center':
            surf_x = self.items_rendered[0][3].left - self.pad_left

        else:  # align='left' or 'horizontal'
            surf_x = self.x - self.pad_left

        surf_y = self.y - self.pad_top
        surf_width = self.total_width + (self.pad_left + self.pad_right)
        surf_height = self.total_height + (self.pad_top + self.pad_bottom)

        self.bg_surface = Surface(self.game.WIN, self.game, surf_x, surf_y, surf_width, surf_height, bg_color, border_color, border_width, transparent)


    def _get_text_dimensions(self):
        # Get width of all items (horizontal-center):
        total_width = 0
        for item, _ in self.items:
            rendered = self.font.render(item, 1, "White")
            total_width += rendered.get_width() + self.spacing

        total_width -= self.spacing

        # Get total height (making surface)
        total_height = 0
        for item, _ in self.items:
            rendered = self.font.render(item, 1, "White")
            total_height += rendered.get_height() + self.spacing

        total_height -= self.spacing

        # Get length of longest text, (align='center')
        longest = ''
        longest_idx = None  # Used when making surface, to get the rect.left of centered text
        for idx, (item, _) in enumerate(self.items):
            if len(item) > len(longest):
                longest = item
                longest_idx = idx

        # Set the total width based on horizontal or vertical
        if self.align != 'horizontal' and self.align != 'horizontal-center':
            longest = self.font.render(longest, 1, "White")
            total_width = longest.get_width()
        else:
            # If horizontal, only one line so render anything:
            total_height = rendered.get_height()

        return total_width, total_height, longest_idx
