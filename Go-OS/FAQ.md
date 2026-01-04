# GhostOS - Frequently Asked Questions (FAQ)

Common questions and answers about GhostOS for Desktop and Android platforms.

## General Questions

### What is GhostOS?

GhostOS is a privacy-focused, customizable operating system available in two variants:
1. **Desktop/Server**: A Debian-based Linux distribution with bootable ISOs
2. **Android**: A Termux-based Linux environment for Android 9+ devices

### Is GhostOS free?

Yes! GhostOS is completely free and open-source. It's based on Debian Linux and other open-source projects.

### Do I need to pay for anything?

No. All components are free. However, you may choose to:
- Donate to upstream projects (Debian, Termux, etc.)
- Purchase USB drives for bootable media
- Pay for cloud storage if using v2.0's backup features

### Is GhostOS safe to use?

Yes. GhostOS:
- Uses official Debian packages and Android APIs
- Makes no system modifications on Android (non-root)
- Can be fully removed without traces
- Contains no telemetry or tracking
- Is open-source and auditable

## Desktop/Server Questions

### Do I need to be root to build GhostOS?

Yes, building the ISO requires root/sudo access because:
- debootstrap needs to create system files
- Loop devices and mounting require root
- GRUB installation requires root

However, **testing the ISO** can be done without root in a VM.

### How long does building take?

Build times vary:
- **v1.0**: 2-3 hours
- **v1.1**: 2.5-3.5 hours
- **v2.0**: 3-4 hours
- **All versions**: 6-8 hours

Depends on CPU speed, disk I/O, and internet connection.

### Can I build GhostOS on Windows?

Not directly. You need a Debian-based Linux system to build. Options:
1. Use WSL2 (Windows Subsystem for Linux) with Debian
2. Use a Linux VM (VirtualBox, VMware)
3. Use a Live Linux USB
4. Dual-boot with Linux

### Can I customize the build?

Yes! Edit the installation scripts in `$HOME/ghostos-ultimate/build/install_v*.sh` before building.

Add packages:
```bash
apt-get install -y \
    your-package-here \
    another-package
```

### Why are the ISOs so large?

GhostOS includes:
- Complete desktop environment
- Development tools (compilers, IDEs)
- Gaming support (Steam, Wine, Proton)
- AI/ML frameworks (v2.0)
- Security tools
- Drivers and firmware
- Offline capability (all packages included)

For smaller ISOs, remove packages from build scripts.

### Can I install GhostOS without USB?

Yes! Boot the ISO in:
- **VirtualBox**: Full virtualization
- **QEMU/KVM**: Hardware virtualization
- **VMware**: Commercial option
- **Network boot**: PXE boot setup

### Will GhostOS work on my hardware?

Probably! GhostOS supports:
- **x86_64**: All modern Intel/AMD CPUs
- **ARM64**: Raspberry Pi, ARM servers (v2.0)
- **NVIDIA**: GPU drivers included
- **AMD**: Full AM5/RDNA support
- **Intel**: Including Arc GPUs

Test in a VM first to verify.

### Can I dual-boot GhostOS with Windows?

Yes, but:
- Back up your data first
- You'll need to partition your drive
- Use GParted or similar tools
- Install GhostOS to separate partition
- GRUB will detect Windows automatically

**Easier option**: Use GhostOS in a VM or on a separate machine.

## Android Questions

### Do I need root for Android GhostOS?

**NO!** GhostOS for Android is specifically designed to work **without root**. This means:
- ✅ No warranty void
- ✅ No bootloader unlock required
- ✅ No security risks
- ✅ Fully reversible

### Why does it need Location permission?

**Android requirement, not GhostOS!**

Android requires location permission for:
- WiFi scanning (security/privacy measure by Google)
- Bluetooth scanning (to prevent tracking)

GhostOS never accesses your actual location. It only uses these permissions to scan WiFi/Bluetooth.

### Can I use GhostOS to hack WiFi?

**No.** Without root access:
- ❌ No monitor mode
- ❌ No packet injection
- ❌ No WEP/WPA cracking
- ❌ No raw 802.11 frames

GhostOS provides legitimate WiFi management, not hacking tools.

### Why install Termux from F-Droid and not Google Play?

Google Play version is **outdated and incompatible**. F-Droid has:
- Latest Termux version
- Regular updates
- Proper Android 10+ support
- Compatible with Termux:API

**Always use F-Droid!**

### Will GhostOS drain my battery?

Minimal impact:
- **Idle**: <1% per hour
- **Active Linux**: 5-10% per hour
- **Compilation**: 15-20% per hour

Tips to save battery:
- Exit Debian when not in use
- Disable WiFi/Bluetooth when not needed
- Use Android's battery optimization

### Can I run Android apps from GhostOS?

No. GhostOS provides:
- Linux environment (Debian)
- Command-line tools
- WiFi/Bluetooth management

Android apps run in Android, not in the Linux environment.

However, you can:
- Access Android files from Linux
- Run Linux CLI tools
- Install Python/Node.js apps
- Compile and run Linux software

### How do I uninstall GhostOS from Android?

