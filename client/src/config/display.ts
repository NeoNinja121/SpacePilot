/**
 * Display configuration for different screen types
 */

export interface DisplayConfig {
  type: string;
  width: number;
  height: number;
  scaling: number;
  touchEnabled: boolean;
  fullscreen: boolean;
}

// Display HAT Mini configuration
// 2.0" IPS LCD with 320x240 resolution
export const DISPLAY_HAT_MINI: DisplayConfig = {
  type: "display_hat_mini",
  width: 320,
  height: 240,
  scaling: 0.5,
  touchEnabled: true,
  fullscreen: true
};

// Standard desktop display configuration
export const DESKTOP_DISPLAY: DisplayConfig = {
  type: "standard",
  width: 1280,
  height: 720,
  scaling: 1,
  touchEnabled: false,
  fullscreen: false
};

// Auto-detect display type
// This will use navigator.userAgent and screen dimensions to determine
// if we're likely running on a Raspberry Pi with Display HAT Mini
export function detectDisplayType(): DisplayConfig {
  // On the Pi, window.screen will report the HAT dimensions
  if (window.screen.width === 320 && window.screen.height === 240) {
    return DISPLAY_HAT_MINI;
  }
  
  // Check for Raspberry Pi in user agent
  const isRaspberryPi = navigator.userAgent.toLowerCase().includes("linux") && 
                         (navigator.userAgent.toLowerCase().includes("arm") || 
                          navigator.userAgent.toLowerCase().includes("aarch64"));
                          
  // If we detect Raspberry Pi and the screen is small, assume it's the HAT
  if (isRaspberryPi && window.screen.width <= 800) {
    return DISPLAY_HAT_MINI;
  }
  
  // Default to standard display
  return DESKTOP_DISPLAY;
}

// Apply display configuration to document
export function applyDisplayConfig(config: DisplayConfig): void {
  // Add meta viewport tag for proper scaling
  const viewport = document.querySelector('meta[name="viewport"]');
  if (viewport) {
    viewport.setAttribute('content', 
      `width=${config.width}, initial-scale=${config.scaling}, maximum-scale=${config.scaling}, user-scalable=no`
    );
  }
  
  // Set CSS variables for display dimensions
  document.documentElement.style.setProperty('--display-width', `${config.width}px`);
  document.documentElement.style.setProperty('--display-height', `${config.height}px`);
  document.documentElement.style.setProperty('--display-scaling', `${config.scaling}`);
  
  // Add display type class to body
  document.body.classList.add(`display-${config.type}`);
  
  // Force fullscreen if needed
  if (config.fullscreen && document.documentElement.requestFullscreen) {
    document.documentElement.requestFullscreen().catch(err => {
      console.warn("Could not enter fullscreen mode:", err);
    });
  }
}
