"""
Ship module for Idle Space Adventure
"""
from game.constants import (
    SHIP_BASE_SPEED, SHIP_BASE_STORAGE, 
    SHIP_BASE_DURABILITY, SHIP_BASE_LUCK
)

class Ship:
    """Ship class for handling ship statistics and upgrades"""
    
    def __init__(self, ship_data=None):
        """Initialize ship with default or provided data"""
        self.data = ship_data or self._default_ship_data()
        self.update_stats()
        
    def _default_ship_data(self):
        """Create default ship data"""
        return {
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
        }
        
    def update_stats(self):
        """Update ship statistics based on part levels"""
        # Calculate engine speed bonus (10% per level for each engine)
        engine_levels = sum(engine["level"] for engine in self.data["engine"])
        engine_multiplier = 1 + (engine_levels * 0.1)
        self.data["speed"] = int(SHIP_BASE_SPEED * engine_multiplier)
        
        # Calculate hull storage bonus (15% per level for each hull part)
        hull_levels = sum(hull["level"] for hull in self.data["hull"])
        storage_multiplier = 1 + (hull_levels * 0.15)
        self.data["storage_capacity"] = int(SHIP_BASE_STORAGE * storage_multiplier)
        
        # Calculate cabin durability bonus (20% per level)
        durability_multiplier = 1 + (self.data["cabin"]["level"] * 0.2)
        self.data["durability"] = int(SHIP_BASE_DURABILITY * durability_multiplier)
        
        # Calculate weapon luck bonus (5% per level)
        luck_multiplier = 1 + (self.data["weapon"]["level"] * 0.05)
        self.data["luck"] = int(SHIP_BASE_LUCK * luck_multiplier)
        
    def upgrade_part(self, part_id, dark_matter):
        """
        Attempt to upgrade a ship part
        
        Args:
            part_id: ID of the part to upgrade
            dark_matter: Current dark matter amount
            
        Returns:
            tuple: (success, cost, new_dark_matter)
        """
        # Find the part to upgrade
        part_to_upgrade = None
        part_category = None
        part_index = None
        
        # Search through all ship parts
        for category in ["engine", "hull", "cabin", "weapon"]:
            if isinstance(self.data[category], list):
                # For array parts like engine and hull
                for i, part in enumerate(self.data[category]):
                    if part["id"] == part_id:
                        part_to_upgrade = part
                        part_category = category
                        part_index = i
                        break
            elif self.data[category]["id"] == part_id:
                # For single parts like cabin and weapon
                part_to_upgrade = self.data[category]
                part_category = category
                break
                
            if part_to_upgrade:
                break
                
        # If part not found or at max level
        if not part_to_upgrade or part_to_upgrade["level"] >= part_to_upgrade["max_level"]:
            return (False, 0, dark_matter)
            
        # Check if enough dark matter
        if dark_matter < part_to_upgrade["cost"]:
            return (False, part_to_upgrade["cost"], dark_matter)
            
        # Upgrade the part
        if part_index is not None:
            # For array parts
            self.data[part_category][part_index]["level"] += 1
            cost = self.data[part_category][part_index]["cost"]
            self.data[part_category][part_index]["cost"] = int(cost * 1.5)
        else:
            # For single parts
            self.data[part_category]["level"] += 1
            cost = self.data[part_category]["cost"]
            self.data[part_category]["cost"] = int(cost * 1.5)
            
        # Update ship stats
        self.update_stats()
        
        # Return success and updated dark matter
        return (True, cost, dark_matter - cost)
        
    def apply_damage_penalties(self, damaged_systems):
        """
        Apply penalties based on damaged systems
        
        Args:
            damaged_systems: List of damaged system IDs
            
        Returns:
            dict: Ship data with penalties applied
        """
        if not damaged_systems:
            return self.data.copy()
            
        # Create a copy of ship data
        penalized_data = self.data.copy()
        
        # Apply penalties
        for system in damaged_systems:
            if system.startswith("engine"):
                # Engine damage reduces speed
                penalized_data["speed"] = int(penalized_data["speed"] * 0.8)
            elif system.startswith("hull"):
                # Hull damage reduces storage
                penalized_data["storage_capacity"] = int(penalized_data["storage_capacity"] * 0.8)
            elif system == "cabin":
                # Cabin damage reduces durability
                penalized_data["durability"] = int(penalized_data["durability"] * 0.7)
            elif system == "weapon":
                # Weapon damage reduces luck
                penalized_data["luck"] = int(penalized_data["luck"] * 0.7)
                
        return penalized_data
