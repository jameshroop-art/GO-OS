# Windows Driver Emulator User Guide

## Overview

The Windows Driver Emulator is a lightweight compatibility layer that allows Windows device drivers to work on GhostOS/Debian 12 without Wine or virtualization. It translates Windows driver API calls to their Linux kernel equivalents.

## What It Does

- **Enables Windows Drivers on Linux**: Load `.sys` driver files directly on the host OS
- **No Wine or VM Required**: Runs natively with minimal overhead
- **Security First**: All operations sandboxed in user-space
- **Supports Common Devices**: USB, HID (keyboards, mice, controllers), Storage, Network, Audio

## Installation

The driver emulator is automatically installed with GhostOS. If you need to install it manually:

```bash
cd /opt/ghostos/windows_driver_emulator
sudo python3 install.py
```

## Command-Line Usage

### Load a Driver

```bash
sudo ghostos-driver-load /path/to/driver.sys
```

Example:
```bash
sudo ghostos-driver-load ~/Downloads/usb_device_driver.sys
```

### List Loaded Drivers

```bash
ghostos-driver-list
```

Output:
```
Loaded drivers: 2
  - usb_device_driver.sys (usb)
  - hid_keyboard.sys (hid)
```

### Unload a Driver

```bash
sudo ghostos-driver-unload driver.sys
```

Example:
```bash
sudo ghostos-driver-unload usb_device_driver.sys
```

### Check Driver Compatibility

Before loading a driver, check if it's compatible:

```bash
ghostos-driver-check /path/to/driver.sys
```

Output:
```
Driver compatibility check: /path/to/driver.sys
Compatible: True
Device type: usb
```

## GUI Usage

The GhostOS ISO Builder includes a graphical driver manager.

### Accessing the Driver Manager

1. Launch the GhostOS ISO Builder:
   ```bash
   cd gui/ghostos-iso-builder
   ./start-gui.sh
   ```

2. Click on the **"🔧 Driver Manager"** tab

### GUI Features

#### Driver Management Tab

- **View Loaded Drivers**: See all currently loaded drivers in a table
- **Load Driver**: Click "➕ Load Driver" to browse and load a `.sys` file
- **Unload Driver**: Select a driver and click "➖ Unload Driver"
- **Check Compatibility**: Click "🔍 Check Compatibility" to verify a driver before loading
- **Refresh**: Click "🔄 Refresh" to update the driver list

#### Device Information Tab

- **Select Device Type**: Choose USB, HID, Storage, Network, or Audio
- **View Devices**: See information about connected devices of that type

#### Configuration Tab

- **Security Options**:
  - Enable security sandboxing (recommended)
  - Enable network isolation (recommended)
  
- **Driver Search Paths**: Configure where the emulator looks for drivers

#### Help Tab

Complete reference documentation built into the GUI.

## Supported Driver Types

### ✅ Fully Supported

1. **USB Devices**
   - Generic USB device drivers
   - USB mass storage
   - USB peripherals

2. **HID Devices**
   - Keyboards
   - Mice
   - Game controllers (Xbox, PlayStation)
   - Touchpads
   - Stylus/pen devices

3. **Storage Devices**
   - External hard drives
   - USB flash drives
   - SD card readers

### ⚠️ Limited Support

4. **Network Adapters**
   - Basic network device support
   - Some features may not work

5. **Audio Devices**
   - Basic audio support
   - Advanced features may be limited

### ❌ Not Supported

- Graphics drivers (GPU drivers)
- Kernel-mode only drivers
- Drivers requiring Windows-specific kernel features
- Anti-cheat drivers
- DRM drivers

## How It Works

```
┌─────────────────────────────────┐
│  Windows Driver (.sys file)     │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Driver Emulator                │
│  - Parse driver metadata        │
│  - Translate WDM/KMDF calls     │
│  - Map to device handlers       │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Device Handlers                │
│  - USB Handler                  │
│  - HID Handler                  │
│  - Storage Handler              │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Linux Kernel                   │
│  - /dev/*, /sys/* devices       │
│  - udev, libusb                 │
└─────────────────────────────────┘
```

