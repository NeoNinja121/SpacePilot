import { useState, useEffect, useCallback } from "react";
import { GameState, GameEvent, ButtonAction } from "@/types/game";
import { TIME, SHIP, EVENT_TYPES } from "@/lib/constants";
import { generateEvent } from "@/lib/eventGenerator";
import { calculateUpgrades } from "@/lib/shipUpgrades";

// Initial game state
const initialState: GameState = {
  distance: 0,
  darkMatter: 100,
  ship: {
    engine: [
      {
        id: "engine-left",
        name: "Left Engine",
        level: 1,
        maxLevel: 10,
        cost: 150,
        description: "Powers the left side of your ship",
        effect: "Increases speed by 10% per level",
      },
      {
        id: "engine-right",
        name: "Right Engine",
        level: 1,
        maxLevel: 10,
        cost: 150,
        description: "Powers the right side of your ship",
        effect: "Increases speed by 10% per level",
      },
    ],
    hull: [
      {
        id: "hull-upper",
        name: "Upper Hull",
        level: 1,
        maxLevel: 10,
        cost: 200,
        description: "Protects the top of your ship",
        effect: "Increases storage by 15% per level",
      },
      {
        id: "hull-lower",
        name: "Lower Hull",
        level: 1,
        maxLevel: 10,
        cost: 200,
        description: "Protects the bottom of your ship",
        effect: "Increases storage by 15% per level",
      },
    ],
    cabin: {
      id: "cabin",
      name: "Pilot Cabin",
      level: 1,
      maxLevel: 10,
      cost: 300,
      description: "Where you live and control the ship",
      effect: "Increases durability by 20% per level",
    },
    weapon: {
      id: "weapon",
      name: "Defense System",
      level: 1,
      maxLevel: 10,
      cost: 250,
      description: "Your ship's defensive capabilities",
      effect: "Increases luck by 5% per level",
    },
    speed: SHIP.BASE_SPEED,
    storageCapacity: SHIP.BASE_STORAGE,
    durability: SHIP.BASE_DURABILITY,
    luck: SHIP.BASE_LUCK,
  },
  events: [],
  lastEventTime: Date.now(),
  boostActive: false,
  boostEndTime: 0,
  damagedSystems: [],
  repairPoints: 3,
  boostPoints: 5,
};