Simple:
```bash
# Remove Debian environment
proot-distro remove debian

# Remove GhostOS
rm -rf ~/ghostos-android

# Edit ~/.bashrc and remove GhostOS lines
nano ~/.bashrc

# Optionally uninstall Termux apps
```

Completely reversible, no traces left.

### Does GhostOS support Android 14?

Yes! GhostOS supports:
- ✅ Android 14 (latest)
- ✅ Android 13
- ✅ Android 12
- ✅ Android 11
- ✅ Android 10
- ✅ Android 9 (minimum)

Older versions (Android 8 and below) are not supported.

### Can I use GhostOS on a tablet?

Yes! GhostOS works on:
- Android phones
- Android tablets
- Chromebooks with Android support
- Android TV boxes (with keyboard)

### Why can't I modify WiFi drivers?

**Android security model prevents it.**

Without root:
- Drivers are in `/system` (read-only)
- Kernel modules require root
- Firmware is protected
- SELinux enforces restrictions

GhostOS optimizes **within** these limits but cannot modify drivers directly.

## Technical Questions

### What's the difference between proot and chroot?

**chroot**: Traditional method, requires root
- Full system access
- Can access all hardware
- Requires root privileges

**proot**: User-space implementation
- No root required
- Runs as regular user
- Safer, more restricted

GhostOS uses **proot** for Android (no root needed).

### Can I access Android storage from Debian?

Yes! Android storage is mounted at:
```bash
/sdcard          # Internal storage
/sdcard/Download # Downloads folder
```

Example:
```bash
ghostos-debian
cd /sdcard/Download
ls -la
```

### Can I use SSH with GhostOS Android?

Yes! Install OpenSSH in Termux:
```bash
pkg install openssh
sshd

# Find your IP
ip addr show wlan0

# Connect from another device
ssh -p 8022 user@<android-ip>
```

### Does GhostOS collect data?

**Absolutely not!**

GhostOS:
- ❌ No telemetry
- ❌ No tracking
- ❌ No analytics
- ❌ No phone-home
- ❌ No data collection

Completely offline after installation.

### Can I contribute to GhostOS?

Yes! Contributions welcome:
1. Fork the repository
2. Make improvements
3. Test your changes
4. Submit pull request

Ideas for contributions:
- Bug fixes
- Documentation improvements
- New features
- Hardware support
- Translations

### What programming languages are supported?

**Desktop GhostOS**: Everything Linux supports
- C, C++, Rust, Go
- Python, Ruby, Perl
- Java, Kotlin, Scala
- JavaScript, TypeScript (Node.js)
- PHP, Lua, and more

**Android GhostOS**: Install via apt in Debian
- Python 3
- Node.js
- Java (OpenJDK)
- C/C++ (gcc, g++)
- Go, Rust (via install)

### Can I run a web server?

**Desktop**: Yes, full server capabilities
- Apache, Nginx
- Node.js servers
- Python Flask/Django
- Database servers

**Android**: Yes, in Debian environment
```bash
ghostos-debian
apt install -y nginx python3-flask nodejs
```

But note: Android may restrict background services.

## Privacy & Security Questions

### Is GhostOS more secure than regular Debian?

Desktop GhostOS includes **additional security**:
- Enhanced firewall (UFW)
- Security scanning (ClamAV, rkhunter)
- Kernel hardening (v2.0)
- AppArmor enforcement (v2.0)
- Privacy controls (telemetry blocking)

But it's based on secure Debian foundation.

### Does GhostOS block telemetry?

Yes! Desktop GhostOS (v1.1+) blocks:
- Microsoft telemetry
- Google analytics
- Facebook tracking
- Amazon telemetry
- Adobe telemetry
- NVIDIA telemetry

Via `/etc/hosts` entries and firewall rules.

### Can GhostOS be used for anonymity?

No! GhostOS is **not** an anonymity OS like Tails or Whonix.

For anonymity:
- Use Tor Browser
- Consider Tails OS
- Use VPN services
- Practice OPSEC

GhostOS provides privacy (reduced telemetry) but not anonymity (hiding identity).

### Is GhostOS audited?

No formal security audit. However:
- Based on audited Debian
- Uses standard packages
- Open-source (you can audit)
- Community reviewed

For high-security needs, use officially audited systems.

## Compatibility Questions

### Does GhostOS work on Raspberry Pi?

**v2.0**: Yes, includes ARM64 support
**v1.0/v1.1**: No, x86_64 only

For Raspberry Pi:
- Build GhostOS v2.0
- Use ARM64 version
- Test on Pi 4 or Pi 5

### Can I run GhostOS on old hardware?

Minimum requirements:
- **Desktop**: 4GB RAM, 2-core CPU, 50GB disk
- **Android**: 2GB RAM, Android 9+

For very old hardware:
- Use lightweight desktop environment
- Remove unnecessary packages
- Consider Alpine Linux base (manual)

### Does GhostOS work on Apple Silicon (M1/M2)?

Not natively. Options:
1. Use ARM64 build (v2.0) in VM
2. Use Parallels/UTM virtualization
3. Use QEMU emulation (slower)

### Can I run Windows apps on GhostOS?

