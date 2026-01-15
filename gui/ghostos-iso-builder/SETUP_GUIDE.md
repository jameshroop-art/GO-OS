# HeckOS Builder - Complete Setup Guide

## Quick Start

### First-Time Setup (5 minutes)

```bash
cd /home/runner/work/GO-OS/GO-OS/gui/ghostos-iso-builder
sudo bash setup.sh
```

This will:
- ✓ Create Python virtual environment
- ✓ Install all system dependencies
- ✓ Install Python packages from requirements.txt  
- ✓ Validate installation
- ✓ Create launcher scripts
- ✓ Add desktop shortcut

### Launch the Builder

```bash
./start.sh
```

Or find "HeckOS Builder" in your applications menu.

## Features

### 🔧 Virtual Environment Management
- Isolated Python environment
- No system Python conflicts
- Automatic activation/deactivation
- Clean dependency management

### 📐 100% Scalable UI
**Automatic detection:**
- Screen resolution (1024x768 → 8K+)
- DPI and scaling factor
- Aspect ratio (4:3, 16:9, 21:9, etc.)
- Touchscreen capability
- Multi-monitor setups

**Dynamic adjustments:**
- Window size optimized for your display
- Font sizes scaled appropriately
- Preview resolution matched to screen
- UI elements properly sized

### 💿 Grub2 Bootable Media Builder

**Create Bootable ISO:**
- Dual-boot support (BIOS + UEFI)
- Hybrid ISO (write to USB with dd)
- Grub2 boot menu with multiple options

**Create Bootable USB:**
- Auto-partitioning (EFI + Main)
- Grub2 installation for both boot modes
- Safe for removable media

**Boot Menu Options:**
1. Live Mode - Try without installing
2. Live Mode (Safe Graphics)
3. Install to Hard Drive
4. Install (Text Mode)
5. Recovery Mode
6. Memory Test
7. Reboot/Shutdown

### 🎨 OS Builder GUI
- Drag-and-drop UI designer
- 30+ widgets
- 6 console-style templates
- AI assembly
- Full preview mode (F5)
- Properties panel
- Theme customization
- ISO manipulation

## System Requirements

**Minimum:**
- Python 3.8+
- 4GB RAM
- 20GB disk space
- 1024x768 display

**Recommended:**
- Python 3.10+
- 8GB+ RAM
- 50GB+ disk space
- 1920x1080+ display

## Installed Dependencies

**System Packages:**
- python3-venv, python3-pip, python3-dev
- build-essential
- genisoimage, squashfs-tools, xorriso
- grub2-common, grub-pc-bin, grub-efi-amd64-bin
- mtools, dosfstools
- git, wget, curl

**Python Packages:**
- PyQt6 (GUI framework)
- PyQt6-WebEngine
- requests, cryptography
- GitPython, python-gitlab
- PyYAML

## Building Your First ISO

1. **Launch Builder:**
   ```bash
   ./start.sh
   ```

2. **Load Source:**
   - Go to "ISO Loader" tab
   - Select source ISO or directory

3. **Customize:**
   - Use "UI Designer" for interface
   - Use "Theme Editor" for appearance
   - Add applications and packages

4. **Build:**
   - Go to "Build" tab
   - Select output type:
     - Bootable ISO (Grub2)
     - Bootable USB
   - Click "Build"
   - Wait for completion

5. **Test:**
   - Preview mode shows live UI
   - Boot in VM or real hardware

## Creating Bootable USB

**Warning:** This will erase the USB drive!

1. **Launch Builder:**
   ```bash
   ./start.sh
   ```

2. **Insert USB Drive**

3. **USB Creation Tab:**
   - Select USB device (e.g., /dev/sdb)
   - Choose source files
   - Click "Create Bootable USB"
   - Confirm operation
   - Wait for completion (5-15 minutes)

4. **Boot from USB:**
   - Restart computer
   - Enter boot menu (F12, ESC, or DEL)
   - Select USB drive
   - Grub2 menu appears

## Hardware Detection Details

The builder automatically detects and adapts to:

