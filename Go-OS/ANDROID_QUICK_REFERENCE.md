# Heck-CheckOS for Android - Quick Reference

Fast reference for Heck-CheckOS Android commands and features.

## Installation (One-Time Setup)

```bash
# Install Termux from F-Droid (NOT Google Play)
# Install Termux:API from F-Droid
# Grant Storage + Location permissions

# In Termux:
pkg update -y && pkg upgrade -y
pkg install wget -y
wget https://raw.githubusercontent.com/jameshroop-art/GO-OS/main/Go-OS/heckcheckos-android.sh
chmod +x heckcheckos-android.sh
bash heckcheckos-android.sh
source ~/.bashrc
```

## Quick Start

```bash
ghostos              # Main menu
ghostos-help         # Full help
ghostos-system       # System info
```

## WiFi Commands

| Command | Description |
|---------|-------------|
| `ghostos-wifi scan` | Scan for WiFi networks |
| `ghostos-wifi status` | Check WiFi connection status |
| `ghostos-wifi info` | Show current WiFi details |
| `ghostos-wifi enable` | Turn WiFi on |
| `ghostos-wifi disable` | Turn WiFi off |
| `ghostos-wifi list` | List saved networks |

### WiFi Examples

```bash
# Check if connected
ghostos-wifi status

# Scan for networks
ghostos-wifi scan

# Get connection details
ghostos-wifi info
```

## Bluetooth Commands

| Command | Description |
|---------|-------------|
| `ghostos-bluetooth scan` | Scan for Bluetooth devices |
| `ghostos-bluetooth status` | Check Bluetooth status |
| `ghostos-bluetooth devices` | List paired devices |
| `ghostos-bluetooth enable` | Turn Bluetooth on |
| `ghostos-bluetooth disable` | Turn Bluetooth off |
| `ghostos-bluetooth info` | Show adapter info |

### Bluetooth Examples

```bash
# Enable and scan
ghostos-bluetooth enable
ghostos-bluetooth scan

# Check paired devices
ghostos-bluetooth devices

# Check status
ghostos-bluetooth status
```

## Driver Optimization

```bash
# Run full optimization
heckcheckos-driver-optimizer
```

**What it does:**
- ✅ Analyzes WiFi signal strength
- ✅ Checks connection quality
- ✅ Provides optimization tips
- ✅ Shows driver information
- ✅ Tests Bluetooth status

## Debian Linux Environment

```bash
# Launch Debian
ghostos-debian

# Inside Debian:
apt update
apt install <package>
exit  # Return to Termux
```

### Common Debian Commands

```bash
# Python development
ghostos-debian
apt update
apt install -y python3 python3-pip
pip3 install requests numpy pandas

# Node.js development
apt install -y nodejs npm
npm install -g express

# Compile C/C++
apt install -y gcc g++ make
```

## System Information

```bash
ghostos-system
```

**Shows:**
- Android version and SDK
- Device model and manufacturer
- Termux configuration
- Heck-CheckOS installation status
- Hardware details

## File Locations

| Path | Contents |
|------|----------|
| `~/heckcheckos-android/` | Heck-CheckOS root directory |
| `~/heckcheckos-android/bin/` | Command scripts |
| `~/heckcheckos-android/config/` | Configuration files |
| `~/heckcheckos-android/drivers/` | Driver info/logs |
| `~/heckcheckos-android/logs/` | Log files |

## Requirements Checklist

- [x] Android 9+ (API 28+)
- [x] Termux (from F-Droid)
- [x] Termux:API (from F-Droid)
- [x] Storage permission granted
- [x] Location permission granted
- [x] 2GB+ free space

## Troubleshooting Quick Fixes

### Commands not found
```bash
source ~/.bashrc
# Or use full path:
~/heckcheckos-android/bin/ghostos
```

### WiFi/Bluetooth not working
```bash
# Install Termux:API
# Grant Location permission
# Restart Termux
```

### Update Heck-CheckOS
```bash
bash ~/heckcheckos-android.sh
# Or:
ghostos-update
```

### Clear Termux cache
```bash
pkg clean
pkg update -y && pkg upgrade -y
```

## Permissions

**Grant in Android Settings → Apps → Termux:**

