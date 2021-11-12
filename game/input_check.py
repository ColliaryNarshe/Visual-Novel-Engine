import pygame
from configuration import map_coordinates



class InputCheck():
    def __init__(self, game):
        self.game = game
        self.map_cursor_active = False  # True when cursor is hovering over location

        # Menu scrolling speed:
        self.speed = self.game.FPS // 6  # Higher total value is slower
        self.count = self.speed


    def check_input(self):
        if self.game.toggle_menu:

            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_RIGHT]:
                self.reset_mouse_cursor()
                # Count to make holding key while scrolling slower:
                self.count += 1
                if self.count >= self.speed:
                    self.game.play_sfx('menu_sound')
                    self.menu_move_down()
                    self.count = 0

            elif keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_LEFT]:
                self.reset_mouse_cursor()
                self.count += 1
                if self.count >= self.speed:
                    self.game.play_sfx('menu_sound')
                    self.menu_move_up()
                    self.count = 0
            else:
                self.count = self.speed

        # ------------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.exit_game()

            # Map mouse check
            if self.game.toggle_map and self.game.map_getting_input:
                pressed = self.check_map_input(event)
                if pressed:
                    self.game.map_getting_input = False
                    return pressed

            # Menu mouse check
            if self.game.toggle_menu:
                pressed = self.check_menu_mouse(event)
                if pressed:
                    self.game.play_sfx('menu_sound')
                    self.game.toggle_menu = False
                    return self.game.menus[self.game.current_menu].items[self.game.menu_cursor_loc][0]

            # Other mouse checks
            if event.type == pygame.MOUSEBUTTONUP:
                # Click to continue dialog or narration, but not when there's a menu
                if (self.game.toggle_dialog or self.game.toggle_narration) and not self.game.toggle_menu:
                    return True

                # Coordinator click
                if self.game.toggle_coordinator:
                    return pygame.mouse.get_pos()

            if event.type == pygame.KEYDOWN:

                # Move cursor on map:
                if self.game.map_getting_input:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        self.map_arrow_down()

                    if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.map_arrow_up()

                # Temp exit:
                if event.key == pygame.K_ESCAPE:
                    self.game.exit_game()

                # Press RETURN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Map
                    if self.game.map_getting_input:
                        # It's possible no item is selected, so check first:
                        current = self.check_map_active_loc()
                        if current:
                            self.game.map_getting_input = False
                            return current
                    else:
                        # Menu
                        if self.game.toggle_menu:
                            if self.game.menu_cursor_loc == -1:
                                return
                            else:
                                self.game.play_sfx('selected')
                                return self.game.menus[self.game.current_menu].items[self.game.menu_cursor_loc][0]

                        return True


    def check_menu_mouse(self, event):
        # Loop through the menu items for the rects
        for idx, (_, _, _, rect, _) in enumerate(self.game.menus[self.game.current_menu].items_rendered):

            # Change color when hovering:
            if rect.collidepoint(pygame.mouse.get_pos()) and self.game.menus[self.game.current_menu].items[idx][1]:
                if self.game.menu_cursor_loc != idx:
                    self.game.play_sfx('menu_sound')
                    self.game.menu_cursor_loc = idx

                if event.type == pygame.MOUSEBUTTONUP:
                    return True


    def reset_mouse_cursor(self):
        """Moves the mouse cursor if hovering over menu. Used when arrow keys are used
           to not interfere with input."""

        for idx, (_, _, _, rect, _) in enumerate(self.game.menus[self.game.current_menu].items_rendered):
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_pos([0, 0])


    def check_map_input(self, event):

        none_active = True # To check if any locations are active
        for idx in self.game.current_map_locs:
            name = self.game.current_map_locs[idx]['name']
            rect = self.game.maps[self.game.current_map].rects[name]

            # If show/hide
            if self.game.maps[self.game.current_map].coordinates[name]['visibility']:
                # If mouse is hovering over a location:
                if rect.collidepoint(pygame.mouse.get_pos()):

                    self.map_cursor_active = True
                    none_active = False

                    if not self.game.current_map_locs[idx]['highlighted']:
                        self.game.play_sfx('menu_sound')
                        self.game.current_map_locs[idx]['highlighted'] = True

                    # If mouse is also clicked
                    if event.type == pygame.MOUSEBUTTONUP:
                        return name

                else:
                    if self.map_cursor_active:
                        self.game.current_map_locs[idx]['highlighted'] = False

        if none_active:
            self.map_cursor_active = False


    def map_arrow_down(self):

        if self.map_cursor_active:  # if mouse is already hovering over a location
            pygame.mouse.set_pos([0, 0])
            # Reset highlight colored locations
            for idx in self.game.current_map_locs:
                self.game.current_map_locs[idx]['highlighted'] = False

        self.map_cursor_active = False

        # Get a current location if any:
        current = self.check_map_active_loc()

        if not current:
            # Set first location
            self.game.current_map_locs[0]['highlighted'] = True
            self.game.play_sfx('menu_sound')
        else:
            # Set next idx in list:
            for loc_index in self.game.current_map_locs:
                if self.game.current_map_locs[loc_index]['highlighted']:
                    # Remove previous highlight:
                    self.game.current_map_locs[loc_index]['highlighted'] = False

                    # Set highlight, either next or back to top
                    if loc_index + 1 == len(self.game.current_map_locs):
                        self.game.current_map_locs[0]['highlighted'] = True
                    else:
                        self.game.current_map_locs[loc_index +1]['highlighted'] = True

                    self.game.play_sfx('menu_sound')
                    return


    def map_arrow_up(self):

        # if mouse is already hovering over a location, reset locations and move cursor
        if self.map_cursor_active:
            pygame.mouse.set_pos([0, 0])
            # Reset highlight colored locations
            for idx in self.game.current_map_locs:
                self.game.current_map_locs[idx]['highlighted'] = False

        self.map_cursor_active = False

        # Get a current location if any:
        current = self.check_map_active_loc()

        last_idx = len(self.game.current_map_locs) - 1

        if not current:
            # Set first location [0] using it's name [0]
            self.game.current_map_locs[last_idx]['highlighted'] = True
            self.game.play_sfx('menu_sound')
        else:
            # Get next idx in list:
            for loc_index in self.game.current_map_locs:
                if self.game.current_map_locs[loc_index]['highlighted']:
                    # Remove the current active:
                    self.game.current_map_locs[loc_index]['highlighted'] = False

                    # If first item, cycle to bottom:
                    if loc_index == 0:
                        self.game.current_map_locs[last_idx]['highlighted'] = True
                    else:
                        self.game.current_map_locs[loc_index - 1]['highlighted'] = True

                    self.game.play_sfx('menu_sound')
                    return


    def check_map_active_loc(self):
        for loc_index in self.game.current_map_locs:
            if self.game.current_map_locs[loc_index]['highlighted']:
                return self.game.current_map_locs[loc_index]['name']


    def menu_move_down(self):
        menu_num = len(self.game.menus[self.game.current_menu].items_rendered)

        self.game.menu_cursor_loc += 1

        if self.game.menu_cursor_loc >= menu_num:
            self.game.menu_cursor_loc = 0

        # Checks the menu list and sees if current is disabled. If so move again.
        if not self.game.menus[self.game.current_menu].items[self.game.menu_cursor_loc][1]:
            self.menu_move_down()


    def menu_move_up(self):
        menu_num = len(self.game.menus[self.game.current_menu].items_rendered)

        self.game.menu_cursor_loc -= 1

        if self.game.menu_cursor_loc <= -1:
            self.game.menu_cursor_loc = menu_num - 1

        # Checks the menu list and sees if current is disabled. If so move again.
        if not self.game.menus[self.game.current_menu].items[self.game.menu_cursor_loc][1]:
            self.menu_move_up()
