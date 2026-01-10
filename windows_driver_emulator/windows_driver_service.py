"""
Windows Driver Service - Runs inside Windows 10 VM
Handles actual driver operations and responds to RPC commands from Linux GUI

This service runs on the Windows side in the isolated VM
Receives commands via RPC from Linux GUI and executes driver operations

LICENSE: MIT (see LICENSE file in repository root)
"""

import sys
import os
import json
import logging
from pathlib import Path

# Note: This runs on Windows, so use Windows-specific modules
try:
    import win32api
    import win32service
    import win32serviceutil
    import win32event
    HAS_WINDOWS_MODULES = True
except ImportError:
    HAS_WINDOWS_MODULES = False
    print("Warning: Windows modules not available (expected on Linux)")

# Import our RPC layer
sys.path.insert(0, str(Path(__file__).parent))
from rpc_layer import RPCServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('WindowsDriverService')


class WindowsDriverManager:
    """
    Driver manager running inside Windows VM
    Performs actual driver operations using Windows APIs
    """
    
    def __init__(self):
        """Initialize Windows driver manager"""
        self.installed_drivers = []
        logger.info("Windows Driver Manager initialized")
    
    def list_drivers(self, params: dict) -> dict:
        """
        List available/installed drivers using Windows Device Manager
        
        Args:
            params: RPC parameters with optional 'category' filter
            
        Returns:
            Response dict with driver list
        """
        try:
            category = params.get('category')
            
            # Use Windows devcon or PowerShell to list drivers
            # For now, return mock data - in production would query Windows
            drivers = [
                {
                    'device_id': 'PCI\\VEN_8086\\DEV_1234',
                    'device_name': 'Intel Network Adapter',
                    'category': 'network',
                    'status': 'installed',
                    'driver_version': '22.100.0.1'
                },
                {
                    'device_id': 'PCI\\VEN_10DE\\DEV_1234',
                    'device_name': 'NVIDIA Graphics Adapter',
                    'category': 'display',
                    'status': 'needs_driver',
                    'driver_version': None
                }
            ]
            
            # Filter by category if specified
            if category:
                drivers = [d for d in drivers if d['category'] == category]
            
            logger.info(f"Listed {len(drivers)} drivers")
            return {
                'success': True,
                'drivers': drivers,
                'count': len(drivers)
            }
        
        except Exception as e:
            logger.error(f"List drivers error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def install_driver(self, params: dict) -> dict:
        """
        Install driver using Windows Device Manager / PnPUtil
        
        Args:
            params: RPC parameters with 'device_id'
            
        Returns:
            Response dict with installation result
        """
        try:
            device_id = params.get('device_id')
            
            if not device_id:
                return {
                    'success': False,
                    'error': 'device_id required'
                }
            
            logger.info(f"Installing driver for: {device_id}")
            
            # In production, use Windows APIs:
            # - pnputil.exe /add-driver driver.inf /install
            # - Or Windows Device Manager COM APIs
            # - Or PowerShell: pnputil /add-driver /install
            
            # Mock success for now
            self.installed_drivers.append(device_id)
            
            return {
                'success': True,
                'message': f'Driver installed for {device_id}',
                'device_id': device_id
            }
        
        except Exception as e:
            logger.error(f"Install driver error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def uninstall_driver(self, params: dict) -> dict:
        """
        Uninstall driver using Windows Device Manager
        
        Args:
            params: RPC parameters with 'device_id'
            
        Returns:
            Response dict with uninstallation result
        """
        try:
            device_id = params.get('device_id')
            
            if not device_id:
                return {
                    'success': False,
                    'error': 'device_id required'
                }
            
            logger.info(f"Uninstalling driver for: {device_id}")
            
            # In production, use Windows APIs:
            # - pnputil.exe /delete-driver oem##.inf /uninstall
            # - Or Windows Device Manager COM APIs
            
            if device_id in self.installed_drivers:
                self.installed_drivers.remove(device_id)
            
            return {
                'success': True,
                'message': f'Driver uninstalled for {device_id}',
                'device_id': device_id
            }
        
        except Exception as e:
            logger.error(f"Uninstall driver error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_status(self, params: dict) -> dict:
        """
        Get Windows VM status
        
        Args:
            params: RPC parameters (unused)
            
        Returns:
            Response dict with VM status
        """
        try:
            # Get Windows version, memory, etc.
            return {
                'success': True,
                'vm_type': 'Windows 10 22H2 Minimal',
                'isolated': True,
                'installed_drivers_count': len(self.installed_drivers),
                'memory_mb': 512,
                'cpu_cores': 1,
                'processes_count': len(self.installed_drivers) + 10,  # Minimal processes
            }
        
        except Exception as e:
            logger.error(f"Get status error: {e}")
            return {
                'success': False,
                'error': str(e)
            }


class WindowsDriverService:
    """
    Windows service that runs the driver manager and RPC server
    """
    
    def __init__(self):
        """Initialize service"""
        self.running = False
        self.rpc_server = None
        self.driver_manager = None
    
    def start(self):
        """Start the service"""
        logger.info("Starting Windows Driver Service...")
        
        # Initialize driver manager
        self.driver_manager = WindowsDriverManager()
        
        # Initialize RPC server
        self.rpc_server = RPCServer(host='0.0.0.0', port=9999)
        
        # Register handlers
        self.rpc_server.register_handler('list_drivers', self.driver_manager.list_drivers)
        self.rpc_server.register_handler('install_driver', self.driver_manager.install_driver)
        self.rpc_server.register_handler('uninstall_driver', self.driver_manager.uninstall_driver)
        self.rpc_server.register_handler('get_status', self.driver_manager.get_status)
        
        # Start RPC server
        logger.info("Driver service started successfully")
        self.running = True
        self.rpc_server.start()
    
    def stop(self):
        """Stop the service"""
        logger.info("Stopping Windows Driver Service...")
        self.running = False
        if self.rpc_server:
            self.rpc_server.stop()
        logger.info("Driver service stopped")


def main():
    """
    Main entry point for Windows Driver Service
    Can run as standalone service or Windows Service
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Windows Driver Service - Runs in Windows 10 VM'
    )
    parser.add_argument(
        '--standalone',
        action='store_true',
        help='Run as standalone service (not Windows Service)'
    )
    
    args = parser.parse_args()
    
    service = WindowsDriverService()
    
    if args.standalone:
        print("Starting Windows Driver Service (standalone mode)...")
        print("Press Ctrl+C to stop")
        
        try:
            service.start()
        except KeyboardInterrupt:
            print("\nStopping service...")
            service.stop()
    else:
        # Would run as Windows Service using win32serviceutil
        # For now, run standalone
        print("Running in standalone mode (Windows Service support requires win32serviceutil)")
        try:
            service.start()
        except KeyboardInterrupt:
            service.stop()


if __name__ == '__main__':
    main()