## Configuration

Edit `/etc/ghostos/driver-emulator.conf`:

```json
{
  "driver_search_paths": [
    "/opt/ghostos/drivers",
    "/usr/local/share/ghostos/drivers",
    "~/.ghostos/drivers"
  ],
  "supported_device_types": [
    "usb",
    "hid",
    "storage",
    "network",
    "audio"
  ],
  "security": {
    "sandbox_enabled": true,
    "network_isolation": true,
    "max_drivers": 32
  },
  "logging": {
    "level": "INFO",
    "file": "/var/log/ghostos/driver-emulator.log"
  }
}
```

### Configuration Options

- **driver_search_paths**: Directories to search for drivers
- **supported_device_types**: Types of devices to support
- **security.sandbox_enabled**: Enable sandboxing (recommended)
- **security.network_isolation**: Isolate driver network access
- **security.max_drivers**: Maximum number of loaded drivers
- **logging.level**: INFO, DEBUG, WARNING, ERROR
- **logging.file**: Path to log file

## Security Considerations

### What's Safe

- ✅ All operations run in user-space (no kernel modifications)
- ✅ Sandboxed execution environment
- ✅ Network isolation available
- ✅ Limited system access
- ✅ Integrated with GhostOS security policies

### What to Watch Out For

- ⚠️ Only load drivers from trusted sources
- ⚠️ Driver quality varies - some may not work properly
- ⚠️ Malicious drivers could still cause problems (though sandboxed)
- ⚠️ Performance depends on driver complexity

### Best Practices

1. **Check compatibility first**: Use `ghostos-driver-check` before loading
2. **Monitor logs**: Check `/var/log/ghostos/driver-emulator.log` for issues
3. **Test incrementally**: Load one driver at a time
4. **Keep sandboxing enabled**: Don't disable security features
5. **Unload unused drivers**: Free resources when drivers aren't needed

## Troubleshooting

### Driver Fails to Load

**Symptom**: Error message when trying to load a driver

**Solutions**:
1. Check driver compatibility:
   ```bash
   ghostos-driver-check /path/to/driver.sys
   ```

2. Verify the driver is a valid `.sys` file:
   ```bash
   file /path/to/driver.sys
   ```

3. Check permissions:
   ```bash
   ls -l /path/to/driver.sys
   ```

4. Check logs:
   ```bash
   sudo tail -f /var/log/ghostos/driver-emulator.log
   ```

### Device Not Recognized

**Symptom**: Driver loads but device doesn't work

**Solutions**:
1. Verify device is connected:
   ```bash
   lsusb          # For USB devices
   lspci          # For PCI devices
   ```

2. Check device permissions:
   ```bash
   ls -l /dev/input/*    # For HID devices
   ls -l /dev/sd*        # For storage devices
   ```

3. Reload udev rules:
   ```bash
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

4. Restart the emulator:
   ```bash
   sudo ghostos-driver-unload driver.sys
   sudo ghostos-driver-load /path/to/driver.sys
   ```

### Performance Issues

**Symptom**: Device works but slowly

**Solutions**:
1. Check CPU usage:
   ```bash
   top
   ```

2. Reduce logging level in `/etc/ghostos/driver-emulator.conf`:
   ```json
   "logging": {
     "level": "WARNING"
   }
   ```

3. Unload unused drivers:
   ```bash
   ghostos-driver-list
   sudo ghostos-driver-unload unused_driver.sys
   ```

### Can't Find Emulator

**Symptom**: Commands not found

**Solutions**:
1. Verify installation:
   ```bash
   ls -l /opt/ghostos/windows_driver_emulator/
   ```

2. Check PATH:
   ```bash
   echo $PATH | grep /usr/local/bin
   ```

3. Reinstall if needed:
   ```bash
   cd /opt/ghostos/windows_driver_emulator
   sudo python3 install.py
   ```

## Examples

### Example 1: Xbox Controller

```bash
# Download Xbox controller driver (example)
# wget https://example.com/xbox_controller.sys

