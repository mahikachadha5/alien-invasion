import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button

class AlienInvasion:
    """Class to manage game assets and behavior."""

    def __init__(self) -> None:
        """Initialize game and make game resources"""
        pygame.init()
        self.game_active = False

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.game_stats = GameStats(self)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        
        self.play_button = Button(self, "Start Game")

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            
            if self.game_active:
                self._update_ship()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()
            self.clock.tick(60)

    def _update_ship(self):
        self.ship.update()

    def _check_keydown_events(self, event):
        """Responds to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Responds to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
        
    def _check_play_button(self, mouse_position): 
        button_clicked = self.play_button.rect.collidepoint(mouse_position)
        if button_clicked and not self.game_active:
            self.game_stats.reset_stats()
            self.game_active = True
            
            self.bullets.empty()
            self.aliens.empty()
            
            self._create_fleet()
            self.ship.center_ship()
            
            pygame.mouse.set_visible(False)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

        

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        
        if not self.game_active: 
            self.play_button.draw_button()

        pygame.display.flip()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        new_bullet = Bullet(self)
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Updates position of bullets and deletes disappeared bullets"""
        self.bullets.update()

        # delete disappeared bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # check for bullets that have hit aliens, remove bullet and alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """Create a fleet of aliens"""
        # create an alien and keep adding aliens until there is no room left
        # spacing is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        self._check_aliens_bottom()
        
        

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _ship_hit(self):
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
        
            self.bullets.empty()
            self.aliens.empty()
        
            self._create_fleet()
            self.ship.center_ship()
            
            sleep(0.5)
        else:
            self.game_active = False
        
    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
                


if __name__ == "__main__":
    # Make a game instance and run game
    ai = AlienInvasion()
    ai.run_game()
