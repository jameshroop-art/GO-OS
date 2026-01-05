# GhostOS Advanced ISO Builder GUI

A comprehensive PyQt6-based GUI for building customized GhostOS ISOs with multi-source support, theme customization, and repository integration.

## Features

### 🎯 Multi-ISO Source Support
- Load multiple ISO sources (Parrot OS, Ubuntu, Debian, etc.)
- Select specific components from each ISO
- Combine packages from different distributions
- Component categorization and filtering

### 💾 USB and File Integration
- Load ISOs directly from USB drives
- Import custom files and folders
- Include files in base system and recovery partition
- Persistent customizations through recovery mode

### 🎨 Advanced Theme Customization
- **Gaming Mode**: Adaptive themes based on running games
  - Game exclusion checklist
  - Performance optimizations
  - Dynamic color matching
  
- **Production Mode**: Professional color schemes
  - Application-specific themes
  - Reduced eye strain palettes
  - Long work session optimization

### 📏 Universal UI Compatibility
- Cross-desktop environment support (MATE, XFCE, KDE, GNOME, Cinnamon)
- Adjustable text scaling (50%-200%)
- Separate terminal scaling
- Real-time preview

### 📦 Repository Integration
- Browse curated external tools and themes
- One-click integration installation
- License compliance tracking
- Dependency management

### 👁️ Live Preview
- Real-time theme visualization
- Smooth animations (20 FPS)
- Component summary
- Build size estimation

### 🔑 Credentials Management
- Secure GitHub token storage
- Hugging Face authentication
- Encrypted credential saving
- CLI authentication alternatives

### ⌨️ Touchscreen Keyboard (NEW!)
- **Primary Target: Android Devices** - Designed for Termux/Android
- **Desktop Touchscreens**: Also works great on Linux touchscreen devices
- **Resizable & Snappable**: Drag and snap to screen edges
- **Touch Calibration**: 5-point calibration wizard for accuracy
- **Custom Layouts**: Visual designer for creating keyboard layouts
- **Multiple Layouts**: QWERTY, numeric keypad, and custom designs
- **Integration-Ready**: Works with all text input fields
- **Persistent Settings**: Calibration saved per installation
- **Android Optimized**: Efficient battery usage, large touch targets

## Installation

### Desktop/Linux Quick Start

```bash
cd gui/ghostos-iso-builder

# Easy launcher with dependency checks
./start-gui.sh
```

### Android/Termux Installation

```bash
# In Termux (from F-Droid)
pkg update && pkg upgrade -y
pkg install python git -y

# Clone repository
git clone https://github.com/jameshroop-art/GO-OS
cd GO-OS/gui/ghostos-iso-builder

# Install dependencies
pip install -r requirements.txt

# Setup display (VNC or X11)
pkg install tigervnc -y
vncserver :1
export DISPLAY=:1

# Launch keyboard
./start-android.sh
```

**For detailed Android setup, see [ANDROID_KEYBOARD_GUIDE.md](ANDROID_KEYBOARD_GUIDE.md)**

### Manual Installation

```bash
cd gui/ghostos-iso-builder

# Install dependencies
pip install -r requirements.txt

# Run the GUI
python main.py
```

## Requirements

- Python 3.8+
- PyQt6 >= 6.6.0
- PyQt6-WebEngine >= 6.6.0
- requests >= 2.31.0
- cryptography >= 41.0.0
- GitPython >= 3.1.40
- python-gitlab >= 4.2.0

## Usage

### Loading ISOs

1. **From File**: Click "➕ Add ISO" and select an ISO file
2. **From USB**: Click "💾 Load from USB" to browse USB drives
3. **Multiple Sources**: Add as many ISOs as needed

### Selecting Components

1. Analyze loaded ISOs to extract component lists
2. Browse components by category
3. Use quick selection:
   - "✓ Select All" - Full installation
   - "⚡ Minimal" - Required components only
   - "✗ Select None" - Deselect all optional

### Adding Custom Files

1. Click "📄 Add File" or "📁 Add Folder"
2. Or "💾 Load from USB" for USB sources
3. Configure:
   - Include in Recovery partition (survives recovery)
   - Include in Base system (always available)
   - Installation path (e.g., /opt/custom)

### Theme Customization

1. Choose theme mode: Default, Gaming, or Production
2. Adjust global and terminal text scaling
3. Select UI compatibility targets
4. Preview changes in real-time

### Repository Integration

1. Browse available integrations
2. Search for specific tools
3. Preview changes before installation
4. One-click install

### Using the Touchscreen Keyboard

1. Click **⌨ Keyboard** button in toolbar
2. Keyboard appears (snaps to bottom by default)
3. **Calibrate** (first time):
   - Click **🎯** button on keyboard
   - Tap 5 calibration targets
   - System calculates offset automatically
4. **Customize**:
   - Click **⚙** for settings
   - Choose different layouts (QWERTY, Numpad)
   - Open Layout Designer for custom keyboards
5. **Position**: Drag title bar to move, snaps to edges
6. Type in any input field with the keyboard

**See [KEYBOARD_GUIDE.md](KEYBOARD_GUIDE.md) for comprehensive keyboard documentation.**

## Architecture

```
gui/ghostos-iso-builder/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── ui/                        # UI components
│   ├── __init__.py
│   ├── iso_loader.py         # Multi-ISO loader with USB support
│   ├── theme_editor.py       # Gaming/Production theme editor
│   ├── preview_pane.py       # Live preview with animations
│   ├── repo_browser.py       # Repository integration browser
│   └── credentials_dialog.py # Secure credentials management
├── themes/                    # Theme definitions
│   ├── gaming/
│   │   ├── adaptive/         # Game-adaptive themes
│   │   └── presets/          # Gaming presets
│   └── production/
│       ├── schemes/          # Professional color schemes
│       └── templates/        # Production templates
├── assets/                    # GUI assets
│   ├── icons/
│   ├── animations/
│   └── previews/
└── config/                    # Configuration files
```

## Key Capabilities

### Multi-Source ISO Building
- Combine Parrot Security tools with Ubuntu packages
- Mix Debian stability with Arch bleeding-edge
- Create truly custom distributions

### Recovery Partition Integration
- Custom files persist through system recovery
- Pre-configured tools available post-recovery
- Personalized recovery environment

### Cross-UI Theme Support
- Themes work across all desktop environments
- Consistent experience regardless of UI choice
- Adaptive scaling for accessibility

### Performance Optimization
- Gaming mode reduces UI overhead
- Production mode optimizes for long sessions
- Component selection minimizes bloat

## License

GhostOS ISO Builder is part of the GO-OS project.

All integrated external projects maintain their original licenses (see integrations/README.md).

## Credits

Built on top of:
- PyQt6 for the GUI framework
- Parrot Security OS as primary base
- Multiple open-source integrations (see integrations/)

Thank you to all contributors and the open-source community! 🎉
