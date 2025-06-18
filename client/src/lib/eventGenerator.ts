import { GameEvent, EventOption } from "@/types/game";
import { EVENT_TYPES } from "./constants";

// Event content pools
const EVERYDAY_EVENTS = [
  {
    title: "Space Debris",
    description: "A small cluster of space debris approaches your ship. Attempt evasive maneuvers?",
    options: [
      {
        text: "Evade",
        effect: "Slight course change, minor fuel consumption",
        successRate: 80,
        darkMatterReward: 10,
        distanceEffect: 0,
      },
      {
        text: "Ignore",
        effect: "Risk of hull damage",
        successRate: 40,
        darkMatterReward: 0,
        distanceEffect: -50,
      },
    ],
  },
  {
    title: "Stray Cat in EVA Suit",
    description: "You spot a cat floating by in a tiny EVA suit. Its collar says 'Whiskers'. Take it aboard?",
    options: [
      {
        text: "Rescue cat",
        effect: "New ship companion, occasional distractions",
        successRate: 100,
        darkMatterReward: 30,
        distanceEffect: 0,
      },
      {
        text: "Let it float by",
        effect: "Such is space life",
        successRate: 100,
        darkMatterReward: 0,
        distanceEffect: 0,
      },
    ],
  },
  {
    title: "Junk Transmission",
    description: "Your comms pick up a strange signal. It sounds like... 80s synth music?",
    options: [
      {
        text: "Boost signal",
        effect: "Dance party for one",
        successRate: 100,
        darkMatterReward: 5,
        distanceEffect: 0,
      },
      {
        text: "Ignore",
        effect: "You'll never know what bangers you missed",
        successRate: 100,
        darkMatterReward: 0,
        distanceEffect: 0,
      },
    ],
  },
  {
    title: "Minor Course Correction",
    description: "Navigation computer suggests a minor course correction to optimize route.",
    options: [
      {
        text: "Adjust course",
        effect: "Optimize travel path",
        successRate: 100,
        darkMatterReward: 0,
        distanceEffect: 150,
      },
      {
        text: "Keep current course",
        effect: "Stay on the longer route",
        successRate: 100,
        darkMatterReward: 5,
        distanceEffect: 0,
      },
    ],
  },
];

const RARE_EVENTS = [
  {
    title: "Derelict Ship",
    description: "You encounter a abandoned vessel drifting through space. It looks salvageable.",
    options: [
      {
        text: "Salvage parts",
        effect: "Risk but potential reward",
        successRate: 60,
        darkMatterReward: 80,
        distanceEffect: -100,
        partReward: "hull-upper",
      },
      {
        text: "Leave it alone",
        effect: "Safer option",
        successRate: 100,
        darkMatterReward: 0,
        distanceEffect: 0,
      },
    ],
  },
  {
    title: "Space Station",
    description: "A small research station appears on your scanners. They're hailing you.",
    options: [
      {
        text: "Dock and trade",
        effect: "Exchange resources",
        successRate: 90,
        darkMatterReward: 50,
        distanceEffect: -200,
      },
      {
        text: "Decline and continue",
        effect: "Maintain current course",
        successRate: 100,
        darkMatterReward: 0,
        distanceEffect: 100,
      },
    ],
  },
  {
    title: "Drifting Manga Collection",
    description: "A sealed container floats by with 'Property of ISS Recreation Dept' labeled on it. Inside appear to be vintage manga comics.",
    options: [
      {
        text: "Collect and read",
        effect: "Entertainment boost",
        successRate: 100,
        darkMatterReward: 25,
        distanceEffect: 0,
      },
      {
        text: "Leave it",
        effect: "Stay focused on your mission",
        successRate: 100,
        darkMatterReward: 0,
        distanceEffect: 50,
      },
    ],
  },
];

