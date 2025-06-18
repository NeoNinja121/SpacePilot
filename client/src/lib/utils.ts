import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { DISTANCE } from "./constants";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Format large distances with appropriate units
export function formatDistance(distance: number): string {
  if (distance < 1000) {
    return `${Math.floor(distance)} mi`;
  } else if (distance < 1000000) {
    return `${(distance / 1000).toFixed(1)} km`;
  } else if (distance < DISTANCE.EARTH_TO_INTERSTELLAR) {
    return `${(distance / 1000000).toFixed(2)} M mi`;
  } else {
    // Convert to light years
    return `${(distance / DISTANCE.EARTH_TO_INTERSTELLAR).toFixed(4)} ly`;
  }
}

// Calculate time to reach a distance milestone
export function calculateTimeToMilestone(
  currentDistance: number,
  targetDistance: number,
  speed: number
): string {
  const remainingDistance = targetDistance - currentDistance;
  if (remainingDistance <= 0) {
    return "Reached";
  }

  const secondsToTarget = remainingDistance / speed;
  return formatTime(secondsToTarget);
}

// Format time in seconds to a human-readable string
export function formatTime(seconds: number): string {
  if (seconds < 60) {
    return `${Math.ceil(seconds)}s`;
  } else if (seconds < 3600) {
    return `${Math.ceil(seconds / 60)}m`;
  } else if (seconds < 86400) {
    return `${Math.ceil(seconds / 3600)}h`;
  } else {
    return `${Math.ceil(seconds / 86400)}d`;
  }
}

// Get next milestone based on current distance
export function getNextMilestone(currentDistance: number): {
  name: string;
  distance: number;
} {
  if (currentDistance < DISTANCE.EARTH_TO_MOON) {
    return { name: "Moon", distance: DISTANCE.EARTH_TO_MOON };
  } else if (currentDistance < DISTANCE.EARTH_TO_MARS) {
    return { name: "Mars", distance: DISTANCE.EARTH_TO_MARS };
  } else if (currentDistance < DISTANCE.EARTH_TO_JUPITER) {
    return { name: "Jupiter", distance: DISTANCE.EARTH_TO_JUPITER };
  } else if (currentDistance < DISTANCE.EARTH_TO_SATURN) {
    return { name: "Saturn", distance: DISTANCE.EARTH_TO_SATURN };
  } else if (currentDistance < DISTANCE.EARTH_TO_URANUS) {
    return { name: "Uranus", distance: DISTANCE.EARTH_TO_URANUS };
  } else if (currentDistance < DISTANCE.EARTH_TO_NEPTUNE) {
    return { name: "Neptune", distance: DISTANCE.EARTH_TO_NEPTUNE };
  } else if (currentDistance < DISTANCE.EARTH_TO_PLUTO) {
    return { name: "Pluto", distance: DISTANCE.EARTH_TO_PLUTO };
  } else {
    return { name: "Interstellar Space", distance: DISTANCE.EARTH_TO_INTERSTELLAR };
  }
}

// Generate a random star field background
export function generateStarField(density: number): string[] {
  const stars = [];
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;
  
  for (let i = 0; i < density; i++) {
    const x = Math.random() * viewportWidth;
    const y = Math.random() * viewportHeight;
    const size = Math.random() * 2 + 1;
    const opacity = Math.random() * 0.5 + 0.5;
    
    stars.push(`${x}px ${y}px ${size}px rgba(255, 255, 255, ${opacity})`);
  }
  
  return stars;
}
