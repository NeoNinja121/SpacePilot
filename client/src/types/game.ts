// Game types for Idle Space Adventure

export interface ShipPart {
  id: string;
  name: string;
  level: number;
  maxLevel: number;
  cost: number; // Cost to upgrade to next level
  description: string;
  effect: string;
}

export interface Ship {
  engine: ShipPart[];
  hull: ShipPart[];
  cabin: ShipPart;
  weapon: ShipPart;
  speed: number;
  storageCapacity: number;
  durability: number;
  luck: number;
}

export interface GameState {
  distance: number;
  darkMatter: number;
  ship: Ship;
  events: GameEvent[];
  lastEventTime: number;
  boostActive: boolean;
  boostEndTime: number;
  damagedSystems: string[];
  repairPoints: number;
  boostPoints: number;
}

export interface GameEvent {
  id: string;
  type: string;
  title: string;
  description: string;
  options?: EventOption[];
  requiresInput: boolean;
  imageUrl?: string;
  timestamp: number;
  resolved: boolean;
  outcome?: string;
}

export interface EventOption {
  text: string;
  effect: string;
  successRate: number;
  darkMatterReward: number;
  distanceEffect: number;
  partReward?: string;
}

export type ButtonAction = "boost" | "repair" | "yes" | "no" | "none";
