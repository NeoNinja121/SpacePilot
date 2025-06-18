"""
Display configuration for different screen types
"""
import pygame
import os
import platform

class DisplayConfig:
    """Configuration for different display types"""
    
    def __init__(self, display_type, width, height, scaling, 
                 touch_enabled=False, fullscreen=False):
        self.type = display_type
        self.width = width
        self.height = height
        self.scaling = scaling
        self.touch_enabled = touch_enabled
        self.fullscreen = fullscreen
        self.is_display_hat_mini = (display_type == "display_hat_mini")
        
# Display HAT Mini configuration
# 2.0" IPS LCD with 320x240 resolution
DISPLAY_HAT_MINI = DisplayConfig(
    display_type="display_hat_mini",
    width=320,
    height=240,
    scaling=0.5,
    touch_enabled=True,
    fullscreen=True
)

# Standard desktop display configuration
DESKTOP_DISPLAY = DisplayConfig(
    display_type="standard",
    width=800,
    height=600,
    scaling=1,
    touch_enabled=False,
    fullscreen=False
)

def detect_display():
    # Force use of Display HAT Mini for development/testing
    return DISPLAY_HAT_MINI
