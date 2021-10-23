import pygame

class Surface:
    def __init__(self, WIN, game, x, y, width, height, bg_color="White", border_color="Black", border_width=0, transparent=0):
        """Coordinates and dimensions can be given in integers or a string with percent sign "22.5%" """
        self.WIN = WIN
        self.game = game
        self.configure(x, y, width, height, bg_color, border_color, border_width)
        self.image = None
        # self.font = pygame.font.SysFont('georgia', 50, 0)
        self.display_text_list = [] # list of tuples, pygame text font and rect, for specific texts
        self.hide_surface = False
        self.triangle = False

        # if transparent:
        #     self.surface.set_alpha(transparent)
        #     self.surface.set_colorkey("black")


    def configure(self, x=None, y=None, width=None, height=None, background_color=None, border_color=None, border_width=None):
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

        self.x, self.y = self.game._convert_percents_into_ints(x, y)
        self.width, self.height = self.game._convert_percents_into_ints(width, height)
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width

        # Text surface/rect:
        self.surface = pygame.Surface((self.width, self.height))
        # self.surface.set_alpha(50)
        self.surface_rect = self.surface.get_rect(topleft=(self.x, self.y))



    def reset_location(self):
        self.surface_rect = self.surface.get_rect(topleft=(self.x, self.y))


    def clear_text(self):
        """Used by both Display_Box and Narration"""
        self.display_text_list = []
        self.surface.fill(self.background_color)


    def display_surface(self):
        # see_through = pygame.Rect(self.surface_rect.x, self.surface_rect.y, self.surface_rect.width, self.surface_rect.height)
        # pygame.draw.rect(self.surface, (0,0,0,50), see_through)

        if not self.hide_surface:
            if self.game.screen_shaking:
                self.surface_rect.x = self.x + self.game.x_offset
            else:
                self.surface_rect.x = self.x

            # Blit surface
            self.WIN.blit(self.surface, self.surface_rect)
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
