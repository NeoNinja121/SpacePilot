import RPi.GPIO as GPIO
import time

BUTTON_PINS = [5, 6, 16, 24]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for pin in BUTTON_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def button_callback(channel):
    print(f"Button on GPIO {channel} pressed")

for pin in BUTTON_PINS:
    GPIO.add_event_detect(pin, GPIO.RISING, callback=button_callback, bouncetime=300)

print("Listening for button presses (A, B, X, Y)... Ctrl+C to stop.")
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting cleanly.")
