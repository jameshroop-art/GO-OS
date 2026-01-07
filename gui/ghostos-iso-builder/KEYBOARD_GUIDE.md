# Touchscreen Keyboard Integration

## Overview

The Heck-CheckOS ISO Builder now includes a fully-featured touchscreen keyboard with calibration support, customization capabilities, and seamless integration with all GUI components.

## Features

### 🎯 Core Features
- **Resizable Keyboard**: Adjust keyboard size to fit your needs
- **Edge Snapping**: Automatically snaps to screen edges (top, bottom, left, right)
- **Touch Calibration**: Multi-point calibration wizard for accurate touch input
- **Layout Switching**: Quick switch between QWERTY, numeric keypad, and custom layouts
- **Always-on-Top**: Stays visible above all other windows
- **Draggable**: Click and drag the title bar to reposition

### 🎨 Customization
- **Visual Layout Designer**: Create custom keyboard layouts with drag-and-drop
- **Key Customization**: Adjust key size, color, font, and function
- **Theme Support**: Matches Gaming and Production mode themes
- **Layout Save/Load**: Save and share custom keyboard layouts
- **Preset Layouts**: Built-in presets for common use cases

### 🔧 Calibration System
- **5-Point Calibration**: Touch 5 points on screen for accuracy calculation
- **Offset Correction**: Automatically corrects touch input offsets
- **Per-Installation Storage**: Calibration persists across sessions
- **Easy Recalibration**: Recalibrate anytime with one click

### 🔌 Integration
- **Auto-Integration**: Works with all text input fields in the GUI
- **Keyboard Shortcuts**: Toggle keyboard with toolbar button
- **Focus-Aware**: Sends keystrokes to the currently focused input field
- **ISO Build Support**: Keyboard included in generated ISOs

## Quick Start

### Starting the GUI with Keyboard Support

```bash
cd gui/heckcheckos-iso-builder
./start-gui.sh
```

The launcher script will:
1. Check for all dependencies
2. Detect touchscreen devices
3. Verify display availability
4. Launch the GUI with keyboard support

### Enabling the Keyboard

1. Click the **⌨ Keyboard** button in the toolbar
2. The keyboard appears at the bottom of the screen
3. Click any input field to focus it
4. Type using the touchscreen keyboard

### First-Time Calibration

1. Click the **🎯** button on the keyboard title bar
2. Follow the on-screen calibration wizard:
   - Tap 5 target points as accurately as possible
   - The system calculates offset corrections
   - Calibration is saved automatically
3. Click **Finish** to apply calibration

## Keyboard Layouts

### Built-in Layouts

#### QWERTY Full
- Standard full keyboard with all keys
- Number row, function keys, and modifiers
- Best for general text input

#### Numeric Keypad
- Calculator-style layout
- Perfect for number entry
- Includes basic operators

#### Custom Layouts
- Design your own keyboard layouts
- Optimized for specific workflows
- Save and load custom configurations

### Creating Custom Layouts

1. Click **⚙** on keyboard → **Custom Layout**
2. Opens the **Keyboard Layout Designer**
3. Add/remove rows and keys
4. Customize each key:
   - Label (display text)
   - Value (actual key sent)
   - Width (key size multiplier)
   - Colors (background and text)
   - Font size
5. Save layout to JSON file
6. Load in any Heck-CheckOS installation

## Calibration Guide

### When to Calibrate

Calibrate your keyboard when:
- First time using a touchscreen
- Touch input seems inaccurate
- After changing screen resolution
- On a new installation
- Touch targets are consistently missed

### Calibration Process

1. **Launch Calibration Wizard**
   - Click 🎯 on keyboard title bar
   - Or Settings → Calibrate Touch

2. **Tap Target Points**
   - 5 targets appear across the screen
   - Tap the center of each target accurately
   - Progress bar shows completion

3. **Review Results**
   - Wizard calculates offset (X, Y pixels)
   - Shows calibration summary
   - Options to restart or accept

4. **Apply Calibration**
   - Click **Finish** to save
   - Calibration applies immediately
   - Stored in `~/.config/heckcheckos-builder/keyboard_calibration.json`

### Calibration Tips

- Use a stylus for more accuracy
- Tap slowly and deliberately
- Ensure screen is clean
- Recalibrate if touch still feels off
- Different users may need different calibrations

## Configuration

### Calibration Storage

Calibration data is stored per-user:
```
~/.config/heckcheckos-builder/
├── keyboard_calibration.json    # Touch offset data
├── keyboard_layouts/            # Custom layouts
│   ├── my_layout.json
│   └── gaming_layout.json
└── keyboard_settings.json       # Keyboard preferences
```

### Calibration File Format

```json
{
  "offset_x": 5,
  "offset_y": -3
}
```

### Layout File Format

```json
{
  "name": "Custom Gaming Layout",
  "version": "1.0",
  "rows": [
    [
      {
        "label": "W",
        "value": "w",
        "width": 1.0,
        "bg_color": "#2d2d2d",
        "fg_color": "#e0e0e0",
        "font_size": 11
      }
    ]
  ]
}
```

## Advanced Usage

### Snapping Behavior

The keyboard automatically snaps to screen edges:

