# Android Compatibility & Technical Details

Technical documentation for GhostOS Android implementation, driver handling, and platform compatibility.

## Architecture Overview

### System Stack

```
┌─────────────────────────────────────┐
│   GhostOS Android Commands          │
│   (ghostos-wifi, ghostos-bluetooth) │
├─────────────────────────────────────┤
│   Termux:API Bridge                 │
│   (Android Intent System)           │
├─────────────────────────────────────┤
│   Android Framework APIs            │
│   (WiFiManager, BluetoothAdapter)   │
├─────────────────────────────────────┤
│   Hardware Abstraction Layer (HAL)  │
├─────────────────────────────────────┤
│   Kernel Drivers                    │
│   (WiFi: nl80211, Bluetooth: HCI)   │
├─────────────────────────────────────┤
│   Hardware                          │
│   (WiFi Chip, Bluetooth Chip)       │
└─────────────────────────────────────┘
```

### Component Details

#### 1. GhostOS Layer
- **Location**: Termux userspace
- **Language**: Bash scripts
- **Purpose**: User-friendly command interface
- **Privileges**: None (standard user)

#### 2. Termux:API Bridge
- **Location**: Termux addon app
- **Purpose**: Bridge between Termux and Android APIs
- **Method**: Android Intent system (IPC)
- **Permissions**: Uses app-granted permissions

#### 3. Android Framework
- **APIs Used**:
  - `android.net.wifi.WifiManager`
  - `android.bluetooth.BluetoothAdapter`
  - `android.net.ConnectivityManager`
- **Access Level**: Standard Android SDK
- **Restrictions**: SELinux policies apply

#### 4. HAL & Kernel
- **Access**: Not directly accessible without root
- **Drivers**: Vendor-specific implementations
- **Security**: Protected by Android security model

## Android Version Compatibility

### Supported Versions

| Android Version | API Level | Status | Notes |
|----------------|-----------|--------|-------|
| Android 14 | 34 | ✅ Fully Supported | Latest features |
| Android 13 | 33 | ✅ Fully Supported | Bluetooth LE Audio |
| Android 12 | 31-32 | ✅ Fully Supported | Privacy dashboard |
| Android 11 | 30 | ✅ Fully Supported | Scoped storage |
| Android 10 | 29 | ✅ Fully Supported | Dark mode |
| Android 9 (Pie) | 28 | ✅ Minimum Required | WiFi RTT |
| Android 8.x | 26-27 | ⚠️ Limited | Missing some APIs |
| Android 7.x | 24-25 | ⚠️ Limited | Deprecated APIs |
| Android 6 and below | <23 | ❌ Not Supported | Too old |

### API Level Requirements

**Minimum SDK: 28 (Android 9)**

Why Android 9+ is required:
- Improved location permission model
- Better WiFi scanning APIs
- Enhanced Bluetooth LE support
- Termux compatibility
- Security updates

### Version-Specific Features

#### Android 9 (API 28)
- WiFi RTT (Round-Trip Time)
- Background app restrictions
- Multi-camera API

#### Android 10 (API 29)
- Enhanced location permissions
- WiFi network suggestions API
- Bluetooth LE Advertising Extensions

#### Android 11 (API 30)
- One-time permissions
- Auto-reset permissions
- Wireless debugging

#### Android 12+ (API 31+)
- Precise location vs approximate
- Bluetooth permissions split
- Nearby device permissions

## WiFi Driver Technical Details

### WiFi Access Methods

#### Without Root (GhostOS Approach)

**Available Operations:**
```java
// Via WifiManager (Android API)
- Enable/disable WiFi
- Scan networks
- Get connection info (SSID, BSSID, RSSI, link speed)
- Get configured networks (with limitations)
- Add network suggestions (Android 10+)
```

**Implementation:**
```bash
# GhostOS uses Termux-API which calls:
am startservice --user 0 \
  -n com.termux.api/.WifiAPI \
  --es command "scan"

# This triggers Android's WiFiManager:
WifiManager wifiManager = (WifiManager) 
  context.getSystemService(Context.WIFI_SERVICE);
wifiManager.startScan();
```

