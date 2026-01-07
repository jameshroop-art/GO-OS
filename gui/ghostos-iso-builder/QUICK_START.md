# GhostOS ISO Builder - Quick Start Guide

## Overview

This guide helps you quickly start the GhostOS ISO Builder GUI with full touchscreen keyboard support and access to all integrations.

## Prerequisites

- **Operating System**: Linux (Debian/Ubuntu-based recommended)
- **Python**: 3.8 or higher
- **Display**: X11 or Wayland
- **Optional**: Touchscreen device for full keyboard features

## Installation Methods

### Method 1: Quick Launch (Recommended)

The easiest way to start the GUI:

```bash
cd /path/to/GO-OS/gui/ghostos-iso-builder
./start-gui.sh
```

This launcher script:
- ✓ Checks Python version
- ✓ Verifies all dependencies
- ✓ Offers to install missing packages
- ✓ Detects touchscreen devices
- ✓ Validates display availability
- ✓ Creates config directories
- ✓ Launches the GUI

### Method 2: Manual Python Launch

If you prefer manual control:

```bash
cd /path/to/GO-OS/gui/ghostos-iso-builder

# Install dependencies first
pip3 install -r requirements.txt

# Launch GUI
python3 main.py
```

### Method 3: System-Wide Installation

Install the GUI system-wide (requires root):

```bash
cd /path/to/GO-OS/gui/ghostos-iso-builder
sudo ./install.sh
```

After installation:
- Run from terminal: `ghostos-builder`
- Launch from app menu: "GhostOS ISO Builder"
- Standalone keyboard: `ghostos-keyboard`

## First Launch

### What to Expect

On first launch, you'll see:

1. **Main Window**: ISO Builder interface
2. **Three Tabs**:
   - 📀 ISO Loader
   - 🎨 Theme Editor
   - 📦 Repository Browser
3. **Toolbar**: Quick access to settings and keyboard
4. **Preview Pane**: Live preview of your configuration

### Initial Setup Steps

1. **Load an ISO**:
   - Click "➕ Add ISO" in the ISO Loader tab
   - Select a Debian 12, Ubuntu, or Debian ISO
   - Wait for analysis to complete

2. **Enable Touchscreen Keyboard** (Optional):
   - Click **⌨ Keyboard** button in toolbar
   - Keyboard appears at screen bottom
   - First-time calibration recommended

3. **Calibrate Keyboard** (If using touchscreen):
   - Click **🎯** on keyboard title bar
   - Follow 5-point calibration wizard
   - Tap each target accurately
   - System calculates and saves offset

4. **Explore Integrations**:
   - Switch to 📦 Repository Browser tab
   - Browse available tools and themes
   - One-click installation available

## Using the Touchscreen Keyboard

### Basic Usage

1. **Show/Hide**: Click **⌨** button in toolbar
2. **Position**: Drag title bar to move keyboard
3. **Snap to Edges**: Drag near screen edges (auto-snaps within 20px)
4. **Type**: Click keys to send input to focused field
5. **Layout**: Click **⌨** on keyboard to switch layouts

### Keyboard Features

| Button | Function |
|--------|----------|
| ⋮⋮ | Drag handle (click and drag to move) |
| ⌨ | Change layout (QWERTY, Numpad, Custom) |
| ⚙ | Settings menu |
| 🎯 | Start calibration wizard |
| ✕ | Hide keyboard |

### Calibration (First Time)

**When to calibrate:**
- First time using touchscreen
- Touch input seems inaccurate
- After screen resolution change
- On new installation

**How to calibrate:**
1. Click 🎯 on keyboard
2. Tap 5 targets accurately
3. System shows offset calculation
4. Click "Finish" to save
5. Calibration persists across sessions

### Creating Custom Layouts

1. Click **⚙** on keyboard → "Custom Layout"
2. Opens **Keyboard Layout Designer**
3. Design your layout:
   - Add/remove rows
   - Customize each key
   - Set colors and sizes
   - Save to JSON file
4. Load custom layouts anytime

## Building Your First ISO

### Step-by-Step Process

1. **Load Base ISO**:
   ```
   Click: ISO Loader → ➕ Add ISO → Select ISO file
   ```

2. **Select Components**:
   ```
   Choose which packages to include
   Use: ✓ Select All, ⚡ Minimal, or custom selection
   ```

3. **Add Custom Files** (Optional):
   ```
   Click: 📄 Add File or 📁 Add Folder
   Configure installation paths
   ```

