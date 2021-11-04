import pygame

class Transitions:
    """Game transitions inherited by game_engine"""

    def fade_out(self):
        """Called from Scene, calls game loop"""
        self.toggle_fade_out = True
        self.fade_timer = 0
        while self.fade_timer < 255:
            self.game_loop_input(1)
        self.game_loop_input(5)
        self.transition_surface.set_alpha(255)
        self.fade_timer = 255
        self.toggle_fade_out = False


    def fade_out_transition(self):
        """Called from game loop"""
        # To fade screen to black
        self.transition_surface.fill((0,0,0))
        self.transition_surface.set_alpha(self.fade_timer)
        self.WIN.blit(self.transition_surface, (0,0))
        self.fade_timer += 5
        if self.fade_timer > 255:
            pygame.event.clear()


    def fade_in(self):
        """Called from Scene, calls mainloop"""
        self.toggle_fade_in = True
        self.fade_timer = 255
        while self.fade_timer > 0:
            self.game_loop_input(1)
        self.transition_surface.set_alpha(255)
        pygame.event.clear()
        self.toggle_fade_in = False


    def fade_in_transition(self):
        """Called from game loop"""
        # To fade screen to black
        self.transition_surface.fill((0,0,0))
        self.transition_surface.set_alpha(self.fade_timer)
        self.WIN.blit(self.transition_surface, (0,0))
        self.fade_timer -= 5
        if self.fade_timer < 0:
            self.fade_timer = 0


    def slide_right(self, image):
        """Called from Scene, calls game loop"""
        self.toggle_slide_right = True
        self.fade_timer = self.win_width
        self.transition_surface.blit(self.backgrounds[image], (0, 0))
        while self.fade_timer > 0:
            self.game_loop_input(1)
        self.game_loop_input(1)
        self.toggle_slide_right = False


    def slide_right_transition(self):
        """Called from game loop"""
        self.WIN.blit(self.transition_surface, (self.fade_timer, 0))
        self.fade_timer -= 30
        if self.fade_timer < 0:
            pygame.event.clear()
            self.fade_timer = 0


    def slide_left(self, image):
        """Called from Scene, calls game loop"""
        self.toggle_slide_left = True
        self.fade_timer = -self.win_width
        self.transition_surface.blit(self.backgrounds[image], (0, 0))
        while self.fade_timer < 0:
            self.game_loop_input(1)
        self.game_loop_input(1)
        self.toggle_slide_left = False


    def slide_left_transition(self):
        """Called from game loop"""
        self.WIN.blit(self.transition_surface, (self.fade_timer, 0))
        self.fade_timer += 30
        if self.fade_timer > 0:
            pygame.event.clear()
            self.fade_timer = 0


    def shake_screen(self, pause=False):
        """Called from scenes"""

        self.shake_speed = 15
        self.shake_time = 0
        self.screen_shaking = True

        if pause:
            while self.screen_shaking:
                self.game_loop_input(1)



    def _shake_handle(self):
        """Called from game loop"""
        if self.x_offset >= 15:
            self.shake_speed = -15
            self.shake_time += 1
        if self.x_offset <= -15:
            self.shake_speed = 15
            self.shake_time += 1

        self.x_offset += self.shake_speed
        if self.shake_time > 5:
            self.x_offset = 0
            self.screen_shaking = False
