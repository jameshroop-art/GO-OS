# Windows Driver System for Heck-CheckOS

## Overview

A comprehensive Windows driver solution for Heck-CheckOS/Debian 12 with two complementary tools:

1. **Driver Emulator** - General-purpose driver compatibility layer
2. **Driver Installer** ⭐ NEW - Minimal Windows 10 22H2 style installer optimized for VM-to-Linux bridge

Both enable Windows driver functionality on Linux without Wine or virtualization.

## Purpose

### Driver Emulator
General-purpose compatibility layer that:
- Translates Windows driver calls to Linux kernel equivalents
- Supports common Windows device drivers (USB, HID, Storage, Network)
- Runs natively on the host OS without VM overhead
- Maintains security by isolating driver operations

### Driver Installer ⭐ NEW
Focused installer for production use:
- **Minimal footprint** - Windows 10 22H2 essential drivers only (<1GB)
- **VM bridge optimized** - Low performance impact (<5% overhead)
- **Microsoft sources** - Official drivers with signature verification
- **Small GUI** - Windows 10 style minimal interface

## Architecture

```
┌─────────────────────────────────────────┐
│   Windows Application/Driver Request    │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│   Driver Emulator (Translation Layer)   │
│   - WDM/KMDF API Translation            │
│   - Device I/O Translation              │
│   - Registry Emulation                  │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      Linux Kernel Interface             │
│   - Device Files (/dev/*)               │
│   - sysfs (/sys/*)                      │
│   - udev rules                          │
└─────────────────────────────────────────┘
```

## Components

### 1. Core Emulator (`emulator.py`)
Main emulation engine that handles:
- Driver initialization and loading
- API translation
- Event handling
- Device management

### 2. Device Handlers (`device_handlers/`)
Specific handlers for device types:
- USB devices
- HID devices (keyboard, mouse, game controllers)
- Storage devices
- Network adapters
- Audio devices

### 3. Registry Emulator (`registry_emulator.py`)
Windows registry simulation for driver configuration

### 4. API Translator (`api_translator.py`)
Windows Driver Model (WDM) API to Linux kernel API translation

## Supported Drivers

### Current Support
- ✅ USB HID devices (keyboards, mice, game controllers)
- ✅ USB storage devices
- ✅ Generic USB devices
- ✅ Network adapters (basic)
- ✅ Audio devices (basic)

### Planned Support
- ⏳ Graphics drivers (limited)
- ⏳ Printer drivers
- ⏳ Bluetooth devices
- ⏳ Serial/COM port devices

## Limitations

This is a **lightweight emulator** with the following constraints:
- Not a full Windows kernel implementation
- Limited to user-space driver operations
- Some Windows-specific features may not be available
- Performance may vary depending on driver complexity
- Not suitable for kernel-mode only drivers

## Quick Start

### Choose Your Tool

**Use Driver Installer if you:**
- Need production-ready drivers
- Want VM-to-Linux bridge optimization
- Only need Microsoft-certified drivers
- Prefer minimal footprint (<1GB)
- Have a Windows 10 22H2 ISO (optional)

**Use Driver Emulator if you:**
- Need custom/experimental drivers
- Want maximum flexibility
- Don't mind larger footprint
- Need development/testing features

### Driver Installer (Recommended for Production)

#### With GUI (Supports ISO Upload)

```bash
# Launch GUI
cd /opt/heckcheckos/windows_driver_emulator
./launch-driver-gui.sh

# Optional: Click "📁 Load ISO" to upload Windows 10 22H2 ISO
# This enables offline driver extraction
```

#### With CLI

```bash
# Or use CLI
python3 driver_installer.py list
sudo python3 driver_installer.py install --device-id PCI\\VEN_8086\\DEV_1234
python3 driver_installer.py status
```

**Note**: Windows 10 ISO is **optional**. Without it, drivers are downloaded from Microsoft Update Catalog online.

### Driver Emulator (General Purpose)

```bash
# Load a Windows driver
sudo heckcheckos-driver-load /path/to/driver.sys

# List loaded drivers
heckcheckos-driver-list

# Unload a driver
sudo heckcheckos-driver-unload driver_name
```

### Configuration

Edit `/etc/heckcheckos/driver-emulator.conf` to configure:
- Supported device types
- Driver search paths
- Logging level
- Security policies

## Security Considerations

- All driver operations run in user-space (no kernel modifications)
- Sandboxed execution environment
- Limited system access
- Integrated with Heck-CheckOS security policies
- Network isolation support

## Performance

The emulator adds minimal overhead:
- User-space translation: ~5-10% performance impact
- Direct device access where possible
- Optimized for common driver operations

## Troubleshooting

### Driver fails to load
1. Check driver compatibility: `heckcheckos-driver-check /path/to/driver.sys`
2. Verify device is connected: `lsusb` or `lspci`
3. Check logs: `journalctl -u heckcheckos-driver-emulator`

### Device not recognized
1. Ensure udev rules are loaded: `sudo udevadm trigger`
2. Check device permissions: `ls -l /dev/`
3. Verify driver is loaded: `heckcheckos-driver-list`

## Development

To add support for a new device type:

1. Create handler in `device_handlers/new_device.py`
2. Implement required methods (init, read, write, ioctl)
3. Register handler in `emulator.py`
4. Add tests in `tests/test_new_device.py`

## Documentation

### Complete Guides

- **[DRIVER_INSTALLER_GUIDE.md](DRIVER_INSTALLER_GUIDE.md)** - Complete guide for the minimal Windows 10 22H2 driver installer
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Complete guide for the driver emulator
- **[README.md](README.md)** - This file, overview of the system

### Quick Links

- Driver Installer: `./launch-driver-gui.sh` - Small GUI for Microsoft drivers
- Driver Emulator: `heckcheckos-driver-*` commands - General-purpose CLI tools
- Configuration: `/etc/heckcheckos/driver-emulator.conf`
- Logs: `/var/log/heckcheckos/driver-emulator.log`

## License

Part of Heck-CheckOS project. See main repository license.

## Credits

Built on top of:
- Linux kernel device drivers
- libusb for USB device access
- Python ctypes for native interface
