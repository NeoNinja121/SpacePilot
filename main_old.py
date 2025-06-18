#!/usr/bin/env python3
"""
Idle Space Adventure - Main Game Loop
For Raspberry Pi Zero 2 with Display HAT Mini
"""

import os
os.environ["SDL_VIDEODRIVER"] = "fbcon"
os.environ["SDL_FBDEV"] = "/dev/fb0"

import sys
import json
import time
import pygame
from pygame.locals import *

# Import game modules
from game.constants import *
from game.ship import Ship
from game.events import EventGenerator, Event
from game.display_config import detect_display, DisplayConfig
from game.sprites import Spaceship
from game.ui import StatusBar, EventDisplay, ButtonBar, MilestoneDisplay
from game.gpio_handler import GPIOHandler

# Initialize pygame
pygame.init()
pygame.mouse.set_visible(False)

class IdleSpaceAdventure:
    """Main game class for Idle Space Adventure"""
    
    def __init__(self):
        # Detect display type and configure
        self.display_config = detect_display()
        
        # Set up display surface based on configuration
        self.screen = pygame.display.set_mode(
            (self.display_config.width, self.display_config.height),
            pygame.FULLSCREEN if self.display_config.fullscreen else 0
        )
        pygame.display.set_caption("Idle Space Adventure")
        
        # Set up clock
        self.clock = pygame.time.Clock()
        
        # Initialize game state
        self.init_game_state()
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        
        # Create spaceship
        self.spaceship = Spaceship(
            self.display_config.width // 2,
            self.display_config.height // 2,
            self.game_state["ship"],
            self.game_state["damaged_systems"],
            small_display=self.display_config.is_display_hat_mini
        )
        self.all_sprites.add(self.spaceship)
        
        # Create UI components
        self.status_bar = StatusBar(
            self.display_config, 
            self.game_state["ship"]["speed"],
            self.game_state["boost_active"],
            self.game_state["boost_points"],
            self.game_state["repair_points"],
            self.game_state["damaged_systems"]
        )
        
        self.button_bar = ButtonBar(
            self.display_config,
            self.game_state["boost_points"],
            self.game_state["boost_active"],
            self.game_state["repair_points"],
            len(self.game_state["damaged_systems"]),
            self.game_state["active_event"] is not None
        )
        
        self.event_display = None
        if self.game_state["active_event"]:
            self.event_display = EventDisplay(
                self.display_config, 
                self.game_state["active_event"]
            )
            
        self.milestone_display = None
        
        # Set up event generator
        self.event_generator = EventGenerator()
        
        # Set up GPIO handler for buttons if on Raspberry Pi
        try:
            self.gpio_handler = GPIOHandler(self.handle_button_press)
            print("GPIO handler initialized successfully")
        except ImportError:
            self.gpio_handler = None
            print("GPIO module not available - running in desktop mode")
        
        # Initialize star field
        self.init_stars()
        
        # Load game state from file
        self.load_game_state()
        
        # Set initial time for event generation
        self.last_update_time = time.time()
        self.last_save_time = time.time()
        self.last_event_time = time.time()
        
    def init_game_state(self):
        """Initialize default game state"""
        self.game_state = {
            "distance": 0,
            "dark_matter": 100,
            "ship": {
                "engine": [
                    {
                        "id": "engine-left",
                        "name": "Left Engine",
                        "level": 1,
                        "max_level": 10,
                        "cost": 150,
                        "description": "Powers the left side of your ship",
                        "effect": "Increases speed by 10% per level"
                    },
                    {
                        "id": "engine-right",
                        "name": "Right Engine",
                        "level": 1,
                        "max_level": 10,
                        "cost": 150,
                        "description": "Powers the right side of your ship",
                        "effect": "Increases speed by 10% per level"
                    },
                ],
                "hull": [
                    {
                        "id": "hull-upper",
                        "name": "Upper Hull",
                        "level": 1,
                        "max_level": 10,
                        "cost": 200,
                        "description": "Protects the top of your ship",
                        "effect": "Increases storage by 15% per level"
                    },
                    {
                        "id": "hull-lower",
                        "name": "Lower Hull",
                        "level": 1,
                        "max_level": 10,
                        "cost": 200,
                        "description": "Protects the bottom of your ship",
                        "effect": "Increases storage by 15% per level"
                    },
                ],
                "cabin": {
                    "id": "cabin",
                    "name": "Pilot Cabin",
                    "level": 1,
                    "max_level": 10,
                    "cost": 300,
                    "description": "Where you live and control the ship",
                    "effect": "Increases durability by 20% per level"
                },
                "weapon": {
                    "id": "weapon",
                    "name": "Defense System",
                    "level": 1,
                    "max_level": 10,
                    "cost": 250,
                    "description": "Your ship's defensive capabilities",
                    "effect": "Increases luck by 5% per level"
                },
                "speed": SHIP_BASE_SPEED,
                "storage_capacity": SHIP_BASE_STORAGE,
                "durability": SHIP_BASE_DURABILITY,
                "luck": SHIP_BASE_LUCK,
            },
            "events": [],
            "active_event": None,
            "last_event_time": time.time(),
            "boost_active": False,
            "boost_end_time": 0,
            "damaged_systems": [],
            "repair_points": 3,
            "boost_points": 5,
            "last_milestone": None
        }
        
    def init_stars(self):
        """Initialize star field backgrounds"""
        # Create stars for different parallax layers
        self.small_stars = []
        self.medium_stars = []
        self.large_stars = []
        
        # Number of stars in each layer (reduced for Display HAT Mini)
        small_count = 20 if self.display_config.is_display_hat_mini else 50
        medium_count = 10 if self.display_config.is_display_hat_mini else 25
        large_count = 0 if self.display_config.is_display_hat_mini else 15
        
        # Generate random star positions
        for _ in range(small_count):
            x = pygame.time.get_ticks() % self.display_config.width
            y = pygame.time.get_ticks() % self.display_config.height
            self.small_stars.append({
                'pos': [x, y],
                'speed': 0.2,
                'size': 1,
                'color': (200, 200, 200)
            })
            
        for _ in range(medium_count):
            x = pygame.time.get_ticks() % self.display_config.width
            y = pygame.time.get_ticks() % self.display_config.height
            self.medium_stars.append({
                'pos': [x, y],
                'speed': 0.5,
                'size': 2,
                'color': (230, 230, 255)
            })
            
        for _ in range(large_count):
            x = pygame.time.get_ticks() % self.display_config.width
            y = pygame.time.get_ticks() % self.display_config.height
            self.large_stars.append({
                'pos': [x, y],
                'speed': 1.0,
                'size': 3,
                'color': (255, 255, 255)
            })
            
    def save_game_state(self):
        """Save the current game state to a file"""
        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
            
        # Remove active event before saving
        save_state = self.game_state.copy()
        save_state['active_event'] = None
        
        # Save to file
        with open('data/game_state.json', 'w') as f:
            json.dump(save_state, f)
            
    def load_game_state(self):
        """Load game state from a file if available"""
        try:
            if os.path.exists('data/game_state.json'):
                with open('data/game_state.json', 'r') as f:
                    loaded_state = json.load(f)
                    # Update the current state with loaded values
                    self.game_state.update(loaded_state)
                    # Update spaceship with loaded state
                    self.spaceship.update_state(
                        self.game_state["ship"],
                        self.game_state["damaged_systems"],
                        self.game_state["boost_active"]
                    )
                    print("Game state loaded successfully")
        except Exception as e:
            print(f"Error loading game state: {e}")
            
    def handle_button_press(self, button_index):
        """Handle button presses from GPIO or keyboard"""
        if self.game_state["active_event"]:
            # During event, buttons 3 and 4 are used for yes/no
            if button_index == 2:  # YES
                self.handle_event_response(True)
            elif button_index == 3:  # NO
                self.handle_event_response(False)
        else:
            # Outside events, buttons have standard functions
            if button_index == 0:  # BOOST
                if (self.game_state["boost_points"] > 0 and 
                        not self.game_state["boost_active"]):
                    # Activate boost
                    self.game_state["boost_active"] = True
                    self.game_state["boost_end_time"] = time.time() + BOOST_DURATION / 1000
                    self.game_state["boost_points"] -= 1
                    self.spaceship.set_boost(True)
            elif button_index == 1:  # REPAIR
                if (self.game_state["repair_points"] > 0 and 
                        len(self.game_state["damaged_systems"]) > 0):
                    # Remove one damaged system
                    self.game_state["damaged_systems"].pop()
                    self.game_state["repair_points"] -= 1
                    self.spaceship.update_damaged_systems(self.game_state["damaged_systems"])
                    
        # Update the button display
        self.button_bar.update(
            self.game_state["boost_points"],
            self.game_state["boost_active"],
            self.game_state["repair_points"],
            len(self.game_state["damaged_systems"]),
            self.game_state["active_event"] is not None
        )
                    
    def handle_event_response(self, is_yes):
        """Handle player response to an event"""
        if not self.game_state["active_event"]:
            return
            
        event = self.game_state["active_event"]
        
        # Apply event effects based on response
        if is_yes and event.options and len(event.options) > 0:
            # Apply "Yes" option effects
            option = event.options[0]
            self.game_state["dark_matter"] += option["dark_matter_reward"]
            self.game_state["distance"] += option["distance_effect"]
            
            # Add part reward if available
            if "part_reward" in option and option["part_reward"]:
                pass  # Would handle part upgrades here
                
        elif not is_yes and event.options and len(event.options) > 1:
            # Apply "No" option effects
            option = event.options[1]
            self.game_state["dark_matter"] += option["dark_matter_reward"]
            self.game_state["distance"] += option["distance_effect"]
            
        # Mark event as resolved and add to history
        event.resolved = True
        event.outcome = "accepted" if is_yes else "declined"
        
        # Add to event history
        self.game_state["events"].append(event)
        
        # Clear active event
        self.game_state["active_event"] = None
        self.event_display = None
                    
    def update_ship_stats(self):
        """Update ship statistics based on part levels"""
        ship = self.game_state["ship"]
        
        # Calculate engine speed bonus (10% per level for each engine)
        engine_levels = sum(engine["level"] for engine in ship["engine"])
        engine_multiplier = 1 + (engine_levels * 0.1)
        ship["speed"] = int(SHIP_BASE_SPEED * engine_multiplier)
        
        # Calculate hull storage bonus (15% per level for each hull part)
        hull_levels = sum(hull["level"] for hull in ship["hull"])
        storage_multiplier = 1 + (hull_levels * 0.15)
        ship["storage_capacity"] = int(SHIP_BASE_STORAGE * storage_multiplier)
        
        # Calculate cabin durability bonus (20% per level)
        durability_multiplier = 1 + (ship["cabin"]["level"] * 0.2)
        ship["durability"] = int(SHIP_BASE_DURABILITY * durability_multiplier)
        
        # Calculate weapon luck bonus (5% per level)
        luck_multiplier = 1 + (ship["weapon"]["level"] * 0.05)
        ship["luck"] = int(SHIP_BASE_LUCK * luck_multiplier)
        
        # Update spaceship with new stats
        self.spaceship.ship_data = ship
            
    def check_milestones(self):
        """Check if the player has reached a new milestone"""
        distance = self.game_state["distance"]
        
        # Check each milestone
        if (self.game_state["last_milestone"] != "MOON" and 
                distance >= DISTANCE_EARTH_TO_MOON):
            self.show_milestone("MOON")
            self.game_state["last_milestone"] = "MOON"
        elif (self.game_state["last_milestone"] != "MARS" and 
                distance >= DISTANCE_EARTH_TO_MARS):
            self.show_milestone("MARS")
            self.game_state["last_milestone"] = "MARS"
        elif (self.game_state["last_milestone"] != "JUPITER" and 
                distance >= DISTANCE_EARTH_TO_JUPITER):
            self.show_milestone("JUPITER")
            self.game_state["last_milestone"] = "JUPITER"
        elif (self.game_state["last_milestone"] != "SATURN" and 
                distance >= DISTANCE_EARTH_TO_SATURN):
            self.show_milestone("SATURN")
            self.game_state["last_milestone"] = "SATURN"
        elif (self.game_state["last_milestone"] != "URANUS" and 
                distance >= DISTANCE_EARTH_TO_URANUS):
            self.show_milestone("URANUS")
            self.game_state["last_milestone"] = "URANUS"
        elif (self.game_state["last_milestone"] != "NEPTUNE" and 
                distance >= DISTANCE_EARTH_TO_NEPTUNE):
            self.show_milestone("NEPTUNE")
            self.game_state["last_milestone"] = "NEPTUNE"
        elif (self.game_state["last_milestone"] != "PLUTO" and 
                distance >= DISTANCE_EARTH_TO_PLUTO):
            self.show_milestone("PLUTO")
            self.game_state["last_milestone"] = "PLUTO"
        elif (self.game_state["last_milestone"] != "INTERSTELLAR" and 
                distance >= DISTANCE_EARTH_TO_INTERSTELLAR):
            self.show_milestone("INTERSTELLAR SPACE")
            self.game_state["last_milestone"] = "INTERSTELLAR"
            
    def show_milestone(self, milestone_name):
        """Show a milestone notification"""
        self.milestone_display = MilestoneDisplay(
            self.display_config,
            milestone_name
        )
        
    def process_event_generation(self):
        """Check if it's time to generate a new event"""
        now = time.time()
        
        # Only generate events if no active event
        if (self.game_state["active_event"] is None and 
                now - self.game_state["last_event_time"] >= EVENT_INTERVAL / 1000):
            # Generate new event
            new_event = self.event_generator.generate_event()
            
            # Set as active event
            self.game_state["active_event"] = new_event
            self.game_state["last_event_time"] = now
            
            # Create event display
            self.event_display = EventDisplay(
                self.display_config,
                new_event
            )
            
            # Update button bar
            self.button_bar.update(
                self.game_state["boost_points"],
                self.game_state["boost_active"],
                self.game_state["repair_points"],
                len(self.game_state["damaged_systems"]),
                True
            )
            
    def update_stars(self):
        """Update star positions for parallax effect"""
        # Move stars based on ship speed
        speed_factor = 2 if self.game_state["boost_active"] else 1
        
        # Update small stars (slow movement)
        for star in self.small_stars:
            star['pos'][0] -= star['speed'] * speed_factor
            if star['pos'][0] < 0:
                star['pos'][0] = self.display_config.width
                star['pos'][1] = pygame.time.get_ticks() % self.display_config.height
                
        # Update medium stars (medium movement)
        for star in self.medium_stars:
            star['pos'][0] -= star['speed'] * speed_factor
            if star['pos'][0] < 0:
                star['pos'][0] = self.display_config.width
                star['pos'][1] = pygame.time.get_ticks() % self.display_config.height
                
        # Update large stars (fast movement)
        for star in self.large_stars:
            star['pos'][0] -= star['speed'] * speed_factor
            if star['pos'][0] < 0:
                star['pos'][0] = self.display_config.width
                star['pos'][1] = pygame.time.get_ticks() % self.display_config.height
                
    def update(self):
        """Update game state"""
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now
        
        # Calculate current speed including boosts
        current_speed = self.game_state["ship"]["speed"]
        if self.game_state["boost_active"]:
            if now < self.game_state["boost_end_time"]:
                current_speed *= 2  # Double speed during boost
            else:
                # End boost if time is up
                self.game_state["boost_active"] = False
                self.spaceship.set_boost(False)
                
        # Add distance based on speed
        self.game_state["distance"] += current_speed * dt / 10
        
        # Passive Dark Matter collection (1 per second)
        dark_matter_gain = 0.1 * dt
        self.game_state["dark_matter"] = min(
            self.game_state["dark_matter"] + dark_matter_gain,
            self.game_state["ship"]["storage_capacity"]
        )
        
        # Check for events
        self.process_event_generation()
        
        # Check for milestones
        self.check_milestones()
        
        # Update stars for parallax effect
        self.update_stars()
        
        # Update all sprites
        self.all_sprites.update()
        
        # Update status bar
        self.status_bar.update(
            self.game_state["ship"]["speed"],
            self.game_state["boost_active"],
            self.game_state["boost_points"],
            self.game_state["repair_points"],
            self.game_state["damaged_systems"]
        )
        
        # Save game state periodically (every 10 seconds)
        if now - self.last_save_time > 10:
            self.save_game_state()
            self.last_save_time = now
            
        # Clear milestone display after 5 seconds
        if self.milestone_display and now - self.milestone_display.create_time > 5:
            self.milestone_display = None
            
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.save_game_state()
                return False
                
            # Handle keyboard input
            if event.type == KEYDOWN:
                if event.key == K_1 or event.key == K_q:
                    self.handle_button_press(0)  # Boost
                elif event.key == K_2 or event.key == K_w:
                    self.handle_button_press(1)  # Repair
                elif event.key == K_3 or event.key == K_e:
                    self.handle_button_press(2)  # Yes
                elif event.key == K_4 or event.key == K_r:
                    self.handle_button_press(3)  # No
                    
        return True
        
    def draw(self):
        """Draw the game screen"""
        # Clear the screen
        self.screen.fill((0, 0, 0))
        
        # Draw stars
        for star in self.small_stars:
            pygame.draw.circle(
                self.screen, 
                star['color'], 
                (int(star['pos'][0]), int(star['pos'][1])), 
                star['size']
            )
            
        for star in self.medium_stars:
            pygame.draw.circle(
                self.screen, 
                star['color'], 
                (int(star['pos'][0]), int(star['pos'][1])), 
                star['size']
            )
            
        for star in self.large_stars:
            pygame.draw.circle(
                self.screen, 
                star['color'], 
                (int(star['pos'][0]), int(star['pos'][1])), 
                star['size']
            )
            
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw UI elements
        self.status_bar.draw(self.screen)
        self.button_bar.draw(self.screen)
        
        # Draw event display if active
        if self.event_display:
            self.event_display.draw(self.screen)
            
        # Draw milestone display if active
        if self.milestone_display:
            self.milestone_display.draw(self.screen)
            
        # Draw header with stats
        self.draw_header()
        
        # Update the display
        pygame.display.flip()
        
    def draw_header(self):
        """Draw the header with game stats"""
        # Set up font
        font_size = 14 if not self.display_config.is_display_hat_mini else 10
        font = pygame.font.SysFont('monospace', font_size)
        
        # Format distance
        if self.game_state["distance"] < 1000:
            distance_text = f"{int(self.game_state['distance'])} mi"
        elif self.game_state["distance"] < 1000000:
            distance_text = f"{self.game_state['distance']/1000:.1f} km"
        elif self.game_state["distance"] < DISTANCE_EARTH_TO_INTERSTELLAR:
            distance_text = f"{self.game_state['distance']/1000000:.2f} M mi"
        else:
            distance_text = f"{self.game_state['distance']/DISTANCE_EARTH_TO_INTERSTELLAR:.4f} ly"
            
        # Create text surfaces
        distance_surf = font.render(f"Dist: {distance_text}", True, (0, 255, 0))
        dark_matter_surf = font.render(
            f"{DARK_MATTER_SYMBOL}: {int(self.game_state['dark_matter'])}", 
            True, 
            (0, 255, 0)
        )
        
        # Draw header background
        header_height = 20 if not self.display_config.is_display_hat_mini else 16
        pygame.draw.rect(
            self.screen, 
            (0, 0, 0), 
            (0, 0, self.display_config.width, header_height)
        )
        pygame.draw.line(
            self.screen, 
            (0, 100, 0), 
            (0, header_height), 
            (self.display_config.width, header_height)
        )
        
        # Draw text
        self.screen.blit(distance_surf, (5, 4))
        self.screen.blit(
            dark_matter_surf, 
            (self.display_config.width - dark_matter_surf.get_width() - 5, 4)
        )
        
    def run(self):
        """Main game loop"""
        running = True
        try:
            while running:
                # Handle events
                running = self.handle_events()
                
                # Update game state
                self.update()
                
                # Draw everything
                self.draw()
                
                # Cap the framerate
                self.clock.tick(30)
                
        except KeyboardInterrupt:
            pass
        finally:
            # Save game state before exiting
            self.save_game_state()
            
            # Clean up resources
            if self.gpio_handler:
                self.gpio_handler.cleanup()
                
            pygame.quit()
            
if __name__ == "__main__":
    game = IdleSpaceAdventure()
    game.run()
