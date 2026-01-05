# Touchscreen Keyboard for Android GhostOS

## Overview

The GhostOS touchscreen keyboard is designed primarily for **Android devices** running the GhostOS environment. It provides a full-featured virtual keyboard with calibration support, perfect for Android tablets and phones.

## Why This Keyboard?

### Android Use Cases

1. **Termux + GhostOS**: Use the keyboard within the Termux proot environment
2. **Python GUI Apps**: Run Python/PyQt6 apps on Android with full keyboard support
3. **Development**: Code and test on Android with proper keyboard input
4. **Remote Access**: Control remote systems from Android with virtual keyboard
5. **Touchscreen Testing**: Test touchscreen calibration and responsiveness

## Android Installation

### Prerequisites

1. **Termux** (from F-Droid, NOT Google Play)
2. **Termux:API** (from F-Droid)
3. **Android 9.0+** (API 28 or higher)
4. **Storage**: 500MB free space
5. **Permissions**: Storage, Display over other apps

### Quick Installation

```bash
# In Termux
pkg update && pkg upgrade -y
pkg install python git -y

# Clone repository
git clone https://github.com/jameshroop-art/GO-OS
cd GO-OS/gui/ghostos-iso-builder

# Install dependencies
pip install -r requirements.txt

# Install X11 packages for GUI (if needed)
pkg install x11-repo -y
pkg install termux-x11-nightly -y
```

### Starting the Keyboard on Android

#### Method 1: VNC Server (Recommended)

```bash
# Install VNC server
pkg install tigervnc -y

# Start VNC server
vncserver :1 -geometry 1920x1080

# In a VNC viewer app, connect to localhost:5901
# Then run:
export DISPLAY=:1
cd GO-OS/gui/ghostos-iso-builder
python3 main.py
```

#### Method 2: Termux:X11

```bash
# Start Termux:X11 app first (from Android launcher)

# In Termux:
export DISPLAY=:0
cd GO-OS/gui/ghostos-iso-builder
./start-gui.sh
```

#### Method 3: Standalone Keyboard

```bash
# Run just the keyboard
cd GO-OS/gui/ghostos-iso-builder
python3 -c "
import sys
from PyQt6.QtWidgets import QApplication
from ui.touchscreen_keyboard import TouchscreenKeyboard

app = QApplication(sys.argv)
kb = TouchscreenKeyboard()
kb.show_keyboard()
sys.exit(app.exec())
"
```

## Android-Specific Features

### Touch Optimization

The keyboard is optimized for touch input:

- **Large Keys**: Default 50px minimum size
- **Touch Targets**: Keys sized for finger taps (not stylus required)
- **Spacing**: 2px gaps prevent accidental presses
- **Feedback**: Visual feedback on key press
- **Snap Zones**: Easy edge positioning with 20px snap distance

### Screen Adaptations

Automatically adapts to Android screens:

- **Portrait Mode**: Keyboard at bottom, reduces to minimal height
- **Landscape Mode**: Full QWERTY layout with larger keys
- **Tablet Mode**: Expanded layout with numpad option
- **Phone Mode**: Compact layout optimized for smaller screens

### Calibration for Android

Android touchscreens typically need less calibration, but it's available:

1. Tap **🎯** button on keyboard
2. Calibrate with your finger (no stylus needed)
3. System adjusts for touch offset
4. Saved to device storage

### Power Efficiency

Optimized for Android battery life:

- **Low CPU**: Minimal processing (~1% CPU)
- **No Background**: Only active when visible
- **Smart Refresh**: Updates only on interaction
- **Sleep Mode**: Dims when inactive

## Android Use Cases

### 1. Termux Development

```bash
# Use keyboard for Python development
cd ~/projects
nano app.py  # Use virtual keyboard for input

# Or use Python REPL
python3
>>> # Type with virtual keyboard
```

### 2. SSH Remote Access

```bash
# SSH with virtual keyboard
pkg install openssh -y
ssh user@remote-server
# Use keyboard for remote terminal input
```

