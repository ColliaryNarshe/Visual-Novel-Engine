import pygame

class Surface:
    def __init__(self, WIN, game, x, y, width, height, bg_color="White", border_color="Black", border_width=0, transparency=255):
        """Coordinates and dimensions can be given in integers or a string with percent sign "22.5%" """
        self.WIN = WIN
        self.game = game
        self.background_color = None
        self.configure(x, y, width, height, bg_color, border_color, border_width, transparency)
        self.image = None
        self.display_text_list = [] # list of tuples, pygame text font and rect, for specific texts
        self.hide_surface = False
        self.triangle = False


    def configure(self, x=None, y=None, width=None, height=None, background_color=None, border_color=None, border_width=None, transparency=None):
        """Used to edit the surface"""
        if x == None:
            x = self.x
        if y == None:
            y = self.y
        if width == None:
            width = self.width
        if height == None:
            height = self.height
        if background_color == None:
            background_color = self.background_color
        if border_color == None:
            border_color = self.border_color
        if border_width == None:
            border_width = self.border_width
        if transparency == None:
            transparency = self.transparency

        self.x, self.y = self.game._convert_percents_into_ints(x, y)
        self.width, self.height = self.game._convert_percents_into_ints(width, height)
        self.background_color = self.game.convert_color(background_color, transparency)
        self.border_color = self.game.convert_color(border_color, transparency)
        self.border_width = border_width
        self.transparency = transparency

        # Text surface/rect:
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect(topleft=(self.x, self.y))



    def reset_location(self):
        self.surface_rect = self.surface.get_rect(topleft=(self.x, self.y))


    def clear_text(self):
        """Used by both Display_Box and Narration"""
        self.display_text_list = []
        if self.background_color:
            self.surface.fill(self.background_color)
        else:
            self.surface.fill((0,0,0,0))


    def display_surface(self):
        if not self.hide_surface:
            if self.game.screen_shaking:
                self.surface_rect.x = self.x + self.game.x_offset
            else:
                self.surface_rect.x = self.x

            # Blit surface
            self.WIN.blit(self.surface, self.surface_rect)
            if self.background_color:
                self.surface.fill(self.background_color)
            if self.border_width:
                pygame.draw.rect(self.WIN, self.border_color, self.surface_rect, self.border_width)

            # Background image if added
            if self.image:
                self.surface.blit(self.image, (0, 0))

            # Blit list of text if not empty:
            if self.display_text_list:
                for text, rect in self.display_text_list:
                    self.surface.blit(text, rect)

            # Triangle, skip if not end of text:
            if self.triangle:
                point1 = (self.surface_rect.width - 30, self.surface_rect.height - 30)
                point2 = (self.surface_rect.width - 10, self.surface_rect.height - 30)
                point3 = (self.surface_rect.width - 20, self.surface_rect.height - 10)
                pygame.draw.polygon(surface=self.surface, color=(255, 0, 0), points=[point1, point2, point3])




#
