import pygame
from demo.chapter1.story import *

class Scene1:
    def __init__(self, game):
        self.game = game
        self.background = None
        self.bg_color = 'Black'


    def run(self):
        self.game.display_narration_scroll(scroll_demo, speed=3)
        self.game.slide_right('sean-musil-field.jpg')
        self.background = 'sean-musil-field.jpg'
        self.game.display_narration(alice)
        self.game.display_narration("This is the end. Return to the title screen?", choices=["Yes!", "Maybe", "No"], set_disabled=[True, True, False])
        self.game.change_scene('chapter1', 'title')
        self.background = None