const COSMIC_EVENTS = [
  {
    title: "Wormhole Detected",
    description: "Sensors detect a small wormhole forming nearby. It could be a shortcut... or a trap.",
    options: [
      {
        text: "Enter wormhole",
        effect: "High risk, high reward",
        successRate: 40,
        darkMatterReward: 200,
        distanceEffect: 2000,
      },
      {
        text: "Avoid wormhole",
        effect: "Safe but slower",
        successRate: 100,
        darkMatterReward: 0,
        distanceEffect: 0,
      },
    ],
  },
  {
    title: "Black Hole Proximity",
    description: "Your ship is being pulled toward a small black hole. Engines straining!",
    options: [
      {
        text: "Full power to engines",
        effect: "Try to escape gravitational pull",
        successRate: 60,
        darkMatterReward: 0,
        distanceEffect: -500,
      },
      {
        text: "Slingshot maneuver",
        effect: "Use gravity to boost speed",
        successRate: 30,
        darkMatterReward: 100,
        distanceEffect: 1000,
      },
    ],
  },
  {
    title: "Space Kaiju",
    description: "An enormous creature that resembles a classic movie monster drifts past your ship. It seems to be asleep.",
    options: [
      {
        text: "Take samples",
        effect: "Scientific discovery",
        successRate: 50,
        darkMatterReward: 150,
        distanceEffect: -300,
      },
      {
        text: "Quietly pass by",
        effect: "Don't wake the kaiju!",
        successRate: 90,
        darkMatterReward: 0,
        distanceEffect: 0,
      },
    ],
  },
  {
    title: "AI Megastructure",
    description: "You encounter what appears to be a massive computing structure built by an ancient AI civilization.",
    options: [
      {
        text: "Connect to network",
        effect: "Download data",
        successRate: 70,
        darkMatterReward: 250,
        distanceEffect: 0,
      },
      {
        text: "Keep distance",
        effect: "Avoid potential AI conflicts",
        successRate: 100,
        darkMatterReward: 0,
        distanceEffect: 100,
      },
    ],
  },
];

const EASTER_EGG_EVENTS = [
  {
    title: "Space Invaders",
    description: "A formation of pixelated alien ships approaches in a suspiciously familiar pattern...",
    options: [
      {
        text: "Fire pixel cannons",
        effect: "Pew pew!",
        successRate: 75,
        darkMatterReward: 80,
        distanceEffect: 0,
      },
      {
        text: "Hide behind asteroid",
        effect: "Wait for them to pass",
        successRate: 100,
        darkMatterReward: 0,
        distanceEffect: -100,
      },
    ],
  },
  {
    title: "Monolith Detection",
    description: "A sleek black monolith floats in space accompanied by classical music.",
    options: [
      {
        text: "Touch it",
        effect: "Evolutionary leap?",
        successRate: 50,
        darkMatterReward: 200,
        distanceEffect: 1000,
      },
      {
        text: "Just appreciate from afar",
        effect: "It's full of stars!",
        successRate: 100,
        darkMatterReward: 20,
        distanceEffect: 0,
      },
    ],
  },
  {
    title: "Debug Console",
    description: "Your ship computer glitches, revealing what appears to be developer debug tools. A message reads: 'Hello player, having fun?'",
    options: [
      {
        text: "Type 'Yes'",
        effect: "Developer Easter Egg",
        successRate: 100,
        darkMatterReward: 42,
        distanceEffect: 0,
      },
      {
        text: "Close console",
        effect: "Return to normal operations",
        successRate: 100,
        darkMatterReward: 0,
        distanceEffect: 0,
      },
    ],
  },
  {
    title: "Red Pill, Blue Pill",
    description: "A strange transmission asks if you'd like to know how deep the rabbit hole goes.",
    options: [
      {
        text: "Red Pill",
        effect: "The truth",
        successRate: 100,
        darkMatterReward: 101,
        distanceEffect: -300,
      },
      {
        text: "Blue Pill",
        effect: "Blissful ignorance",
        successRate: 100,
        darkMatterReward: 0,
        distanceEffect: 300,
      },
    ],
  },
];

// Generate a random event based on rarity weightings
export function generateEvent(): GameEvent {
  // Determine event type based on rarity
  const rng = Math.random() * 100;
  let eventType: string;
  let eventPool: any[];
  
  if (rng < 70) {
    // 70% chance of everyday event
    eventType = EVENT_TYPES.EVERYDAY;
    eventPool = EVERYDAY_EVENTS;
  } else if (rng < 90) {
    // 20% chance of rare event
    eventType = EVENT_TYPES.RARE;
    eventPool = RARE_EVENTS;
  } else if (rng < 98) {
    // 8% chance of cosmic event
    eventType = EVENT_TYPES.COSMIC;
    eventPool = COSMIC_EVENTS;
  } else {
    // 2% chance of easter egg event
    eventType = EVENT_TYPES.EASTER_EGG;
    eventPool = EASTER_EGG_EVENTS;
  }
  
  // Pick a random event from the selected pool
  const randomIndex = Math.floor(Math.random() * eventPool.length);
  const eventTemplate = eventPool[randomIndex];
  
  // Create the event object
  const event: GameEvent = {
    id: `event-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
    type: eventType,
    title: eventTemplate.title,
    description: eventTemplate.description,
    options: eventTemplate.options,
    requiresInput: true, // Most events require player input
    timestamp: Date.now(),
    resolved: false,
  };
  
  return event;
}