### 3. GUI Applications

```python
# Run GUI apps with keyboard support
from PyQt6.QtWidgets import QApplication, QLineEdit
from ui.touchscreen_keyboard import TouchscreenKeyboard

app = QApplication([])
text_input = QLineEdit()
text_input.show()

keyboard = TouchscreenKeyboard()
keyboard.key_pressed.connect(text_input.insert)
keyboard.show()

app.exec()
```

### 4. Text Editing

```bash
# Edit configuration files
nano ~/.bashrc  # Use keyboard for text input
vim ~/.zshrc    # Keyboard works with vim
```

## Android-Specific Settings

### Display Scaling

Adjust for different Android screen densities:

```python
# In main.py or startup script
import os
os.environ['QT_SCALE_FACTOR'] = '1.5'  # For high-DPI Android screens
```

### Touch Sensitivity

Adjust touch thresholds for Android:

```python
keyboard = TouchscreenKeyboard()
keyboard.SNAP_DISTANCE = 30  # Larger snap zone for fingers
```

### Layout for Phones

Use compact layout on phones:

```python
keyboard.change_layout('numpad')  # Numeric keypad for easier one-hand use
```

## Troubleshooting Android Issues

### Keyboard Not Appearing

**Problem**: Keyboard doesn't show on Android

**Solutions**:
```bash
# Check X11/VNC is running
echo $DISPLAY

# Verify PyQt6 installation
pip list | grep PyQt6

# Check Android permissions
# Settings → Termux → Permissions → Display over other apps

# Try forcing Qt platform
export QT_QPA_PLATFORM=xcb
python3 main.py
```

### Touch Input Not Working

**Problem**: Touches not registering

**Solutions**:
1. Run calibration wizard
2. Check Android touch driver: `getevent -l`
3. Verify X11 input: `xinput list`
4. Try increasing key size
5. Disable pointer acceleration

### VNC Connection Issues

**Problem**: Can't connect to VNC

**Solutions**:
```bash
# Kill existing VNC servers
vncserver -kill :1

# Restart with specific geometry
vncserver :1 -geometry 1920x1080 -depth 24

# Check listening ports
netstat -tulpn | grep 5901

# Connect to correct address in VNC viewer
# Use: localhost:5901 or 127.0.0.1:5901
```

### Performance Issues

**Problem**: Keyboard is slow on Android

**Solutions**:
1. Reduce key count (use numpad layout)
2. Disable animations
3. Lower screen resolution in VNC
4. Close background apps
5. Use lighter color themes

### Storage Issues

**Problem**: Not enough space

**Solutions**:
```bash
# Check available space
df -h $HOME

# Clean package cache
pkg clean

# Remove unnecessary files
rm -rf ~/.cache/*

# Move to external SD (if available)
termux-setup-storage
mv ~/GO-OS /sdcard/GO-OS
ln -s /sdcard/GO-OS ~/GO-OS
```

## Performance Tips for Android

### Optimize for Battery

```bash
# Use compact layouts
keyboard.change_layout('numpad')

# Disable background refresh
keyboard.setUpdatesEnabled(False)  # When not in use

# Hide when not needed
keyboard.hide_keyboard()
```

### Optimize for Speed

```bash
# Reduce visual effects
# Use solid colors instead of gradients
# Disable key press animations
# Use lightweight font
```

### Optimize for Small Screens

```python
# Adjust keyboard size for phone screens
keyboard.resize(600, 200)  # Smaller keyboard for phones

# Use numpad mode for one-hand typing
keyboard.change_layout('numpad')
```

## Android Device Compatibility

### Tested Devices

- ✅ Android 9.0+ (API 28+)
- ✅ ARMv7, ARM64, x86, x86_64
- ✅ Tablets (7" to 12")
- ✅ Phones (5" to 7")
- ✅ Termux + VNC
- ✅ Termux + X11

### Known Limitations

