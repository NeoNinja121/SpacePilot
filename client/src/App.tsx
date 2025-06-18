import * as React from "react";
import GameScreen from "@/components/GameScreen";
import MilestoneDisplay from "@/components/MilestoneDisplay";
import { useGameState } from "@/hooks/useGameState";
import { enablePiOptimizations, measureFPS } from "@/utils/performance";
import { detectDisplayType, applyDisplayConfig } from "@/config/display";
import "./space.css";

function App() {
  const { gameState } = useGameState();
  const [isFullscreen, setIsFullscreen] = React.useState(false);
  const [isDisplayHatMini, setIsDisplayHatMini] = React.useState(false);
  
  // Apply display and Pi-specific optimizations on mount
  React.useEffect(() => {
    // Detect display type and apply configuration
    const displayConfig = detectDisplayType();
    applyDisplayConfig(displayConfig);
    setIsDisplayHatMini(displayConfig.type === "display_hat_mini");
    
    // Enable performance optimizations for Raspberry Pi
    enablePiOptimizations();
    
    // Start measuring FPS for adaptive performance
    const fpsInterval = setInterval(() => {
      measureFPS();
    }, 1000);
    
    // Setup fullscreen detection
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    
    document.addEventListener("fullscreenchange", handleFullscreenChange);
    
    // Auto-enter fullscreen on Pi and Display HAT Mini
    if (displayConfig.fullscreen) {
      document.documentElement.requestFullscreen().catch(err => {
        console.warn("Could not enter fullscreen mode:", err);
      });
    }
    
    return () => {
      clearInterval(fpsInterval);
      document.removeEventListener("fullscreenchange", handleFullscreenChange);
    };
  }, []);

  return (
    <div className={`font-mono text-sm select-none ${isFullscreen ? 'fullscreen-mode' : ''} ${isDisplayHatMini ? 'display-hat-mini' : ''}`}>
      <GameScreen isDisplayHatMini={isDisplayHatMini} />
      {!isDisplayHatMini && <MilestoneDisplay currentDistance={gameState.distance} />}
    </div>
  );
}

export default App;
