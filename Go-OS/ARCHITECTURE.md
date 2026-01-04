# GhostOS Architecture Overview

Visual and technical overview of GhostOS architecture for both Desktop and Android platforms.

## Desktop/Server Architecture

### Build System Flow

```
┌─────────────────────────────────────────────────────────┐
│  ghostos-build.sh (Build Script)                        │
│  - Version selection (1.0, 1.1, 2.0, or all)           │
│  - USB detection and bootable creation option           │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Dependency Installation                                 │
│  - debootstrap, squashfs-tools, xorriso, grub           │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Generate Installation Scripts                          │
│  - install_v1.0.sh (base system)                        │
│  - install_v1.1.sh (enhanced privacy)                   │
│  - install_v2.0.sh (next-gen features)                  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Create Root Filesystem (debootstrap)                   │
│  - Base Debian Bookworm system                          │
│  - Core utilities and libraries                         │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Execute Installation Scripts (chroot)                  │
│  - Install version-specific packages                    │
│  - Configure system                                     │
│  - Setup drivers and firmware                           │
│  - Apply privacy/security settings                      │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Create Bootloader (GRUB)                               │
│  - BIOS/Legacy boot support                             │
│  - UEFI boot support                                    │
│  - Boot menu configuration                              │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Generate ISO Image (xorriso)                           │
│  - Hybrid ISO (can be written to USB)                   │
│  - Squashfs compressed filesystem                       │
│  - MD5 and SHA256 checksums                             │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Optional: Create Bootable USB (dd)                     │
│  - Write ISO to USB drive                               │
│  - Verify write                                         │
└─────────────────────────────────────────────────────────┘
```

### Desktop System Stack

```
┌────────────────────────────────────────────────────────┐
│  User Applications                                      │
│  - Firefox, Steam, VS Code, LibreOffice, etc.         │
├────────────────────────────────────────────────────────┤
│  Desktop Environment                                    │
│  - XFCE (default) or Wayland/Sway (v2.0)              │
│  - Picom compositor (v1.1+)                            │
├────────────────────────────────────────────────────────┤
│  Display Server                                         │
│  - X11 (v1.0, v1.1) or Wayland (v2.0)                 │
├────────────────────────────────────────────────────────┤
│  System Services                                        │
│  - systemd, NetworkManager, PulseAudio                 │
│  - Security: UFW, AppArmor (v2.0), ClamAV (v1.1+)     │
├────────────────────────────────────────────────────────┤
│  Package Management                                     │
│  - apt/dpkg (Debian package manager)                   │
│  - Flatpak (optional additional packages)              │
├────────────────────────────────────────────────────────┤
│  Linux Kernel                                           │
│  - Debian kernel with firmware                         │
│  - Drivers: AMD, NVIDIA, Intel, USB4, Thunderbolt     │
├────────────────────────────────────────────────────────┤
│  Hardware                                               │
│  - CPU: x86_64 (all), ARM64 (v2.0)                    │
│  - GPU: AMD, NVIDIA, Intel                             │
│  - Peripherals: All standard Linux hardware            │
└────────────────────────────────────────────────────────┘
```

## Android Architecture

### Installation Flow

```
┌─────────────────────────────────────────────────────────┐
│  User Downloads ghostos-android.sh                      │
│  - From GitHub or wget                                  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Android Version Check                                   │
│  - Verify Android 9+ (API 28+)                          │
│  - Check Termux environment                             │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Update Termux Packages                                  │
│  - pkg update && pkg upgrade                            │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Install Dependencies                                    │
│  - proot, proot-distro, termux-api                      │
│  - wget, curl, git, python, openssh                     │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Install Debian Environment (proot-distro)              │
│  - Downloads Debian rootfs                              │
│  - Sets up proot environment                            │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Create GhostOS Directory Structure                      │
│  - ~/ghostos-android/bin (commands)                     │
│  - ~/ghostos-android/config (configuration)             │
│  - ~/ghostos-android/drivers (driver info)              │
│  - ~/ghostos-android/logs (log files)                   │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Generate Management Scripts                             │
│  - ghostos-wifi (WiFi management)                       │
│  - ghostos-bluetooth (Bluetooth management)             │
│  - ghostos-driver-optimizer (optimization)              │
│  - ghostos-debian (environment launcher)                │
│  - ghostos-system (system info)                         │
│  - ghostos-help (help system)                           │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Add to PATH                                             │
│  - Update ~/.bashrc                                     │
│  - Create aliases                                       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  Installation Complete                                   │
│  - Display instructions                                 │
│  - Remind about Termux:API                              │
│  - Show available commands                              │
└─────────────────────────────────────────────────────────┘
```

### Android System Stack

