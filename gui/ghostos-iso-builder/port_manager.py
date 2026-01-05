#!/usr/bin/env python3
"""
GhostOS Port Manager
Detects used ports on Parrot OS and allocates free ports for Windows integration
"""

import socket
import subprocess
import json
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class PortManager:
    """Manages port allocation to avoid conflicts"""
    
    # Common Parrot OS / Linux services and their default ports
    KNOWN_SERVICES = {
        'ssh': [22],
        'http': [80, 8080],
        'https': [443, 8443],
        'vnc': [5900, 5901, 5902, 5903],
        'mysql': [3306],
        'postgresql': [5432],
        'redis': [6379],
        'mongodb': [27017],
        'apache': [80, 443],
        'nginx': [80, 443],
        'docker': [2375, 2376],
        'kubernetes': [6443, 8080, 10250, 10251, 10252],
        'x11': [6000, 6001, 6002],
        'spice': [5900, 5901],
        'rdp': [3389],
    }
    
    # Port ranges for different purposes
    PORT_RANGES = {
        'system': (1, 1023),          # System/privileged ports
        'user': (1024, 49151),        # User/registered ports
        'dynamic': (49152, 65535),    # Dynamic/private ports
    }
    
    # Windows VM suggested ports (will be adjusted if occupied)
    WINDOWS_SUGGESTED_PORTS = {
        'rdp': 3390,           # RDP (shifted from 3389)
        'vnc': 5910,           # VNC display
        'spice': 5920,         # SPICE display
        'qemu_monitor': 4444,  # QEMU monitor
        'smb': 4450,           # Samba/file sharing
        'http': 8090,          # Windows HTTP services
        'https': 8453,         # Windows HTTPS services
    }
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "ghostos-builder"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.port_config_file = self.config_dir / "port_allocations.json"
        
    def is_port_in_use(self, port: int, protocol: str = 'tcp') -> bool:
        """Check if a port is currently in use"""
        try:
            if protocol == 'tcp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            return result == 0
        except:
            return False
    
    def scan_used_ports(self, start_port: int = 1, end_port: int = 65535) -> List[int]:
        """Scan for ports currently in use on the system"""
        used_ports = []
        
        # Method 1: Use netstat/ss if available
        try:
            result = subprocess.run(
                ['ss', '-tuln'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 5:
                    # Extract port from address:port format
                    addr_port = parts[4]
                    if ':' in addr_port:
                        port_str = addr_port.split(':')[-1]
                        try:
                            port = int(port_str)
                            if start_port <= port <= end_port:
                                used_ports.append(port)
                        except ValueError:
                            pass
        except:
            pass
        
        # Method 2: Fallback - check common ports manually
        if not used_ports:
            print("Scanning common ports...")
            for port in range(1, 10000):
                if self.is_port_in_use(port):
                    used_ports.append(port)
        
        return sorted(list(set(used_ports)))
    
    def get_parrot_os_ports(self) -> Dict[str, List[int]]:
        """Get ports used by Parrot OS services"""
        used_ports = {}
        
        print("Detecting Parrot OS service ports...")
        
        # Check known services
        for service, ports in self.KNOWN_SERVICES.items():
            service_ports = []
            for port in ports:
                if self.is_port_in_use(port):
                    service_ports.append(port)
            
            if service_ports:
                used_ports[service] = service_ports
        
        return used_ports
    
    def find_free_port(self, preferred_port: int, start_range: int = None, 
                      end_range: int = None) -> int:
        """Find a free port, starting with preferred port"""
        
        # Check if preferred port is free
        if not self.is_port_in_use(preferred_port):
            return preferred_port
        
        # Set default range
        if start_range is None:
            start_range = max(1024, preferred_port - 100)
        if end_range is None:
            end_range = min(65535, preferred_port + 1000)
        
        # Search for free port in range
        for port in range(start_range, end_range):
            if not self.is_port_in_use(port):
                return port
        
        raise RuntimeError(f"No free ports found in range {start_range}-{end_range}")
    
    def allocate_windows_ports(self) -> Dict[str, int]:
        """Allocate free ports for Windows VM services"""
        
        print("\nAllocating ports for Windows VM...")
        print("=" * 50)
        
        # Get currently used ports
        parrot_ports = self.get_parrot_os_ports()
        all_used = []
        for ports in parrot_ports.values():
            all_used.extend(ports)
        
        print(f"\nParrot OS is using {len(all_used)} ports")
        print(f"Used port ranges: {min(all_used) if all_used else 'none'} - {max(all_used) if all_used else 'none'}")
        
        # Allocate Windows ports
        windows_ports = {}
        
        for service, preferred_port in self.WINDOWS_SUGGESTED_PORTS.items():
            allocated_port = self.find_free_port(preferred_port)
            windows_ports[service] = allocated_port
            
            if allocated_port != preferred_port:
                print(f"  {service:20s}: {preferred_port} (occupied) -> {allocated_port} (allocated)")
            else:
                print(f"  {service:20s}: {allocated_port} ✓")
        
        return windows_ports
    
    def save_port_config(self, windows_ports: Dict[str, int]):
        """Save port configuration to file"""
        config = {
            'windows_ports': windows_ports,
            'parrot_ports': self.get_parrot_os_ports(),
            'timestamp': str(subprocess.check_output(['date']).decode().strip())
        }
        
        with open(self.port_config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n✓ Port configuration saved to: {self.port_config_file}")
    
    def load_port_config(self) -> Optional[Dict]:
        """Load saved port configuration"""
        if not self.port_config_file.exists():
            return None
        
        try:
            with open(self.port_config_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def generate_vm_config(self, windows_ports: Dict[str, int]) -> str:
        """Generate VM configuration with allocated ports"""
        
        config = f"""
# Windows 10 VM Configuration
# Generated port allocations to avoid conflicts with Parrot OS

# Display Options
VNC_PORT={windows_ports['vnc']}
SPICE_PORT={windows_ports['spice']}
RDP_PORT={windows_ports['rdp']}

# Management
QEMU_MONITOR_PORT={windows_ports['qemu_monitor']}

# Network Services
SMB_PORT={windows_ports['smb']}
HTTP_PORT={windows_ports['http']}
HTTPS_PORT={windows_ports['https']}

# QEMU Command Example:
# qemu-system-x86_64 \\
#   -vnc 127.0.0.1:{windows_ports['vnc'] - 5900} \\
#   -monitor telnet:127.0.0.1:{windows_ports['qemu_monitor']},server,nowait \\
#   -netdev user,id=net0,hostfwd=tcp::{windows_ports['rdp']}-:3389 \\
#   -device e1000,netdev=net0

# Connect to VM:
# VNC: vncviewer localhost:{windows_ports['vnc'] - 5900}
# RDP: rdesktop localhost:{windows_ports['rdp']}
# SPICE: remote-viewer spice://localhost:{windows_ports['spice']}
"""
        
        return config
    
    def check_and_report(self):
        """Full port check and report"""
        print("\n" + "=" * 60)
        print("  GhostOS Port Manager - System Analysis")
        print("=" * 60)
        
        # Get Parrot OS ports
        parrot_ports = self.get_parrot_os_ports()
        
        print("\n📊 Parrot OS Services:")
        if parrot_ports:
            for service, ports in parrot_ports.items():
                print(f"  • {service:20s}: {', '.join(map(str, ports))}")
        else:
            print("  No services detected on common ports")
        
        # Allocate Windows ports
        windows_ports = self.allocate_windows_ports()
        
        # Generate config
        vm_config = self.generate_vm_config(windows_ports)
        
        # Save configuration
        self.save_port_config(windows_ports)
        
        # Save VM config
        vm_config_file = self.config_dir / "windows_vm_ports.conf"
        with open(vm_config_file, 'w') as f:
            f.write(vm_config)
        
        print(f"\n✓ VM configuration saved to: {vm_config_file}")
        
        print("\n" + "=" * 60)
        print("Configuration complete! Use these ports for Windows VM.")
        print("=" * 60)
        
        return windows_ports


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='GhostOS Port Manager - Allocate ports for Windows VM'
    )
    parser.add_argument(
        '--scan-only',
        action='store_true',
        help='Only scan and display used ports'
    )
    parser.add_argument(
        '--check-port',
        type=int,
        help='Check if specific port is in use'
    )
    
    args = parser.parse_args()
    
    manager = PortManager()
    
    if args.check_port:
        in_use = manager.is_port_in_use(args.check_port)
        print(f"Port {args.check_port}: {'IN USE ❌' if in_use else 'FREE ✓'}")
        return 0 if not in_use else 1
    
    if args.scan_only:
        used = manager.scan_used_ports(1, 10000)
        print(f"Found {len(used)} ports in use:")
        for i in range(0, len(used), 10):
            print(f"  {', '.join(map(str, used[i:i+10]))}")
        return 0
    
    # Full check and allocation
    manager.check_and_report()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
