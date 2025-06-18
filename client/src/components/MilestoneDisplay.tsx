import * as React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { DISTANCE } from "@/lib/constants";

interface MilestoneDisplayProps {
  currentDistance: number;
}

const MilestoneDisplay: React.FC<MilestoneDisplayProps> = ({ currentDistance }) => {
  const [showMilestone, setShowMilestone] = React.useState(false);
  const [currentMilestone, setCurrentMilestone] = React.useState("");
  const [lastMilestone, setLastMilestone] = React.useState("");

  // Check for milestone achievements
  React.useEffect(() => {
    // Check each milestone
    if (lastMilestone !== "MOON" && currentDistance >= DISTANCE.EARTH_TO_MOON) {
      setCurrentMilestone("MOON");
      setLastMilestone("MOON");
      setShowMilestone(true);
    } else if (lastMilestone !== "MARS" && currentDistance >= DISTANCE.EARTH_TO_MARS) {
      setCurrentMilestone("MARS");
      setLastMilestone("MARS");
      setShowMilestone(true);
    } else if (lastMilestone !== "JUPITER" && currentDistance >= DISTANCE.EARTH_TO_JUPITER) {
      setCurrentMilestone("JUPITER");
      setLastMilestone("JUPITER");
      setShowMilestone(true);
    } else if (lastMilestone !== "SATURN" && currentDistance >= DISTANCE.EARTH_TO_SATURN) {
      setCurrentMilestone("SATURN");
      setLastMilestone("SATURN");
      setShowMilestone(true);
    } else if (lastMilestone !== "URANUS" && currentDistance >= DISTANCE.EARTH_TO_URANUS) {
      setCurrentMilestone("URANUS");
      setLastMilestone("URANUS");
      setShowMilestone(true);
    } else if (lastMilestone !== "NEPTUNE" && currentDistance >= DISTANCE.EARTH_TO_NEPTUNE) {
      setCurrentMilestone("NEPTUNE");
      setLastMilestone("NEPTUNE");
      setShowMilestone(true);
    } else if (lastMilestone !== "PLUTO" && currentDistance >= DISTANCE.EARTH_TO_PLUTO) {
      setCurrentMilestone("PLUTO");
      setLastMilestone("PLUTO");
      setShowMilestone(true);
    } else if (lastMilestone !== "INTERSTELLAR" && currentDistance >= DISTANCE.EARTH_TO_INTERSTELLAR) {
      setCurrentMilestone("INTERSTELLAR SPACE");
      setLastMilestone("INTERSTELLAR");
      setShowMilestone(true);
    }

    // Hide milestone notification after 5 seconds
    if (showMilestone) {
      const timer = setTimeout(() => {
        setShowMilestone(false);
      }, 5000);
      
      return () => clearTimeout(timer);
    }
  }, [currentDistance, lastMilestone, showMilestone]);

  if (!showMilestone) {
    return null;
  }

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 pointer-events-none">
      <Card className="bg-black/80 border-2 border-yellow-500 max-w-xs animate-pulse">
        <CardContent className="p-6">
          <div className="text-center">
            <div className="text-yellow-400 text-sm mb-2">MILESTONE REACHED</div>
            <div className="text-yellow-200 text-2xl font-bold">{currentMilestone}</div>
            <div className="mt-2 text-yellow-400 text-xs">
              {getMilestoneMessage(currentMilestone)}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// Helper function to get milestone-specific messages
function getMilestoneMessage(milestone: string): string {
  switch (milestone) {
    case "MOON":
      return "One small step for a space traveler, one giant leap for your journey!";
    case "MARS":
      return "The red planet welcomes you. No signs of life, but plenty of dust storms!";
    case "JUPITER":
      return "The gas giant looms large. Your ship feels tiny against its vastness.";
    case "SATURN":
      return "Those rings would make a nice screensaver. Too bad you can't stop for photos.";
    case "URANUS":
      return "Yes, everyone makes the same joke. Moving on quickly!";
    case "NEPTUNE":
      return "The blue giant marks the edge of our classical solar system.";
    case "PLUTO":
      return "It will always be a planet in your heart.";
    case "INTERSTELLAR SPACE":
      return "You've left the solar system behind. The true void of space awaits!";
    default:
      return "Journey continues into the unknown...";
  }
}

export default MilestoneDisplay;
