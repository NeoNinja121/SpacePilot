import * as React from "react";
import { cn } from "@/lib/utils";

interface SpaceShipProps {
  boostActive: boolean;
  damagedSystems: string[];
  smallDisplay?: boolean;
}

const SpaceShip: React.FC<SpaceShipProps> = ({ 
  boostActive, 
  damagedSystems,
  smallDisplay = false 
}) => {
  const [frame, setFrame] = React.useState(0);
  
  // Animation frame for thruster
  React.useEffect(() => {
    const interval = setInterval(() => {
      setFrame((prevFrame) => (prevFrame + 1) % 4);
    }, boostActive ? 50 : 150); // Faster animation during boost
    
    return () => clearInterval(interval);
  }, [boostActive]);
  
  // Check if specific part is damaged
  const isPartDamaged = (partId: string) => {
    return damagedSystems.includes(partId);
  };

  // Scale down sizes for small displays like Display HAT Mini
  const scale = smallDisplay ? 0.7 : 1;
  
  // Determine sizes based on display type
  const shipWidth = 48 * scale;
  const shipHeight = 32 * scale;
  const hullWidth = 32 * scale;
  const hullHeight = 16 * scale;
  const cabinSize = 12 * scale;
  const engineWidth = 16 * scale;
  const engineHeight = 8 * scale;
  const windowSize = 6 * scale;

  return (
    <div className="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="relative" style={{ width: `${shipWidth}rem`, height: `${shipHeight}rem` }}>
        {/* Ship hull */}
        <div 
          className={cn(
            "absolute bg-zinc-800 border-2 border-zinc-600 rounded-xl",
            isPartDamaged("hull-upper") && "border-red-500"
          )}
          style={{ 
            width: `${hullWidth}rem`, 
            height: `${hullHeight}rem`,
            left: `${8 * scale}rem`, 
            top: `${8 * scale}rem` 
          }}
        />
        
        {/* Cabin */}
        <div 
          className={cn(
            "absolute bg-zinc-700 border border-zinc-500 rounded-full",
            isPartDamaged("cabin") && "border-red-500"
          )}
          style={{ 
            width: `${cabinSize}rem`, 
            height: `${10 * scale}rem`,
            left: `${24 * scale}rem`, 
            top: `${4 * scale}rem` 
          }}
        >
          {/* Cabin window */}
          <div 
            className="absolute bg-blue-400 rounded-full overflow-hidden"
            style={{ 
              width: `${windowSize}rem`, 
              height: `${windowSize}rem`,
              left: `${3 * scale}rem`, 
              top: `${2 * scale}rem` 
            }}
          >
            {/* Pilot silhouette */}
            <div 
              className="absolute bg-black rounded-t-full"
              style={{ 
                width: `${4 * scale}rem`, 
                height: `${3 * scale}rem`,
                left: `${1 * scale}rem`, 
                top: `${3 * scale}rem` 
              }}
            />
          </div>
        </div>
        
        {/* Left engine */}
        <div 
          className={cn(
            "absolute bg-zinc-700 border border-zinc-500 rounded-lg",
            isPartDamaged("engine-left") && "border-red-500 bg-red-900"
          )}
          style={{ 
            width: `${engineWidth}rem`, 
            height: `${engineHeight}rem`,
            left: `${4 * scale}rem`, 
            top: `${12 * scale}rem` 
          }}
        />
        
        {/* Right engine */}
        <div 
          className={cn(
            "absolute bg-zinc-700 border border-zinc-500 rounded-lg",
            isPartDamaged("engine-right") && "border-red-500 bg-red-900"
          )}
          style={{ 
            width: `${engineWidth}rem`, 
            height: `${engineHeight}rem`,
            right: `${4 * scale}rem`, 
            top: `${12 * scale}rem` 
          }}
        />
        
        {/* Weapon */}
        <div 
          className={cn(
            "absolute bg-zinc-600 border border-zinc-400 rounded-sm",
            isPartDamaged("weapon") && "border-red-500"
          )}
          style={{ 
            width: `${8 * scale}rem`, 
            height: `${4 * scale}rem`,
            left: `${20 * scale}rem`, 
            bottom: `${2 * scale}rem` 
          }}
        />
        
        {/* Engine thruster effects - left */}
        {!isPartDamaged("engine-left") && (
          <div 
            className="absolute overflow-hidden"
            style={{ 
              left: 0, 
              top: `${14 * scale}rem`,
              width: `${4 * scale}rem`
            }}
          >
            <div 
              className={cn(
                "w-0 h-0",
                "border-t-transparent border-b-transparent",
                boostActive ? "border-r-yellow-500" : "border-r-orange-500",
                `thruster-${frame}`
              )}
              style={{
                borderTopWidth: `${8 * scale}px`,
                borderRightWidth: `${16 * scale}px`,
                borderBottomWidth: `${8 * scale}px`,
              }}
            />
          </div>
        )}
        
        {/* Engine thruster effects - right */}
        {!isPartDamaged("engine-right") && (
          <div 
            className="absolute overflow-hidden"
            style={{ 
              right: 0, 
              top: `${14 * scale}rem`,
              width: `${4 * scale}rem`
            }}
          >
            <div 
              className={cn(
                "w-0 h-0",
                "border-t-transparent border-b-transparent",
                boostActive ? "border-r-yellow-500" : "border-r-orange-500",
                `thruster-${frame}`
              )}
              style={{
                borderTopWidth: `${8 * scale}px`,
                borderRightWidth: `${16 * scale}px`,
                borderBottomWidth: `${8 * scale}px`,
              }}
            />
          </div>
        )}
        
        {/* Boost effect */}
        {boostActive && (
          <div 
            className="absolute overflow-hidden"
            style={{ 
              left: `${-24 * scale}rem`, 
              top: `${8 * scale}rem`,
              width: `${24 * scale}rem`,
              height: `${16 * scale}rem`
            }}
          >
            <div className="absolute left-0 top-0 w-full h-full flex space-x-1">
              {[0, 1, 2, 3, 4].map((i) => (
                <div 
                  key={i}
                  className={cn(
                    "bg-yellow-500 opacity-70 rounded-full",
                    `boost-particle-${i}`
                  )}
                  style={{
                    width: `${4 * scale}rem`,
                    height: `${16 * scale}rem`,
                    animationDelay: `${i * 0.1}s`,
                    animationDuration: '0.5s',
                  }}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SpaceShip;
