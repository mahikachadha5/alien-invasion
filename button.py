import pygame


class Button:
    """A class to build buttons for the game."""

    def __init__(self, ai_game, msg):
        """initialize button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # dimensions
        self.width, self.height = 200, 50
        self.button_color = (80, 200, 120)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 32)

        # center button
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        self._prep_msg(msg)
        
    def _prep_msg(self, msg):
        """turn message into a rendered image and center text on the button"""
        self.msg_img = self.font.render(msg,True, self.text_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center
    
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_img, self.msg_img_rect)