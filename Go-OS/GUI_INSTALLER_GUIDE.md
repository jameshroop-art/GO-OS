# Heck-CheckOS GUI Installer & USB Creator

## Overview

The Heck-CheckOS GUI Installer is a comprehensive graphical tool for creating bootable USB drives and managing disk partitions for PC installation. It provides an intuitive interface for preparing Heck-CheckOS installations on any computer.

## Features

### 📀 Bootable USB Creator
- **Automatic ISO Detection** - Browse and select Heck-CheckOS ISO files
- **Drive Detection** - Automatically detects all connected USB and hard drives
- **Multiple Boot Modes**:
  - Standard USB (BIOS/UEFI compatible)
  - Persistent USB (saves changes between boots)
  - Full Installation (installs Heck-CheckOS to drive)
- **Safety Features**:
  - Confirmation dialogs before destructive operations
  - Drive information display (size, model, type)
  - Verification options for ISO and USB integrity

### 💾 Disk Partitioner
- **Universal Format Support** - Format drives to any filesystem type:
  - **Linux Filesystems**: ext4, ext3, ext2, btrfs, xfs, f2fs, jfs, reiserfs
  - **Windows Filesystems**: NTFS, FAT32, exFAT
  - **Swap**: Linux swap space
- **Partition Operations**:
  - Create new partitions
  - Delete existing partitions
  - Resize partitions
  - Format partitions
- **Visual Tree View** - See all drives and partitions in hierarchical view
- **Real-time Information** - Device names, sizes, types, and mount points

### ⚙️ Advanced Options
- **Partition Schemes**:
  - GPT (GUID Partition Table) - Recommended for UEFI systems
  - MBR (Master Boot Record) - Legacy BIOS compatibility
- **Boot Configuration**:
  - UEFI boot support
  - Secure Boot compatibility
- **Verification**:
  - ISO checksum verification before writing
  - USB verification after creation
- **System Requirements Check** - Verifies all necessary tools are installed

## Installation

### Prerequisites

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-tk parted e2fsprogs ntfs-3g dosfstools
```

**Linux (Fedora/RedHat):**
```bash
sudo dnf install python3 python3-tkinter parted e2fsprogs ntfs-3g dosfstools
```

**Linux (Arch):**
```bash
sudo pacman -Sy python python-tk parted e2fsprogs ntfs-3g dosfstools
```

**Additional Filesystem Tools (Optional but Recommended):**
```bash
# Debian/Ubuntu
sudo apt-get install btrfs-progs xfsprogs f2fs-tools jfsutils reiserfsprogs exfat-utils

# Fedora/RedHat
sudo dnf install btrfs-progs xfsprogs f2fs-tools jfsutils reiserfsprogs exfat-utils

