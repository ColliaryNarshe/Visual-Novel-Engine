import pygame
from sys import exit
from os import remove as os_remove
import json
from importlib import import_module
from collections import OrderedDict

from display.dialog_box import Dialog_Box
from display.maps import Map
from display.menu import Menu
from display.narration import Narration_Box
from display.surfaces import Surface
from game.input_check import InputCheck
from game.transitions import Transitions
from configuration import flag_variables
from game.get_data import get_data, get_saves

from game.coordinator import Coordinator


clock = pygame.time.Clock()

class Game(Transitions):
    def __init__(self, project_dir, starting_chapter, starting_scene):
        pygame.init()
        WIN = pygame.display.set_mode((1100,700))
        pygame.display.set_caption("Visual Novel Engine")
        self.WIN = WIN
        self.FPS = 30
        self.win_width = self.WIN.get_width()
        self.win_height = self.WIN.get_height()
        self.current_chapter = starting_chapter
        self.current_scene = starting_scene
        self.project_dir = project_dir
        project = import_module(project_dir + '.scene_list')
        self.input_class = InputCheck(self)

        self.current_menu = ''
        self.current_map = ''
        self.input_return = None
        self.menu_cursor_loc = -1

        self.transition_surface = pygame.Surface((self.win_width, self.win_height))

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

        # Saved games:
        self.saves = {}
        self.flag_vars = {**flag_variables}  # User variables, added to saved game

        # Game flags
        self.toggle_dialog = False
        self.toggle_narration = False
        self.toggle_narration_scroll = False
        self.toggle_menu = False
        self.toggle_map = False
        self.map_getting_input = False  # Turns off map input but still display
        self.toggle_hover = False  # Mouse hover

        # Display:
        self.menus = {}

        self.dialog_boxes = {'default': Dialog_Box(self, 'default_dialog')}
        self.create_dialog('default2', name_tag_y=-56, transparency=200, choice_menu_x=0, choice_menu_y=0, x='15%', width='70%', border_width=2, txt_wrap=63, max_lines=4, x_txt_padding=15, y_txt_padding=10, image_border_width=0)
        self.dialog_box = self.dialog_boxes['default']

        self.narration_box = Narration_Box(self)
        self.toggle_coordinator = False
        self.coordinator = Coordinator(self)

        self.scenes = {}

        get_data(self)
        project.get_scenes(self)


    def game_loop_input(self, no_input: int=False, tick=True):
        """
        Main game loop.
        no_input takes a number which equals number of cycles (without input)
        0 or False will continue loop until input by user is given.
        tick will toggle the FPS limiter.
        """

        rep_max = 0

        while True:
            if tick:
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

            if self.toggle_narration_scroll:
                self.narration_box.narration_scroll()

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
    def display_dialog(self, dialog: list=[], text_size=None, font_name=None, color=None, bold=None, bg_color=None, transparency=None, border_width=None, remove=True, set_disabled=[]):
        """Gets the list of dialog quotes and feeds them to dialog_box
            set_disabled must be same length as choices list"""
        # [['Arjen', 0, "Dialog"], ['Eilan', 0, "Okay."]] Number is image idx

        # Change font and box if arguments given, saving old values to revert after dialog.
        font_changed = False
        box_changed = False
        if text_size or font_name or color or bold != None:
            font_changed = True
            prev_font_name = self.dialog_box.font_name
            prev_text_size = self.dialog_box.text_size
            prev_color = self.dialog_box.color
            prev_bold = self.dialog_box.bold
            self.dialog_box.change_font(font_name, text_size, color)

        # if new font changes text size, make sure wrap and max_lines is 'auto'
        if text_size or font_name or bold:
            txt_wrap = 'auto'
            max_lines = 'auto'
            box_changed = True
        else:
            txt_wrap = self.dialog_box.wrap_num
            max_lines = self.dialog_box.max_lines

        if bg_color != None or transparency != None or border_width != None or box_changed:
            box_changed = True
            prev_bg_color = self.dialog_box.surface.background_color
            prev_transparency = self.dialog_box.surface.transparency
            prev_border = self.dialog_box.surface.border_width
            prev_txt_wrap = self.dialog_box.wrap_num
            prev_max_lines = self.dialog_box.max_lines
            self.dialog_box.config_surface(background_color=bg_color, transparency=transparency, border_width=border_width, txt_wrap=txt_wrap, max_lines=max_lines)

        self.toggle_dialog = True
        self.menu_cursor_loc = -1

        for quote in dialog:
            # Display the text:
            self.dialog_box.parse_quote(quote, set_disabled)
            # Draw background to clear old (nametag different sizes)
            self.display_background()

        if remove:
            self.dialog_box.remove_dialog_box()

        if font_changed:
            self.dialog_box.change_font(prev_font_name, prev_text_size, prev_color, prev_bold)

        if box_changed:
            self.dialog_box.config_surface(background_color=prev_bg_color, transparency=prev_transparency, border_width=prev_border, txt_wrap=prev_txt_wrap, max_lines=prev_max_lines)


    def create_dialog(self, name, x=None, y=None, width=None, height=None,
                      background_color=None, border_color=None, border_width=None,
                      transparency=None, name_tag_x=None, name_tag_y=None,
                      choice_menu_x=None, choice_menu_y=None,
                      txt_wrap='auto', max_lines='auto',
                      x_txt_padding=None, y_txt_padding=None,
                      image_size='auto', image_border_width=None):


        self.dialog_boxes[name] = Dialog_Box(self, name)

        self.dialog_boxes[name].config_surface(x, y, width, height, background_color, border_color, border_width, transparency, choice_menu_x, choice_menu_y, txt_wrap, max_lines, x_txt_padding, y_txt_padding, image_size, image_border_width)
        self.dialog_boxes[name].config_surface(x=name_tag_x, y=name_tag_y, transparency=transparency, name_tag=True)


    def switch_dialog(self, name):
        self.dialog_box = self.dialog_boxes[name]


    # Narration Box -----------------------------------
    def display_narration(self, text, choices=[], remove=True, set_disabled=[]):
        self.toggle_narration = True
        self.menu_cursor_loc = -1

        self.narration_box.parse_narration(text, choices, set_disabled)

        if remove:
            self.narration_box.remove_narration_box()


    def display_narration_scroll(self, text, speed=1, speedup=True, y_offset=0, font_name=None, size=35, color=None, bold=False):

        pygame.event.clear()

        # Font choices
        if not font_name: font_name = self.narration_box.font_name
        if not color: color = self.narration_box.color
        self.narration_box.scroll_font = pygame.font.SysFont(font_name, size, bold)
        any_text = self.narration_box.scroll_font.render("Anything", 1, "White")
        self.narration_box.scroll_txt_height = any_text.get_height()
        self.narration_box.scroll_color = color

        # Speed variables:
        self.narration_box.speedup_on = speedup  # T/F
        self.narration_box.speed_slow = speed
        self.narration_box.speed_fast = 3 * speed
        self.narration_box.scroll_speed = self.narration_box.speed_slow

        # Start and end locations
        self.narration_box.y_offset = y_offset  # Start and end heights (y is distance from top and bottom)
        self.narration_box.start_y = self.win_height + self.narration_box.scroll_txt_height - y_offset
        self.narration_box.start_y_float = self.narration_box.start_y # Used to keep track of floats
        self.narration_box.end_y = self.narration_box.start_y

        # Text
        self.narration_box.scroll_text = text.splitlines()

        self.toggle_narration_scroll = True
        self.scrolling = True

        while self.scrolling:
            self.game_loop_input(1)

        self.toggle_narration_scroll = False


    # Map
    def display_map(self, map, display_only=False, reset_loc=False, set_loc=None):
        self.toggle_map = True
        self.menu_cursor_loc = -1
        self.current_map = map.lower()

        # Add locations to list to have index locations for input_check
        self.current_map_locs = OrderedDict()

        map_dict = self.maps[self.current_map].coordinates

        for idx, name in enumerate(map_dict):
            if map_dict[name]['visibility']:  # If show/hide
                self.current_map_locs[idx] = {
                    'name': name,
                    'highlighted': False
                }

            # Reset highlighted location to normal
            if reset_loc:
                self.current_map_locs[idx]['highlighted'] = False
            if set_loc:
                if set_loc.lower() == name.lower():
                    self.current_map_locs[idx]['highlighted'] = True

        # If there are no locations, bit map as an image only
        if not self.current_map_locs:
            display_only = True

        if not display_only:
            self.map_getting_input = True
            self.game_loop_input()


    def show_map_loc(self, map: str, loc_name: str):
        self.maps[map.lower()].coordinates[loc_name]['visibility'] = True


    def hide_map_loc(self, map: str, loc_name: str):
        self.maps[map.lower()].coordinates[loc_name]['visibility'] = False


    def remove_map(self, keep_display=False):
        if not keep_display:
            self.toggle_map = False

        self.map_getting_input = False


    # Create new menus -----------------------------------
    def create_menu(self, name, items: list, x, y, color="Black", size=50, spacing=10, align='left', bold=0, font='georgia'):
        """To be called from scenes.py, make menu with optional background surface"""
        self.menus[name] = Menu(self, name, items, x, y, color, size, spacing, align, bold, font)


    # Images / Portraits ---------------------------------
    def _display_portraits(self):
        """For game loop"""

        # Using a copy of dictionary to remove any animations from dict that go off screen:
        for key, portrait in dict(self.portraits_to_blit).items():

            if portrait.portrait_animating:
                portrait.new_x -= portrait.x_move
                portrait.new_y -= portrait.y_move
                portrait.x = int(portrait.new_x)
                portrait.y = int(portrait.new_y)
                portrait.animation_count -= 1

                if portrait.animation_count == 0:
                    pygame.event.clear()
                    portrait.x, portrait.y = portrait.x_end, portrait.y_end
                    portrait.portrait_animating = False

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


    # Background -----------------------------------------
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


    def play_sfx(self, name, vol='default'):
        if name in self.sounds:
            if vol != 'default':
                self.sounds[name].set_volume(vol)
            self.sounds[name].play()


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
        self.input_return = self.input_class.check_input()


    def save(self, index:int = None, name:str = None) -> ".json file":
        """Save chapter, scene, and flags to json file
           If no arguments given, creates new save with unused index #
           index/name: specify specific index/name, possibly replacing an older save."""

        if index != None:
            new_name = 'Save ' + str(index)
        elif name:
            new_name = name
        else:
            # Find first unused name: Save 0, Save 1, etc.
            for idx, saved_name in enumerate(sorted(self.saves)):
                if 'Save ' + str(idx) != saved_name:
                    new_name = 'Save ' + str(idx)
                    break
            else:
                idx = len(self.saves)
                new_name = 'Save ' + str(idx)

        self.saves[new_name] = {
            "chapter": self.current_chapter,
            "scene": self.current_scene,
            "flags": self.flag_vars
        }

        self._write_json_file()


    def _write_json_file(self):
        """Save self.saves to json file"""

        dir = self.project_dir + "/saves.json"

        with open(dir, 'w') as f:
            json.dump(self.saves, f, indent=4)


    def get_saved_file_names(self, menu=True) -> list:
        """
        Returns name list of saved files to scenes, in menu format:
        [['save 0', True], ['save 1', True]]
        menu=False returns: ['save 0', 'save 1']
        """

        if not self.saves:
            return {}

        save_names = []
        for key in sorted(self.saves):
            if menu:
                save_names.append([key, True])
            else:
                save_names.append(key)

        return save_names


    def load_saved_game(self, save_name):
        """Sets chapter, scene, and flags"""
        self.current_chapter = self.saves[save_name]['chapter']
        self.current_scene = self.saves[save_name]['scene']
        self.flag_vars = self.saves[save_name]['flags']


    def delete_saved_game(self, save_name):
        """Removes given save from self.saves and updates json file.
           If there are no saves, deletes json file."""
        try:
            del self.saves[save_name]
        except KeyError:
            print(f"Save file '{save_name}' not found.")
            return

        if not self.saves:
            os_remove(self.project_dir + "/saves.json")
        else:
            self._write_json_file()


    def convert_color(self, color: 'str or tuple', transparency) -> tuple:
        """Converts a color text into tuple and changes transparency"""

        if not color:
            return None

        if transparency == None:
            transparency = 255

        if isinstance(color, tuple):
            return (color[0], color[1], color[2], transparency)

        for name, value in pygame.color.THECOLORS.items():
            if color.lower() == name:
                return (value[0], value[1], value[2], transparency)


    def exit_game(self):
        # Can put a warning window here, maybe auto save function
        pygame.quit()
        exit()




# End
