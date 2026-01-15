#!/usr/bin/env python3
"""
HeckOS Builder - Grub2 ISO & Bootable USB Creator
Creates bootable installation media with Grub2 support
Supports: Live USB, Installer ISO, Hybrid mode (try/install)
"""

import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Callable, Dict, List

class Grub2MediaBuilder:
    """Builds Grub2-compatible bootable media (ISO/USB)"""
    
    def __init__(self, source_dir: str, output_path: str, config: Dict):
        """
        Initialize Grub2 media builder
        
        Args:
            source_dir: Directory containing OS files
            output_path: Output path for ISO/USB image
            config: Configuration dictionary
        """
        self.source_dir = Path(source_dir)
        self.output_path = Path(output_path)
        self.config = config
        self.temp_dir = None
        
    def build_iso(self, progress_callback: Optional[Callable[[int, str], None]] = None) -> Path:
        """
        Build bootable ISO with Grub2
        
        Args:
            progress_callback: Optional callback for progress updates (percent, message)
            
        Returns:
            Path to created ISO file
        """
        self._report_progress(progress_callback, 0, "Initializing ISO build...")
        
        # Create temporary working directory
        self.temp_dir = tempfile.mkdtemp(prefix="heckos_iso_")
        temp_path = Path(self.temp_dir)
        
        try:
            # Step 1: Prepare ISO structure
            self._report_progress(progress_callback, 10, "Preparing ISO structure...")
            iso_root = temp_path / "iso"
            iso_root.mkdir(parents=True)
            
            # Step 2: Copy OS files
            self._report_progress(progress_callback, 20, "Copying OS files...")
            self._copy_os_files(iso_root)
            
            # Step 3: Create boot directory structure
            self._report_progress(progress_callback, 35, "Creating boot structure...")
            boot_dir = iso_root / "boot"
            grub_dir = boot_dir / "grub"
            grub_dir.mkdir(parents=True, exist_ok=True)
            
            # Step 4: Install Grub2 bootloader
            self._report_progress(progress_callback, 45, "Installing Grub2 bootloader...")
            self._install_grub2(iso_root, grub_dir)
            
            # Step 5: Create Grub2 configuration
            self._report_progress(progress_callback, 55, "Configuring Grub2 menu...")
            self._create_grub_config(grub_dir)
            
            # Step 6: Build ISO image
            self._report_progress(progress_callback, 70, "Building ISO image...")
            self._build_iso_image(iso_root)
            
            # Step 7: Make ISO hybrid (bootable as USB)
            self._report_progress(progress_callback, 85, "Creating hybrid ISO (USB-bootable)...")
            self._make_hybrid_iso()
            
            # Step 8: Verify ISO
            self._report_progress(progress_callback, 95, "Verifying ISO integrity...")
            self._verify_iso()
            
            self._report_progress(progress_callback, 100, "ISO build complete!")
            
            return self.output_path
            
        finally:
            # Cleanup temporary directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_bootable_usb(self, usb_device: str, progress_callback: Optional[Callable[[int, str], None]] = None) -> bool:
        """
        Create bootable USB drive
        
        Args:
            usb_device: USB device path (e.g., /dev/sdb)
            progress_callback: Optional callback for progress updates
            
        Returns:
            True if successful, False otherwise
        """
        self._report_progress(progress_callback, 0, "Initializing USB creation...")
        
        # Verify device exists
        if not os.path.exists(usb_device):
            raise FileNotFoundError(f"USB device not found: {usb_device}")
        
        # Warning - this will erase the USB drive
        print(f"WARNING: This will erase all data on {usb_device}")
        
        try:
            # Step 1: Unmount device
            self._report_progress(progress_callback, 10, "Unmounting USB device...")
            self._unmount_device(usb_device)
            
            # Step 2: Create partition table
            self._report_progress(progress_callback, 20, "Creating partition table...")
            self._create_usb_partitions(usb_device)
            
            # Step 3: Format partitions
            self._report_progress(progress_callback, 35, "Formatting partitions...")
            self._format_usb_partitions(usb_device)
            
            # Step 4: Mount USB
            self._report_progress(progress_callback, 45, "Mounting USB...")
            mount_point = self._mount_usb(usb_device)
            
            # Step 5: Copy OS files
            self._report_progress(progress_callback, 55, "Copying OS files to USB...")
            self._copy_os_files(Path(mount_point))
            
            # Step 6: Install Grub2 to USB
            self._report_progress(progress_callback, 75, "Installing Grub2 to USB...")
            self._install_grub2_usb(usb_device, mount_point)
            
            # Step 7: Create Grub2 config
            self._report_progress(progress_callback, 90, "Configuring Grub2...")
            grub_dir = Path(mount_point) / "boot" / "grub"
            self._create_grub_config(grub_dir)
            
            # Step 8: Sync and unmount
            self._report_progress(progress_callback, 95, "Finalizing USB...")
            subprocess.run(['sync'], check=True)
            self._unmount_device(usb_device)
            
            self._report_progress(progress_callback, 100, "Bootable USB created!")
            
            return True
            
        except Exception as e:
            print(f"Error creating bootable USB: {e}")
            return False
    
    def _copy_os_files(self, destination: Path):
        """Copy OS files to destination"""
        # Copy squashfs filesystem
        squashfs_src = self.source_dir / "filesystem.squashfs"
        if squashfs_src.exists():
            shutil.copy2(squashfs_src, destination / "filesystem.squashfs")
        
        # Copy kernel and initrd
        kernel_src = self.source_dir / "vmlinuz"
        initrd_src = self.source_dir / "initrd.img"
        
        boot_dest = destination / "boot"
        boot_dest.mkdir(exist_ok=True)
        
        if kernel_src.exists():
            shutil.copy2(kernel_src, boot_dest / "vmlinuz")
        
        if initrd_src.exists():
            shutil.copy2(initrd_src, boot_dest / "initrd.img")
        
        # Copy additional files
        for item in self.source_dir.iterdir():
            if item.is_file() and item.name not in ['filesystem.squashfs', 'vmlinuz', 'initrd.img']:
                shutil.copy2(item, destination / item.name)
    
    def _install_grub2(self, iso_root: Path, grub_dir: Path):
        """Install Grub2 bootloader files"""
        # Copy Grub2 modules for BIOS boot
        grub_bios_modules = [
            'biosdisk', 'part_msdos', 'part_gpt', 'fat', 'ext2', 'iso9660',
            'normal', 'linux', 'boot', 'multiboot', 'chain', 'configfile',
            'search', 'search_fs_uuid', 'search_fs_file', 'test', 'echo',
            'loadenv', 'ls', 'cat', 'help', 'video', 'all_video', 'gfxterm',
            'font', 'png', 'jpeg', 'gfxmenu'
        ]
        
        # Create core.img for BIOS boot
        grub_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy Grub2 i386-pc modules
        grub_i386_dir = grub_dir / "i386-pc"
        grub_i386_dir.mkdir(exist_ok=True)
        
        system_grub_dir = Path("/usr/lib/grub/i386-pc")
        if system_grub_dir.exists():
            for module_file in system_grub_dir.glob("*.mod"):
                shutil.copy2(module_file, grub_i386_dir / module_file.name)
            for module_file in system_grub_dir.glob("*.lst"):
                shutil.copy2(module_file, grub_i386_dir / module_file.name)
        
        # Copy Grub2 x86_64-efi modules for UEFI boot
        grub_efi_dir = grub_dir / "x86_64-efi"
        grub_efi_dir.mkdir(exist_ok=True)
        
        system_grub_efi_dir = Path("/usr/lib/grub/x86_64-efi")
        if system_grub_efi_dir.exists():
            for module_file in system_grub_efi_dir.glob("*.mod"):
                shutil.copy2(module_file, grub_efi_dir / module_file.name)
            for module_file in system_grub_efi_dir.glob("*.lst"):
                shutil.copy2(module_file, grub_efi_dir / module_file.name)
        
        # Create EFI boot directory
        efi_boot_dir = iso_root / "EFI" / "boot"
        efi_boot_dir.mkdir(parents=True, exist_ok=True)
        
        # Create EFI bootable image
        self._create_efi_image(efi_boot_dir, grub_efi_dir)
    
    def _create_efi_image(self, efi_boot_dir: Path, grub_efi_dir: Path):
        """Create EFI bootable image"""
        # Create minimal grub.cfg for EFI
        efi_grub_cfg = efi_boot_dir / "grub.cfg"
        efi_grub_cfg.write_text("""
search --set=root --file /boot/grub/grub.cfg
configfile /boot/grub/grub.cfg
""")
        
        # Generate EFI boot image
        try:
            subprocess.run([
                'grub-mkstandalone',
                '--format=x86_64-efi',
                '--output=' + str(efi_boot_dir / "bootx64.efi"),
                '--locales=""',
                '--fonts=""',
                'boot/grub/grub.cfg=' + str(efi_grub_cfg)
            ], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: Could not create EFI boot image. UEFI boot may not work.")
    
    def _create_grub_config(self, grub_dir: Path):
        """Create Grub2 configuration file"""
        grub_cfg_path = grub_dir / "grub.cfg"
        
        # Get configuration options
        os_name = self.config.get('os_name', 'HeckOS')
        os_version = self.config.get('os_version', '1.0')
        timeout = self.config.get('grub_timeout', 10)
        default_option = self.config.get('grub_default', 0)
        
        # Build Grub2 configuration
        grub_config = f'''# HeckOS Grub2 Configuration
# Generated by HeckOS Builder

set timeout={timeout}
set default={default_option}

# Set theme colors
set color_normal=white/black
set color_highlight=black/light-gray

# Menu title
menuentry "{os_name} {os_version} - Live Mode (Try without installing)" {{
    set gfxpayload=keep
    linux /boot/vmlinuz boot=live quiet splash
    initrd /boot/initrd.img
}}

menuentry "{os_name} {os_version} - Live Mode (Safe Graphics)" {{
    set gfxpayload=keep
    linux /boot/vmlinuz boot=live nomodeset quiet splash
    initrd /boot/initrd.img
}}

menuentry "{os_name} {os_version} - Install to Hard Drive" {{
    set gfxpayload=keep
    linux /boot/vmlinuz boot=live install quiet splash
    initrd /boot/initrd.img
}}

menuentry "{os_name} {os_version} - Install to Hard Drive (Text Mode)" {{
    set gfxpayload=text
    linux /boot/vmlinuz boot=live install text
    initrd /boot/initrd.img
}}

submenu "Advanced Options" {{
    menuentry "{os_name} - Recovery Mode" {{
        linux /boot/vmlinuz boot=live recovery
        initrd /boot/initrd.img
    }}
    
    menuentry "{os_name} - Memory Test (memtest86+)" {{
        linux16 /boot/memtest86+.bin
    }}
    
    menuentry "Boot from First Hard Drive" {{
        set root=(hd0)
        chainloader +1
    }}
}}

menuentry "Reboot" {{
    reboot
}}

menuentry "Shutdown" {{
    halt
}}
'''
        
        grub_cfg_path.write_text(grub_config)
    
    def _build_iso_image(self, iso_root: Path):
        """Build ISO image using xorriso/genisoimage"""
        iso_label = self.config.get('iso_label', 'HECKOS')
        
        # Use xorriso for hybrid BIOS/UEFI ISO
        cmd = [
            'xorriso',
            '-as', 'mkisofs',
            '-r',  # Rock Ridge extensions
            '-V', iso_label,
            '-o', str(self.output_path),
            '-J',  # Joliet extensions
            '-joliet-long',
            '-cache-inodes',
            '-b', 'boot/grub/i386-pc/eltorito.img',  # BIOS boot
            '-c', 'boot/grub/boot.cat',
            '-no-emul-boot',
            '-boot-load-size', '4',
            '-boot-info-table',
            '--grub2-boot-info',
            '--grub2-mbr', '/usr/lib/grub/i386-pc/boot_hybrid.img',
            '-eltorito-alt-boot',  # EFI boot
            '-e', 'EFI/boot/efiboot.img',
            '-no-emul-boot',
            '-append_partition', '2', '0xef', str(iso_root / 'EFI' / 'boot' / 'efiboot.img'),
            str(iso_root)
        ]
        
        # Create EFI boot image first
        self._create_efi_boot_image(iso_root)
        
        # Create El Torito boot image for BIOS
        self._create_eltorito_image(iso_root)
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            # Fallback to genisoimage if xorriso fails
            print("xorriso failed, trying genisoimage...")
            self._build_iso_with_genisoimage(iso_root, iso_label)
    
    def _create_efi_boot_image(self, iso_root: Path):
        """Create EFI boot image"""
        efi_img_path = iso_root / "EFI" / "boot" / "efiboot.img"
        efi_img_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create FAT filesystem image (10MB)
        try:
            subprocess.run([
                'dd',
                'if=/dev/zero',
                f'of={efi_img_path}',
                'bs=1M',
                'count=10'
            ], check=True, capture_output=True)
            
            subprocess.run([
                'mkfs.vfat',
                '-n', 'HECKOS_EFI',
                str(efi_img_path)
            ], check=True, capture_output=True)
            
            # Mount and copy EFI files
            mount_point = Path(tempfile.mkdtemp())
            subprocess.run(['mount', '-o', 'loop', str(efi_img_path), str(mount_point)], check=True)
            
            try:
                efi_dest = mount_point / "EFI" / "boot"
                efi_dest.mkdir(parents=True, exist_ok=True)
                
                efi_src = iso_root / "EFI" / "boot" / "bootx64.efi"
                if efi_src.exists():
                    shutil.copy2(efi_src, efi_dest / "bootx64.efi")
                
            finally:
                subprocess.run(['umount', str(mount_point)], check=True)
                mount_point.rmdir()
                
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Warning: Could not create EFI boot image: {e}")
    
    def _create_eltorito_image(self, iso_root: Path):
        """Create El Torito boot image for BIOS"""
        eltorito_path = iso_root / "boot" / "grub" / "i386-pc" / "eltorito.img"
        eltorito_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy from system Grub2
        system_eltorito = Path("/usr/lib/grub/i386-pc/cdboot.img")
        if system_eltorito.exists():
            shutil.copy2(system_eltorito, eltorito_path)
        else:
            print("Warning: El Torito boot image not found")
    
    def _build_iso_with_genisoimage(self, iso_root: Path, iso_label: str):
        """Fallback ISO building with genisoimage"""
        cmd = [
            'genisoimage',
            '-r',
            '-V', iso_label,
            '-o', str(self.output_path),
            '-b', 'boot/grub/i386-pc/eltorito.img',
            '-c', 'boot/grub/boot.cat',
            '-no-emul-boot',
            '-boot-load-size', '4',
            '-boot-info-table',
            str(iso_root)
        ]
        
        subprocess.run(cmd, check=True)
    
    def _make_hybrid_iso(self):
        """Make ISO hybrid (bootable as USB with dd)"""
        try:
            subprocess.run([
                'isohybrid',
                '--uefi',
                str(self.output_path)
            ], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: Could not make ISO hybrid. USB boot may not work.")
    
    def _verify_iso(self):
        """Verify ISO integrity"""
        if not self.output_path.exists():
            raise FileNotFoundError(f"ISO not created: {self.output_path}")
        
        # Check ISO size
        size_mb = self.output_path.stat().st_size / (1024 * 1024)
        print(f"ISO created: {self.output_path} ({size_mb:.1f} MB)")
    
    def _unmount_device(self, device: str):
        """Unmount all partitions on device"""
        try:
            result = subprocess.run(
                ['mount'],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.split('\n'):
                if device in line:
                    mount_point = line.split()[2]
                    subprocess.run(['umount', mount_point], check=True)
        except subprocess.CalledProcessError:
            pass
    
    def _create_usb_partitions(self, device: str):
        """Create partition table on USB device"""
        # Use parted to create GPT partition table
        subprocess.run([
            'parted', '-s', device,
            'mklabel', 'gpt'
        ], check=True)
        
        # Create EFI partition (100MB)
        subprocess.run([
            'parted', '-s', device,
            'mkpart', 'EFI', 'fat32', '1MiB', '101MiB'
        ], check=True)
        
        subprocess.run([
            'parted', '-s', device,
            'set', '1', 'esp', 'on'
        ], check=True)
        
        # Create main partition (rest of space)
        subprocess.run([
            'parted', '-s', device,
            'mkpart', 'primary', 'ext4', '101MiB', '100%'
        ], check=True)
    
    def _format_usb_partitions(self, device: str):
        """Format USB partitions"""
        # Format EFI partition
        subprocess.run([
            'mkfs.vfat',
            '-F', '32',
            '-n', 'HECKOS_EFI',
            f'{device}1'
        ], check=True)
        
        # Format main partition
        subprocess.run([
            'mkfs.ext4',
            '-L', 'HECKOS',
            f'{device}2'
        ], check=True)
    
    def _mount_usb(self, device: str) -> str:
        """Mount USB main partition"""
        mount_point = tempfile.mkdtemp(prefix="heckos_usb_")
        subprocess.run([
            'mount',
            f'{device}2',
            mount_point
        ], check=True)
        
        return mount_point
    
    def _install_grub2_usb(self, device: str, mount_point: str):
        """Install Grub2 to USB device"""
        # Install Grub2 for BIOS
        subprocess.run([
            'grub-install',
            '--target=i386-pc',
            '--boot-directory=' + os.path.join(mount_point, 'boot'),
            device
        ], check=True)
        
        # Install Grub2 for UEFI
        efi_mount = tempfile.mkdtemp(prefix="heckos_efi_")
        try:
            subprocess.run([
                'mount',
                f'{device}1',
                efi_mount
            ], check=True)
            
            subprocess.run([
                'grub-install',
                '--target=x86_64-efi',
                '--efi-directory=' + efi_mount,
                '--boot-directory=' + os.path.join(mount_point, 'boot'),
                '--removable'
            ], check=True)
            
        finally:
            subprocess.run(['umount', efi_mount], check=True)
            os.rmdir(efi_mount)
    
    def _report_progress(self, callback: Optional[Callable], percent: int, message: str):
        """Report progress to callback if provided"""
        if callback:
            callback(percent, message)
        else:
            print(f"[{percent:3d}%] {message}")


# Example usage
if __name__ == '__main__':
    config = {
        'os_name': 'HeckOS',
        'os_version': '1.0',
        'iso_label': 'HECKOS',
        'grub_timeout': 10,
        'grub_default': 0
    }
    
    builder = Grub2MediaBuilder(
        source_dir='/path/to/os/files',
        output_path='/path/to/output.iso',
        config=config
    )
    
    # Build ISO
    iso_path = builder.build_iso()
    print(f"ISO created: {iso_path}")