- **Within 20px of edge**: Snaps to that edge
- **Dragging**: Highlight shows snap preview
- **Corners**: Snaps to nearest single edge
- **Release**: Locks to snapped position

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Show/Hide Keyboard | Click **⌨** button |
| Change Layout | Click **⌨** on keyboard |
| Calibrate | Click **🎯** on keyboard |
| Settings | Click **⚙** on keyboard |
| Close Keyboard | Click **✕** on keyboard |

### Integrating in Custom ISOs

The keyboard is automatically included when building ISOs with the self-install option enabled:

1. Build ISO with **🔧 Self-Installation: ENABLED**
2. Keyboard installs to `/opt/heckcheckos-builder/ui/touchscreen_keyboard.py`
3. Calibration data migrates to new installations
4. Desktop entry includes keyboard launcher

### Using Keyboard Standalone

You can use the keyboard outside the ISO builder:

```python
#!/usr/bin/env python3
from PyQt6.QtWidgets import QApplication
from ui.touchscreen_keyboard import TouchscreenKeyboard

app = QApplication([])
keyboard = TouchscreenKeyboard()
keyboard.show()
app.exec()
```

## API Reference

### TouchscreenKeyboard Class

```python
class TouchscreenKeyboard(QWidget):
    # Signals
    key_pressed = pyqtSignal(str)    # Emitted when key pressed
    keyboard_hidden = pyqtSignal()    # Emitted when keyboard hidden
    position_changed = pyqtSignal(QPoint)  # Emitted when position changes
    
    # Methods
    def show_keyboard(self)           # Show keyboard
    def hide_keyboard(self)           # Hide keyboard
    def start_calibration(self)       # Start calibration wizard
    def change_layout(self, name)     # Switch keyboard layout
    def save_calibration(self)        # Save calibration to file
    def load_calibration(self)        # Load calibration from file
```

### CalibrationWizard Class

```python
class CalibrationWizard(QDialog):
    # Methods
    def get_offset(self) -> QPoint    # Get calculated offset
    def restart_calibration(self)     # Restart calibration
    def skip_calibration(self)        # Skip and use no offset
```

### KeyboardLayoutDesigner Class

```python
class KeyboardLayoutDesigner(QDialog):
    # Methods
    def get_layout(self) -> dict      # Get current layout data
    def save_layout(self)             # Save to JSON file
    def load_layout(self)             # Load from JSON file
    def load_preset(self, name)       # Load preset layout
```

## Troubleshooting

### Keyboard Not Appearing

**Problem**: Clicking keyboard button does nothing

**Solutions**:
- Check that PyQt6 is installed: `pip3 install PyQt6`
- Verify display is available: `echo $DISPLAY`
- Check for errors in terminal output
- Try restarting the GUI

### Touch Input Inaccurate

**Problem**: Touch lands in wrong location

**Solutions**:
- Run calibration wizard (🎯 button)
- Ensure screen is clean and dry
- Try recalibrating with a stylus
- Check screen resolution hasn't changed
- Verify touchscreen drivers are working

### Calibration Not Saving

**Problem**: Calibration resets after restart

**Solutions**:
- Check write permissions: `~/.config/heckcheckos-builder/`
- Verify file exists: `keyboard_calibration.json`
- Check disk space: `df -h ~`
- Review file permissions: `ls -la ~/.config/heckcheckos-builder/`

### Keyboard Doesn't Snap

**Problem**: Keyboard won't snap to edges

**Solutions**:
- Drag closer to edge (within 20px)
- Check screen resolution detection
- Try restarting the application
- Verify window manager allows positioning

### Custom Layout Won't Load

**Problem**: Custom layout file doesn't load

**Solutions**:
- Validate JSON syntax: `python3 -m json.tool layout.json`
- Check file permissions: `ls -l layout.json`
- Verify layout format matches schema
- Try loading a built-in preset first

## Performance Optimization

### For Low-End Devices

If keyboard is slow on low-end hardware:

1. Use simpler layouts (fewer keys)
2. Reduce key animation effects
3. Use solid colors instead of gradients
4. Disable preview animations

### For Touchscreens

For best touchscreen experience:

1. Calibrate on first use
2. Use larger key sizes
3. Enable haptic feedback (if available)
4. Increase touch target sizes

## Contributing

To add new keyboard features:

1. Fork the repository
2. Create feature branch
3. Add your changes to `ui/touchscreen_keyboard.py`
4. Test with calibration
5. Update this documentation
6. Submit pull request

### Adding New Layouts

1. Create layout in Designer
2. Save to JSON file
3. Add to presets in `keyboard_designer.py`
4. Document in this README

## License

The touchscreen keyboard is part of Heck-CheckOS ISO Builder and follows the same license terms. See main repository LICENSE for details.

## Credits

Built with:
- PyQt6 for GUI framework
- Python 3.8+ for implementation
- Inspired by Android and tablet keyboard designs

## Support

For issues or questions:
- GitHub Issues: https://github.com/jameshroop-art/GO-OS/issues
- Documentation: See main README.md
- Examples: Check `gui/heckcheckos-iso-builder/examples/`

---

**Heck-CheckOS ISO Builder** - Professional ISO customization with integrated touchscreen keyboard support