# Arch
sudo pacman -Sy btrfs-progs xfsprogs f2fs-tools jfsutils reiserfsprogs exfat-utils
```

### Running the GUI Installer

**Method 1: Using the Launcher Script (Recommended)**
```bash
sudo bash heckcheckos-installer-gui.sh
```

The launcher script will:
- Check for all dependencies
- Offer to install missing packages
- Launch the GUI with proper permissions

**Method 2: Direct Python Launch**
```bash
sudo python3 heckcheckos-installer-gui.py
```

**Note:** Root/administrator privileges are required for:
- Creating bootable USB drives
- Formatting partitions
- Modifying disk structures

## Usage Guide

### Creating a Bootable USB

1. **Launch the Installer**
   ```bash
   sudo bash heckcheckos-installer-gui.sh
   ```

2. **Select ISO File**
   - Click "Browse..." button
   - Navigate to your Heck-CheckOS ISO file
   - Select the ISO and click Open

3. **Select Target Drive**
   - Click "🔄 Refresh Drives" to scan for USB drives
   - Select your target USB drive from the list
   - **WARNING:** All data on the selected drive will be erased!

4. **Choose Boot Mode**
   - **Standard USB**: Creates a basic bootable USB (recommended)
   - **Persistent USB**: Allows saving changes between boots
   - **Full Installation**: Installs Heck-CheckOS directly to the drive

5. **Create USB**
   - Click "🚀 Create Bootable USB"
   - Confirm the operation
   - Wait for completion (progress shown in status bar)

### Partitioning and Formatting Drives

1. **View Drives and Partitions**
   - Switch to the "💾 Disk Partitioner" tab
   - Click "🔄 Refresh Drives"
   - View all drives and partitions in the tree view

2. **Format a Partition**
   - Select a partition from the tree view
   - Choose format type from dropdown:
     - **ext4**: Linux default (recommended for Linux)
     - **NTFS**: Windows compatibility
     - **FAT32/exFAT**: Universal compatibility
     - **btrfs/xfs**: Advanced Linux filesystems
     - **swap**: Linux virtual memory
   - Click "🔧 Format Selected"
   - Confirm the operation

3. **Create New Partition**
   - Click "➕ Create Partition"
   - Follow prompts for partition size and type

4. **Delete Partition**
   - Select partition to delete
   - Click "🗑️ Delete Selected"
   - Confirm deletion

5. **Resize Partition**
   - Select partition to resize
   - Click "📏 Resize Partition"
   - Specify new size

### Advanced Configuration

1. **Partition Scheme Selection**
   - Switch to "⚙️ Advanced Options" tab
   - Choose partition scheme:
     - **GPT**: Modern, recommended for UEFI systems
     - **MBR**: Legacy BIOS compatibility

2. **Boot Options**
   - Enable/disable UEFI boot support
   - Enable/disable Secure Boot compatibility

3. **Verification Options**
   - Enable ISO checksum verification
   - Enable USB verification after creation

4. **Check System Requirements**
   - Click "🔍 Check System Requirements"
   - View list of installed tools and missing dependencies

## Filesystem Format Guide

### Linux Filesystems

**ext4 (Fourth Extended Filesystem)**
- **Use Case**: Default Linux filesystem, general purpose
- **Features**: Journaling, large file support, reliable
- **Recommended For**: Linux installations, home partitions
- **Max File Size**: 16 TB
- **Max Volume Size**: 1 EB

**ext3/ext2**
- **Use Case**: Legacy Linux filesystems
- **Features**: ext3 has journaling, ext2 does not
- **Recommended For**: Older systems, compatibility

**btrfs (B-tree File System)**
- **Use Case**: Advanced Linux filesystem
- **Features**: Snapshots, compression, RAID support
- **Recommended For**: Advanced users, servers
- **Max File Size**: 16 EB
- **Max Volume Size**: 16 EB

**xfs**
- **Use Case**: High-performance Linux filesystem
- **Features**: Excellent for large files, parallel I/O
- **Recommended For**: Servers, large file storage
- **Max File Size**: 8 EB
- **Max Volume Size**: 8 EB

**f2fs (Flash-Friendly File System)**
- **Use Case**: Optimized for flash storage
- **Features**: Wear-leveling, TRIM support
- **Recommended For**: SSDs, USB drives, SD cards
- **Max File Size**: 3.94 TB
- **Max Volume Size**: 16 TB

**jfs (Journaled File System)**
- **Use Case**: IBM's journaling filesystem
- **Features**: Good performance, low CPU usage
- **Recommended For**: Servers, legacy systems

**reiserfs**
- **Use Case**: Legacy journaling filesystem
- **Features**: Efficient for small files
- **Recommended For**: Legacy systems only

### Universal Filesystems

**NTFS (New Technology File System)**
- **Use Case**: Windows primary filesystem
- **Features**: Journaling, permissions, compression
- **Recommended For**: Windows compatibility, dual-boot
- **Max File Size**: 256 TB
- **Max Volume Size**: 256 TB
- **Note**: Full read/write support on Linux via ntfs-3g

**FAT32 (File Allocation Table 32)**
- **Use Case**: Universal compatibility
- **Features**: Simple, widely supported
- **Recommended For**: USB drives, camera cards
- **Max File Size**: 4 GB (limitation!)
- **Max Volume Size**: 2 TB
- **Pros**: Works on Windows, Linux, Mac, cameras, TVs
- **Cons**: 4GB file size limit

**exFAT (Extended File Allocation Table)**
- **Use Case**: Universal compatibility with large files
- **Features**: No 4GB file size limit
- **Recommended For**: USB drives, external drives
- **Max File Size**: 16 EB
- **Max Volume Size**: 128 PB
- **Pros**: Universal support, large files
- **Cons**: No journaling

### Special Purpose

**swap**
- **Use Case**: Linux virtual memory
- **Features**: Used as overflow RAM
- **Recommended For**: Linux installations
- **Recommended Size**: 1-2x your RAM size

## Format Recommendations by Use Case

### Installation USB Drive
- **Recommended**: FAT32 or exFAT
- **Why**: Universal compatibility, bootloader support
- **Size**: 8GB minimum

### Linux System Partition (/)
- **Recommended**: ext4
- **Alternative**: btrfs (for snapshots)
- **Size**: 32GB minimum

### Linux Home Partition (/home)
- **Recommended**: ext4
- **Alternative**: btrfs, xfs (for large files)
- **Size**: As needed

### Dual-Boot Data Partition
- **Recommended**: NTFS or exFAT
- **Why**: Both Windows and Linux can read/write
- **Size**: As needed

### USB Flash Drive
- **Recommended**: exFAT (if >4GB files) or FAT32
- **Why**: Universal compatibility
- **Size**: Any

### External HDD/SSD
- **Recommended**: 
  - exFAT (universal)
  - NTFS (Windows-focused)
  - ext4 (Linux-focused)
- **Why**: Depends on primary use

### SSD/NVMe Drive
- **Recommended**: ext4, f2fs, or xfs
- **Why**: Good performance, TRIM support
- **Size**: Any

## Safety and Best Practices

### Before Creating Bootable USB
1. **Backup Data**: Always backup important data before operations
2. **Verify ISO**: Check ISO checksum to ensure file integrity
3. **Double-Check Drive**: Ensure you've selected the correct drive
4. **Eject Safely**: Always eject USB drives properly after creation

### Partition Management
1. **Unmount First**: Unmount partitions before formatting
2. **Know Your Data**: Understand what data is on each partition
3. **Test After Format**: Verify partition is working after format
4. **Keep Backups**: Always maintain backups of critical data

### Common Issues

**"Permission Denied" Error**
- **Solution**: Run with sudo/administrator privileges
```bash
sudo bash heckcheckos-installer-gui.sh
```

**"Device is Busy" Error**
- **Solution**: Unmount the device first
```bash
sudo umount /dev/sdX1
```

**USB Not Booting**
- **Solution**: Ensure BIOS/UEFI boot order is correct
- **Solution**: Try recreating USB with different boot mode
- **Solution**: Verify ISO file integrity

**Format Operation Fails**
- **Solution**: Check if partition is mounted (unmount first)
- **Solution**: Verify required tools are installed
- **Solution**: Check for disk errors with fsck

## System Requirements

### To Run the GUI Installer
- Linux-based operating system (Ubuntu, Fedora, Arch, etc.)
- Python 3.6 or higher
- Python tkinter library
- Root/administrator privileges
- X11 or Wayland display server (graphical environment)

### To Create Heck-CheckOS USB
- USB drive with minimum 8GB capacity
- Heck-CheckOS ISO file (download from official sources)
- USB 3.0 port (recommended for faster writes)

### For Heck-CheckOS Installation
- 64-bit x86_64 processor
- 8GB RAM minimum (16GB recommended)
- 32GB storage minimum (64GB+ recommended)
- UEFI firmware (recommended)
- Graphics card with 1GB VRAM minimum

## Troubleshooting

### GUI Won't Launch
```bash
# Check if X11/Wayland is running
echo $DISPLAY
echo $WAYLAND_DISPLAY