**Limitations:**
- ❌ Cannot enable monitor mode
- ❌ Cannot change MAC address (requires root)
- ❌ Cannot inject packets
- ❌ Cannot access raw 802.11 frames
- ❌ Cannot modify driver parameters

#### With Root (Not GhostOS)

**Would Enable:**
```bash
# Direct driver access via nl80211
iw dev wlan0 interface add mon0 type monitor
iw dev mon0 set channel 6

# MAC address change
ip link set dev wlan0 down
macchanger -r wlan0
ip link set dev wlan0 up

# Driver parameter tuning
echo "options cfg80211 ieee80211_regdom=US" > /etc/modprobe.d/cfg80211.conf
```

**GhostOS Does NOT Do This** (no root required).

### WiFi Driver Stack on Android

```
Application Layer: GhostOS Scripts
        ↓
Termux:API Bridge
        ↓
Android Framework: WifiManager
        ↓
WiFi Service: WifiServiceImpl
        ↓
System Server: ConnectivityService
        ↓
WiFi HAL: android.hardware.wifi@1.x
        ↓
Vendor Implementation: libwifi-hal.so
        ↓
Kernel Driver: nl80211 / cfg80211
        ↓
Hardware: WiFi Chipset
```

### Common WiFi Chipsets on Android

| Chipset Family | Example Models | Driver | Root Capabilities |
|---------------|----------------|--------|-------------------|
| Qualcomm Ath | WCN3990, WCN3680 | ath10k, ath9k | Monitor mode possible |
| Broadcom | BCM4339, BCM43455 | bcmdhd | Limited monitor mode |
| MediaTek | MT7921, MT7668 | mt76 | Some monitor support |
| Realtek | RTL8188, RTL8821 | rtl8xxxu | Good monitor support |
| Intel | AC 9560, AX201 | iwlwifi | Best Linux support |

**Note:** Even with root, Android's WiFi HAL may restrict advanced features.

## Bluetooth Driver Technical Details

### Bluetooth Access Methods

#### Without Root (GhostOS Approach)

**Available Operations:**
```java
// Via BluetoothAdapter (Android API)
- Enable/disable Bluetooth
- Scan for devices (BR/EDR and BLE)
- Get paired devices
- Get adapter info (name, address)
- Connect to paired devices
- BLE GATT operations
```

**Implementation:**
```bash
# GhostOS uses Termux-API:
am startservice --user 0 \
  -n com.termux.api/.BluetoothAPI \
  --es command "scan"

# Triggers BluetoothAdapter:
BluetoothAdapter adapter = BluetoothAdapter.getDefaultAdapter();
adapter.startDiscovery();
```

**Limitations:**
- ❌ Cannot access HCI directly
- ❌ Cannot sniff Bluetooth traffic
- ❌ Cannot inject arbitrary HCI commands
- ❌ Cannot modify Bluetooth firmware
- ❌ Limited low-level control

#### With Root (Not GhostOS)

**Would Enable:**
```bash
# Direct HCI access
hcitool scan
hcitool info <bdaddr>
hcidump -x

# Raw HCI commands
hcitool cmd 0x01 0x0001

# Firmware modification
btfwloader -f firmware.bin

# BlueZ full stack
bluetoothctl
```

**GhostOS Does NOT Do This** (no root required).

### Bluetooth Stack on Android

```
Application Layer: GhostOS Scripts
        ↓
Termux:API Bridge
        ↓
Android Framework: BluetoothAdapter
        ↓
Bluetooth Service: BluetoothManagerService
        ↓
System Server: Bluetooth Stack (Fluoride/Gabeldorsche)
        ↓
Bluetooth HAL: android.hardware.bluetooth@1.x
        ↓
Vendor Implementation: libbt-vendor.so
        ↓
Kernel Driver: HCI (hci_uart, hci_smd)
        ↓
Hardware: Bluetooth Chipset
```

### Common Bluetooth Chipsets on Android

| Chipset | Vendor | Driver | Capabilities |
|---------|--------|--------|--------------|
| Broadcom BCM43xx | Cypress/Infineon | bcm_bt_lpm | BLE 5.0, BR/EDR |
| Qualcomm WCN39xx | Qualcomm | btqcomsmd | BLE 5.1, aptX |
| MediaTek MT76xx | MediaTek | btmtk | BLE 5.0 |
| Intel AX series | Intel | btintel | BLE 5.2 |