export function useGameState() {
  const [gameState, setGameState] = useState<GameState>(initialState);
  const [activeEvent, setActiveEvent] = useState<GameEvent | null>(null);

  // Initialize or load saved state
  useEffect(() => {
    const savedState = localStorage.getItem("idleSpaceGame");
    if (savedState) {
      try {
        const parsedState = JSON.parse(savedState);
        setGameState(parsedState);
      } catch (e) {
        console.error("Failed to load saved game state");
        setGameState(initialState);
      }
    }
  }, []);

  // Save state periodically
  useEffect(() => {
    const saveInterval = setInterval(() => {
      localStorage.setItem("idleSpaceGame", JSON.stringify(gameState));
    }, 10000);

    return () => clearInterval(saveInterval);
  }, [gameState]);

  // Main game loop
  useEffect(() => {
    const gameLoop = setInterval(() => {
      setGameState((prevState) => {
        // Calculate current speed including boosts
        let currentSpeed = prevState.ship.speed;
        if (prevState.boostActive && prevState.boostEndTime > Date.now()) {
          currentSpeed *= 2; // Double speed during boost
        } else if (prevState.boostActive) {
          // End boost if time is up
          return {
            ...prevState,
            boostActive: false,
          };
        }

        // Add distance based on speed
        const newDistance = prevState.distance + currentSpeed / 10;

        // Passive Dark Matter collection (1 per second)
        const newDarkMatter = Math.min(
          prevState.darkMatter + 0.1,
          prevState.ship.storageCapacity
        );

        // Check for new events
        const now = Date.now();
        let updatedEvents = [...prevState.events];
        let lastEventTime = prevState.lastEventTime;

        if (now - prevState.lastEventTime >= TIME.EVENT_INTERVAL) {
          const newEvent = generateEvent();
          updatedEvents.push(newEvent);
          lastEventTime = now;

          // Set active event if it requires input
          if (newEvent.requiresInput) {
            setActiveEvent(newEvent);
          }
        }

        return {
          ...prevState,
          distance: newDistance,
          darkMatter: newDarkMatter,
          events: updatedEvents,
          lastEventTime,
        };
      });
    }, 100); // Update 10 times per second

    return () => clearInterval(gameLoop);
  }, []);

  // Handle button presses
  const handleButtonPress = useCallback(
    (buttonIndex: number) => {
      let action: ButtonAction = "none";

      // Map button index to action based on context
      if (activeEvent) {
        // During events, buttons 3 and 4 are used for yes/no
        if (buttonIndex === 2) {
          action = "yes";
        } else if (buttonIndex === 3) {
          action = "no";
        }
      } else {
        // Outside events, buttons have their standard functions
        if (buttonIndex === 0) {
          action = "boost";
        } else if (buttonIndex === 1) {
          action = "repair";
        }
      }

      // Apply the action
      setGameState((prevState) => {
        switch (action) {
          case "boost":
            if (prevState.boostPoints > 0 && !prevState.boostActive) {
              return {
                ...prevState,
                boostActive: true,
                boostEndTime: Date.now() + TIME.BOOST_DURATION,
                boostPoints: prevState.boostPoints - 1,
              };
            }
            break;
          case "repair":
            if (prevState.repairPoints > 0 && prevState.damagedSystems.length > 0) {
              const updatedDamagedSystems = [...prevState.damagedSystems];
              updatedDamagedSystems.pop(); // Remove one damaged system
              return {
                ...prevState,
                damagedSystems: updatedDamagedSystems,
                repairPoints: prevState.repairPoints - 1,
              };
            }
            break;
          case "yes":
          case "no":
            if (activeEvent) {
              // Resolve the active event
              const resolvedEvent = {
                ...activeEvent,
                resolved: true,
                outcome: action === "yes" ? "accepted" : "declined",
              };

              // Apply event effects here
              let updatedState = { ...prevState };
              
              // Add dark matter reward
              if (action === "yes" && activeEvent.options && activeEvent.options[0]) {
                updatedState.darkMatter += activeEvent.options[0].darkMatterReward;
                updatedState.distance += activeEvent.options[0].distanceEffect;
              }

              // Update the event in the list
              const updatedEvents = prevState.events.map((event) =>
                event.id === activeEvent.id ? resolvedEvent : event
              );

              setActiveEvent(null);
              
              return {
                ...updatedState,
                events: updatedEvents,
              };
            }
            break;
          default:
            break;
        }
        return prevState;
      });
    },
    [activeEvent]
  );

  // Upgrade ship part
  const upgradeShipPart = useCallback((partId: string) => {
    setGameState((prevState) => {
      // Find the part to upgrade
      let partToUpgrade = null;
      let partCategory = "";

      // Search through all ship parts
      for (const category of ["engine", "hull", "cabin", "weapon"]) {
        if (Array.isArray(prevState.ship[category])) {
          // For array parts like engine and hull
          const foundPart = prevState.ship[category].find((part) => part.id === partId);
          if (foundPart) {
            partToUpgrade = foundPart;
            partCategory = category;
            break;
          }
        } else if (prevState.ship[category].id === partId) {
          // For single parts like cabin and weapon
          partToUpgrade = prevState.ship[category];
          partCategory = category;
          break;
        }
      }

      if (!partToUpgrade || partToUpgrade.level >= partToUpgrade.maxLevel) {
        return prevState; // Can't upgrade
      }

      // Check if enough dark matter
      if (prevState.darkMatter < partToUpgrade.cost) {
        return prevState; // Not enough currency
      }

      // Create a deep copy of the ship to modify
      const newShip = JSON.parse(JSON.stringify(prevState.ship));

      // Upgrade the part
      if (Array.isArray(newShip[partCategory])) {
        const index = newShip[partCategory].findIndex((p) => p.id === partId);
        newShip[partCategory][index].level += 1;
        newShip[partCategory][index].cost = Math.floor(
          newShip[partCategory][index].cost * 1.5
        );
      } else {
        newShip[partCategory].level += 1;
        newShip[partCategory].cost = Math.floor(
          newShip[partCategory].cost * 1.5
        );
      }

      // Recalculate ship stats based on upgrades
      const upgradedShip = calculateUpgrades(newShip);

      return {
        ...prevState,
        darkMatter: prevState.darkMatter - partToUpgrade.cost,
        ship: upgradedShip,
      };
    });
  }, []);

  return {
    gameState,
    activeEvent,
    handleButtonPress,
    upgradeShipPart,
  };
}
