import pygame
from configuration import map_coordinates

map_cursor_active = False  # True when cursor is hovering over location

def check_input(game):
    if game.toggle_menu:

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_RIGHT]:
            reset_mouse_cursor(game)
            # Count to make holding key while scrolling slower:
            game.count += 1
            if game.count >= game.speed:
                game.sounds['menu_sound'].play()
                menu_move_down(game)
                game.count = 0


        elif keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_LEFT]:
            reset_mouse_cursor(game)
            game.count += 1
            if game.count >= game.speed:
                game.sounds['menu_sound'].play()
                menu_move_up(game)
                game.count = 0
        else:
            game.count = game.speed

    # ------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.exit_game()

        # Map mouse check
        if game.toggle_map and game.map_getting_input:
            pressed = check_map_input(game, event)
            if pressed:
                game.map_getting_input = False
                return pressed

        # Menu mouse check
        if game.toggle_menu:
            pressed = check_menu_mouse(game, event)
            if pressed:
                game.sounds['selected'].play()
                game.toggle_menu = False
                return game.menu_cursor_loc

        # Other mouse checks
        if event.type == pygame.MOUSEBUTTONUP:
            # Click to continue dialog or narration, but not when there's a menu
            if (game.toggle_dialog or game.toggle_narration) and not game.toggle_menu:
                return game.menu_cursor_loc

            # Coordinator click
            if game.toggle_coordinator:
                return pygame.mouse.get_pos()

        if event.type == pygame.KEYDOWN:

            # Move cursor on map:
            if game.map_getting_input:
                if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    map_arrow_down(game)

                if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                    map_arrow_up(game)

            # Temp exit:
            if event.key == pygame.K_ESCAPE:
                game.exit_game()

            # Press RETURN:
            if event.key == pygame.K_RETURN:
                # Map
                if game.map_getting_input:
                    # It's possible no item is selected, so check first:
                    current = check_map_active_loc(game)
                    if current:
                        game.map_getting_input = False
                        return current
                else:
                    # Menu
                    if game.toggle_menu:
                        if game.menu_cursor_loc == -1:
                            return
                        else:
                            game.sounds['selected'].play()

                    return game.menu_cursor_loc


def check_menu_mouse(game, event):
    # Loop through the menu items for the rects
    for idx, (_, _, _, rect, _) in enumerate(game.menus[game.current_menu].items_rendered):

        # Change color when hovering:
        if rect.collidepoint(pygame.mouse.get_pos()) and game.menus[game.current_menu].items[idx][1]:
            if game.menu_cursor_loc != idx:
                game.sounds['menu_sound'].play()
                game.menu_cursor_loc = idx

            if event.type == pygame.MOUSEBUTTONUP:
                return True


def reset_mouse_cursor(game):
    """Moves the mouse cursor if hovering over menu. Used when arrow keys are used
       to not interfere with input."""

    for idx, (_, _, _, rect, _) in enumerate(game.menus[game.current_menu].items_rendered):
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_pos([0, 0])


def check_map_input(game, event):
    global map_cursor_active

    none_active = True # To check if any locations or active
    for name, (rect, hover) in game.maps[game.current_map].rects.items():
        # If show/hide
        if game.maps[game.current_map].coordinates[name][2]:
            # If mouse is hovering over a location:
            if rect.collidepoint(pygame.mouse.get_pos()):

                map_cursor_active = True
                none_active = False

                if not game.maps[game.current_map].rects[name][1]:
                    game.sounds['menu_sound'].play()
                    game.maps[game.current_map].rects[name][1] = True

                # If mouse is also clicked
                if event.type == pygame.MOUSEBUTTONUP:
                    # game.maps[game.current_map].rects[name][1] = False # To turn off highlight
                    return name

            else:
                if map_cursor_active:
                    game.maps[game.current_map].rects[name][1] = False

    if none_active:
        map_cursor_active = False


def map_arrow_down(game):
    global map_cursor_active

    if map_cursor_active:  # if mouse is already hovering over a location
        pygame.mouse.set_pos([0, 0])
        # Reset highlight colored locations
        for name in game.maps[game.current_map].rects:
            game.maps[game.current_map].rects[name][1] = False

    map_cursor_active = False

    # Get a current location if any:
    current = check_map_active_loc(game)

    if not current:
        # Set first location [0] using it's name [0]
        game.maps[game.current_map].rects[ game.map_loc_list[0][0] ][1] = True
        game.sounds['menu_sound'].play()
    else:
        # Get next idx in list:
        for idx, loc in enumerate(game.map_loc_list):
            if game.maps[game.current_map].rects[loc[0]][1]:
                game.maps[game.current_map].rects[loc[0]][1] = False
                # If last item, cycle to top:
                if idx+1 == len(game.map_loc_list):
                    next_name = game.map_loc_list[0][0]
                else:
                    next_name = game.map_loc_list[idx+1][0]
                # Set location
                game.maps[game.current_map].rects[next_name][1] = True
                game.sounds['menu_sound'].play()
                return


def map_arrow_up(game):
    global map_cursor_active

    # if mouse is already hovering over a location, reset locations and move cursor
    if map_cursor_active:
        pygame.mouse.set_pos([0, 0])
        # Reset highlight colored locations
        for name in game.maps[game.current_map].rects:
            game.maps[game.current_map].rects[name][1] = False

    map_cursor_active = False

    # Get a current location if any:
    current = check_map_active_loc(game)

    last_idx = len(game.map_loc_list) - 1
    if not current:
        # Set first location [0] using it's name [0]
        game.maps[game.current_map].rects[game.map_loc_list[last_idx][0]][1] = True
        game.sounds['menu_sound'].play()
    else:
        # Get next idx in list:
        for idx, loc in enumerate(game.map_loc_list):
            if game.maps[game.current_map].rects[loc[0]][1]:
                # Remove the current active:
                game.maps[game.current_map].rects[loc[0]][1] = False
                # If first item, cycle to bottom:
                if idx == 0:
                    next_name = game.map_loc_list[last_idx][0]
                else:
                    next_name = game.map_loc_list[idx-1][0]
                # Set location
                game.maps[game.current_map].rects[next_name][1] = True
                game.sounds['menu_sound'].play()
                return


def check_map_active_loc(game):
    for name in game.maps[game.current_map].rects:
        if game.maps[game.current_map].rects[name][1]:
            return name


def menu_move_down(game):
    menu_num = len(game.menus[game.current_menu].items_rendered)

    game.menu_cursor_loc += 1

    if game.menu_cursor_loc >= menu_num:
        game.menu_cursor_loc = 0

    # Checks the menu list and sees if current is disabled. If so move again.
    if not game.menus[game.current_menu].items[game.menu_cursor_loc][1]:
        menu_move_down(game)


def menu_move_up(game):
    menu_num = len(game.menus[game.current_menu].items_rendered)

    game.menu_cursor_loc -= 1

    if game.menu_cursor_loc <= -1:
        game.menu_cursor_loc = menu_num - 1

    # Checks the menu list and sees if current is disabled. If so move again.
    if not game.menus[game.current_menu].items[game.menu_cursor_loc][1]:
        menu_move_up(game)



# end