| Permission | Required For |
|------------|--------------|
| Storage | File access, Debian environment |
| Location | WiFi/Bluetooth scanning (Android requirement) |

**Note:** Location is required by Android for WiFi/Bluetooth scanning, even though Heck-CheckOS doesn't use your location.

## Non-Root Limitations

### ❌ Cannot Do (Without Root)
- Modify kernel drivers
- Enable monitor mode
- Packet injection
- Access /system partition
- Load kernel modules

### ✅ Can Do (Without Root)
- Control WiFi on/off
- Scan WiFi networks
- View connection info
- Control Bluetooth on/off
- Scan Bluetooth devices
- Run full Linux (proot)
- Install Linux packages
- Develop and compile code

## Common Use Cases

### Web Development
```bash
ghostos-debian
apt update
apt install -y nodejs npm python3 python3-pip
npm install -g @angular/cli
pip3 install flask django
```

### Python Data Science
```bash
ghostos-debian
apt update
apt install -y python3 python3-pip
pip3 install jupyter numpy pandas matplotlib scipy
```

### Network Monitoring
```bash
# Check WiFi signal
heckcheckos-driver-optimizer

# Monitor connection
ghostos-wifi status

# In Debian:
ghostos-debian
apt install -y iperf3 nmap curl
```

### System Administration
```bash
ghostos-system        # System info
ghostos-wifi status   # Network status
ghostos-debian        # Full Linux environment
```

## Tips & Tricks

### 1. Add Custom Aliases
```bash
nano ~/.bashrc

# Add:
alias wifi='ghostos-wifi'
alias bt='ghostos-bluetooth'
alias opt='heckcheckos-driver-optimizer'
alias deb='ghostos-debian'

source ~/.bashrc
```

### 2. Create Quick Scripts
```bash
nano ~/heckcheckos-android/bin/my-script
# Add your commands
chmod +x ~/heckcheckos-android/bin/my-script
```

### 3. Access Android Storage
```bash
# In Termux/Debian:
cd /sdcard
ls -la
```

### 4. Share Files with Android
```bash
# Copy to Android Downloads
cp file.txt /sdcard/Download/
```

### 5. Run in Background
```bash
# Use Termux:Boot or Termux:Widget
# Or use screen/tmux in Debian
```

## Performance Tips

### WiFi Optimization
1. Run `heckcheckos-driver-optimizer` regularly
2. Move closer to router if signal < -70 dBm
3. Avoid WiFi congestion (check other networks)
4. Use 5GHz WiFi if available

### Bluetooth Optimization
1. Keep devices within 10 meters
2. Remove obstacles between devices
3. Unpair unused devices
4. Restart Bluetooth if issues occur

### Battery Saving
1. Exit Debian when not in use
2. Disable WiFi/Bluetooth when not needed
3. Use `ghostos-wifi disable` / `ghostos-bluetooth disable`
4. Kill background processes in Debian

## Command Cheat Sheet

```bash
# Quick status check
ghostos-system && ghostos-wifi status && ghostos-bluetooth status

# Full optimization
heckcheckos-driver-optimizer

# Enable everything
ghostos-wifi enable && ghostos-bluetooth enable

# Disable everything
ghostos-wifi disable && ghostos-bluetooth disable

# Scan everything
ghostos-wifi scan && ghostos-bluetooth scan

# Launch environment
ghostos-debian

# Update system
pkg update -y && pkg upgrade -y && ghostos-update
```

## Version Info

- **Heck-CheckOS Version**: 1.0-android
- **Target**: Android 9+ (API 28+)
- **Architecture**: ARM, ARM64, x86, x86_64
- **Based on**: Termux + proot-distro + Debian

## Links

- **GitHub**: https://github.com/jameshroop-art/GO-OS
- **Termux**: https://termux.com
- **F-Droid**: https://f-droid.org
- **Full Docs**: See `ANDROID_INSTALLATION.md`

## Support

```bash
ghostos-help          # Built-in help
ghostos-system        # Check installation

# Or visit:
# https://github.com/jameshroop-art/GO-OS/issues
```

---

**Remember**: Heck-CheckOS runs WITHOUT root access, so some features are limited. For full driver access, root is required (but voids warranty and security).

This quick reference covers 90% of daily use cases. For detailed information, see `ANDROID_INSTALLATION.md` or run `ghostos-help`.
