import pygame
from collections import OrderedDict
from configuration import map_settings

class Map:
    def __init__(self, game, map_loc, coordinates=None):
        self.game = game
        self.map_loc = map_loc
        self.coordinates = OrderedDict()  # coordinates from configuration.py
        self.rects = {}  # location rects

        if coordinates:
            # ['pub', (x,y), None, True]
            for loc_name, coordinates, padding, visibility in coordinates:
                self.coordinates[loc_name] = {
                    'coordinates': coordinates,
                    'padding': padding,
                    'visibility': visibility
                }

        self.config_map(
            map_settings['x_y'], map_settings['width_height'],
            map_settings['border_color'], map_settings['border_width'],
            map_settings['dot_radius'], map_settings['dot_color'],
            map_settings['dot_highlight_color'], map_settings['padding_multiplier'],
            map_settings['txt_color'], map_settings['txt_bg'],
            map_settings['font_size'], map_settings['bold'],
            map_settings['font'], map_settings['dot_transparency'],
            map_settings['txt_bg_transparency'])


    def config_map(self, x_y=None, width_height=None, border_color=None, border_width=None, dot_radius=None, dot_color=None, highlight=None, pad_multi=None, txt_color=None, txt_bg=None, font_size=None, bold=None, font=None, dot_transparency=None, txt_bg_transparency=None):
        if x_y:
            self.x, self.y = self.game._convert_percents_into_ints(x_y[0], x_y[1])
        if width_height:
            self.width, self.height = self.game._convert_percents_into_ints(width_height[0], width_height[1])
        if border_color: self.border_color = border_color
        if border_width: self.border_width = border_width
        if dot_radius: self.dot_radius = dot_radius
        if dot_color: self.dot_color = self.game.convert_color(dot_color, dot_transparency)
        if highlight: self.dot_highlight_color = self.game.convert_color(highlight, dot_transparency)
        if pad_multi: self.padding = self.game.win_width * pad_multi
        if txt_color: self.txt_color = txt_color
        if txt_bg: self.txt_bg = self.game.convert_color(txt_bg, txt_bg_transparency)
        if font_size: self.font_size = font_size
        if bold: self.bold = bold
        if font: self.font_name = font

        self.font = pygame.font.SysFont(self.font_name, self.font_size, self.bold)

        self.map_image = pygame.image.load(self.map_loc).convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.width, self.height))
        self.map_rect = self.map_image.get_rect(topleft=(self.x, self.y))
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        for name in self.coordinates:
            padding = self.coordinates[name]['padding']
            coor = self.coordinates[name]['coordinates']

            if not padding:
                padding = self.padding

            center_x = self.x + (self.width * coor[0])
            center_y = self.y + (self.height * coor[1])
            x = center_x - padding
            y = center_y - padding
            length = padding * 2
            rect = pygame.Rect(x, y, length, length)

            self.rects[name] = rect

            # Draw the textbox:
            left = self.x + (self.width // 4)
            top = self.y + (self.height - 85)
            w = self.width // 2
            h = 75

            self.text_box_rect = pygame.Rect(left, top, w, h)


    def blit_map(self):
        # Blit the map (on different surface than dots for transparency)
        self.game.WIN.blit(self.map_image, self.map_rect)

        # Border
        if self.border_width:
            pygame.draw.rect(self.game.WIN, self.border_color, self.map_rect, self.border_width)

        # get rects, draw dots
        for loc_idx in self.game.current_map_locs:
            name = self.game.current_map_locs[loc_idx]['name']
            hover = self.game.current_map_locs[loc_idx]['highlighted']
            rect = self.rects[name]

            if self.coordinates[name]['visibility']:
                if hover:
                    # Change circle color
                    pygame.draw.circle(self.surface, self.dot_highlight_color, (rect.centerx, rect.centery), self.dot_radius)
                    # Text box:
                    pygame.draw.rect(self.surface, self.txt_bg, self.text_box_rect)
                    # Text box border:
                    if self.border_width:
                        pygame.draw.rect(self.surface, self.border_color, self.text_box_rect, self.border_width)
                    # Location Name in text box:
                    txt = self.font.render(name, 1, self.txt_color)
                    txt_rect = txt.get_rect(center=(self.text_box_rect.center))
                    self.surface.blit(txt, txt_rect)
                else:
                    pygame.draw.circle(self.surface, self.dot_color, (rect.centerx, rect.centery), self.dot_radius)

        self.game.WIN.blit(self.surface, (self.x, self.y))