# Install missing dependencies
sudo apt-get install python3-tk

# Verify Python version
python3 --version
```

### Can't See USB Drives
```bash
# Manual drive detection
lsblk

# Check USB devices
lsusb

# Refresh with udev
sudo udevadm trigger
```

### Format Tools Missing
```bash
# Install all filesystem tools (Debian/Ubuntu)
sudo apt-get install e2fsprogs ntfs-3g dosfstools btrfs-progs xfsprogs \
                     f2fs-tools jfsutils reiserfsprogs exfat-utils

# Check installed tools
which mkfs.ext4 mkfs.ntfs mkfs.vfat mkfs.exfat mkfs.btrfs mkfs.xfs
```

## Security Considerations

### Running as Root
- The GUI requires root privileges for disk operations
- Only use on trusted systems
- Review operations before confirming
- Never run untrusted scripts as root

### Data Security
- Formatting permanently deletes data (no easy recovery)
- Use secure erase for sensitive drives
- Encrypted partitions should be properly unmounted
- Consider full disk encryption for sensitive installations

### Safe USB Creation
- Always verify ISO checksums before use
- Download ISOs from official sources only
- Scan USB drive for malware after creation (optional)
- Use trusted, new USB drives for sensitive installations

## Command-Line Alternative

For advanced users who prefer command-line:

```bash
# Create bootable USB with dd
sudo dd if=ghostos.iso of=/dev/sdX bs=4M status=progress conv=fsync

# Format partition as ext4
sudo mkfs.ext4 -F /dev/sdX1

# Format partition as NTFS
sudo mkfs.ntfs -f /dev/sdX1

# Format partition as FAT32
sudo mkfs.vfat -F 32 /dev/sdX1

# Format partition as exFAT
sudo mkfs.exfat /dev/sdX1
```

## Support

For issues with the GUI Installer:
- Check system logs: `journalctl -xe`
- Verify dependencies are installed
- Ensure running with proper privileges
- Review this documentation for common issues

For Heck-CheckOS-specific issues:
- Refer to main Heck-CheckOS documentation
- Check FAQ and troubleshooting guides
- Review installation logs

## License

This tool is part of the Heck-CheckOS Security Edition project.
Distributed under the same license as Heck-CheckOS.

## Credits

Heck-CheckOS GUI Installer - Automated USB creation and disk partitioning tool
Part of the Heck-CheckOS Security Edition ecosystem
