import pygame
from sys import exit
from importlib import import_module

from display.dialog_box import Dialog_Box
from display.maps import Map
from display.menu import Menu
from display.narration import Narration_Box
from display.surfaces import Surface
from game.input_check import check_input as ch_in
from game.transitions import Transitions
from configuration import flag_variables
from game.get_data import get_data

from game.coordinator import Coordinator


clock = pygame.time.Clock()

class Game(Transitions):
    def __init__(self, WIN, project_dir, starting_chapter, starting_scene):
        self.WIN = WIN
        self.FPS = 30
        self.win_width = self.WIN.get_width()
        self.win_height = self.WIN.get_height()
        self.current_chapter = starting_chapter
        self.current_scene = starting_scene
        self.project_dir = project_dir
        project = import_module(project_dir + '.scene_list')

        self.current_menu = ''
        self.current_map = ''
        self.input_return = None
        self.menu_cursor_loc = -1

        self.transition_surface = pygame.Surface((self.win_width, self.win_height), flags=pygame.SRCALPHA)

        # Menu scrolling speed (used in input_check.py):
        self.speed = self.FPS // 6  # Higher total value is slower
        self.count = self.speed

        # Transitions ----------
        self.toggle_fade_out = False  # Fade to black
        self.toggle_fade_in = False
        self.toggle_slide_left = False  # Slide the new background across screen
        self.toggle_slide_right = False

        # Screen shake:
        self.screen_shaking = False
        self.x_offset = 0

        # Assets:
        self.sounds = {}
        self.music = {}
        self.backgrounds = {}
        self.portraits = {}
        self.maps = {}
        self.dialog_images = {}  # Character images

        self.backdrop_text = []
        self.portraits_to_blit = {}
        self.map_loc_list = []  # Used to cycle locations in input_check

        # Used by user to create variables (To use later when saving):
        self.flag_vars = {**flag_variables}
        # Other methods of merging dictionaries:
        # self.flag_vars |= flag_variables
        # self.flag_vars.update(flag_variables)

        # Game flags: toggle game, dialog, narration, menu, map
        self.game_running = True
        self.toggle_dialog = False
        self.toggle_narration = False
        self.toggle_menu = False
        self.toggle_map = False
        self.map_getting_input = False  # Turns off map input but still display
        self.toggle_hover = False  # Mouse hover

        # Display:
        self.menus = {}
        self.dialog_boxes = {'default': Dialog_Box(self, 'default_dialog')}
        self.dialog_box = self.dialog_boxes['default']  # Create a function to change it and method for newly created ones are added to dict
        self.narration_box = Narration_Box(self)
        self.toggle_coordinator = False
        self.coordinator = Coordinator(self, self.maps)

        self.scenes = {}

        get_data(self)
        project.get_scenes(self)


    def game_loop_input(self, no_input=False):
        """Main game loop.
           Take a number for no_input which equals repetions which can be used as
           a pause of sorts, or to refresh the screen (without input)"""

        rep_max = 0

        while True:
            clock.tick(self.FPS)

            # Check for keyboard input, returns None to game.input_return
            if not no_input:

                self.check_input()

                # If got results, return out of loop and reset cursor location
                if self.input_return != None:
                    return

            else:
                self.input_return = None

            self.display_background()

            if self.toggle_map:
                self.maps[self.current_map].blit_map()

            self._display_portraits()

            if self.toggle_narration:
                self.narration_box.display_narration_box()

            if self.toggle_dialog:
                self.dialog_box.display_dialog_box()

            if self.toggle_menu:
                self.menus[self.current_menu].display_menu()

            # Transitions & Effects ---------------------------

            if self.toggle_fade_out:
                self.fade_out_transition()

            if self.toggle_fade_in:
                self.fade_in_transition()

            if self.toggle_slide_right:
                self.slide_right_transition()

            if self.toggle_slide_left:
                self.slide_left_transition()

            if self.screen_shaking:
                self._shake_handle()

            pygame.display.flip()

            # Used to loop around for game pause without input:
            # Also need to run twice to refresh screen before doing text writing by character
            if no_input:
                rep_max += 1
                if rep_max >= no_input:
                    return


    # Dialog Box -------------------------------------
    def display_dialog(self, dialog: list=[], remove=True, set_disabled=[]):
        """Gets the list of dialog quotes and feeds them to dialog_box
            set_disabled must be same length as choices list"""
        # [['Arjen', 0, "Dialog"], ['Eilan', 0, "Okay."]] Number is image idx

        self.toggle_dialog = True
        self.menu_cursor_loc = -1

        for quote in dialog:
            # Display the text:
            self.dialog_box.parse_quotes(quote, set_disabled)

            # Draw background to clear old (nametag different sizes)
            self.display_background()

        if remove:
            self.dialog_box.remove_dialog_box()


    def create_dialog(self, name, x=None, y=None, width=None, height=None,
                      background_color=None, border_color=None, border_width=None,
                      name_tag_x=None, name_tag_y=None):


        self.dialog_boxes[name] = Dialog_Box(self, name)

        if not x:
            x = self.dialog_boxes[name].surface.x
        if not y:
            y = self.dialog_boxes[name].surface.y
        if not width:
            width = self.dialog_boxes[name].surface.width
        if not height:
            height = self.dialog_boxes[name].surface.height
        if not background_color:
            background_color = self.dialog_boxes[name].background_color
        if not border_color:
            border_color = self.dialog_boxes[name].border_color
        if not border_width:
            border_width = self.dialog_boxes[name].border_width
        if not name_tag_x:
            name_tag_x = self.dialog_boxes[name].name_tag_x
        if not name_tag_y:
            name_tag_y = self.dialog_boxes[name].name_tag_y

        self.dialog_boxes[name].config_surface(x, y, width, height, background_color, border_color, border_width)
        self.dialog_boxes[name].config_surface(x=name_tag_x, y=name_tag_y, name_tag=True)


    def switch_dialog(self, name):
        self.dialog_box = self.dialog_boxes[name]


    # Narration Box -----------------------------------
    def display_narration(self, text, choices=[], remove=True, set_disabled=[]):
        self.toggle_narration = True
        self.menu_cursor_loc = -1

        self.narration_box.parse_narration(text, choices, set_disabled)

        if remove:
            self.narration_box.remove_narration_box()


    # Map
    def display_map(self, map, display_only=False, reset_loc=False, set_loc=None):
        self.toggle_map = True
        self.menu_cursor_loc = -1
        self.current_map = map.lower()

        # Add locations to list to have index locations for input_check
        self.map_loc_list = []
        for name, loc in self.maps[self.current_map].coordinates.items():
            if loc[2]:  # If show/hide
                self.map_loc_list.append([name] + loc)
            # Reset highlighted location to normal
            if reset_loc:
                self.maps[self.current_map].rects[name][1] = False
            if set_loc:
                if set_loc.lower() == name.lower():
                    self.maps[self.current_map].rects[name][1] = True

        # If there are no locations, bit map as an image only
        if not self.map_loc_list:
            display_only = True

        if not display_only:
            self.map_getting_input = True
            self.game_loop_input()


    def show_map_loc(self, map: str, loc_name: str):
        self.maps[map.lower()].coordinates[loc_name][2] = True


    def hide_map_loc(self, map: str, loc_name: str):
        self.maps[map.lower()].coordinates[loc_name][2] = False


    def remove_map(self, keep_display=False):
        if not keep_display:
            self.toggle_map = False

        self.map_getting_input = False


    # Create new menus ------------------------------------
    def create_menu(self, name, items: list, x, y, color="Black", size=50, spacing=10, align='left', bold=0, font='georgia'):
        """To be called from scenes.py, make menu with optional background surface"""
        self.menus[name] = Menu(self, name, items, x, y, color, size, spacing, align, bold, font)


    # Images / Portraits ---------------------------------
    def _display_portraits(self):
        """For game loop"""

        # Using a copy of dictionary to remove any animations from dict that go off screen:
        for key, portrait in dict(self.portraits_to_blit).items():

            # move_in_left animation, with no game pause:
            if portrait.in_left_animating:
                portrait.x += portrait.speed
                if portrait.x >= portrait.left_in:
                    pygame.event.clear()  # Clear input made during animation
                    portrait.in_left_animating = False

            # move_in_right animation, with no game pause:
            if portrait.in_right_animating:
                portrait.x -= portrait.speed
                if portrait.x <= portrait.right_in:
                    pygame.event.clear()
                    portrait.in_right_animating = False

            # Move_out_left animation, with no game pause:
            if portrait.out_left_animating:
                portrait.x -= portrait.speed
                if portrait.x + portrait.width < 0:
                    pygame.event.clear()
                    portrait.out_left_animating = False
                    self.portraits_to_blit[key].remove()  # Remove from original dict

            # Move_out_right animation, with no game pause:
            if portrait.out_right_animating:
                portrait.x += portrait.speed
                if portrait.x > portrait.game.win_width:
                    pygame.event.clear()
                    portrait.out_right_animating = False
                    self.portraits_to_blit[key].remove()  # Remove from original dict

            # Blit the portraits:
            self.WIN.blit(portrait.image, (portrait.x + self.x_offset, portrait.y))


    # Background -------------------------------------------
    def display_background(self):

        # If there is a background image:
        if self.scenes[self.current_chapter][self.current_scene].background:
            bg = self.scenes[self.current_chapter][self.current_scene].background.lower()
            # x is -15 because image is 30px wider than width (for screen shake)
            self.WIN.blit(self.backgrounds[bg], (-15 + self.x_offset, 0))
        # If there is no image, use color:
        else:
            if self.scenes[self.current_chapter][self.current_scene].bg_color:
                self.WIN.fill(self.scenes[self.current_chapter][self.current_scene].bg_color)

        # If there is text, blit it to window (not bg image in case there is none)
        if self.backdrop_text:
            for text, rect, x_original in self.backdrop_text:
                # When screen shaking, add x_offset to rect.x
                if self.screen_shaking:
                    rect.x = x_original + self.x_offset
                else:
                    rect.x = x_original

                self.WIN.blit(text, rect)

        # pygame.draw.line(self.WIN, 'white', (self.win_width//2, 0), (self.win_width//2, self.win_height), width=4)


    def display_bg_text(self, text, x, y, color='White', font='georgia', size=60, bold=0):
        """Render text to the background image
           Can take % for x or y, and x can take 'center' """

        # Check if font given (can't use self.font as default parameter)

        font = pygame.font.SysFont(font, size, bold)

        # Text:
        rendered_text = font.render(text, 1, color)

        # Convert percents and 'center'
        x, y = self._convert_percents_into_ints(x, y)
        if x == 'center':
            x = (self.win_width // 2) - (rendered_text.get_width() // 2)

        text_rect = rendered_text.get_rect(topleft=(x, y))
        self.backdrop_text.append((rendered_text, text_rect, x))  # x used to return from offset


    def clear_bg_text(self):
        """Clears text written onto background"""
        self.backdrop_text = []


    # Music ----------------------------------
    def play_song(self, song_name='', volume=None, fade=False, stop=False, pause=False, unpause=False, repetition=-1):
        """Given a song location will play song. Called from scenes"""

        if song_name:
            pygame.mixer.music.load(self.music[song_name.lower()])
            pygame.mixer.music.play(repetition)

        if volume:
            pygame.mixer.music.set_volume(volume)  # Float 0.0-1.0
        elif fade:
            pygame.mixer.music.fadeout(fade)
        elif stop:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        elif pause:
            pygame.mixer.music.pause()
        elif unpause:
            pygame.mixer.music.unpause()


    # ------
    def _convert_percents_into_ints(self, x, y) -> (int, int):
        """Takes either integer or string percents: "40%"
           Converts percent of screen size into integer"""

        if isinstance(x, str) and "%" in x:
            percent = float(x[:-1])
            new_x = int((percent / 100) * self.win_width)
        else:
            new_x = x

        if isinstance(y, str) and "%" in y:
            percent = float(y[:-1])
            new_y = int((percent / 100) * self.win_height)
        else:
            new_y = y

        return new_x, new_y


    # Game ---------------------------------------
    def run(self):
        self.scenes[self.current_chapter][self.current_scene].run()


    def change_scene(self, chapter, scene):
        self.current_chapter = chapter
        self.current_scene = scene


    def check_input(self):
        self.input_return = ch_in(self)


    def exit_game(self):
        # Can put a warning window here, maybe auto save function:
        pygame.quit()
        exit()














# End
