#!/usr/bin/env python3
"""
Installation script for GhostOS Windows Driver Emulator
"""

import os
import sys
import shutil
import subprocess

def main():
    """Install the Windows Driver Emulator"""
    
    if os.geteuid() != 0:
        print("Error: Installation must be run as root")
        print("Run: sudo python3 install.py")
        sys.exit(1)
    
    print("=" * 60)
    print("GhostOS Windows Driver Emulator Installation")
    print("=" * 60)
    print()
    
    # Create directories
    print("[1/6] Creating directories...")
    dirs = [
        '/opt/ghostos/windows_driver_emulator',
        '/opt/ghostos/drivers',
        '/etc/ghostos',
        '/var/log/ghostos'
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"  Created: {directory}")
    
    # Copy emulator files
    print("\n[2/6] Installing emulator files...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    files_to_copy = [
        'emulator.py',
        'README.md',
        'driver-emulator.conf'
    ]
    
    for filename in files_to_copy:
        src = os.path.join(current_dir, filename)
        dst = os.path.join('/opt/ghostos/windows_driver_emulator', filename)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  Installed: {filename}")
    
    # Copy device handlers
    print("\n[3/6] Installing device handlers...")
    device_handlers_src = os.path.join(current_dir, 'device_handlers')
    device_handlers_dst = '/opt/ghostos/windows_driver_emulator/device_handlers'
    
    if os.path.exists(device_handlers_src):
        if os.path.exists(device_handlers_dst):
            shutil.rmtree(device_handlers_dst)
        shutil.copytree(device_handlers_src, device_handlers_dst)
        print("  Installed device handlers")
    
    # Install CLI utilities
    print("\n[4/6] Installing CLI utilities...")
    cli_tools = [
        'ghostos-driver-load',
        'ghostos-driver-list',
        'ghostos-driver-unload',
        'ghostos-driver-check'
    ]
    
    for tool in cli_tools:
        src = os.path.join(current_dir, tool)
        dst = os.path.join('/usr/local/bin', tool)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            os.chmod(dst, 0o755)
            print(f"  Installed: {tool}")
    
    # Install configuration
    print("\n[5/6] Installing configuration...")
    config_src = os.path.join(current_dir, 'driver-emulator.conf')
    config_dst = '/etc/ghostos/driver-emulator.conf'
    
    if os.path.exists(config_src):
        if not os.path.exists(config_dst):
            shutil.copy2(config_src, config_dst)
            print(f"  Installed: {config_dst}")
        else:
            print(f"  Configuration already exists: {config_dst}")
    
    # Set permissions
    print("\n[6/6] Setting permissions...")
    os.chmod('/opt/ghostos/windows_driver_emulator/emulator.py', 0o755)
    print("  Permissions set")
    
    print()
    print("=" * 60)
    print("Installation complete!")
    print("=" * 60)
    print()
    print("Usage:")
    print("  ghostos-driver-load <driver_path>   - Load a driver")
    print("  ghostos-driver-list                 - List loaded drivers")
    print("  ghostos-driver-unload <driver>      - Unload a driver")
    print("  ghostos-driver-check <driver_path>  - Check compatibility")
    print()
    print("Configuration: /etc/ghostos/driver-emulator.conf")
    print("Logs: /var/log/ghostos/driver-emulator.log")
    print()

if __name__ == '__main__':
    main()
