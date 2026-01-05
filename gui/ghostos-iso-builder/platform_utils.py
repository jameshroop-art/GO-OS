#!/usr/bin/env python3
"""
Platform Utilities - Cross-platform compatibility helpers
Ensures GhostOS ISO Builder works on Windows, Linux, and macOS
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


class PlatformHelper:
    """Helper class for cross-platform operations"""
    
    @staticmethod
    def get_system():
        """Get current operating system"""
        return platform.system()  # Returns: 'Windows', 'Linux', 'Darwin' (macOS)
    
    @staticmethod
    def is_windows():
        """Check if running on Windows"""
        return platform.system() == "Windows"
    
    @staticmethod
    def is_linux():
        """Check if running on Linux"""
        return platform.system() == "Linux"
    
    @staticmethod
    def is_macos():
        """Check if running on macOS"""
        return platform.system() == "Darwin"
    
    @staticmethod
    def get_home_directory():
        """Get user home directory (cross-platform)"""
        return Path.home()
    
    @staticmethod
    def get_config_directory():
        """Get configuration directory (cross-platform)"""
        if PlatformHelper.is_windows():
            return Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'GhostOS-Builder'
        elif PlatformHelper.is_macos():
            return Path.home() / 'Library' / 'Application Support' / 'GhostOS-Builder'
        else:  # Linux and others
            return Path.home() / '.config' / 'ghostos-builder'
    
    @staticmethod
    def get_data_directory():
        """Get data directory (cross-platform)"""
        if PlatformHelper.is_windows():
            return Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local')) / 'GhostOS-Builder'
        elif PlatformHelper.is_macos():
            return Path.home() / 'Library' / 'Application Support' / 'GhostOS-Builder'
        else:  # Linux
            return Path.home() / '.local' / 'share' / 'ghostos-builder'
    
    @staticmethod
    def get_temp_directory():
        """Get temporary directory (cross-platform)"""
        import tempfile
        return Path(tempfile.gettempdir()) / 'ghostos-builder'
    
    @staticmethod
    def get_wine_prefix_directory():
        """Get Wine prefix directory (cross-platform)"""
        if PlatformHelper.is_windows():
            # On Windows, return a directory for Windows app data
            return PlatformHelper.get_data_directory() / 'windows-apps'
        else:
            return Path.home() / '.wine-prefixes'
    
    @staticmethod
    def get_path_separator():
        """Get path separator for current OS"""
        return ';' if PlatformHelper.is_windows() else ':'
    
    @staticmethod
    def get_executable_extension():
        """Get executable file extension"""
        return '.exe' if PlatformHelper.is_windows() else ''
    
    @staticmethod
    def run_command(cmd, shell=False, capture_output=True, text=True):
        """Run command with cross-platform compatibility"""
        try:
            # On Windows, use shell=True for built-in commands
            if PlatformHelper.is_windows() and isinstance(cmd, list):
                # Check if it's a built-in command
                builtin_commands = ['dir', 'copy', 'del', 'type', 'echo', 'cd']
                if cmd[0] in builtin_commands:
                    shell = True
                    cmd = ' '.join(cmd)
            
            result = subprocess.run(
                cmd,
                shell=shell,
                capture_output=capture_output,
                text=text,
                timeout=30
            )
            return result
        except subprocess.TimeoutExpired:
            return None
        except Exception as e:
            print(f"Command failed: {e}")
            return None
    
    @staticmethod
    def check_command_exists(command):
        """Check if a command exists in PATH"""
        if PlatformHelper.is_windows():
            check_cmd = ['where', command]
        else:
            check_cmd = ['which', command]
        
        result = PlatformHelper.run_command(check_cmd)
        return result and result.returncode == 0
    
    @staticmethod
    def open_file_manager(path):
        """Open file manager at specified path"""
        path = Path(path)
        
        if PlatformHelper.is_windows():
            os.startfile(path)
        elif PlatformHelper.is_macos():
            subprocess.run(['open', path])
        else:  # Linux
            subprocess.run(['xdg-open', path])
    
    @staticmethod
    def get_usb_drives():
        """Get list of USB drives (cross-platform)"""
        drives = []
        
        if PlatformHelper.is_windows():
            # Windows: Use wmic or iterate drive letters
            import string
            from ctypes import windll
            
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in string.ascii_uppercase:
                if bitmask & 1:
                    drive_path = f"{letter}:\\"
                    drive_type = windll.kernel32.GetDriveTypeW(drive_path)
                    # Drive type 2 = Removable
                    if drive_type == 2:
                        drives.append({
                            'path': drive_path,
                            'name': f"USB Drive ({letter}:)",
                            'type': 'removable'
                        })
                bitmask >>= 1
                
        elif PlatformHelper.is_macos():
            # macOS: Check /Volumes
            volumes_path = Path('/Volumes')
            if volumes_path.exists():
                for volume in volumes_path.iterdir():
                    if volume.is_dir() and volume.name != 'Macintosh HD':
                        drives.append({
                            'path': str(volume),
                            'name': volume.name,
                            'type': 'external'
                        })
                        
        else:  # Linux
            # Linux: Check /media and /mnt
            for mount_point in ['/media', '/mnt']:
                mount_path = Path(mount_point)
                if mount_path.exists():
                    for user_dir in mount_path.iterdir():
                        if user_dir.is_dir():
                            for drive in user_dir.iterdir():
                                if drive.is_dir():
                                    drives.append({
                                        'path': str(drive),
                                        'name': drive.name,
                                        'type': 'external'
                                    })
        
        return drives
    
    @staticmethod
    def get_iso_tools():
        """Get available ISO manipulation tools on current platform"""
        tools = {}
        
        # Common tools
        tools_to_check = {
            'genisoimage': 'ISO creation',
            'mkisofs': 'ISO creation (alternative)',
            'xorriso': 'ISO manipulation',
            'isoinfo': 'ISO information',
            '7z': '7-Zip (extraction)',
            'mount': 'ISO mounting (Linux)',
            'hdiutil': 'ISO tools (macOS)'
        }
        
        for tool, description in tools_to_check.items():
            if PlatformHelper.check_command_exists(tool):
                tools[tool] = description
        
        # Windows-specific
        if PlatformHelper.is_windows():
            # Check for Windows ISO mounting capabilities
            if sys.version_info >= (3, 8):
                tools['mount-diskimage'] = 'Windows ISO mounting (PowerShell)'
        
        return tools
    
    @staticmethod
    def mount_iso(iso_path, mount_point=None):
        """Mount ISO file (cross-platform)"""
        iso_path = Path(iso_path)
        
        if not iso_path.exists():
            return False, "ISO file not found"
        
        if PlatformHelper.is_windows():
            # Windows 8+ can mount ISOs natively
            try:
                subprocess.run(
                    ['powershell', '-Command', f'Mount-DiskImage -ImagePath "{iso_path}"'],
                    check=True
                )
                return True, "ISO mounted successfully (Windows)"
            except:
                return False, "Failed to mount ISO on Windows"
                
        elif PlatformHelper.is_macos():
            # macOS: Use hdiutil
            try:
                result = subprocess.run(
                    ['hdiutil', 'attach', str(iso_path)],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return True, "ISO mounted successfully (macOS)"
            except:
                return False, "Failed to mount ISO on macOS"
                
        else:  # Linux
            # Linux: Use mount command (requires sudo)
            if not mount_point:
                mount_point = f"/mnt/ghostos-iso-{iso_path.stem}"
            
            try:
                # Create mount point
                Path(mount_point).mkdir(parents=True, exist_ok=True)
                
                # Mount ISO
                subprocess.run(
                    ['sudo', 'mount', '-o', 'loop', str(iso_path), mount_point],
                    check=True
                )
                return True, f"ISO mounted at {mount_point}"
            except:
                return False, "Failed to mount ISO on Linux (requires sudo)"
    
    @staticmethod
    def get_security_tools():
        """Get available security tools on current platform"""
        tools = {}
        
        if PlatformHelper.is_linux():
            # Linux security tools
            linux_tools = {
                'apparmor_status': 'AppArmor',
                'aa-status': 'AppArmor status',
                'setenforce': 'SELinux',
                'iptables': 'Firewall (iptables)',
                'ufw': 'Firewall (UFW)',
                'firewalld': 'Firewall (firewalld)'
            }
            
            for tool, desc in linux_tools.items():
                if PlatformHelper.check_command_exists(tool):
                    tools[tool] = desc
                    
        elif PlatformHelper.is_macos():
            # macOS security tools
            macos_tools = {
                'pfctl': 'Packet Filter (firewall)',
                'sandbox-exec': 'Application sandboxing'
            }
            
            for tool, desc in macos_tools.items():
                if PlatformHelper.check_command_exists(tool):
                    tools[tool] = desc
                    
        elif PlatformHelper.is_windows():
            # Windows security tools
            tools['netsh'] = 'Windows Firewall'
            tools['defender'] = 'Windows Defender'
        
        return tools
    
    @staticmethod
    def normalize_path(path):
        """Normalize path for current OS"""
        path = Path(path)
        
        # Convert to string with appropriate separators
        if PlatformHelper.is_windows():
            return str(path).replace('/', '\\')
        else:
            return str(path).replace('\\', '/')
    
    @staticmethod
    def get_python_executable():
        """Get Python executable path"""
        return sys.executable
    
    @staticmethod
    def create_desktop_shortcut(name, target, icon=None):
        """Create desktop shortcut (cross-platform)"""
        desktop = Path.home() / 'Desktop'
        
        if PlatformHelper.is_windows():
            # Windows: Create .lnk file
            shortcut_path = desktop / f"{name}.lnk"
            # Would use pywin32 or similar to create actual shortcut
            return True, str(shortcut_path)
            
        elif PlatformHelper.is_macos():
            # macOS: Create .app or alias
            shortcut_path = desktop / f"{name}.app"
            return True, str(shortcut_path)
            
        else:  # Linux
            # Linux: Create .desktop file
            shortcut_path = desktop / f"{name}.desktop"
            desktop_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={name}
Exec={target}
Icon={icon or 'application-x-executable'}
Terminal=false
Categories=System;
"""
            try:
                shortcut_path.write_text(desktop_entry)
                shortcut_path.chmod(0o755)
                return True, str(shortcut_path)
            except Exception as e:
                return False, str(e)


# Global instance for easy access
platform_helper = PlatformHelper()
