"""
GPIO Handler for Raspberry Pi buttons
"""

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

class GPIOHandler:
    """Handler for GPIO button inputs on Raspberry Pi"""
    
    def __init__(self, callback_function, use_display_hat_buttons=True):
        """
        Initialize GPIO handler with callback function
        
        Args:
            callback_function: Function to call when button is pressed
            use_display_hat_buttons: Use Display HAT Mini buttons if True
        """
        if not GPIO_AVAILABLE:
            raise ImportError("RPi.GPIO module not available")
            
        self.callback = callback_function
        
        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Set up pins for buttons
        if use_display_hat_buttons:
            # Display HAT Mini buttons
            self.button_pins = [16, 24, 5, 6]  # A, X, B, Y  → reordered to match game logic

        else:
            # Default GPIO pins
            self.button_pins = [17, 27, 22, 23]
            
        # Set up GPIO pins with pull-down resistors
        for pin in self.button_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(pin, GPIO.RISING, 
                                 callback=self._button_callback,
                                 bouncetime=300)
                                 
        print(f"GPIO initialized with pins: {self.button_pins}")
        
    def _button_callback(self, channel):
        """Internal callback for GPIO button press"""
        button_index = self.button_pins.index(channel)
        self.callback(button_index)
        
    def cleanup(self):
        """Clean up GPIO resources"""
        if GPIO_AVAILABLE:
            GPIO.cleanup()
            
class KeyboardHandler:
    """
    Fallback handler for systems without GPIO
    Uses pygame events for keyboard control
    """
    
    def __init__(self, callback_function):
        """Initialize keyboard handler"""
        self.callback = callback_function
        
    def process_key(self, key):
        """Process keyboard input"""
        # Map keys to button indices
        key_mapping = {
            '1': 0,  # Boost
            'q': 0,
            '2': 1,  # Repair
            'w': 1,
            '3': 2,  # Yes
            'e': 2,
            '4': 3,  # No
            'r': 3
        }
        
        if key in key_mapping:
            self.callback(key_mapping[key])
            
    def cleanup(self):
        """No cleanup needed"""
        pass
