"""
Event system for Idle Space Adventure
"""
import random
import time
from game.constants import (
    EVENT_TYPE_EVERYDAY, EVENT_TYPE_RARE, 
    EVENT_TYPE_COSMIC, EVENT_TYPE_EASTER_EGG
)

class Event:
    """Game event class"""
    
    def __init__(self, event_id, event_type, title, description, 
                 options=None, requires_input=True):
        """Initialize event"""
        self.id = event_id or f"event-{int(time.time())}-{random.randint(0, 999)}"
        self.type = event_type
        self.title = title
        self.description = description
        self.options = options or []
        self.requires_input = requires_input
        self.timestamp = time.time()
        self.resolved = False
        self.outcome = None

class EventGenerator:
    """Generator for random game events"""
    
    def __init__(self):
        """Initialize event pools"""
        # Event content pools
        self.everyday_events = [
            {
                "title": "Space Debris",
                "description": "A small cluster of space debris approaches your ship. Attempt evasive maneuvers?",
                "options": [
                    {
                        "text": "Evade",
                        "effect": "Slight course change, minor fuel consumption",
                        "success_rate": 80,
                        "dark_matter_reward": 10,
                        "distance_effect": 0,
                    },
                    {
                        "text": "Ignore",
                        "effect": "Risk of hull damage",
                        "success_rate": 40,
                        "dark_matter_reward": 0,
                        "distance_effect": -50,
                    },
                ],
            },
            {
                "title": "Stray Cat in EVA Suit",
                "description": "You spot a cat floating by in a tiny EVA suit. Its collar says 'Whiskers'. Take it aboard?",
                "options": [
                    {
                        "text": "Rescue cat",
                        "effect": "New ship companion, occasional distractions",
                        "success_rate": 100,
                        "dark_matter_reward": 30,
                        "distance_effect": 0,
                    },
                    {
                        "text": "Let it float by",
                        "effect": "Such is space life",
                        "success_rate": 100,
                        "dark_matter_reward": 0,
                        "distance_effect": 0,
                    },
                ],
            },
            {
                "title": "Junk Transmission",
                "description": "Your comms pick up a strange signal. It sounds like... 80s synth music?",
                "options": [
                    {
                        "text": "Boost signal",
                        "effect": "Dance party for one",
                        "success_rate": 100,
                        "dark_matter_reward": 5,
                        "distance_effect": 0,
                    },
                    {
                        "text": "Ignore",
                        "effect": "You'll never know what bangers you missed",
                        "success_rate": 100,
                        "dark_matter_reward": 0,
                        "distance_effect": 0,
                    },
                ],
            },
            {
                "title": "Minor Course Correction",
                "description": "Navigation computer suggests a minor course correction to optimize route.",
                "options": [
                    {
                        "text": "Adjust course",
                        "effect": "Optimize travel path",
                        "success_rate": 100,
                        "dark_matter_reward": 0,
                        "distance_effect": 150,
                    },
                    {
                        "text": "Keep current course",
                        "effect": "Stay on the longer route",
                        "success_rate": 100,
                        "dark_matter_reward": 5,
                        "distance_effect": 0,
                    },
                ],
            },
        ]

        self.rare_events = [
            {
                "title": "Derelict Ship",
                "description": "You encounter a abandoned vessel drifting through space. It looks salvageable.",
                "options": [
                    {
                        "text": "Salvage parts",
                        "effect": "Risk but potential reward",
                        "success_rate": 60,
                        "dark_matter_reward": 80,
                        "distance_effect": -100,
                        "part_reward": "hull-upper",
                    },
                    {
                        "text": "Leave it alone",
                        "effect": "Safer option",
                        "success_rate": 100,
                        "dark_matter_reward": 0,
                        "distance_effect": 0,
                    },
                ],
            },
            {
                "title": "Space Station",
                "description": "A small research station appears on your scanners. They're hailing you.",
                "options": [
                    {
                        "text": "Dock and trade",
                        "effect": "Exchange resources",
                        "success_rate": 90,
                        "dark_matter_reward": 50,
                        "distance_effect": -200,
                    },
                    {
                        "text": "Decline and continue",
                        "effect": "Maintain current course",
                        "success_rate": 100,
                        "dark_matter_reward": 0,
                        "distance_effect": 100,
                    },
                ],
            },
            {
                "title": "Drifting Manga Collection",
                "description": "A sealed container floats by with 'Property of ISS Recreation Dept' labeled on it. Inside appear to be vintage manga comics.",
                "options": [
                    {
                        "text": "Collect and read",
                        "effect": "Entertainment boost",
                        "success_rate": 100,
                        "dark_matter_reward": 25,
                        "distance_effect": 0,
                    },
                    {
                        "text": "Leave it",
                        "effect": "Stay focused on your mission",
                        "success_rate": 100,
                        "dark_matter_reward": 0,
                        "distance_effect": 50,
                    },
                ],
            },
        ]

        self.cosmic_events = [
            {
                "title": "Wormhole Detected",
                "description": "Sensors detect a small wormhole forming nearby. It could be a shortcut... or a trap.",
                "options": [
                    {
                        "text": "Enter wormhole",
                        "effect": "High risk, high reward",
                        "success_rate": 40,
                        "dark_matter_reward": 200,
                        "distance_effect": 2000,
                    },
                    {
                        "text": "Avoid wormhole",
                        "effect": "Safe but slower",
                        "success_rate": 100,
                        "dark_matter_reward": 0,
                        "distance_effect": 0,
                    },
                ],
            },
            {
                "title": "Black Hole Proximity",
                "description": "Your ship is being pulled toward a small black hole. Engines straining!",
                "options": [
                    {
                        "text": "Full power to engines",
                        "effect": "Try to escape gravitational pull",
                        "success_rate": 60,
                        "dark_matter_reward": 0,
                        "distance_effect": -500,
                    },
                    {
                        "text": "Slingshot maneuver",
                        "effect": "Use gravity to boost speed",
                        "success_rate": 30,
                        "dark_matter_reward": 100,
                        "distance_effect": 1000,
                    },
                ],
            },
            {
                "title": "Space Kaiju",
                "description": "An enormous creature that resembles a classic movie monster drifts past your ship. It seems to be asleep.",
                "options": [
                    {
                        "text": "Take samples",
                        "effect": "Scientific discovery",
                        "success_rate": 50,
                        "dark_matter_reward": 150,
                        "distance_effect": -300,
                    },
                    {
                        "text": "Quietly pass by",
                        "effect": "Don't wake the kaiju!",
                        "success_rate": 90,
                        "dark_matter_reward": 0,
                        "distance_effect": 0,
                    },
                ],
            },
            {
                "title": "AI Megastructure",
                "description": "You encounter what appears to be a massive computing structure built by an ancient AI civilization.",
                "options": [
                    {
                        "text": "Connect to network",
                        "effect": "Download data",
                        "success_rate": 70,
                        "dark_matter_reward": 250,
                        "distance_effect": 0,
                    },
                    {
                        "text": "Keep distance",
                        "effect": "Avoid potential AI conflicts",
                        "success_rate": 100,
                        "dark_matter_reward": 0,
                        "distance_effect": 100,
                    },
                ],
            },
        ]

        self.easter_egg_events = [
            {
                "title": "Space Invaders",
                "description": "A formation of pixelated alien ships approaches in a suspiciously familiar pattern...",
                "options": [
                    {
                        "text": "Fire pixel cannons",
                        "effect": "Pew pew!",
                        "success_rate": 75,
                        "dark_matter_reward": 80,
                        "distance_effect": 0,
                    },
                    {
                        "text": "Hide behind asteroid",
                        "effect": "Wait for them to pass",
                        "success_rate": 100,
                        "dark_matter_reward": 0,
                        "distance_effect": -100,
                    },
                ],
            },
            {
                "title": "Monolith Detection",
                "description": "A sleek black monolith floats in space accompanied by classical music.",
                "options": [
                    {
                        "text": "Touch it",
                        "effect": "Evolutionary leap?",
                        "success_rate": 50,
                        "dark_matter_reward": 200,
                        "distance_effect": 1000,
                    },
                    {
                        "text": "Just appreciate from afar",
                        "effect": "It's full of stars!",
                        "success_rate": 100,
                        "dark_matter_reward": 20,
                        "distance_effect": 0,
                    },
                ],
            },
            {
                "title": "Debug Console",
                "description": "Your ship computer glitches, revealing what appears to be developer debug tools. A message reads: 'Hello player, having fun?'",
                "options": [
                    {
                        "text": "Type 'Yes'",
                        "effect": "Developer Easter Egg",
                        "success_rate": 100,
                        "dark_matter_reward": 42,
                        "distance_effect": 0,
                    },
                    {
                        "text": "Close console",
                        "effect": "Return to normal operations",
                        "success_rate": 100,
                        "dark_matter_reward": 0,
                        "distance_effect": 0,
                    },
                ],
            },
            {
                "title": "Red Pill, Blue Pill",
                "description": "A strange transmission asks if you'd like to know how deep the rabbit hole goes.",
                "options": [
                    {
                        "text": "Red Pill",
                        "effect": "The truth",
                        "success_rate": 100,
                        "dark_matter_reward": 101,
                        "distance_effect": -300,
                    },
                    {
                        "text": "Blue Pill",
                        "effect": "Blissful ignorance",
                        "success_rate": 100,
                        "dark_matter_reward": 0,
                        "distance_effect": 300,
                    },
                ],
            },
        ]
        
    def generate_event(self):
        """
        Generate a random event based on rarity weightings
        Returns an Event object
        """
        # Determine event type based on rarity
        rng = random.random() * 100
        
        if rng < 70:
            # 70% chance of everyday event
            event_type = EVENT_TYPE_EVERYDAY
            event_pool = self.everyday_events
        elif rng < 90:
            # 20% chance of rare event
            event_type = EVENT_TYPE_RARE
            event_pool = self.rare_events
        elif rng < 98:
            # 8% chance of cosmic event
            event_type = EVENT_TYPE_COSMIC
            event_pool = self.cosmic_events
        else:
            # 2% chance of easter egg event
            event_type = EVENT_TYPE_EASTER_EGG
            event_pool = self.easter_egg_events
            
        # Pick a random event from the selected pool
        event_template = random.choice(event_pool)
        
        # Create event object
        event = Event(
            event_id=None,  # Auto-generate ID
            event_type=event_type,
            title=event_template["title"],
            description=event_template["description"],
            options=event_template["options"],
            requires_input=True
        )
        
        return event

# Simple global shortcut for random event generation
_event_gen = EventGenerator()

def get_random_event():
    return _event_gen.generate_event()
