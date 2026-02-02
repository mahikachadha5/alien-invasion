import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.stats = ai_game.game_stats

        # Font settings
        self.text_color = (211, 211, 211)
        self.font = pygame.font.SysFont(None, 32)

        # Prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        
    def prep_score(self): 
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score}"
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Position top-left
        self.score_rect = self.score_image.get_rect()
        self.score_rect.topleft = (20, 20)
    
    def prep_high_score(self): 
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"High Score: {high_score}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        # Position top-left
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.topright = (self.screen_rect.right - 20, 20)
        
    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
       
