// Game constants for Idle Space Adventure

// Distance constants (in miles)
export const DISTANCE = {
  EARTH_TO_MOON: 238900,
  EARTH_TO_MARS: 140000000,
  EARTH_TO_JUPITER: 365000000,
  EARTH_TO_SATURN: 746000000,
  EARTH_TO_URANUS: 1600000000,
  EARTH_TO_NEPTUNE: 2700000000,
  EARTH_TO_PLUTO: 3100000000,
  EARTH_TO_INTERSTELLAR: 9461000000000, // 1 light year
};

// Time constants (in milliseconds)
export const TIME = {
  EVENT_INTERVAL: 600000, // 10 minutes
  BOOST_DURATION: 30000, // 30 seconds
  ANIMATION_SPEED: 150,
};

// Ship defaults
export const SHIP = {
  BASE_SPEED: 100, // miles per second
  BASE_STORAGE: 1000, // Dark Matter units
  BASE_DURABILITY: 100,
  BASE_LUCK: 5, // percentage
};

// Event types
export const EVENT_TYPES = {
  EVERYDAY: "everyday",
  RARE: "rare",
  COSMIC: "cosmic",
  EASTER_EGG: "easter_egg",
};

// Japanese kanji for Dark Matter
export const DARK_MATTER_SYMBOL = "暗物質";