Yes, via Wine/Proton:
- Desktop GhostOS includes Wine
- Steam Proton for games
- CrossOver (commercial option)

Not all Windows apps work. Check compatibility.

### Does GhostOS support NVIDIA drivers?

Yes! Desktop GhostOS includes:
- Proprietary NVIDIA drivers
- CUDA toolkit
- cuDNN (v2.0)
- Gaming optimizations

Works with RTX 40, 30, 20, 10 series.

## Troubleshooting Questions

### Build failed - what do I do?

**Desktop build**:
1. Check internet connection
2. Verify sufficient disk space (`df -h`)
3. Check logs: `$HOME/ghostos-ultimate/logs/`
4. Try again (often transient network issues)
5. Report issue on GitHub with full log

**Android install**:
1. Update Termux: `pkg update && pkg upgrade`
2. Clear cache: `pkg clean`
3. Check permissions (Storage, Location)
4. Install Termux:API
5. Try again

### Commands not found on Android

```bash
# Solution:
source ~/.bashrc

# Or use full path:
~/ghostos-android/bin/ghostos
```

### Termux:API not working

1. Install from F-Droid (not Google Play)
2. Grant Location permission
3. Restart Termux
4. Test: `termux-wifi-connectioninfo`

### ISO won't boot

1. Verify ISO checksum: `md5sum -c *.md5`
2. Re-write to USB with `dd`
3. Check BIOS/UEFI settings:
   - Disable Secure Boot
   - Enable USB boot
   - Check boot order
4. Try different USB drive

### Bluetooth not working on Android

1. Install Termux:API
2. Grant Location permission (Android requirement)
3. Enable Bluetooth in Android settings
4. Run: `ghostos-bluetooth enable`
5. Test: `ghostos-bluetooth status`

### Out of disk space during build

**Free up space**:
```bash
# Clear apt cache
sudo apt-get clean

# Remove old kernels
sudo apt autoremove

# Check usage
df -h

# Or use different directory:
# Edit script: PROJECT_DIR="/mnt/external/ghostos"
```

## Performance Questions

### How does GhostOS compare to Ubuntu/Mint?

**Similarities**:
- Based on Debian (like Ubuntu)
- Similar performance
- Same package ecosystem

**Differences**:
- More privacy-focused (telemetry blocking)
- Gaming-optimized (Steam, Wine pre-installed)
- Security tools included
- AMD AM5 optimizations
- Customized for specific hardware

### Is Android GhostOS slow?

**proot overhead**: ~10-20% slower than native

**But**:
- Still very usable
- Faster than full emulation
- Native Termux is full speed
- Most tasks are I/O bound anyway

### Can I play games on GhostOS?

**Desktop**: Yes!
- Steam pre-installed
- Proton for Windows games
- Native Linux games
- RetroArch for emulation
- Lutris for game management

**Android**: No gaming focus
- Debian proot not for gaming
- Android games run in Android (not GhostOS)

## Comparison Questions

### GhostOS vs Arch Linux?

| Feature | GhostOS | Arch |
|---------|---------|------|
| Base | Debian | Arch |
| Stability | Stable | Rolling |
| Difficulty | Easy | Advanced |
| Gaming | Pre-configured | Manual setup |
| Privacy | Built-in | Manual setup |
| Learning curve | Low | High |

### GhostOS vs Linux Deploy (Android)?

| Feature | GhostOS | Linux Deploy |
|---------|---------|--------------|
| Root required | No | Yes (for full features) |
| WiFi/Bluetooth tools | Yes | No |
| Pre-configured | Yes | No |
| Setup complexity | Easy | Medium |
| Driver optimization | Yes | No |

### GhostOS vs Andronix (Android)?

| Feature | GhostOS | Andronix |
|---------|---------|----------|
| Root required | No | No |
| WiFi management | Yes | No |
| Bluetooth management | Yes | No |
| Free | Yes | Freemium |
| Driver tools | Yes | No |

## Future Plans

### What's next for GhostOS?

**Desktop**:
- More hardware support
- Additional privacy features
- Better gaming integration
- ARM optimizations

**Android**:
- GUI launcher (VNC)
- Additional distro options
- Performance improvements
- More automation tools

### Will root features be added?

**No.** GhostOS will remain root-free on Android to maintain:
- Security
- Warranty protection
- Simplicity
- Universal compatibility

For root features, use other tools (but understand the risks).

### Can I request features?

Yes! Submit feature requests:
1. Check existing issues on GitHub
2. Create new issue with:
   - Clear description
   - Use case
   - Expected behavior
3. Be patient (volunteer project)

## Still Have Questions?

### Get Help

1. **Documentation**: Read guides in `Go-OS/` directory
2. **Built-in help**: Run `ghostos-help` (Android)
3. **GitHub Issues**: Search existing issues
4. **Create Issue**: If problem not found

### Resources

- **GitHub**: https://github.com/jameshroop-art/GO-OS
- **Termux Wiki**: https://wiki.termux.com
- **Debian Docs**: https://www.debian.org/doc/
- **F-Droid**: https://f-droid.org

---

**Can't find your answer?** Open an issue on GitHub with your question!
