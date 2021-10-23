import pygame
from collections import OrderedDict
from configuration import map_settings

class Map:
    def __init__(self, game, map_loc, coordinates=None):
        self.game = game
        self.map_loc = map_loc
        self.coordinates = OrderedDict()  # coordinates from configuration.py
        self.rects = {}  # location rects
        self.dot_color = map_settings['dot_color']
        self.dot_highlight_color = map_settings['dot_highlight_color']
        self.padding = self.game.win_width * map_settings['padding_multiplier'] #.025

        if coordinates:
            # ['pub', (x,y), None, True]
            for loc_name, coordinates, padding, show in coordinates:
                self.coordinates[loc_name] = [coordinates, padding, show]


        self.config_map(txt_color=map_settings['txt_color'], txt_bg=map_settings['txt_bg'], font_size=map_settings['font_size'], dot_radius=map_settings['dot_radius'])


    def config_map(self, x=15, y=15, width="80%", height="80%", border_color='Grey', border_width=4, txt_color='white', txt_bg='Black', font_size=50, font='georgia', bold=1, dot_radius=30, pad_multi=None):
        self.txt_color = txt_color
        self.txt_bg = txt_bg
        self.font_size = font_size
        self.bold = bold
        self.font_name = font
        self.font = pygame.font.SysFont(self.font_name, self.font_size, self.bold)
        self.dot_radius = dot_radius

        if pad_multi:
            self.padding = self.game.win_width * pad_multi
        self.x, self.y = self.game._convert_percents_into_ints(x, y)
        self.width, self.height = self.game._convert_percents_into_ints(width, height)
        self.border_width = border_width
        self.border_color = border_color

        self.map_image = pygame.image.load(self.map_loc).convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.width, self.height))
        self.map_rect = self.map_image.get_rect(topleft=(self.x, self.y))

        for name, (coor, padding, _) in self.coordinates.items():
            if not padding:
                padding = self.padding

            center_x = self.x + (self.width * coor[0])
            center_y = self.y + (self.height * coor[1])
            x = center_x - padding
            y = center_y - padding
            length = padding * 2
            rect = pygame.Rect(x, y, length, length)

            self.rects[name] = [rect, False]

            # Draw the textbox:
            left = self.x + (self.width // 4)
            top = self.y + (self.height - 75)
            w = self.width // 2
            h = 75

            self.text_box_rect = pygame.Rect(left, top, w, h)


    def blit_map(self):
        # Blit the map
        self.game.WIN.blit(self.map_image, self.map_rect)

        # Border
        if self.border_width:
            pygame.draw.rect(self.game.WIN, self.border_color, self.map_rect, self.border_width)

        # get rects, draw dots
        for name, (rect, hover) in self.rects.items():
            if self.coordinates[name][2]:
                if hover:
                    # Change circle color
                    pygame.draw.circle(self.game.WIN, self.dot_highlight_color, (rect.centerx, rect.centery), self.dot_radius)
                    # Text box:
                    pygame.draw.rect(self.game.WIN, self.txt_bg, self.text_box_rect)
                    # Text box border:
                    if self.border_width:
                        pygame.draw.rect(self.game.WIN, self.border_color, self.text_box_rect, self.border_width)
                    # Location Name in text box:
                    txt = self.font.render(name, 1, self.txt_color)
                    txt_rect = txt.get_rect(center=(self.text_box_rect.center))
                    self.game.WIN.blit(txt, txt_rect)
                else:
                    pygame.draw.circle(self.game.WIN, self.dot_color, (rect.centerx, rect.centery), self.dot_radius)
