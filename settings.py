class Settings:
    """A class to store all general settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (6, 25, 58)

        # ship settings
        self.ship_speed = 2
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (211, 211, 211)
        self.bullets_allowed = 3
        
        # alien settings 
        self.alien_speed = 1
        self.fleet_drop_speed = 10
        # fleet direction; 1 is right -1 is left 
        self.fleet_direction = 1
        
