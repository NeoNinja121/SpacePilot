# Idle Space Adventure - Raspberry Pi Zero 2 Setup Guide

This document provides instructions for setting up and running Idle Space Adventure on a Raspberry Pi Zero 2.

## Hardware Requirements

- Raspberry Pi Zero 2 W
- MicroSD card (at least 8GB)
- 4 physical push buttons
- Jumper wires
- 4 x 10kΩ resistors (for button pull-downs)
- Power supply (5V, 2.5A recommended)
- Display with HDMI input (or HDMI to compatible adapter)

## Software Setup

### 1. Prepare the Raspberry Pi OS

1. Download and install Raspberry Pi Imager from the [official website](https://www.raspberrypi.org/software/)
2. Insert your MicroSD card and launch the Raspberry Pi Imager
3. Select "Choose OS" > "Raspberry Pi OS (32-bit)" or "Raspberry Pi OS Lite (32-bit)" for better performance
4. Select your MicroSD card
5. Click on the gear icon to access advanced options:
   - Set hostname: `idlespace`
   - Enable SSH
   - Set username and password
   - Configure Wi-Fi
6. Click "Write" to create the SD card

### 2. First Boot and Updates

1. Insert the SD card into your Pi Zero 2 and power it on
2. Connect to your Pi via SSH or use a keyboard/monitor:
   ```
   ssh pi@idlespace.local
   ```
3. Update your system:
   ```
   sudo apt update
   sudo apt upgrade -y
   ```

### 3. Install Required Software

Install Node.js, Git, and other dependencies:

```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Git
sudo apt install -y git

# Install other dependencies
sudo apt install -y chromium-browser xorg openbox
```

### 4. Clone and Set Up the Game

```bash
# Clone the repository
git clone https://github.com/yourusername/idle-space-adventure.git
cd idle-space-adventure

# Install dependencies
npm install

# Build the game
npm run build
```

### 5. Set Up GPIO Buttons

Connect your buttons to GPIO pins:

- Button 1 (BOOST): GPIO 17
- Button 2 (REPAIR): GPIO 27
- Button 3 (YES): GPIO 22
- Button 4 (NO): GPIO 23

Install the GPIO library:

```bash
npm install onoff
```

Create a file called `gpio-handler.js` in the project root:

```javascript
const { Gpio } = require('onoff');
const { exec } = require('child_process');

// Initialize GPIO buttons with pull-down resistors
const button1 = new Gpio(17, 'in', 'rising', { debounceTimeout: 50 });
const button2 = new Gpio(27, 'in', 'rising', { debounceTimeout: 50 });
const button3 = new Gpio(22, 'in', 'rising', { debounceTimeout: 50 });
const button4 = new Gpio(23, 'in', 'rising', { debounceTimeout: 50 });

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
```

### 6. Set Up Autostart

Create a startup script in `/etc/xdg/autostart/idle-space.desktop`:

```
[Desktop Entry]
Type=Application
Name=Idle Space Adventure
Exec=/usr/bin/chromium-browser --start-fullscreen --app=http://localhost:3001 --kiosk --noerrdialogs --disable-translate
```

Create a systemd service for the game:

```bash
sudo nano /etc/systemd/system/idle-space.service
```

Add the following content:

```
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
```

Create another service for the GPIO button handler:

```bash
sudo nano /etc/systemd/system/gpio-buttons.service
```

Add the following content:

```
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
```

Enable and start the services:

```bash
sudo systemctl enable idle-space.service
sudo systemctl enable gpio-buttons.service
sudo systemctl start idle-space.service
sudo systemctl start gpio-buttons.service
```

### 7. Performance Optimization

For better performance on the Pi Zero 2:

1. Disable screen blanking:
   ```bash
   sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
   ```
   Add these lines:
   ```
   @xset s off
   @xset -dpms
   @xset s noblank
   ```

2. Overclock the Pi (optional but improves performance):
   ```bash
   sudo nano /boot/config.txt
   ```
   Add:
   ```
   arm_freq=1100
   gpu_freq=500
   over_voltage=2
   ```

## Troubleshooting

- **Game runs slowly**: Try the lite version of Raspberry Pi OS, reduce background services, and ensure proper cooling for the Pi Zero 2.
- **Buttons not responding**: Check wiring connections and ensure GPIO numbers match the configuration.
- **Screen remains blank**: Check HDMI connections and try forcing HDMI output in `/boot/config.txt`.
- **Game crashes**: Check logs with `journalctl -u idle-space.service` to identify issues.

## Maintenance

- **Update the game**:
  ```bash
  cd ~/idle-space-adventure
  git pull
  npm install
  npm run build
  sudo systemctl restart idle-space.service
  ```

- **Backup game data**:
  ```bash
  cp ~/idle-space-adventure/data/game_stats.json ~/game_backup.json
  ```

## Resources

- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)
- [Node.js on Raspberry Pi](https://www.w3schools.com/nodejs/nodejs_raspberrypi.asp)
- [Chromium Command Line Switches](https://peter.sh/experiments/chromium-command-line-switches/)
