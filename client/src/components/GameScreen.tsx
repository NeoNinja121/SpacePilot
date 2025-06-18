import * as React from "react";
import { useGameState } from "@/hooks/useGameState";
import SpaceShip from "@/components/SpaceShip";
import EventDisplay from "@/components/EventDisplay";
import StatusBar from "@/components/StatusBar";
import GPIOButtonHandler from "@/components/GPIOButtonHandler";
import { DARK_MATTER_SYMBOL } from "@/lib/constants";
import { formatDistance } from "@/lib/utils";
import { Button } from "@/components/ui/button";

interface GameScreenProps {
  isDisplayHatMini?: boolean;
}

const GameScreen: React.FC<GameScreenProps> = ({ isDisplayHatMini = false }) => {
  const { gameState, activeEvent, handleButtonPress, upgradeShipPart } = useGameState();

  return (
    <div className="flex flex-col h-screen bg-black text-green-400 font-mono overflow-hidden">
      {/* Header with game stats */}
      <div className={`flex justify-between items-center ${isDisplayHatMini ? 'p-1 text-xs' : 'p-2'} border-b border-green-600`}>
        <div>Dist: {formatDistance(gameState.distance)}</div>
        <div>
          {DARK_MATTER_SYMBOL}: {Math.floor(gameState.darkMatter)}
        </div>
      </div>

      {/* Main game view */}
      <div className="flex-1 relative overflow-hidden">
        {/* Space background with parallax stars */}
        <div className="absolute inset-0 bg-black">
          <div className={`stars-small ${isDisplayHatMini ? 'stars-small-hat' : ''}`}></div>
          <div className={`stars-medium ${isDisplayHatMini ? 'stars-medium-hat' : ''}`}></div>
          {!isDisplayHatMini && <div className="stars-large"></div>}
        </div>

        {/* Spaceship */}
        <SpaceShip
          boostActive={gameState.boostActive}
          damagedSystems={gameState.damagedSystems}
          smallDisplay={isDisplayHatMini}
        />

        {/* Active event overlay */}
        {activeEvent && (
          <EventDisplay
            event={activeEvent}
            onRespond={(isYes) => handleButtonPress(isYes ? 2 : 3)}
            smallDisplay={isDisplayHatMini}
          />
        )}

        {/* Status indicators */}
        <StatusBar
          speed={gameState.ship.speed}
          boostActive={gameState.boostActive}
          boostPoints={gameState.boostPoints}
          repairPoints={gameState.repairPoints}
          damagedSystems={gameState.damagedSystems}
          smallDisplay={isDisplayHatMini}
        />
      </div>

      {/* Physical button indicators */}
      <div className={`grid grid-cols-4 gap-1 ${isDisplayHatMini ? 'p-1' : 'p-2'} border-t border-green-600`}>
        <Button
          variant="outline"
          className={`bg-black text-green-400 border-green-600 ${isDisplayHatMini ? 'h-8 text-xs' : 'h-12'}`}
          onClick={() => handleButtonPress(0)}
          disabled={gameState.boostPoints === 0 || gameState.boostActive}
        >
          {isDisplayHatMini ? "B1" : "BOOST (1)"}
        </Button>
        <Button
          variant="outline"
          className={`bg-black text-green-400 border-green-600 ${isDisplayHatMini ? 'h-8 text-xs' : 'h-12'}`}
          onClick={() => handleButtonPress(1)}
          disabled={
            gameState.repairPoints === 0 || gameState.damagedSystems.length === 0
          }
        >
          {isDisplayHatMini ? "R2" : "REPAIR (2)"}
        </Button>
        <Button
          variant="outline"
          className={`bg-black text-green-400 border-green-600 ${isDisplayHatMini ? 'h-8 text-xs' : 'h-12'}`}
          onClick={() => handleButtonPress(2)}
          disabled={!activeEvent}
        >
          {isDisplayHatMini ? "Y3" : "YES (3)"}
        </Button>
        <Button
          variant="outline"
          className={`bg-black text-green-400 border-green-600 ${isDisplayHatMini ? 'h-8 text-xs' : 'h-12'}`}
          onClick={() => handleButtonPress(3)}
          disabled={!activeEvent}
        >
          {isDisplayHatMini ? "N4" : "NO (4)"}
        </Button>
      </div>
      
      {/* GPIO Button Handler for Raspberry Pi */}
      <GPIOButtonHandler onButtonPress={handleButtonPress} />
    </div>
  );
};

export default GameScreen;