## Driver "Patching" Without Root

### What GhostOS Actually Does

Since direct driver modification requires root, GhostOS implements **userspace optimization**:

#### 1. Signal Strength Analysis
```bash
# Read WiFi signal strength
termux-wifi-connectioninfo | grep rssi

# Analyze and provide recommendations
if [ $RSSI -lt -70 ]; then
  echo "Weak signal - move closer to router"
fi
```

#### 2. Connection Quality Monitoring
```bash
# Check link speed
LINK_SPEED=$(termux-wifi-connectioninfo | grep link_speed)

# Monitor packet loss (if available)
ping -c 10 8.8.8.8 | grep 'packet loss'
```

#### 3. Configuration Optimization
```bash
# Suggest better WiFi channels (if scanning available)
# Recommend 5GHz over 2.4GHz
# Identify interference sources
```

#### 4. Performance Tuning
```bash
# Android system settings (where accessible)
# Termux environment variables
# Network buffer tuning (userspace)
```

### What "Patching" Means in Non-Root Context

| Term | Root Meaning | Non-Root Meaning (GhostOS) |
|------|--------------|----------------------------|
| **Driver Patch** | Modify driver code/firmware | Optimize within API limits |
| **WiFi Optimization** | Change driver parameters | Analyze and recommend |
| **Bluetooth Tuning** | Modify HCI parameters | Monitor and suggest |
| **Performance Fix** | Kernel module updates | Userspace improvements |

### Actual Modifications GhostOS Makes

✅ **Does Modify:**
- Termux environment configuration
- User scripts and aliases
- Application-level settings
- Debian proot environment

❌ **Does NOT Modify:**
- Kernel drivers
- System partition
- Android framework
- Hardware firmware
- Bootloader

## Security & Permissions

### Permission Model

#### Android Manifest (Termux:API)
```xml
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.BLUETOOTH"/>
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN"/>
<uses-permission android:name="android.permission.BLUETOOTH_SCAN"/>
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT"/>
```

#### Runtime Permissions Required
- **Location** (for WiFi/Bluetooth scanning - Android requirement)
- **Nearby Devices** (Android 12+ for Bluetooth)
- **Storage** (for file access)

### SELinux Context

GhostOS runs in Termux's SELinux context:
```bash
# Check context
getenforce  # Usually: Enforcing
id -Z       # Shows: u:r:untrusted_app:s0:c...
```

**Restrictions:**
- Cannot access `/system`, `/vendor`, `/data/system`
- Cannot load kernel modules
- Cannot modify system properties (most)
- Cannot access other apps' data

### Security Boundaries

```
┌───────────────────────────────────────┐
│  Android Kernel (Privileged)          │
│  - Drivers, HAL, System Services      │
│  - Root/System UID required           │
├───────────────────────────────────────┤
│  Android Framework (Protected)        │
│  - APIs with permission checks        │
│  - SELinux enforced                   │
├───────────────────────────────────────┤
│  Termux:API (User App)                │
│  - Standard app permissions           │
│  - User UID (10xxx)                   │
├───────────────────────────────────────┤
│  GhostOS Scripts (Userspace)          │
│  - No special privileges              │
│  - Sandboxed environment              │
└───────────────────────────────────────┘
```

**GhostOS operates entirely in the bottom layer.**

## Performance Considerations

### CPU Architecture Support

| Architecture | Support | Performance |
|--------------|---------|-------------|
| ARM64 (aarch64) | ✅ Best | Native, fastest |
| ARM (armv7) | ✅ Good | Native, fast |
| x86_64 | ✅ Good | Emulation/native |
| x86 | ✅ Limited | Slower emulation |

### Resource Usage

**Typical Footprint:**
- **RAM**: 50-200 MB (Termux + scripts)
- **RAM**: +300-500 MB (Debian proot active)
- **Storage**: 500 MB (base install)
- **Storage**: +2-3 GB (Debian with packages)
- **CPU**: <5% idle, 20-40% during compilation
- **Battery**: Minimal when idle

