import * as React from "react";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

interface StatusBarProps {
  speed: number;
  boostActive: boolean;
  boostPoints: number;
  repairPoints: number;
  damagedSystems: string[];
  smallDisplay?: boolean;
}

const StatusBar: React.FC<StatusBarProps> = ({
  speed,
  boostActive,
  boostPoints,
  repairPoints,
  damagedSystems,
  smallDisplay = false,
}) => {
  // Status message rotation
  const [messageIndex, setMessageIndex] = React.useState(0);
  
  // Use shorter status messages for small displays
  const statusMessages = smallDisplay ? [
    "Systems OK",
    "DM collector on",
    "Dest: Unknown",
    "Mission: Explore",
    "Temp: OK",
    "Life sup: OK",
  ] : [
    "Systems nominal",
    "Dark matter collector active",
    "Destination: The unknown",
    "Current mission: Go further than anyone before",
    "Ship temperature: Cozy",
    "Life support: Operational",
  ];

  // Change message every 5 seconds
  React.useEffect(() => {
    const interval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % statusMessages.length);
    }, 5000);
    
    return () => clearInterval(interval);
  }, [statusMessages.length]);

  // Random screen flicker effect for damaged systems
  const [flicker, setFlicker] = React.useState(false);
  
  React.useEffect(() => {
    if (damagedSystems.length > 0) {
      const flickerInterval = setInterval(() => {
        setFlicker((prev) => !prev);
      }, Math.random() * 1000 + 500);
      
      return () => clearInterval(flickerInterval);
    }
  }, [damagedSystems.length]);

  return (
    <div 
      className={cn(
        "absolute bottom-0 left-0 right-0 bg-black/80 border-t border-green-800",
        smallDisplay ? "p-1" : "p-2",
        damagedSystems.length > 0 && flicker && "bg-red-900/20"
      )}
    >
      {/* Status message - simplified on small displays */}
      {!smallDisplay && (
        <div className="mb-2 text-xs font-mono text-green-500">
          {statusMessages[messageIndex]}
          {damagedSystems.length > 0 && " | WARNING: SYSTEMS DAMAGED"}
        </div>
      )}
      
      <div className="grid grid-cols-2 gap-2">
        {/* Speed indicator */}
        <div>
          <div className={`flex justify-between items-center ${smallDisplay ? "text-[10px]" : "text-xs"} mb-1`}>
            <span>SPD</span>
            <span className={boostActive ? "text-yellow-400" : "text-green-400"}>
              {boostActive ? `${speed * 2}` : speed} mi/s
            </span>
          </div>
          <Progress 
            value={boostActive ? 100 : 50} 
            className={`bg-black ${smallDisplay ? "h-1" : "h-1.5"}`}
          />
        </div>
        
        {/* System status */}
        <div>
          <div className={`flex justify-between items-center ${smallDisplay ? "text-[10px]" : "text-xs"} mb-1`}>
            <span>SYS</span>
            <span className={damagedSystems.length > 0 ? "text-red-400" : "text-green-400"}>
              {damagedSystems.length > 0 
                ? `${damagedSystems.length} DMG` 
                : "OK"}
            </span>
          </div>
          <Progress 
            value={100 - (damagedSystems.length * 16.6)} 
            className={`bg-black ${smallDisplay ? "h-1" : "h-1.5"}`}
          />
        </div>
      </div>
      
      {/* Button resources - simplified on small displays */}
      <div className={`flex justify-between ${smallDisplay ? "mt-1 text-[9px]" : "mt-2 text-xs"} font-mono`}>
        <div 
          className={boostPoints > 0 ? "text-green-500" : "text-red-500"}
        >
          B:{boostPoints}
        </div>
        {smallDisplay && statusMessages[messageIndex].substring(0, 8)}
        <div 
          className={repairPoints > 0 ? "text-green-500" : "text-red-500"}
        >
          R:{repairPoints}
        </div>
      </div>
    </div>
  );
};

export default StatusBar;