**Screen Categories:**
- Small (≤1024px) - Netbooks, old laptops
- Laptop (≤1366px) - Standard laptops
- Desktop (≤1920px) - Full HD displays
- High-res (≤2560px) - QHD displays
- Ultra HD (≤3840px) - 4K displays
- Ultrawide (>3840px) - 5K+, ultrawide displays

**Window Sizing:**
- Small: 95% of screen
- Laptop: 90% of screen
- Desktop: 1400x900 (or 85%)
- 4K+: Up to 1920x1200 (70%)

**Font Scaling:**
- Automatic DPI-based adjustment
- Title: 14-19pt
- Header: 12-17pt
- Body: 9-13pt
- Elements scale proportionally

## Troubleshooting

**Setup fails:**
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check system dependencies
sudo apt-get update
sudo apt-get install python3-venv python3-pip

# Re-run setup
sudo bash setup.sh
```

**GUI won't start:**
```bash
# Check virtual environment
ls venv/  # Should exist

# Manually activate and test
source venv/bin/activate
python3 main.py

# Check display
echo $DISPLAY  # Should show :0 or similar
```

**ISO build fails:**
```bash
# Check for system tools
which genisoimage xorriso grub-mkstandalone

# Install if missing
sudo apt-get install genisoimage xorriso grub2-common grub-pc-bin grub-efi-amd64-bin

# Check disk space
df -h .
```

**USB creation fails:**
```bash
# Check USB device
lsblk  # Find your USB device

# Unmount first
sudo umount /dev/sdb*

# Try again with correct device
```

## File Locations

**Installation:**
- `/home/runner/work/GO-OS/GO-OS/gui/ghostos-iso-builder/`

**Virtual Environment:**
- `./venv/` (in installation directory)

**Logs:**
- `/tmp/heckos-builder-setup.log`
- `./builder.log`

**Output:**
- Default: `./output/`
- ISOs: `./output/heckos-*.iso`
- USB images: As specified

**Configuration:**
- `./config/`
- User settings auto-saved

## Advanced Usage

**Command-Line Arguments:**
```bash
./start.sh --help              # Show help
./start.sh --version           # Show version
./start.sh --debug             # Debug mode
./start.sh --no-hardware-detect # Skip hardware detection
```

**Hardware Detection Test:**
```bash
source venv/bin/activate
python3 hardware_detector.py  # Print detected config
```

**Grub2 Builder Test:**
```bash
source venv/bin/activate
python3 grub2_builder.py      # See example usage
```

## File Types

The builder uses HeckOS-specific file formats:
- `.heckos-layout` - UI layouts (JSON)
- `.heckos-theme` - Theme definitions (JSON)
- `.heckos-config` - System configs (JSON)
- `.heckos-widget` - Custom widgets
- `.heckos-template` - Complete templates
- `.heckos-project` - Full projects (ZIP)

See `FILE_TYPES_SPECIFICATION.md` for details.

## Getting Help

**Documentation:**
- `OS_BUILDER_GUI_GUIDE.md` - Complete GUI guide
- `CONSOLE_TEMPLATES_GUIDE.md` - Template documentation
- `PROPERTY_PANEL_CONTROLS_SPEC.md` - Control specifications
- `FILE_TYPES_SPECIFICATION.md` - File format details

**Logs:**
- Check `/tmp/heckos-builder-setup.log` for setup issues
- Check `./builder.log` for runtime issues

**Community:**
- GitHub Issues: Report bugs and request features
- Discussions: Ask questions and share tips

## What's Next?

1. **Explore Templates:**
   - Try the 6 console-style templates
   - Blue Console, Green Console, PC Gaming Hub
   - Portable Console, Retro Arcade, Modern Gaming Hub

2. **Customize Your OS:**
   - Drag-and-drop UI designer
   - Theme editor with color schemes
   - Add your own applications

3. **Build and Test:**
   - Create bootable ISO
   - Test in virtual machine
   - Install on real hardware

4. **Share Your Creation:**
   - Export templates
   - Share configurations
   - Contribute improvements

## License

MIT License - See LICENSE file

## Legal Notice

HeckOS is a derivative work based on Debian 12 (Bookworm).
NOT an official Debian release. NOT endorsed by the Debian Project.
See LEGAL_COMPLIANCE.md for full legal information.

---

**Ready to build your custom OS? Run `./start.sh` to begin!**