4. **Customize Theme**:
   ```
   Switch to: 🎨 Theme Editor tab
   Choose: Default, Gaming, or Production mode
   Adjust: Text scaling, UI targets
   ```

5. **Add Integrations**:
   ```
   Switch to: 📦 Repository Browser
   Browse and install: Tools, themes, shells
   ```

6. **Validate Configuration**:
   ```
   Click: 🔍 Validate Configuration
   Fix any reported issues
   ```

7. **Build ISO**:
   ```
   Click: 🚀 Build ISO
   Monitor progress in build dialog
   ISO saved to: $HOME/ghostos-ultimate/
   ```

## Integrations Available

### Default Integrations

The builder includes access to:

- **Themes**: Dracula, Nord, Gruvbox
- **Shells**: Oh My Zsh, Powerlevel10k, Starship
- **Editors**: NvChad (Neovim), Vim configs
- **Terminals**: Alacritty, Kitty configurations
- **Launchers**: Rofi, Dmenu alternatives
- **Plugin Managers**: Tmux, Zsh plugins

### Installing Integrations

1. Navigate to **📦 Repository Browser** tab
2. Browse available integrations
3. Click on any integration for details
4. Click "Install" to add to your ISO

All integrations respect original licenses and maintain attribution.

## Configuration Files

### Storage Locations

```
$HOME/.config/ghostos-builder/
├── keyboard_calibration.json    # Touch offset data
├── keyboard_layouts/            # Custom keyboard layouts
├── keyboard_settings.json       # Keyboard preferences
├── builder_config.json          # GUI configuration
└── recent_isos.json            # Recent ISO paths
```

### Keyboard Calibration

**File**: `keyboard_calibration.json`

```json
{
  "offset_x": 5,
  "offset_y": -3
}
```

### Custom Keyboard Layout

**File**: `keyboard_layouts/my_layout.json`

```json
{
  "name": "My Custom Layout",
  "version": "1.0",
  "rows": [
    [
      {"label": "Q", "value": "q", "width": 1.0}
    ]
  ]
}
```

## Troubleshooting

### GUI Won't Start

**Problem**: Script fails or GUI doesn't appear

**Solutions**:
```bash
# Check Python version (need 3.8+)
python3 --version

# Verify dependencies
pip3 list | grep PyQt6

# Install/update dependencies
pip3 install --upgrade -r requirements.txt

# Check display
echo $DISPLAY

# Try with verbose output
python3 main.py --verbose
```

### Keyboard Not Working

**Problem**: Keyboard button does nothing

**Solutions**:
```bash
# Verify PyQt6 installation
python3 -c "from PyQt6.QtWidgets import QApplication; print('OK')"

# Check config directory permissions
ls -la ~/.config/ghostos-builder/

# Reset keyboard config
rm -rf ~/.config/ghostos-builder/keyboard*

# Restart GUI
```

### Touch Input Inaccurate

**Problem**: Touches land in wrong location

**Solutions**:
1. Run calibration: Click 🎯 on keyboard
2. Clean touchscreen surface
3. Check screen resolution hasn't changed
4. Try recalibrating with stylus for precision
5. Verify touchscreen drivers working:
   ```bash
   xinput list | grep -i touch
   ```

### Dependencies Missing

**Problem**: Import errors on startup

**Solutions**:
```bash
# Install all dependencies
pip3 install -r requirements.txt

# Or install individually
pip3 install PyQt6 PyQt6-WebEngine
pip3 install requests cryptography
pip3 install GitPython python-gitlab PyYAML

# Check installation
pip3 list | grep -E "PyQt6|requests|cryptography"
```

### ISO Build Fails

**Problem**: Build process errors

**Solutions**:
1. Validate configuration first (🔍 button)
2. Check disk space: `df -h ~`
3. Verify ISO source is valid
4. Run with root if needed: `sudo python3 main.py`
5. Check build log for specific errors

### Integration Installation Fails

**Problem**: Repository integration won't install

**Solutions**:
1. Check internet connection
2. Verify repository accessibility
3. Check disk space
4. Review integration logs
5. Try manual installation from integration README

## Advanced Usage

### Command-Line Arguments

```bash
# Launch with specific ISO
python3 main.py --iso /path/to/debian.iso

# Load configuration
python3 main.py --config /path/to/config.json

# Enable debug logging
python3 main.py --debug

# Start with keyboard visible
python3 main.py --show-keyboard
```

