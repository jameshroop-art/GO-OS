# Heck-CheckOS Component Launcher

## Run Components As Needed

This launcher system allows you to run Heck-CheckOS components independently, on an as-needed basis, without having to start the full GUI.

## Quick Start

```bash
cd gui/heckcheckos-iso-builder

# Interactive menu
./launch-menu.sh

# Or run components directly:
./start-keyboard-only.sh      # Just the keyboard
./start-gui.sh                 # Full GUI with keyboard
python3 port_manager.py        # Port management tool
```

## Available Components

### 1. Touchscreen Keyboard Only
**Script**: `start-keyboard-only.sh`

Launch just the touchscreen keyboard without the full ISO builder GUI.

```bash
./start-keyboard-only.sh
```

**Use cases**:
- You just need a virtual keyboard
- Using other applications that need keyboard input
- Testing keyboard functionality
- Running on low-resource devices

### 2. ISO Builder GUI Only
**Launch via menu**: Option 3

Start the ISO builder without launching the keyboard automatically.

```bash
export GHOSTOS_NO_KEYBOARD=1
python3 main.py
```

**Use cases**:
- Don't need keyboard right now
- Using physical keyboard
- Want to launch keyboard manually later

### 3. Full GUI (Default)
**Script**: `start-gui.sh`

Launch complete system with all components.

```bash
./start-gui.sh
```

**Use cases**:
- Full ISO building workflow
- Need both keyboard and GUI
- Default operation mode

### 4. Port Manager
**Script**: `port_manager.py`

Scan Debian 12 ports and allocate free ports for Windows VM.

```bash
python3 port_manager.py
```

**Use cases**:
- Setting up Windows integration
- Avoiding port conflicts
- Checking what ports are in use

### 5. Interactive Launcher Menu
**Script**: `launch-menu.sh`

Interactive menu to launch any component.

```bash
./launch-menu.sh
```

Features:
- Shows running status of components
- Launch any component with one key
- Port management integration
- Windows VM port configuration

## Port Management

### Why Port Management?

When running Windows integration alongside Debian 12, both systems need network ports. If both try to use the same port (e.g., port 3389 for RDP), crashes will occur.

### How It Works

The Port Manager:
1. **Scans Debian 12**: Detects all ports currently in use
2. **Checks Services**: Identifies SSH, HTTP, VNC, databases, etc.
3. **Allocates Free Ports**: Finds available ports for Windows
4. **Generates Config**: Creates configuration files

### Using Port Manager

```bash
# Full scan and allocation
python3 port_manager.py

# Check if specific port is free
python3 port_manager.py --check-port 3389

# Just scan ports (no allocation)
python3 port_manager.py --scan-only
```

### Port Allocation Examples

Debian 12 using port 5900 (VNC):
- Windows VNC shifted to 5910 ✓

Debian 12 using port 3389 (RDP):
- Windows RDP shifted to 3390 ✓

All changes are automatic and saved to:
```
~/.config/heckcheckos-builder/port_allocations.json
~/.config/heckcheckos-builder/windows_vm_ports.conf
```

## Configuration Files

### Port Allocations
**Location**: `~/.config/heckcheckos-builder/port_allocations.json`

```json
{
  "windows_ports": {
    "rdp": 3390,
    "vnc": 5910,
    "spice": 5920,
    "qemu_monitor": 4444,
    "smb": 4450,
    "http": 8090,
    "https": 8453
  },
  "debian_ports": {
    "ssh": [22],
    "vnc": [5900, 5901]
  }
}
```

### Windows VM Configuration
**Location**: `~/.config/heckcheckos-builder/windows_vm_ports.conf`

Contains environment variables and QEMU command examples with allocated ports.

## Usage Examples

### Example 1: Just Need Keyboard

```bash
cd gui/heckcheckos-iso-builder
./start-keyboard-only.sh
```

Keyboard appears, ready to use with any application.

### Example 2: Setup Windows VM Ports

