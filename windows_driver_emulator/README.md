# Windows Driver Emulator for Heck-CheckOS

## Overview

A lightweight Windows driver compatibility layer for Heck-CheckOS/Debian 12, enabling Windows driver functionality on the Linux host without Wine or virtualization.

## Purpose

This emulator provides a temporary compatibility layer that:
- Translates Windows driver calls to Linux kernel equivalents
- Supports common Windows device drivers (USB, HID, Storage, Network)
- Runs natively on the host OS without VM overhead
- Maintains security by isolating driver operations

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

## Usage

### Installation

The emulator is automatically installed with Heck-CheckOS. To manually install:

```bash
cd /opt/heckcheckos/windows_driver_emulator
sudo python3 install.py
```

### Loading a Driver

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

## License

Part of Heck-CheckOS project. See main repository license.

## Credits

Built on top of:
- Linux kernel device drivers
- libusb for USB device access
- Python ctypes for native interface
