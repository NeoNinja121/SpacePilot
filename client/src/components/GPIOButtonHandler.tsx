import * as React from "react";

interface GPIOButtonHandlerProps {
  onButtonPress: (buttonIndex: number) => void;
}

// This component handles integrating the Raspberry Pi's GPIO buttons with the game
const GPIOButtonHandler: React.FC<GPIOButtonHandlerProps> = ({ onButtonPress }) => {
  // This component doesn't render anything visible
  React.useEffect(() => {
    // In a real Raspberry Pi implementation, this is where you would:
    // 1. Initialize GPIO pins for the 4 physical buttons
    // 2. Set up event listeners for button presses
    // 3. Call onButtonPress when physical buttons are pressed
    
    // Mock implementation for development environments (non-Pi)
    const handleKeyDown = (e: KeyboardEvent) => {
      switch (e.key) {
        case "1":
        case "q":
          onButtonPress(0); // Button 1 (Boost)
          break;
        case "2":
        case "w":
          onButtonPress(1); // Button 2 (Repair)
          break;
        case "3":
        case "e":
          onButtonPress(2); // Button 3 (Yes)
          break;
        case "4":
        case "r":
          onButtonPress(3); // Button 4 (No)
          break;
        default:
          break;
      }
    };

    // Add keyboard event listeners for development testing
    window.addEventListener("keydown", handleKeyDown);

    // Function to call when component unmounts
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      // In a real implementation, you would clean up GPIO resources here
    };
  }, [onButtonPress]);

  // This component doesn't render anything visible
  return null;
};

export default GPIOButtonHandler;
