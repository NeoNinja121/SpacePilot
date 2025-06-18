# Display HAT Mini Setup Guide for Idle Space Adventure

This guide will help you set up Idle Space Adventure on a Raspberry Pi Zero 2 with a Display HAT Mini.

## Hardware Requirements

- Raspberry Pi Zero 2 W
- [Display HAT Mini](https://shop.pimoroni.com/products/display-hat-mini) (2.0" IPS LCD, 320×240 pixels)
- 4 momentary tactile buttons (or use the buttons on the Display HAT Mini)
- MicroSD card (at least 8GB)
- Power supply (5V/2.5A recommended)

## Display HAT Mini Installation

1. Before powering your Raspberry Pi, connect the Display HAT Mini to the GPIO pins
2. Make sure the Display HAT Mini is seated correctly on all 40 GPIO pins

## Software Setup

### 1. Install Raspberry Pi OS

Follow the OS installation instructions in the main README-RaspberryPi.md file.

### 2. Install Display HAT Mini Drivers

```bash
# Install required packages
sudo apt update
sudo apt install -y python3-pip python3-rpi.gpio python3-spidev python3-pil python3-numpy git

# Install Display HAT Mini drivers
git clone https://github.com/pimoroni/displayhatmini-python
cd displayhatmini-python
sudo ./install.sh
```

### 3. Configure Display Resolution

Edit the config.txt file to set the correct resolution:

```bash
sudo nano /boot/config.txt
```

Add these lines at the end:

```
# Display HAT Mini configuration
dtoverlay=vc4-kms-dpi-at056a,28,rgb888
hdmi_timings=320 0 20 40 20 240 0 4 10 4 0 0 0 60 0 6400000 1
enable_dpi_lcd=1
dpi_output_format=0x7f216
dpi_group=2
dpi_mode=87
```

### 4. Configure X-Server for Touchscreen

Create a configuration file for X:

```bash
sudo nano /etc/X11/xorg.conf.d/40-libinput.conf
```

Add the following:

```
Section "InputClass"
    Identifier "libinput touchscreen catchall"
    MatchIsTouchscreen "on"
    MatchDevicePath "/dev/input/event*"
    Driver "libinput"
    Option "TransformationMatrix" "1 0 0 0 1 0 0 0 1"
EndSection
```

### 5. Rotate Display (Optional)

If you need to rotate the display, edit the config.txt file:

```bash
sudo nano /boot/config.txt
```

Add one of these lines based on your desired orientation:

```
# 90 degrees (landscape)
display_rotate=1

# 180 degrees
display_rotate=2

# 270 degrees
display_rotate=3
```

### 6. Setup Game for Display HAT Mini

The game already includes optimizations for the Display HAT Mini's 320×240 resolution. When the game detects this screen size, it will automatically:

- Use a more compact UI layout
- Show abbreviated text
- Use larger buttons for better touch interaction
- Reduce animation complexity for better performance

### 7. Using the Display HAT Mini Buttons

The Display HAT Mini has 4 buttons labeled A, B, X, Y that connect to these GPIO pins:

- Button A: GPIO 5
- Button B: GPIO 6
- Button X: GPIO 16
- Button Y: GPIO 24

Edit the gpio-handler.js file to use these pins:

```bash
nano gpio-handler.js
```

Update the GPIO pin numbers:

```javascript
// Initialize GPIO buttons for Display HAT Mini
const button1 = new Gpio(5, 'in', 'rising', { debounceTimeout: 50 });  // A button - BOOST
const button2 = new Gpio(6, 'in', 'rising', { debounceTimeout: 50 });  // B button - REPAIR
const button3 = new Gpio(16, 'in', 'rising', { debounceTimeout: 50 }); // X button - YES
const button4 = new Gpio(24, 'in', 'rising', { debounceTimeout: 50 }); // Y button - NO
```

### 8. Final Tweaks for Better Performance

1. Reduce Chrome's memory usage:

```bash
sudo nano /etc/xdg/autostart/idle-space.desktop
```

Update the Chromium command:

```
[Desktop Entry]
Type=Application
Name=Idle Space Adventure
Exec=/usr/bin/chromium-browser --start-fullscreen --app=http://localhost:3001 --kiosk --noerrdialogs --disable-translate --disable-features=TranslateUI --disable-gpu --disable-software-rasterizer --disable-dev-shm-usage --no-sandbox --process-per-site
```

2. Allocate more memory to GPU:

```bash
sudo nano /boot/config.txt
```

Add:

```
gpu_mem=128
```

3. Reboot your Raspberry Pi:

```bash
sudo reboot
```

## Troubleshooting Display HAT Mini Issues

### Screen shows random colors or no image

- Check that the Display HAT Mini is properly seated on all GPIO pins
- Verify your config.txt settings match the ones above
- Try lowering the GPU clock speed if you're overclocking

### Touch input is misaligned

Run the touchscreen calibration tool:

```bash
sudo apt-get install -y xinput-calibrator
DISPLAY=:0 xinput_calibrator
```

Follow the on-screen instructions and update your configuration with the results.

### Display is too dim

The Display HAT Mini has a backlight control. You can adjust it with:

```bash
python3 -c "import displayhatmini; displayhatmini.set_backlight(0.8)" # 80% brightness
```

Add this to your startup scripts to set it automatically.

### Game runs slowly

- Try overclocking your Pi Zero 2 (see main README)
- Close any background processes
- Lower the resolution in the game's display settings (if available)
- Ensure the GPU memory split is at least 128MB