### Optimization Tips

1. **Minimize Debian Usage**: Exit when not needed
2. **Use Native Termux**: Faster than proot
3. **Clear Package Cache**: `pkg clean` regularly
4. **Disable Unused Services**: In Debian environment
5. **Monitor Battery**: Use Android battery settings

## Compatibility Testing

### Tested Devices

| Device | Android Version | Status | Notes |
|--------|----------------|--------|-------|
| Pixel 6 | Android 14 | ✅ Works | All features |
| Samsung Galaxy S21 | Android 13 | ✅ Works | All features |
| OnePlus 9 | Android 12 | ✅ Works | All features |
| Xiaomi Mi 11 | Android 11 | ✅ Works | All features |
| Moto G7 | Android 9 | ✅ Works | Minimum supported |

### Known Issues

#### Device-Specific

**Xiaomi (MIUI):**
- May restrict background Termux
- Solution: Disable battery optimization for Termux

**Samsung (One UI):**
- Extra permission dialogs
- Solution: Grant all requested permissions

**Huawei (EMUI):**
- May lack Google Play Services (affects some features)
- Solution: Use F-Droid version, no Google dependencies

**OnePlus (OxygenOS):**
- Aggressive RAM management
- Solution: Lock Termux in recents

#### Android Version-Specific

**Android 11+:**
- Scoped storage restrictions
- Solution: Grant storage permission, use `/sdcard`

**Android 12+:**
- Bluetooth permission split
- Solution: Grant all Bluetooth permissions

**Android 13+:**
- Nearby devices permission
- Solution: Grant nearby devices permission

## Development & Debugging

### Enable Debug Logging

```bash
# In GhostOS scripts, add:
set -x  # Enable bash debug mode

# View Android logs:
pkg install android-tools
adb logcat | grep -i "wifi\|bluetooth"
```

### Testing WiFi/Bluetooth

```bash
# WiFi test suite
ghostos-wifi status
ghostos-wifi scan
ghostos-wifi info

# Bluetooth test suite
ghostos-bluetooth status
ghostos-bluetooth scan
ghostos-bluetooth devices

# Full diagnostic
ghostos-driver-optimizer
ghostos-system
```

### Common Debug Commands

```bash
# Check Android version
getprop ro.build.version.release
getprop ro.build.version.sdk

# Check WiFi interface
ip link show wlan0

# Check Bluetooth status
getprop bluetooth.enable

# View system properties
getprop | grep -i "wifi\|bluetooth"

# Test Termux-API
termux-wifi-connectioninfo
termux-bluetooth-connectioninfo
```

## Future Enhancements

### Planned Features (No Root Required)

- [ ] WiFi signal strength graphing
- [ ] Bluetooth device history tracking
- [ ] Network performance benchmarking
- [ ] Automated connection optimization
- [ ] Integration with other Termux tools
- [ ] Additional proot distributions
- [ ] GUI launcher (via VNC)

### Wishlist (Would Require Root)

- [ ] WiFi monitor mode support
- [ ] Bluetooth HCI direct access
- [ ] Packet capture capabilities
- [ ] Driver parameter modification
- [ ] Firmware updates
- [ ] Custom kernel modules

**Note:** Root features will never be part of GhostOS as they compromise Android security and void warranties.

## Conclusion

GhostOS for Android provides powerful WiFi and Bluetooth management without root by:

1. **Using Android's Official APIs**: Works within security model
2. **Leveraging Termux:API**: Bridges userspace to Android framework
3. **Optimizing Userspace**: Performance tuning without kernel access
4. **Providing Linux Environment**: Full Debian via proot

While not as powerful as root solutions, GhostOS offers:
- ✅ Security (no system modifications)
- ✅ Reversibility (easy uninstall)
- ✅ Warranty-safe (no bootloader unlock)
- ✅ Practical features (covers 90% of use cases)

For advanced driver modification, root access would be required, but GhostOS demonstrates that most practical WiFi and Bluetooth management can be accomplished without it.

---

**Technical Support**: See GitHub issues or consult Android documentation for platform-specific details.
