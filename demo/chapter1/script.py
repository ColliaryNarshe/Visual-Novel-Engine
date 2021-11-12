import pygame
from demo.chapter1.story import *

class TitleScreen:
    # __init__ with top three variables required for every scene class:
    def __init__(self, game):
        self.game = game
        self.background = 'jonathan-kemper-title.jpg'
        self.bg_color = 'White'

        # Optional space for any useful code:
        self.menu_list = [["Start", True], ["Chapter 2", True], ["Quit", True]]


    def run(self):
        self.game.play_song('Farm(cut).mp3', .4)

        # Draw title onto background:
        self.game.display_bg_text("Visual Novel Engine", x='center', y='17%', color="Blue", size=60, bold=1)

        # Create and display menu:
        self.game.create_menu('start_screen', self.menu_list, '50%', '50%', 'White', size=40, bold=1, align='center')
        self.game.menus['start_screen'].show_menu(remove=False)


        if self.game.input_return == 'Start':
            self.game.play_song(fade=2000)
            self.game.fade_out()
            self.game.menus['start_screen'].remove_menu()
            self.game.clear_bg_text()
            self.game.change_scene('chapter1', 'scene1')

        elif self.game.input_return == 'Chapter 2':
            self.game.play_song(fade=1000)
            self.game.fade_out()
            self.game.menus['start_screen'].remove_menu()
            self.game.clear_bg_text()
            self.game.change_scene('chapter2', 'scene1')
            self.game.play_song('Fantasy_Motion(cut).mp3', 0.4)

        elif self.game.input_return == 'Quit':
            self.game.exit_game()



class Scene1:
    def __init__(self, game):
        self.game = game
        self.background = 'dylan-nolte-texture.jpg'
        self.bg_color = 'White'


    def run(self):
        self.game.play_song('Fantasy_Motion(cut).mp3', 0.4)
        # Display map as background
        self.game.display_map('city1.png', display_only=True, reset_loc=True)
        self.game.fade_in()

        # Portrait with dialog
        self.game.portraits['SF_People1_6.png'].blit_image(dialog='left') # Takes optional y coordinate
        self.game.display_dialog([["Julia", '', "Hello, my name is Julia. Hmmm I'm covering the map, I should move over."]], remove=False)
        self.game.portraits['SF_People1_6.png'].switch_sides()
        self.game.display_dialog([["Julia", '', "Great! That's much better. Now, why don't you choose a place to go?"]])

        # Make the map interactive (retrieve input from self.game.input_return):
        self.game.display_map('city1.png')
        self.game.display_dialog([["Julia", '', f"I see! So you like going to the {self.game.input_return}. Well, it's your choice!"]])

        self.game.portraits['SF_People1_6.png'].move_out_right()
        self.game.remove_map()

        # Dialog with choices:
        self.game.display_dialog(demo_dialog)
        self.game.dialog_box.move_dialog_up()

        # Check dialog menu choice to display different text:
        if self.game.input_return == 'Yes':
            self.game.display_dialog([["John", 0, "Great! My name is John and I approve this dialog box location."]])
        elif self.game.input_return == 'No':
            self.game.display_dialog([['', 0, "Well too bad!"]])
        elif self.game.input_return == 'Maybe':
            self.game.display_dialog([["Arjen", '', "Geez, make up your mind. Wait, what happened to my headshot?"]])

        # Bring dialog box back down
        self.game.dialog_box.move_dialog_down()

        self.game.change_scene('chapter2', 'scene1')