```
┌────────────────────────────────────────────────────────┐
│  Layer 7: GhostOS Commands (User Interface)            │
│  - ghostos-wifi, ghostos-bluetooth, ghostos-*          │
│  - Shell scripts in ~/ghostos-android/bin/             │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│  Layer 6: Termux Environment (Userspace)               │
│  - Bash shell                                          │
│  - Linux command-line tools                            │
│  - No root, standard user permissions                  │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│  Layer 5: Debian proot Environment (Optional)          │
│  - Full Debian Linux (userspace)                       │
│  - apt package manager                                 │
│  - Python, Node.js, compilers, etc.                    │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│  Layer 4: Termux:API Bridge                            │
│  - Bridges Termux to Android APIs                      │
│  - Uses Android Intent system (IPC)                    │
│  - No root required                                    │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│  Layer 3: Android Framework APIs                       │
│  - WifiManager (WiFi control)                          │
│  - BluetoothAdapter (Bluetooth control)                │
│  - ConnectivityManager (network info)                  │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│  Layer 2: Hardware Abstraction Layer (HAL)             │
│  - WiFi HAL (android.hardware.wifi@1.x)                │
│  - Bluetooth HAL (android.hardware.bluetooth@1.x)      │
│  - Vendor-specific implementations                     │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│  Layer 1: Linux Kernel & Drivers                       │
│  - WiFi drivers (nl80211, cfg80211)                    │
│  - Bluetooth drivers (HCI)                             │
│  - Hardware firmware                                   │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│  Layer 0: Hardware                                      │
│  - WiFi chipset (Qualcomm, Broadcom, etc.)            │
│  - Bluetooth chipset                                   │
│  - CPU, RAM, Storage                                   │
└────────────────────────────────────────────────────────┘
```

### WiFi Control Flow (Non-Root)

```
User Command: ghostos-wifi scan
        │
        ▼
GhostOS Script (~/ghostos-android/bin/ghostos-wifi)
        │
        ▼
Calls: termux-wifi-scaninfo
        │
        ▼
Termux:API App (com.termux.api)
        │
        ▼
Android Intent System (IPC)
        │
        ▼
WifiManager.startScan()
        │
        ▼
Android System Server (system_server)
        │
        ▼
WiFi Service (WifiServiceImpl)
        │
        ▼
WiFi HAL (Hardware Abstraction Layer)
        │
        ▼
Vendor WiFi Implementation (libwifi-hal.so)
        │
        ▼
Kernel Driver (nl80211/cfg80211)
        │
        ▼
WiFi Hardware Scan
        │
        ▼
Results Flow Back Up Through Stack
        │
        ▼
JSON Output to User
```

### Bluetooth Control Flow (Non-Root)

```
User Command: ghostos-bluetooth scan
        │
        ▼
GhostOS Script (~/ghostos-android/bin/ghostos-bluetooth)
        │
        ▼
Calls: termux-bluetooth-scaninfo
        │
        ▼
Termux:API App (com.termux.api)
        │
        ▼
Android Intent System (IPC)
        │
        ▼
BluetoothAdapter.startDiscovery()
        │
        ▼
Android Bluetooth Manager Service
        │
        ▼
Bluetooth Stack (Fluoride/Gabeldorsche)
        │
        ▼
Bluetooth HAL (Hardware Abstraction Layer)
        │
        ▼
Vendor BT Implementation (libbt-vendor.so)
        │
        ▼
Kernel Driver (HCI - hci_uart/hci_smd)
        │
        ▼
Bluetooth Hardware Scan
        │
        ▼
Results Flow Back Up Through Stack
        │
        ▼
JSON Output to User
```

## Security Boundaries

### Desktop Security Model

```
┌────────────────────────────────────────┐
│  Root/System Level                     │
│  - Kernel, drivers, system files       │
│  - Requires root/sudo access           │
│  - Full hardware control               │
├────────────────────────────────────────┤
│  System Services Level                 │
│  - systemd, NetworkManager, etc.       │
│  - Root-owned, restricted access       │
├────────────────────────────────────────┤
│  User Level                            │
│  - User applications                   │
│  - Limited file access                 │
│  - No system modification              │
└────────────────────────────────────────┘
```

### Android Security Model (GhostOS Context)

```
┌────────────────────────────────────────┐  ◄─ Cannot Access
│  Kernel & System Partition             │     (Requires Root)
│  - Drivers, firmware, /system          │
│  - Root UID (0) only                   │
├────────────────────────────────────────┤
│  Android Framework (Protected)         │  ◄─ Access via APIs
│  - System services, HAL                │     (With Permissions)
│  - System UID (1000)                   │
├────────────────────────────────────────┤
│  Termux:API (User App)                 │  ◄─ Bridge Layer
│  - User UID (10xxx)                    │
│  - Standard app permissions            │
├────────────────────────────────────────┤
│  GhostOS Scripts (Userspace)           │  ◄─ GhostOS Operates Here
│  - Same UID as Termux                  │     (No Special Access)
│  - Sandboxed environment               │
└────────────────────────────────────────┘
```

## Data Flow

### Desktop Build Data Flow