### Environment Variables

```bash
# Custom config directory
export GHOSTOS_CONFIG_DIR="$HOME/.ghostos"

# Disable keyboard
export GHOSTOS_NO_KEYBOARD=1

# Set default theme
export GHOSTOS_THEME="gaming"

# Launch
python3 main.py
```

### Keyboard-Only Mode

Run just the touchscreen keyboard:

```bash
# If installed system-wide
ghostos-keyboard

# Or directly
python3 -c "
import sys
sys.path.insert(0, 'gui/ghostos-iso-builder')
from PyQt6.QtWidgets import QApplication
from ui.touchscreen_keyboard import TouchscreenKeyboard

app = QApplication(sys.argv)
kb = TouchscreenKeyboard()
kb.show_keyboard()
sys.exit(app.exec())
"
```

### Batch ISO Building

Create multiple ISOs with different configs:

```bash
#!/bin/bash
for config in configs/*.json; do
    python3 main.py --config "$config" --build --output "isos/"
done
```

## Tips & Best Practices

### Performance

- **Large ISOs**: Building takes 30-60 minutes depending on selections
- **RAM**: Minimum 8GB recommended, 16GB for smooth operation
- **Disk**: Ensure 50-100GB free space for build process
- **CPU**: Multi-core benefits from parallel operations

### Keyboard Usage

- **First-time calibration**: Essential for accuracy
- **Recalibrate**: After resolution changes
- **Custom layouts**: Save layouts for different workflows
- **Snap positions**: Use edge snapping for consistent placement
- **Numpad mode**: Switch to numpad for number entry

### ISO Building

- **Test in VM first**: Use QEMU or VirtualBox before hardware
- **Validate config**: Always validate before building
- **Component selection**: Start with minimal, add as needed
- **Custom files**: Use recovery partition for important files
- **Integrations**: Test integrations individually first

### Backup

Before major operations:
```bash
# Backup config
cp -r ~/.config/ghostos-builder ~/ghostos-backup-$(date +%F)

# Backup custom layouts
tar -czf layouts-backup.tar.gz ~/.config/ghostos-builder/keyboard_layouts/

# Backup built ISOs
cp $HOME/ghostos-ultimate/*.iso ~/iso-backups/
```

## Support & Resources

### Documentation

- **Main README**: `gui/ghostos-iso-builder/README.md`
- **Keyboard Guide**: `gui/ghostos-iso-builder/KEYBOARD_GUIDE.md`
- **Architecture**: `Go-OS/ARCHITECTURE.md`
- **FAQ**: `Go-OS/FAQ.md`

### Getting Help

1. **Check Documentation**: Review relevant README files
2. **Search Issues**: Look for similar problems on GitHub
3. **Create Issue**: Open new issue with details:
   - Platform and versions
   - Error messages
   - Steps to reproduce
   - Log files

### Links

- **Repository**: https://github.com/jameshroop-art/GO-OS
- **Issues**: https://github.com/jameshroop-art/GO-OS/issues
- **Debian 12**: https://www.debian.org
- **Debian**: https://www.debian.org

## Next Steps

After successful first launch:

1. ✅ Explore all three tabs
2. ✅ Load and analyze an ISO
3. ✅ Calibrate touchscreen keyboard
4. ✅ Browse available integrations
5. ✅ Create a test ISO with minimal components
6. ✅ Test ISO in virtual machine
7. ✅ Design custom keyboard layout
8. ✅ Build production ISO with all features

## Quick Reference

### Essential Commands

```bash
# Start GUI (recommended)
./start-gui.sh

# Start GUI (manual)
python3 main.py

# Install system-wide
sudo ./install.sh

# Standalone keyboard
ghostos-keyboard

# Uninstall
sudo /opt/ghostos-builder/uninstall.sh
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+O | Load ISO |
| Ctrl+S | Save configuration |
| Ctrl+Q | Quit application |
| F11 | Toggle fullscreen |

### Quick Actions

- **Load ISO**: Click "➕ Add ISO"
- **Show Keyboard**: Click "⌨" toolbar button
- **Calibrate**: Click "🎯" on keyboard
- **Validate**: Click "🔍 Validate Configuration"
- **Build**: Click "🚀 Build ISO"

---

**GhostOS ISO Builder** - Professional ISO customization with integrated touchscreen keyboard support

For detailed keyboard documentation, see [KEYBOARD_GUIDE.md](KEYBOARD_GUIDE.md)
