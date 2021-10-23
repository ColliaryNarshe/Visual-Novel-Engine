import pygame


class Coordinator:
    """Used from game"""
    def __init__(self, game, maps):
        self.game = game
        self.maps = maps

    def coordinate(self, name):
        from game.input_check import check_input
        map_loc = self.maps[name].map_loc
        map_image = pygame.image.load(map_loc).convert_alpha()
        map_image = pygame.transform.scale(map_image, (self.game.win_width, self.game.win_height))

        FPS = 30
        self.game.toggle_coordinator = True
        clock = pygame.time.Clock()

        while True:
            clock.tick(FPS)

            coordinates = check_input(self.game)
            if coordinates:
                x = coordinates[0] / self.game.win_width
                y = coordinates[1] / self.game.win_height
                print(round(x, 3), round(y, 3))


            self.game.WIN.blit(map_image, (0, 0))
            pygame.display.flip()



# ------------------------------------------------------------------------------
#  To run from file directly
def coordinate():
    pygame.init()

    WIN = pygame.display.set_mode((1400,950))
    pygame.display.set_caption("Coordinator")

    # Used as placeholder before edited by user input
    map_location = 'assets/maps/'

    clock = pygame.time.Clock()
    font = pygame.font.SysFont('georgia', 50, 1)
    small_font = pygame.font.SysFont('georgia', 30, 1)

    # Instructions text:
    txt_top = small_font.render("Type map location and press ENTER:", 1, 'blue4')
    txt_top_rect = txt_top.get_rect(midbottom=(700, 400))

    # Error message:
    error_txt = small_font.render("No such file or directory. Try again.", 1, 'DarkRed')
    error_rect = error_txt.get_rect(center=(700, 600))
    error_message = False

    map_name_screen = True

    while map_name_screen:
        clock.tick(30)

        WIN.fill('aquamarine4')
        # Input box:
        txt = font.render(map_location, 1, 'white')
        txt_rect = txt.get_rect(center=(700, 475))
        # Blits
        WIN.blit(txt_top, txt_top_rect)
        WIN.blit(txt, txt_rect)

        if error_message:
            WIN.blit(error_txt, error_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                from sys import exit
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    from sys import exit
                    exit()


                if event.key == pygame.K_RETURN:
                    try:
                        map_img = pygame.image.load(map_location).convert_alpha()
                        map_img = pygame.transform.scale(map_img, (1400, 950))
                        map_name_screen = False
                    except FileNotFoundError:
                        error_message = True

                elif event.key == pygame.K_BACKSPACE:
                    map_location = map_location[:-1]

                else:
                    map_location += event.unicode


    while True:
        WIN.blit(map_img, (0,0))
        clock.tick(30)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                from sys import exit
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    from sys import exit
                    exit()

            if event.type == pygame.MOUSEBUTTONUP:
                coordinates = pygame.mouse.get_pos()
                if coordinates:
                    x = coordinates[0] / 1400
                    y = coordinates[1] / 950
                    print(round(x, 3), round(y, 3))


if __name__ == "__main__":
    coordinate()
