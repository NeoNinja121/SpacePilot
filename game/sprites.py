"""
Game sprites for Idle Space Adventure
"""
import pygame
import math
import random
from game.constants import *

class Spaceship(pygame.sprite.Sprite):
    """Spaceship sprite for the player"""
    
    def __init__(self, x, y, ship_data, damaged_systems=None, small_display=False):
        """Initialize the spaceship sprite"""
        super().__init__()
        
        # Store ship data and state
        self.ship_data = ship_data
        self.damaged_systems = damaged_systems or []
        self.boost_active = False
        self.thruster_frame = 0
        self.frame_counter = 0
        self.small_display = small_display
        
        # Set scale based on display size
        self.scale = 0.7 if small_display else 1.0
        
        # Create the base image
        self.create_ship_image()
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def create_ship_image(self):
        """Create the ship image with all parts"""
        # Size calculations
        hull_width = int(64 * self.scale)
        hull_height = int(32 * self.scale)
        cabin_size = int(24 * self.scale)
        engine_width = int(32 * self.scale)
        engine_height = int(16 * self.scale)
        
        # Create a surface for the ship
        ship_width = int(96 * self.scale)
        ship_height = int(64 * self.scale)
        self.image = pygame.Surface((ship_width, ship_height), pygame.SRCALPHA)
        
        # Draw hull (main body)
        hull_color = (70, 70, 70) if "hull-upper" not in self.damaged_systems else (150, 50, 50)
        hull_border = (100, 100, 100) if "hull-upper" not in self.damaged_systems else (200, 0, 0)
        pygame.draw.rect(
            self.image, 
            hull_color, 
            (
                (ship_width - hull_width) // 2, 
                (ship_height - hull_height) // 2, 
                hull_width, 
                hull_height
            ),
            0, 
            border_radius=int(5 * self.scale)
        )
        pygame.draw.rect(
            self.image, 
            hull_border, 
            (
                (ship_width - hull_width) // 2, 
                (ship_height - hull_height) // 2, 
                hull_width, 
                hull_height
            ),
            int(2 * self.scale), 
            border_radius=int(5 * self.scale)
        )
        
        # Draw cabin
        cabin_color = (80, 80, 80) if "cabin" not in self.damaged_systems else (150, 50, 50)
        cabin_border = (100, 100, 100) if "cabin" not in self.damaged_systems else (200, 0, 0)
        pygame.draw.circle(
            self.image, 
            cabin_color, 
            (ship_width // 2, ship_height // 3), 
            cabin_size // 2
        )
        pygame.draw.circle(
            self.image, 
            cabin_border, 
            (ship_width // 2, ship_height // 3), 
            cabin_size // 2, 
            int(2 * self.scale)
        )
        
        # Draw cabin window
        pygame.draw.circle(
            self.image, 
            (100, 150, 255), 
            (ship_width // 2, ship_height // 3), 
            cabin_size // 3
        )
        
        # Draw pilot silhouette
        pygame.draw.rect(
            self.image, 
            (0, 0, 0), 
            (
                ship_width // 2 - int(4 * self.scale), 
                ship_height // 3, 
                int(8 * self.scale), 
                int(6 * self.scale)
            ),
            0, 
            border_radius=int(4 * self.scale)
        )
        
        # Draw left engine
        engine_left_color = (70, 70, 70) if "engine-left" not in self.damaged_systems else (150, 50, 50)
        engine_left_border = (100, 100, 100) if "engine-left" not in self.damaged_systems else (200, 0, 0)
        pygame.draw.rect(
            self.image, 
            engine_left_color, 
            (
                (ship_width - hull_width) // 2 - engine_width // 2, 
                ship_height // 2, 
                engine_width // 2, 
                engine_height
            ),
            0, 
            border_radius=int(3 * self.scale)
        )
        pygame.draw.rect(
            self.image, 
            engine_left_border, 
            (
                (ship_width - hull_width) // 2 - engine_width // 2, 
                ship_height // 2, 
                engine_width // 2, 
                engine_height
            ),
            int(1 * self.scale), 
            border_radius=int(3 * self.scale)
        )
        
        # Draw right engine
        engine_right_color = (70, 70, 70) if "engine-right" not in self.damaged_systems else (150, 50, 50)
        engine_right_border = (100, 100, 100) if "engine-right" not in self.damaged_systems else (200, 0, 0)
        pygame.draw.rect(
            self.image, 
            engine_right_color, 
            (
                (ship_width + hull_width) // 2, 
                ship_height // 2, 
                engine_width // 2, 
                engine_height
            ),
            0, 
            border_radius=int(3 * self.scale)
        )
        pygame.draw.rect(
            self.image, 
            engine_right_border, 
            (
                (ship_width + hull_width) // 2, 
                ship_height // 2, 
                engine_width // 2, 
                engine_height
            ),
            int(1 * self.scale), 
            border_radius=int(3 * self.scale)
        )
        
        # Draw weapon
        weapon_color = (60, 60, 60) if "weapon" not in self.damaged_systems else (150, 50, 50)
        weapon_border = (90, 90, 90) if "weapon" not in self.damaged_systems else (200, 0, 0)
        pygame.draw.rect(
            self.image, 
            weapon_color, 
            (
                ship_width // 2 - int(8 * self.scale), 
                ship_height - int(12 * self.scale), 
                int(16 * self.scale), 
                int(6 * self.scale)
            ),
            0, 
            border_radius=int(2 * self.scale)
        )
        pygame.draw.rect(
            self.image, 
            weapon_border, 
            (
                ship_width // 2 - int(8 * self.scale), 
                ship_height - int(12 * self.scale), 
                int(16 * self.scale), 
                int(6 * self.scale)
            ),
            int(1 * self.scale), 
            border_radius=int(2 * self.scale)
        )
        
        # Draw thrusters if engines aren't damaged
        if "engine-left" not in self.damaged_systems:
            self.draw_thruster(
                (ship_width - hull_width) // 2 - int(8 * self.scale),
                ship_height // 2 + engine_height // 2,
                "left"
            )
            
        if "engine-right" not in self.damaged_systems:
            self.draw_thruster(
                (ship_width + hull_width) // 2 + int(8 * self.scale),
                ship_height // 2 + engine_height // 2,
                "right"
            )
            
        # Draw boost effect if active
        if self.boost_active:
            self.draw_boost_effect()
            
    def draw_thruster(self, x, y, side):
        """Draw thruster flames for the engines"""
        # Determine flame size based on animation frame
        if self.thruster_frame == 0:
            size = int(6 * self.scale)
        elif self.thruster_frame == 1:
            size = int(8 * self.scale)
        elif self.thruster_frame == 2:
            size = int(10 * self.scale)
        else:
            size = int(7 * self.scale)
            
        # Draw flame
        color = (255, 165, 0) if not self.boost_active else (255, 255, 0)
        
        if side == "left":
            # Triangle pointing left
            points = [
                (x, y),
                (x - size, y - size // 2),
                (x - size, y + size // 2)
            ]
        else:
            # Triangle pointing right
            points = [
                (x, y),
                (x + size, y - size // 2),
                (x + size, y + size // 2)
            ]
            
        pygame.draw.polygon(self.image, color, points)
        
    def draw_boost_effect(self):
        """Draw boost particle effects"""
        ship_width = self.image.get_width()
        ship_height = self.image.get_height()
        
        # Draw multiple particles in a row behind the ship
        for i in range(5):
            # Vary the size and position slightly
            size = int((5 - i) * self.scale) + random.randint(0, 2)
            offset_y = random.randint(-4, 4)
            
            # Calculate position (left side of ship, random vertical position)
            x = int(ship_width * 0.2) - (i * int(5 * self.scale))
            y = (ship_height // 2) + offset_y
            
            # Draw particle
            alpha = 180 - (i * 30)  # Fade out with distance
            color = (255, 255, 0, alpha)
            
            # Create a surface with per-pixel alpha
            particle = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(particle, color, (size // 2, size // 2), size // 2)
            
            # Blit the particle onto the ship image
            self.image.blit(particle, (x, y))
            
    def update(self):
        """Update the spaceship animation"""
        self.frame_counter += 1
        
        # Update thruster animation every few frames
        if self.frame_counter % (5 if not self.boost_active else 3) == 0:
            self.thruster_frame = (self.thruster_frame + 1) % 4
            self.create_ship_image()  # Redraw the ship with updated thruster
            
    def set_boost(self, active):
        """Set boost state"""
        self.boost_active = active
        self.create_ship_image()
        
    def update_damaged_systems(self, damaged_systems):
        """Update the list of damaged systems"""
        self.damaged_systems = damaged_systems
        self.create_ship_image()
        
    def update_state(self, ship_data, damaged_systems, boost_active):
        """Update all ship state variables"""
        self.ship_data = ship_data
        self.damaged_systems = damaged_systems
        self.boost_active = boost_active
        self.create_ship_image()