# Check compatibility
ghostos-driver-check xbox_controller.sys

# Output: Compatible: True, Device type: hid

# Load the driver
sudo ghostos-driver-load xbox_controller.sys

# Verify it loaded
ghostos-driver-list

# Test the controller
jstest /dev/input/js0

# When done, unload
sudo ghostos-driver-unload xbox_controller.sys
```

### Example 2: USB Storage

```bash
# Check USB storage driver
ghostos-driver-check usb_storage.sys

# Load driver
sudo ghostos-driver-load usb_storage.sys

# List storage devices
lsblk

# Mount the device
sudo mount /dev/sdb1 /mnt/usb

# Access files
ls /mnt/usb

# Unmount and unload
sudo umount /mnt/usb
sudo ghostos-driver-unload usb_storage.sys
```

### Example 3: Wireless Keyboard

```bash
# Load HID driver for wireless keyboard
sudo ghostos-driver-load wireless_keyboard_hid.sys

# Check HID devices
ls -l /dev/input/event*

# Test keyboard input
evtest /dev/input/event5

# View loaded drivers
ghostos-driver-list
```

## FAQ

### Q: Do I need Wine installed?

A: No! The driver emulator works independently of Wine. It's a lightweight alternative for device drivers only.

### Q: Will this work with all Windows drivers?

A: No. It works with user-space compatible drivers for common devices (USB, HID, Storage). Kernel-mode only drivers and graphics drivers are not supported.

### Q: Is it safe to use?

A: Yes, when loading drivers from trusted sources. The emulator runs in user-space with sandboxing enabled, limiting potential damage from malicious drivers.

### Q: Does it affect system performance?

A: Minimal impact (5-10% overhead). The emulator is designed to be lightweight.

### Q: Can I use it with Wine?

A: Yes! They work independently. Use Wine for applications and the driver emulator for hardware devices.

### Q: What if my driver isn't supported?

A: Check the compatibility first with `ghostos-driver-check`. If it's not supported, you may need to use the native Linux driver or contact the hardware manufacturer for Linux support.

### Q: How do I report bugs?

A: Check the logs at `/var/log/ghostos/driver-emulator.log` and report issues on the GhostOS GitHub repository with the log output.

## Advanced Usage

### Creating Custom Device Handlers

To add support for a new device type:

1. Create a handler in `/opt/ghostos/windows_driver_emulator/device_handlers/`:
   ```python
   from .base_handler import DeviceHandler
   
   class MyDeviceHandler(DeviceHandler):
       def __init__(self):
           super().__init__('mydevice')
       
       def load(self, driver_path, metadata):
           # Implement driver loading
           pass
       
       def unload(self, driver_name):
           # Implement driver unloading
           pass
       
       def enumerate_devices(self):
           # Implement device enumeration
           pass
   ```

2. Register in `emulator.py`:
   ```python
   from device_handlers import MyDeviceHandler
   
   self.device_handlers['mydevice'] = MyDeviceHandler()
   ```

3. Test your handler:
   ```bash
   python3 -m pytest tests/test_my_device.py
   ```

## Further Resources

- **README**: `/opt/ghostos/windows_driver_emulator/README.md`
- **Configuration**: `/etc/ghostos/driver-emulator.conf`
- **Logs**: `/var/log/ghostos/driver-emulator.log`
- **Source Code**: `/opt/ghostos/windows_driver_emulator/`
- **GhostOS Documentation**: Main repository documentation

## Support

For help:
1. Check this guide
2. Check the logs
3. Visit the GhostOS GitHub repository
4. Open an issue with log output and driver information

---

**Note**: This is a temporary patch for driver support. For full Windows application compatibility, consider using Wine (for applications) or see WINDOWS_INTEGRATION_REQUIREMENTS.md for VM-based solutions.
