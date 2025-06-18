/**
 * Utilities for optimizing game performance on low-powered devices like Raspberry Pi Zero 2
 */

// Track frame rate
let frameCount = 0;
let lastTime = performance.now();
let fps = 0;

// Measure frames per second
export function measureFPS(): number {
  frameCount++;
  const currentTime = performance.now();
  const elapsedTime = currentTime - lastTime;
  
  if (elapsedTime >= 1000) {
    fps = frameCount / (elapsedTime / 1000);
    frameCount = 0;
    lastTime = currentTime;
  }
  
  return fps;
}

// Throttle animations based on device performance
export function shouldSkipFrame(targetFPS: number = 30): boolean {
  // If FPS is dropping below target, start skipping frames
  return fps > 0 && fps < targetFPS / 2;
}

// Reduce animation complexity based on measured performance
export function getAnimationQuality(): "high" | "medium" | "low" {
  if (fps === 0 || fps > 45) {
    return "high";
  } else if (fps > 25) {
    return "medium";
  } else {
    return "low";
  }
}

// Optimize star field density based on performance
export function getOptimalStarDensity(): number {
  const quality = getAnimationQuality();
  
  switch (quality) {
    case "high":
      return 100;
    case "medium":
      return 50;
    case "low":
      return 20;
    default:
      return 30;
  }
}

// Reduce animation frame rate when needed
export function getOptimalAnimationInterval(): number {
  const quality = getAnimationQuality();
  
  switch (quality) {
    case "high":
      return 100;
    case "medium":
      return 150;
    case "low":
      return 250;
    default:
      return 150;
  }
}

// Helper for Raspberry Pi to detect if running on low-power hardware
export function detectLowPowerHardware(): boolean {
  // This is a simple heuristic - in a real implementation, you would
  // check for Raspberry Pi specific environment variables or device info
  
  // Look for common mobile/low-power CPU signatures
  const userAgent = navigator.userAgent.toLowerCase();
  const isMobile = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent);
  
  // Check available memory (if API is available)
  const lowMemory = navigator.deviceMemory !== undefined && navigator.deviceMemory < 4;
  
  // Check hardware concurrency (CPU cores)
  const lowCpuCores = navigator.hardwareConcurrency !== undefined && navigator.hardwareConcurrency <= 4;
  
  return isMobile || lowMemory || lowCpuCores;
}

// Enable optimizations for Pi hardware
export function enablePiOptimizations(): void {
  // Reduce animation frame rates
  document.documentElement.style.setProperty('--animation-speed-factor', '0.5');
  
  // Disable complex CSS animations
  if (detectLowPowerHardware()) {
    const styleSheet = document.createElement('style');
    styleSheet.textContent = `
      @media (display-mode: fullscreen) {
        .stars-small, .stars-medium { animation-duration: 180s !important; }
        .stars-large { animation-duration: 120s !important; }
        .boost-particle-0, .boost-particle-1, .boost-particle-2, .boost-particle-3, .boost-particle-4 {
          animation-duration: 1s !important;
        }
      }
    `;
    document.head.appendChild(styleSheet);
  }
}
