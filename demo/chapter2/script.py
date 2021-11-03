import pygame
from demo.chapter1.story import *

class Scene1:
    def __init__(self, game):
        self.game = game
        self.background = 'sean-musil-field.jpg'
        self.bg_color = 'White'


    def run(self):
        self.game.display_narration(alice)
        self.game.display_narration("This is the end. Return to the title screen?", choices=["Yes!", "Maybe", "No"], set_disabled=[True, True, False])
        self.game.change_scene('chapter1', 'title')
