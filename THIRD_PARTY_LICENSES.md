# Third-Party Licenses and Attributions

This document lists all third-party software, libraries, and components used in the GhostOS project, along with their licenses and attributions.

## Base Operating Systems

### Debian 12 (Bookworm)
- **License:** DFSG-compliant (GPL, LGPL, BSD, MIT, Apache, etc.)
- **Copyright:** Software in the Public Interest, Inc. and individual package maintainers
- **Website:** https://www.debian.org
- **Description:** Universal Operating System - Stable Linux distribution
- **Note:** GhostOS is a derivative work that adds custom configurations, security tools, and packages to Debian 12
- **Trademark:** Debian® is a registered trademark of Software in the Public Interest, Inc.

## Build Tools and System Utilities

### debootstrap
- **License:** GPL
- **Description:** Tool for installing a Debian base system
- **Used for:** Bootstrapping Debian 12 in the build process

### squashfs-tools
- **License:** GPL
- **Description:** Tools for creating and extracting SquashFS filesystems
- **Used for:** Creating compressed filesystem for the ISO

### GRUB (GNU GRand Unified Bootloader)
- **License:** GPLv3+
- **Copyright:** Free Software Foundation, Inc.
- **Website:** https://www.gnu.org/software/grub/
- **Used for:** ISO bootloader

### xorriso
- **License:** GPLv3+
- **Description:** ISO 9660 Rock Ridge filesystem manipulator
- **Used for:** Creating bootable ISO images

### live-build
- **License:** GPL
- **Description:** Debian Live build system
- **Used for:** Creating live system images

## Android Components

### Termux
- **License:** GPLv3
- **Copyright:** Termux contributors
- **Website:** https://termux.com
- **Repository:** https://github.com/termux
- **Description:** Android terminal emulator and Linux environment
- **Note:** Must be installed from F-Droid, not Google Play

### Termux:API
- **License:** GPLv3
- **Copyright:** Termux contributors
- **Description:** Provides Android API access to Termux
- **Used for:** WiFi and Bluetooth management

### proot
- **License:** GPL
- **Website:** https://proot-me.github.io/
- **Repository:** https://github.com/proot-me/proot
- **Description:** User-space implementation of chroot, mount --bind, and binfmt_misc
- **Used for:** Running Debian environment on Android without root

## Desktop Environments and GUI

### XFCE
- **License:** GPL, LGPL, BSD
- **Website:** https://www.xfce.org
- **Description:** Lightweight desktop environment
- **Used in:** GhostOS v1.0, v1.1

### GNOME (if used)
- **License:** GPL, LGPL
- **Website:** https://www.gnome.org
- **Description:** Desktop environment
- **May be used in:** Various configurations

### Wayland (v2.0)
- **License:** MIT
- **Website:** https://wayland.freedesktop.org
- **Description:** Display server protocol
- **Used in:** GhostOS v2.0

## Security and Privacy Tools

### ClamAV
- **License:** GPLv2
- **Website:** https://www.clamav.net
- **Description:** Antivirus engine
- **Used for:** Malware scanning

### UFW (Uncomplicated Firewall)
- **License:** GPLv3
- **Description:** Front-end for iptables
- **Used for:** Firewall management

### rkhunter
- **License:** GPL
- **Description:** Rootkit Hunter
- **Used for:** Security scanning

### chkrootkit
- **License:** BSD
- **Description:** Checks for signs of a rootkit
- **Used for:** Security scanning

### Unbound
- **License:** BSD
- **Website:** https://nlnetlabs.nl/projects/unbound/
- **Description:** Validating, recursive, caching DNS resolver
- **Used for:** DNS privacy

## Development Tools

### GCC (GNU Compiler Collection)
- **License:** GPLv3+
- **Website:** https://gcc.gnu.org
- **Description:** Compiler suite

### Python
- **License:** PSF License (Python Software Foundation License)
- **Website:** https://www.python.org
- **Description:** Programming language

### Node.js
- **License:** MIT
- **Website:** https://nodejs.org
- **Description:** JavaScript runtime

### Git
- **License:** GPLv2
- **Website:** https://git-scm.com
- **Description:** Version control system

## Gaming Support

### Steam
- **License:** Proprietary (Valve Corporation)
- **Trademark:** Steam® is a trademark of Valve Corporation
- **Website:** https://store.steampowered.com
- **Note:** Not included in ISO, users must install separately
- **Used for:** Gaming platform

### Wine
- **License:** LGPL
- **Website:** https://www.winehq.org
- **Description:** Windows compatibility layer

### Proton
- **License:** Various (BSD, LGPL, etc.)
- **Copyright:** Valve Corporation and contributors
- **Description:** Wine fork for Steam Play

### Lutris
- **License:** GPLv3
- **Website:** https://lutris.net
- **Description:** Open gaming platform

