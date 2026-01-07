#!/usr/bin/env python3
"""
GhostOS ISO Builder Backend
Actual ISO creation with pre-applied configurations
"""

import os
import sys
import shutil
import subprocess
import tempfile
import json
from pathlib import Path
from datetime import datetime


class ISOBuilder:
    """Builds custom GhostOS ISO with pre-applied configurations"""
    
    def __init__(self, config: dict, output_dir: str = None):
        """
        Initialize ISO builder
        
        Args:
            config: Build configuration dictionary
            output_dir: Output directory for ISO (default: ~/ghostos-ultimate)
        """
        self.config = config
        self.output_dir = Path(output_dir or Path.home() / "ghostos-ultimate")
        self.work_dir = None
        self.iso_dir = None
        self.rootfs_dir = None
        
    def check_dependencies(self):
        """Check if required tools are installed"""
        required_tools = [
            'debootstrap',
            'mksquashfs',
            'xorriso',
            'grub-mkstandalone',
            'isohybrid',
            'chroot'
        ]
        
        missing = []
        for tool in required_tools:
            if shutil.which(tool) is None:
                missing.append(tool)
        
        if missing:
            raise RuntimeError(
                f"Missing required tools: {', '.join(missing)}\n"
                f"Install with: sudo apt-get install squashfs-tools xorriso "
                f"grub-pc-bin grub-efi-amd64-bin syslinux syslinux-utils "
                f"debootstrap isolinux"
            )
    
    def create_work_dirs(self):
        """Create working directories"""
        self.work_dir = Path(tempfile.mkdtemp(prefix="ghostos-build-"))
        self.iso_dir = self.work_dir / "iso"
        self.rootfs_dir = self.work_dir / "rootfs"
        
        # Create directory structure
        (self.iso_dir / "boot" / "grub").mkdir(parents=True)
        (self.iso_dir / "EFI" / "BOOT").mkdir(parents=True)
        (self.iso_dir / "live").mkdir(parents=True)
        self.rootfs_dir.mkdir(parents=True)
        
        print(f"✓ Working directory: {self.work_dir}")
    
    def bootstrap_base_system(self, progress_callback=None):
        """Bootstrap Debian 12 base system"""
        if progress_callback:
            progress_callback(10, "Bootstrapping Debian 12 (Bookworm)...")
        
        print("[*] Bootstrapping Debian 12 (Bookworm) base system...")
        
        cmd = [
            'debootstrap',
            '--arch=amd64',
            '--include=wget,curl,ca-certificates,gnupg,sudo,systemd,network-manager',
            'bookworm',
            str(self.rootfs_dir),
            'http://deb.debian.org/debian'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Debootstrap failed: {result.stderr}")
        
        print("✓ Base system bootstrapped")
    
    def configure_repositories(self):
        """Configure Debian repositories"""
        print("[*] Configuring Debian 12 repositories...")
        
        sources_list = self.rootfs_dir / "etc" / "apt" / "sources.list"
        sources_list.write_text("""# Debian 12 (Bookworm) - Stable Release Base
deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
deb http://deb.debian.org/debian bookworm-updates main contrib non-free non-free-firmware
deb http://deb.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
deb http://deb.debian.org/debian bookworm-backports main contrib non-free non-free-firmware
""")
        
        print("✓ Repositories configured")
    
    def apply_theme(self, theme_config: dict, progress_callback=None):
        """Apply theme configuration to the system"""
        if progress_callback:
            progress_callback(30, "Applying theme customizations...")
        
        print(f"[*] Applying theme: {theme_config.get('mode', 'default')}")
        
        # Create theme directory
        theme_dir = self.rootfs_dir / "usr" / "share" / "ghostos" / "themes"
        theme_dir.mkdir(parents=True, exist_ok=True)
        
        # Write theme configuration
        theme_file = theme_dir / "current.json"
        theme_file.write_text(json.dumps(theme_config, indent=2))
        
        # Apply theme mode
        mode = theme_config.get('mode', 'default')
        if mode == 'dark':
            # Set dark theme as default
            gtk_settings = self.rootfs_dir / "etc" / "gtk-3.0" / "settings.ini"
            gtk_settings.parent.mkdir(parents=True, exist_ok=True)
            gtk_settings.write_text("""[Settings]
gtk-application-prefer-dark-theme=1
gtk-theme-name=Adwaita-dark
gtk-icon-theme-name=Adwaita
""")
        elif mode == 'gaming':
            # Gaming-optimized theme
            gtk_settings = self.rootfs_dir / "etc" / "gtk-3.0" / "settings.ini"
            gtk_settings.parent.mkdir(parents=True, exist_ok=True)
            gtk_settings.write_text("""[Settings]
gtk-theme-name=Adwaita-dark
gtk-icon-theme-name=Adwaita
gtk-enable-animations=0
""")
        
        print("✓ Theme applied")
    
    def install_custom_packages(self, packages: list, progress_callback=None):
        """Install custom packages in the chroot"""
        if not packages:
            return
        
        if progress_callback:
            progress_callback(40, f"Installing {len(packages)} custom packages...")
        
        print(f"[*] Installing custom packages: {', '.join(packages[:5])}...")
        
        # Update package cache
        self._run_in_chroot(['apt-get', 'update'])
        
        # Install packages
        self._run_in_chroot(['apt-get', 'install', '-y'] + packages)
        
        print("✓ Custom packages installed")
    
    def add_custom_files(self, custom_files: list, progress_callback=None):
        """Add custom files to the system"""
        if not custom_files:
            return
        
        if progress_callback:
            progress_callback(50, f"Adding {len(custom_files)} custom files...")
        
        print(f"[*] Adding {len(custom_files)} custom files...")
        
        custom_dir = self.rootfs_dir / "opt" / "custom"
        custom_dir.mkdir(parents=True, exist_ok=True)
        
        for file_info in custom_files:
            src = Path(file_info['path'])
            if src.exists():
                dest = custom_dir / src.name
                shutil.copy2(src, dest)
                print(f"  + {src.name}")
        
        print("✓ Custom files added")
    
    def install_ghostos_builder(self, self_install_config: dict, progress_callback=None):
        """Install GhostOS Builder to the ISO"""
        if not self_install_config.get('enabled', False):
            return
        
        if progress_callback:
            progress_callback(60, "Installing GhostOS Builder...")
        
        print("[*] Installing GhostOS Builder to ISO...")
        
        # Copy builder files
        builder_dir = self.rootfs_dir / "opt" / "ghostos-builder"
        builder_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy GUI builder files
        gui_src = Path(__file__).parent
        shutil.copytree(gui_src, builder_dir / "gui", dirs_exist_ok=True)
        
        # Create desktop entry
        if self_install_config.get('desktop_entry', True):
            desktop_file = self.rootfs_dir / "usr" / "share" / "applications" / "ghostos-builder.desktop"
            desktop_file.parent.mkdir(parents=True, exist_ok=True)
            desktop_file.write_text("""[Desktop Entry]
Type=Application
Name=GhostOS Builder
Comment=Build and customize GhostOS ISOs
Exec=/opt/ghostos-builder/gui/start-gui.sh
Icon=applications-system
Terminal=false
Categories=System;Settings;
""")
        
        # Create CLI launcher
        if self_install_config.get('cli_launcher', True):
            launcher = self.rootfs_dir / "usr" / "local" / "bin" / "ghostos-builder"
            launcher.parent.mkdir(parents=True, exist_ok=True)
            launcher.write_text("""#!/bin/bash
cd /opt/ghostos-builder/gui
python3 main.py "$@"
""")
            launcher.chmod(0o755)
        
        print("✓ GhostOS Builder installed")
    
    def create_grub_config(self, version: str):
        """Create GRUB bootloader configuration"""
        print("[*] Creating GRUB configuration...")
        
        grub_cfg = self.iso_dir / "boot" / "grub" / "grub.cfg"
        grub_cfg.write_text(f"""set timeout=30
set default=0

insmod all_video
insmod gfxterm
terminal_output gfxterm
set gfxmode=1920x1080
set gfxpayload=keep

menuentry "👻 GhostOS {version} - Install (Pre-configured)" {{
    linux /live/vmlinuz boot=live quiet splash installer-mode
    initrd /live/initrd.img
}}

menuentry "👻 GhostOS {version} - Live Mode (Pre-configured)" {{
    linux /live/vmlinuz boot=live quiet splash
    initrd /live/initrd.img
}}

menuentry "👻 GhostOS {version} - Safe Mode" {{
    linux /live/vmlinuz boot=live nomodeset
    initrd /live/initrd.img
}}
""")
        
        print("✓ GRUB configuration created")
    
    def create_squashfs(self, progress_callback=None):
        """Create squashfs filesystem"""
        if progress_callback:
            progress_callback(70, "Creating compressed filesystem...")
        
        print("[*] Creating squashfs filesystem...")
        
        # Copy kernel and initrd
        kernel = list((self.rootfs_dir / "boot").glob("vmlinuz-*"))
        initrd = list((self.rootfs_dir / "boot").glob("initrd.img-*"))
        
        if kernel:
            shutil.copy2(kernel[0], self.iso_dir / "live" / "vmlinuz")
        if initrd:
            shutil.copy2(initrd[0], self.iso_dir / "live" / "initrd.img")
        
        # Create squashfs
        squashfs_file = self.iso_dir / "live" / "filesystem.squashfs"
        cmd = [
            'mksquashfs',
            str(self.rootfs_dir),
            str(squashfs_file),
            '-comp', 'xz',
            '-b', '1M',
            '-Xbcj', 'x86',
            '-e', 'boot'
        ]
        
        subprocess.run(cmd, check=True)
        print("✓ Squashfs created")
    
    def create_bootloader(self):
        """Create GRUB bootloader for BIOS and UEFI"""
        print("[*] Creating bootloader...")
        
        grub_cfg = self.iso_dir / "boot" / "grub" / "grub.cfg"
        
        # EFI bootloader
        subprocess.run([
            'grub-mkstandalone',
            '--format=x86_64-efi',
            f'--output={self.iso_dir}/EFI/BOOT/BOOTX64.EFI',
            '--locales=',
            '--fonts=',
            f'boot/grub/grub.cfg={grub_cfg}'
        ], check=True)
        
        # BIOS bootloader
        core_img = self.iso_dir / "boot" / "grub" / "core.img"
        subprocess.run([
            'grub-mkstandalone',
            '--format=i386-pc',
            f'--output={core_img}',
            '--locales=',
            '--fonts=',
            f'boot/grub/grub.cfg={grub_cfg}'
        ], check=True)
        
        # Create BIOS boot image
        cdboot = Path("/usr/lib/grub/i386-pc/cdboot.img")
        bios_img = self.iso_dir / "boot" / "grub" / "bios.img"
        
        with open(bios_img, 'wb') as out:
            with open(cdboot, 'rb') as f1:
                out.write(f1.read())
            with open(core_img, 'rb') as f2:
                out.write(f2.read())
        
        print("✓ Bootloader created")
    
    def build_iso(self, output_filename: str, progress_callback=None):
        """Build the final ISO file"""
        if progress_callback:
            progress_callback(90, "Building ISO image...")
        
        print("[*] Building ISO image...")
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / output_filename
        
        # Build ISO
        cmd = [
            'xorriso', '-as', 'mkisofs',
            '-iso-level', '3',
            '-full-iso9660-filenames',
            '-volid', 'GHOSTOS-CUSTOM',
            '-appid', 'GhostOS Custom Build',
            '-publisher', 'jameshroop-art',
            '-eltorito-boot', 'boot/grub/bios.img',
            '-no-emul-boot',
            '-boot-load-size', '4',
            '-boot-info-table',
            '--grub2-boot-info',
            '--grub2-mbr', '/usr/lib/grub/i386-pc/boot_hybrid.img',
            '-eltorito-alt-boot',
            '-e', 'EFI/BOOT/BOOTX64.EFI',
            '-no-emul-boot',
            '-isohybrid-gpt-basdat',
            '-output', str(output_path),
            str(self.iso_dir)
        ]
        
        subprocess.run(cmd, check=True)
        
        # Make hybrid ISO
        subprocess.run(['isohybrid', '--uefi', str(output_path)], check=True)
        
        # Create checksums
        subprocess.run(['md5sum', output_filename], 
                      cwd=self.output_dir,
                      stdout=open(output_path.with_suffix('.iso.md5'), 'w'))
        
        subprocess.run(['sha256sum', output_filename],
                      cwd=self.output_dir,
                      stdout=open(output_path.with_suffix('.iso.sha256'), 'w'))
        
        print(f"✓ ISO created: {output_path}")
        return output_path
    
    def cleanup(self):
        """Clean up temporary files"""
        if self.work_dir and self.work_dir.exists():
            print("[*] Cleaning up temporary files...")
            shutil.rmtree(self.work_dir)
    
    def _run_in_chroot(self, cmd: list):
        """Run command in chroot environment"""
        # Mount required filesystems
        for mount in ['dev', 'dev/pts', 'proc', 'sys']:
            target = self.rootfs_dir / mount
            if not target.exists():
                target.mkdir(parents=True, exist_ok=True)
            subprocess.run(['mount', '--bind', f'/{mount}', str(target)], check=False)
        
        try:
            # Run command in chroot
            subprocess.run(['chroot', str(self.rootfs_dir)] + cmd, check=True)
        finally:
            # Unmount
            for mount in ['sys', 'proc', 'dev/pts', 'dev']:
                subprocess.run(['umount', str(self.rootfs_dir / mount)], check=False)
    
    def build(self, progress_callback=None):
        """Execute full build process"""
        try:
            # Check dependencies
            self.check_dependencies()
            
            # Create working directories
            self.create_work_dirs()
            
            # Bootstrap base system
            self.bootstrap_base_system(progress_callback)
            
            # Configure repositories
            self.configure_repositories()
            
            # Apply theme
            if 'theme' in self.config:
                self.apply_theme(self.config['theme'], progress_callback)
            
            # Install custom packages
            if 'packages' in self.config:
                self.install_custom_packages(self.config['packages'], progress_callback)
            
            # Add custom files
            if 'custom_files' in self.config:
                self.add_custom_files(self.config['custom_files'], progress_callback)
            
            # Install GhostOS Builder if enabled
            if 'self_install' in self.config:
                self.install_ghostos_builder(self.config['self_install'], progress_callback)
            
            # Create GRUB config
            version = self.config.get('version', 'custom')
            self.create_grub_config(version)
            
            # Create squashfs
            self.create_squashfs(progress_callback)
            
            # Create bootloader
            self.create_bootloader()
            
            # Build ISO
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"GhostOS-custom-{timestamp}.iso"
            output_path = self.build_iso(filename, progress_callback)
            
            if progress_callback:
                progress_callback(100, "Build complete!")
            
            return output_path
            
        finally:
            # Always cleanup
            self.cleanup()


if __name__ == "__main__":
    # Test build
    config = {
        'version': 'test',
        'theme': {'mode': 'dark'},
        'packages': [],
        'custom_files': [],
        'self_install': {'enabled': False}
    }
    
    builder = ISOBuilder(config)
    try:
        output = builder.build()
        print(f"\n✓ Build successful: {output}")
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)