- ⚠️ Requires VNC or X11 server (no native Android UI)
- ⚠️ Not compatible with Google Play Termux
- ⚠️ Requires F-Droid Termux
- ⚠️ May need "Draw over other apps" permission
- ⚠️ Performance varies by device hardware

## Integration with Android Features

### Termux:API Integration

```bash
# Use with Termux:API features
termux-clipboard-set "$(python3 keyboard_input.py)"
termux-sms-send -n +1234567890 "$(python3 keyboard_input.py)"
```

### Android Storage Access

```bash
# Access shared storage
termux-setup-storage

# Save keyboard layouts to shared storage
mkdir -p ~/storage/shared/keyboard_layouts
cp ~/.config/ghostos-builder/keyboard_layouts/* ~/storage/shared/keyboard_layouts/
```

### Android Notifications

```python
# Send notification on keyboard action
import subprocess
subprocess.run(['termux-notification', '--title', 'Keyboard', '--content', 'Layout changed'])
```

## Advanced Android Usage

### Autostart on Termux Launch

Add to `~/.bashrc`:

```bash
# Auto-start keyboard in background
if [ -n "$DISPLAY" ]; then
    ~/GO-OS/gui/ghostos-iso-builder/start-keyboard.sh &
fi
```

### Custom Android Layouts

Create Android-optimized layouts:

```json
{
  "name": "Android Compact",
  "optimized_for": "phone",
  "rows": [
    [
      {"label": "Q", "value": "q", "width": 1.2},
      {"label": "W", "value": "w", "width": 1.2}
    ]
  ]
}
```

### Integration with Android Apps

Use keyboard with Termux apps:

```bash
# Use with Termux text editors
pkg install micro -y
micro myfile.txt  # Virtual keyboard for input

# Use with programming environments
pkg install nodejs -y
node  # REPL with keyboard support
```

## Security on Android

### Permissions

Required Android permissions:
- ✅ Storage (for config files)
- ✅ Display over other apps (for floating keyboard)
- ❌ Internet (NOT required - no network access)
- ❌ Location (NOT required)
- ❌ Camera (NOT required)

### Privacy

- All data stored locally in Termux home
- No telemetry or analytics
- No internet connection required
- Calibration data never leaves device
- Open source - verify the code yourself

## Future Android Enhancements

Planned features for Android:

- [ ] Native Android UI (no X11/VNC required)
- [ ] Haptic feedback on key press
- [ ] Android keyboard integration (use as system keyboard)
- [ ] Gesture typing support
- [ ] Multi-language support
- [ ] Android Auto support
- [ ] Wear OS compatibility
- [ ] Android TV remote keyboard

## Support for Android

### Getting Help

1. **Check Documentation**: This guide + main KEYBOARD_GUIDE.md
2. **Termux Wiki**: https://wiki.termux.com
3. **GitHub Issues**: Tag with "android" label
4. **Termux Community**: Reddit r/termux

### Reporting Android-Specific Issues

When reporting issues, include:

```bash
# Device info
uname -a
getprop ro.build.version.release  # Android version
getprop ro.product.model           # Device model

# Termux info
pkg list-installed | grep -E "python|pyqt|x11"

# Display info
echo $DISPLAY
xrandr -q  # If X11 available

# Keyboard logs
python3 main.py 2>&1 | tee keyboard.log
```

## Resources

### Android Development

- **Termux**: https://termux.com
- **F-Droid**: https://f-droid.org
- **Termux:API**: https://wiki.termux.com/wiki/Termux:API
- **Python on Android**: https://wiki.termux.com/wiki/Python

### Related Projects

- **PyQt6 Android**: Community builds for ARM/Android
- **XSDL**: X Server for Android
- **Termux:X11**: Native X11 for Termux
- **AnLinux**: Linux on Android (alternative)

---

**GhostOS Touchscreen Keyboard** - Professional virtual keyboard for Android and touchscreen Linux devices

For desktop touchscreen usage, see [KEYBOARD_GUIDE.md](KEYBOARD_GUIDE.md)