## Graphics and Hardware Support

### NVIDIA Drivers
- **License:** Proprietary (NVIDIA Corporation)
- **Trademark:** NVIDIA® is a trademark of NVIDIA Corporation
- **Note:** Not redistributed; users must install from official sources

### Mesa
- **License:** MIT and other permissive licenses
- **Website:** https://www.mesa3d.org
- **Description:** Open-source graphics drivers

### AMD GPU Drivers
- **License:** Various (MIT, GPL)
- **Note:** Open-source AMDGPU drivers

## AI/ML Tools (v2.0)

### TensorFlow
- **License:** Apache 2.0
- **Copyright:** Google LLC and contributors
- **Website:** https://www.tensorflow.org

### PyTorch
- **License:** BSD
- **Copyright:** Facebook, Inc. and contributors
- **Website:** https://pytorch.org

### Ollama
- **License:** MIT
- **Website:** https://ollama.ai
- **Description:** Local AI model runner

## Package Managers

### APT (Advanced Package Tool)
- **License:** GPL
- **Description:** Debian package manager

### pip
- **License:** MIT
- **Description:** Python package installer

### npm
- **License:** Artistic License 2.0
- **Description:** Node.js package manager

## Additional Libraries and Tools

### OpenSSL
- **License:** Apache 2.0 (OpenSSL 3.x), OpenSSL License (older versions)
- **Website:** https://www.openssl.org

### curl
- **License:** curl license (MIT-like)
- **Website:** https://curl.se

### wget
- **License:** GPLv3+
- **Website:** https://www.gnu.org/software/wget/

### systemd
- **License:** LGPLv2.1+, GPLv2+
- **Website:** https://systemd.io

### NetworkManager
- **License:** GPL
- **Description:** Network management daemon

### BlueZ
- **License:** GPL
- **Website:** http://www.bluez.org
- **Description:** Linux Bluetooth stack

## Documentation Tools

### Markdown
- **License:** Various (typically BSD or MIT for parsers)
- **Description:** Lightweight markup language

## Fonts

Various open-source fonts may be included:
- **License:** OFL (Open Font License), GPL, Apache
- **Examples:** DejaVu, Liberation, Noto

## Icons and Themes

Various icon sets and themes:
- **License:** GPL, CC-BY-SA, and other open-source licenses
- **May include:** Papirus, Adwaita, Numix, etc.

## Summary of License Types

This project incorporates software under the following license types:

1. **GPL (GNU General Public License)**
   - v2, v3, and various versions
   - Copyleft license requiring source code availability

2. **LGPL (GNU Lesser General Public License)**
   - Used for libraries
   - Less restrictive than GPL

3. **MIT License**
   - Permissive license
   - Minimal restrictions

4. **BSD License**
   - Permissive license (2-clause, 3-clause variants)

5. **Apache License 2.0**
   - Permissive license with patent grants

6. **Creative Commons**
   - Used for documentation and some assets

7. **Proprietary**
   - Some optional components (NVIDIA drivers, Steam, etc.)
   - Not redistributed with the project

## Compliance Requirements

When using or redistributing this software:

1. **GPL Compliance:**
   - Provide source code for GPL-licensed components
   - Maintain copyright notices
   - Include license text
   - Document modifications

2. **Attribution:**
   - Credit original authors and projects
   - Maintain attribution notices
   - Include upstream URLs

3. **Trademark Respect:**
   - Do not use trademarks without permission
   - Clearly indicate derivative nature
   - Avoid implying endorsement

4. **License Preservation:**
   - Include all license files
   - Do not remove copyright notices
   - Pass license terms downstream

## Upstream Project Credits

Special thanks to:
- **Debian Project** - For Debian 12 (Bookworm) base system
- **Termux Contributors** - For Android environment
- **All package maintainers** - For individual packages
- **Open-source community** - For making this possible

## How to Find License Information

For any package in the built system:

```bash
# On Debian systems
dpkg -L <package-name> | grep -i license
cat /usr/share/doc/<package-name>/copyright

# List all installed packages
dpkg -l

# On Android/Termux
pkg show <package-name>
```

## Reporting License Issues

If you believe any license or attribution is missing or incorrect:
1. Open an issue on GitHub
2. Provide specific package/component details
3. Include correct license information
4. We will address it promptly

## Updates to This Document

This document is updated as new components are added or licenses change. Last updated: 2026-01-07

## Disclaimer

This document is provided in good faith to document known third-party components and their licenses. It may not be exhaustive. Users should verify license compliance for their specific use case.

---

**For legal compliance questions, see:** [LEGAL_COMPLIANCE.md](LEGAL_COMPLIANCE.md)  
**For trademark information, see:** [TRADEMARK_NOTICE.md](TRADEMARK_NOTICE.md)  
**For project license, see:** [LICENSE](LICENSE)