```
Source: Debian Repos ─┐
                      │
                      ├──► Build Host ──► Rootfs ──► Squashfs ──► ISO File
                      │                                             │
Downloaded Packages ──┘                                             │
                                                                    ▼
                                                              USB Drive or
                                                              VM/Hardware Boot
```

### Android Installation Data Flow

```
GitHub Repo ──► wget ──► ghostos-android.sh ──► Execution
                                                     │
                                                     ▼
F-Droid/Termux ──────────────────► Package Installation
                                                     │
                                                     ▼
proot-distro ──────────────────► Debian Rootfs Download
                                                     │
                                                     ▼
                                          Script Generation
                                                     │
                                                     ▼
                                           PATH Configuration
                                                     │
                                                     ▼
                                          Ready to Use!
```

### Android Runtime Data Flow (WiFi Scan Example)

```
User Input
    │
    ▼
ghostos-wifi scan (Script)
    │
    ▼
termux-wifi-scaninfo (Command)
    │
    ▼
Termux:API (App)
    │
    ▼
Android Intent ──► WifiManager ──► WiFi HAL ──► Driver ──► Hardware
                                                                │
                Scan Results Flow Back ◄────────────────────────┘
    │
    ▼
JSON Output
    │
    ▼
Display to User
```

## Component Relationships

### Desktop Components

```
┌─────────────────────────────────────────────────────┐
│                GhostOS Desktop ISO                   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Bootloader (GRUB)                          │   │
│  │  - BIOS boot                                │   │
│  │  - UEFI boot                                │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Live System (Squashfs)                     │   │
│  │  ┌───────────────────────────────────────┐  │   │
│  │  │  Debian Base                          │  │   │
│  │  │  - Core utilities, libraries          │  │   │
│  │  └───────────────────────────────────────┘  │   │
│  │  ┌───────────────────────────────────────┐  │   │
│  │  │  Desktop Environment                  │  │   │
│  │  │  - XFCE or Wayland/Sway              │  │   │
│  │  └───────────────────────────────────────┘  │   │
│  │  ┌───────────────────────────────────────┐  │   │
│  │  │  Applications                         │  │   │
│  │  │  - Firefox, Steam, VS Code, etc.     │  │   │
│  │  └───────────────────────────────────────┘  │   │
│  │  ┌───────────────────────────────────────┐  │   │
│  │  │  Drivers & Firmware                   │  │   │
│  │  │  - AMD, NVIDIA, Intel, etc.          │  │   │
│  │  └───────────────────────────────────────┘  │   │
│  │  ┌───────────────────────────────────────┐  │   │
│  │  │  Security & Privacy                   │  │   │
│  │  │  - UFW, ClamAV, AppArmor             │  │   │
│  │  └───────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### Android Components

```
┌─────────────────────────────────────────────────────┐
│         GhostOS for Android Installation            │
│  ┌─────────────────────────────────────────────┐   │
│  │  Termux Environment                         │   │
│  │  - Base packages (bash, coreutils)          │   │
│  │  - Network tools (wget, curl)               │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Termux:API                                 │   │
│  │  - WiFi API bridge                          │   │
│  │  - Bluetooth API bridge                     │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  proot & proot-distro                       │   │
│  │  - Userspace chroot alternative             │   │
│  │  - No root required                         │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  Debian Environment (proot)                 │   │
│  │  - Full Debian with apt                     │   │
│  │  - Python, Node.js, compilers               │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │  GhostOS Scripts                            │   │
│  │  - ~/ghostos-android/bin/                   │   │
│  │  - WiFi/Bluetooth management                │   │
│  │  - Driver optimization                      │   │
│  │  - System utilities                         │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Version Progression

### Desktop Evolution

```
v1.0 (Stable)
    │
    │ + Enhanced privacy controls
    │ + Malwarebytes-style security
    │ + Improved UI with animations
    ▼
v1.1 (Enhanced)
    │
    │ + Wayland support
    │ + AI assistant (Ollama)
    │ + Cloud backup (encrypted)
    │ + Plugin system
    │ + ARM64 support
    ▼
v2.0 (Next-Gen)
    │
    │ Future: More features, hardware support
    ▼
v3.0 (Future)
```

### Android Development

```
Initial Concept
    │
    │ + Android 9+ compatibility check
    │ + Termux integration
    │ + Basic WiFi/Bluetooth control
    ▼
v1.0-android (Current)
    │
    │ + Performance optimizations
    │ + GUI launcher option
    │ + Additional distributions
    ▼
Future Android Versions
```

## Conclusion

This architecture overview provides a visual representation of how GhostOS works on both Desktop and Android platforms. Key takeaways:

**Desktop**: Traditional Linux distribution build system creating bootable ISOs
**Android**: Clever use of userspace tools to provide Linux environment and hardware control without root

Both platforms share the GhostOS philosophy:
- Privacy-focused
- Security-conscious
- User-friendly
- Fully customizable
- Open-source

---

For more details, see platform-specific documentation in the `Go-OS/` directory.