```bash
cd gui/heckcheckos-iso-builder
python3 port_manager.py
```

Output:
```
Debian 12 is using 45 ports
Used port ranges: 22 - 8080

Allocating ports for Windows VM:
  rdp                 : 3390 ✓
  vnc                 : 5910 ✓
  spice               : 5920 ✓
  ...

✓ Port configuration saved
```

### Example 3: Interactive Menu

```bash
cd gui/heckcheckos-iso-builder
./launch-menu.sh
```

Menu appears:
```
╔════════════════════════════════════════════════════════╗
║        Heck-CheckOS - Component Launcher Menu             ║
║        Run components independently as needed         ║
╚════════════════════════════════════════════════════════╝

Available Components:

  1) Full GUI (ISO Builder + Keyboard)
  2) Touchscreen Keyboard Only
  3) ISO Builder GUI Only (No Keyboard)
  4) Port Manager (Check/Allocate Ports)
  5) Windows VM Port Configuration
  
Select option: _
```

### Example 4: Check Specific Port

```bash
python3 port_manager.py --check-port 3389
```

Output:
```
Port 3389: IN USE ❌
```

or

```
Port 3389: FREE ✓
```

## Environment Variables

### GHOSTOS_NO_KEYBOARD
Disable automatic keyboard loading.

```bash
export GHOSTOS_NO_KEYBOARD=1
python3 main.py
```

### DISPLAY
Set display for X11/VNC.

```bash
export DISPLAY=:1
./start-keyboard-only.sh
```

## Troubleshooting

### Keyboard Won't Start

```bash
# Check dependencies
pip3 list | grep PyQt6

# Check display
echo $DISPLAY

# Try setting display
export DISPLAY=:0
./start-keyboard-only.sh
```

### Port Conflicts

```bash
# Scan for conflicts
python3 port_manager.py --scan-only

# Re-allocate ports
python3 port_manager.py

# Check specific port
python3 port_manager.py --check-port 5900
```

### Component Already Running

```bash
# Check running processes
ps aux | grep "main.py\|touchscreen"

# Kill if needed
pkill -f main.py
pkill -f touchscreen_keyboard
```

## Android/Termux Usage

All launchers work on Android via Termux:

```bash
# In Termux
pkg install python git

# Setup display (VNC)
vncserver :1
export DISPLAY=:1

# Launch components
cd GO-OS/gui/heckcheckos-iso-builder
./launch-menu.sh
```

## Integration with Windows

When Windows integration is set up:

1. **Run Port Manager First**:
   ```bash
   python3 port_manager.py
   ```

2. **Use Allocated Ports**:
   - Read from `~/.config/heckcheckos-builder/windows_vm_ports.conf`
   - Use allocated ports in Windows VM configuration
   - No conflicts with Debian 12

3. **Example QEMU Command**:
   ```bash
   # Ports from configuration
   VNC_PORT=5910
   RDP_PORT=3390
   
   qemu-system-x86_64 \
     -vnc 127.0.0.1:10 \  # Port 5910
     -netdev user,id=net0,hostfwd=tcp::${RDP_PORT}-:3389 \
     ...
   ```

## Benefits

✅ **Flexibility**: Run only what you need
✅ **Resource Efficiency**: Don't load unnecessary components
✅ **No Conflicts**: Port manager prevents crashes
✅ **Easy Testing**: Test components individually
✅ **Android Friendly**: Works great on Termux
✅ **Windows Ready**: Prepares ports for Windows integration

## See Also

- [KEYBOARD_GUIDE.md](KEYBOARD_GUIDE.md) - Keyboard documentation
- [ANDROID_KEYBOARD_GUIDE.md](ANDROID_KEYBOARD_GUIDE.md) - Android specifics
- [WINDOWS_INTEGRATION_REQUIREMENTS.md](../WINDOWS_INTEGRATION_REQUIREMENTS.md) - Windows setup
- [QUICK_START.md](QUICK_START.md) - General quick start guide
