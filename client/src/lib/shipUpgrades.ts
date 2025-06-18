import { Ship } from "@/types/game";
import { SHIP } from "./constants";

// Calculate ship stats based on part levels
export function calculateUpgrades(ship: Ship): Ship {
  // Deep copy the ship to avoid mutating the original
  const upgradedShip = JSON.parse(JSON.stringify(ship));
  
  // Calculate engine speed bonus (10% per level for each engine)
  const engineLevels = ship.engine.reduce((sum, engine) => sum + engine.level, 0);
  const engineMultiplier = 1 + (engineLevels * 0.1);
  upgradedShip.speed = Math.floor(SHIP.BASE_SPEED * engineMultiplier);
  
  // Calculate hull storage bonus (15% per level for each hull part)
  const hullLevels = ship.hull.reduce((sum, hull) => sum + hull.level, 0);
  const storageMultiplier = 1 + (hullLevels * 0.15);
  upgradedShip.storageCapacity = Math.floor(SHIP.BASE_STORAGE * storageMultiplier);
  
  // Calculate cabin durability bonus (20% per level)
  const durabilityMultiplier = 1 + (ship.cabin.level * 0.2);
  upgradedShip.durability = Math.floor(SHIP.BASE_DURABILITY * durabilityMultiplier);
  
  // Calculate weapon luck bonus (5% per level)
  const luckMultiplier = 1 + (ship.weapon.level * 0.05);
  upgradedShip.luck = Math.floor(SHIP.BASE_LUCK * luckMultiplier);
  
  return upgradedShip;
}

// Calculate repair cost based on damaged systems
export function calculateRepairCost(damagedSystems: string[]): number {
  return damagedSystems.length * 50;
}

// Apply damage to a random ship system
export function applyDamage(ship: Ship, damagedSystems: string[]): string[] {
  // List of possible systems to damage
  const systems = [
    "engine-left",
    "engine-right",
    "hull-upper",
    "hull-lower",
    "cabin",
    "weapon",
  ];
  
  // Filter out already damaged systems
  const availableSystems = systems.filter(
    (system) => !damagedSystems.includes(system)
  );
  
  if (availableSystems.length === 0) {
    return damagedSystems; // All systems already damaged
  }
  
  // Randomly select a system to damage
  const randomIndex = Math.floor(Math.random() * availableSystems.length);
  const newDamagedSystem = availableSystems[randomIndex];
  
  return [...damagedSystems, newDamagedSystem];
}

// Calculate performance penalties from damage
export function calculateDamagePenalties(ship: Ship, damagedSystems: string[]): Ship {
  if (damagedSystems.length === 0) {
    return ship; // No damage, no penalties
  }
  
  // Deep copy the ship
  const penalizedShip = JSON.parse(JSON.stringify(ship));
  
  // Apply penalties based on which systems are damaged
  damagedSystems.forEach((system) => {
    if (system.startsWith("engine")) {
      // Engine damage reduces speed
      penalizedShip.speed = Math.floor(penalizedShip.speed * 0.8);
    } else if (system.startsWith("hull")) {
      // Hull damage reduces storage
      penalizedShip.storageCapacity = Math.floor(penalizedShip.storageCapacity * 0.8);
    } else if (system === "cabin") {
      // Cabin damage reduces durability
      penalizedShip.durability = Math.floor(penalizedShip.durability * 0.7);
    } else if (system === "weapon") {
      // Weapon damage reduces luck
      penalizedShip.luck = Math.floor(penalizedShip.luck * 0.7);
    }
  });
  
  return penalizedShip;
}
