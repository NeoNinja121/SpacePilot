#!/bin/bash
# Setup script for Idle Space Adventure on Raspberry Pi with Display HAT Mini

# Exit on error
set -e

echo "===== Idle Space Adventure - Display HAT Mini Setup ====="
echo "This script will configure your Raspberry Pi and Display HAT Mini"
echo "for optimal performance with Idle Space Adventure."
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo)."
  exit 1
fi

# Install required packages
echo "Installing required packages..."
apt update
apt install -y python3-pip python3-rpi.gpio python3-spidev python3-pil python3-numpy git xdotool

# Install Display HAT Mini driver if not already installed
if [ ! -d "/home/pi/displayhatmini-python" ]; then
  echo "Installing Display HAT Mini driver..."
  cd /home/pi
  git clone https://github.com/pimoroni/displayhatmini-python
  cd displayhatmini-python
  ./install.sh
else
  echo "Display HAT Mini driver already installed."
fi

# Configure boot/config.txt
echo "Configuring display settings..."
CONFIG_FILE="/boot/config.txt"

# Backup config.txt
cp $CONFIG_FILE ${CONFIG_FILE}.backup

# Check if Display HAT Mini config is already in config.txt
if ! grep -q "# Display HAT Mini configuration" $CONFIG_FILE; then
  # Add Display HAT Mini configuration
  cat >> $CONFIG_FILE << 'EOF'

# Display HAT Mini configuration
dtoverlay=vc4-kms-dpi-at056a,28,rgb888
hdmi_timings=320 0 20 40 20 240 0 4 10 4 0 0 0 60 0 6400000 1
enable_dpi_lcd=1
dpi_output_format=0x7f216
dpi_group=2
dpi_mode=87
gpu_mem=128
EOF
  echo "Added Display HAT Mini configuration to $CONFIG_FILE"
else
  echo "Display HAT Mini configuration already exists in $CONFIG_FILE"
fi

# Create touchscreen config
TOUCH_CONFIG="/etc/X11/xorg.conf.d/40-libinput.conf"
mkdir -p /etc/X11/xorg.conf.d/

# Check if touchscreen config already exists
if [ ! -f "$TOUCH_CONFIG" ]; then
  echo "Creating touchscreen configuration..."
  cat > $TOUCH_CONFIG << 'EOF'
Section "InputClass"
    Identifier "libinput touchscreen catchall"
    MatchIsTouchscreen "on"
    MatchDevicePath "/dev/input/event*"
    Driver "libinput"
    Option "TransformationMatrix" "1 0 0 0 1 0 0 0 1"
EndSection
EOF
  echo "Created touchscreen configuration at $TOUCH_CONFIG"
else
  echo "Touchscreen configuration already exists."
fi

# Create GPIO handler script
HANDLER_FILE="/home/pi/idle-space-adventure/gpio-handler.js"
mkdir -p /home/pi/idle-space-adventure

echo "Creating GPIO handler script..."
cat > $HANDLER_FILE << 'EOF'
const { Gpio } = require('onoff');
const { exec } = require('child_process');

// Initialize GPIO buttons for Display HAT Mini
const button1 = new Gpio(5, 'in', 'rising', { debounceTimeout: 50 });  // A button - BOOST
const button2 = new Gpio(6, 'in', 'rising', { debounceTimeout: 50 });  // B button - REPAIR
const button3 = new Gpio(16, 'in', 'rising', { debounceTimeout: 50 }); // X button - YES
const button4 = new Gpio(24, 'in', 'rising', { debounceTimeout: 50 }); // Y button - NO

// Use xdotool to simulate key presses
function simulateKeyPress(key) {
  exec(`DISPLAY=:0 xdotool key ${key}`);
}

// Watch for button presses
button1.watch((err, value) => {
  if (err) throw err;
  if (value === 1) simulateKeyPress('1');
});

button2.watch((err, value) => {
  if (err) throw err;
  if (value === 1) simulateKeyPress('2');
});

button3.watch((err, value) => {
  if (err) throw err;
  if (value === 1) simulateKeyPress('3');
});

button4.watch((err, value) => {
  if (err) throw err;
  if (value === 1) simulateKeyPress('4');
});

// Cleanup on exit
process.on('SIGINT', () => {
  button1.unexport();
  button2.unexport();
  button3.unexport();
  button4.unexport();
  process.exit();
});

console.log('GPIO button handler running. Press Ctrl+C to exit.');
EOF
echo "Created GPIO handler script at $HANDLER_FILE"
chmod +x $HANDLER_FILE

# Create autostart files for the game
echo "Creating autostart configuration..."
AUTOSTART_DIR="/etc/xdg/autostart"
mkdir -p $AUTOSTART_DIR

AUTOSTART_FILE="$AUTOSTART_DIR/idle-space.desktop"
cat > $AUTOSTART_FILE << 'EOF'
[Desktop Entry]
Type=Application
Name=Idle Space Adventure
Exec=/usr/bin/chromium-browser --start-fullscreen --app=http://localhost:3001 --kiosk --noerrdialogs --disable-translate --disable-features=TranslateUI --disable-gpu --disable-software-rasterizer --disable-dev-shm-usage --no-sandbox --process-per-site
EOF
echo "Created autostart configuration at $AUTOSTART_FILE"

# Create systemd service files
echo "Creating systemd service files..."
GAME_SERVICE="/etc/systemd/system/idle-space.service"
cat > $GAME_SERVICE << 'EOF'
[Unit]
Description=Idle Space Adventure Game
After=network.target

[Service]
ExecStart=/usr/bin/node /home/pi/idle-space-adventure/dist/server/index.js
WorkingDirectory=/home/pi/idle-space-adventure
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF
echo "Created game service at $GAME_SERVICE"

GPIO_SERVICE="/etc/systemd/system/gpio-buttons.service"
cat > $GPIO_SERVICE << 'EOF'
[Unit]
Description=GPIO Button Handler for Idle Space Adventure
After=idle-space.service

[Service]
ExecStart=/usr/bin/node /home/pi/idle-space-adventure/gpio-handler.js
WorkingDirectory=/home/pi/idle-space-adventure
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF
echo "Created GPIO handler service at $GPIO_SERVICE"

# Create backlight control script
BACKLIGHT_SCRIPT="/home/pi/set-display-brightness.py"
cat > $BACKLIGHT_SCRIPT << 'EOF'
#!/usr/bin/env python3
import displayhatmini
import sys

# Default brightness is 80%
brightness = 0.8

if len(sys.argv) > 1:
    try:
        brightness = float(sys.argv[1])
        # Ensure brightness is between 0 and 1
        brightness = max(0, min(1, brightness))
    except ValueError:
        print("Brightness must be a number between 0 and 1")
        sys.exit(1)

displayhatmini.set_backlight(brightness)
print(f"Display brightness set to {brightness*100}%")
EOF
chmod +x $BACKLIGHT_SCRIPT
echo "Created backlight control script at $BACKLIGHT_SCRIPT"

# Enable services
echo "Enabling services..."
systemctl enable idle-space.service
systemctl enable gpio-buttons.service

echo "Setup complete! Please install the node.js onoff package:"
echo "npm install onoff"
echo ""
echo "Reboot your Raspberry Pi to apply all changes:"
echo "sudo reboot"
