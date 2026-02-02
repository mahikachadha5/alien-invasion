import pygame
import sys
import os


class Ship:
    """Initialize the ship and set its starting position."""

    def __init__(self, ai_game):
        self.settings = ai_game.settings

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        current_path = os.path.dirname(__file__)  # folder containing ship.py
        image_path = os.path.join(current_path, 'images', 'ship.bmp')

        # Load the ship image and get its rect
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

        self.center_ship()

        # movement flags; start with a ship thats not moving
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update ship's pos based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update rect object from self.x
        self.rect.x = self.x

    def center_ship(self):
        # Start each game with the ship at the bottom center of screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y = self.rect.y - 10
        # store a float for the ship's exact horizontal position
        self.x = float(self.rect.x)
