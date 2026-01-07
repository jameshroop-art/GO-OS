"""Storage device handler for Windows Driver Emulator"""

import os
import subprocess
import logging
from typing import Dict, Any, List
from .base_handler import DeviceHandler

logger = logging.getLogger('StorageHandler')


class StorageHandler(DeviceHandler):
    """Handler for storage devices - hard drives, USB drives, etc."""
    
    def __init__(self):
        super().__init__('storage')
        self.storage_devices = {}
    
    def load(self, driver_path: str, metadata: Dict[str, Any]) -> bool:
        """
        Load a storage driver
        
        Args:
            driver_path: Path to driver file
            metadata: Driver metadata
            
        Returns:
            True if successful, False otherwise
        """
        driver_name = os.path.basename(driver_path)
        logger.info(f"Loading storage driver: {driver_name}")
        
        try:
            # Enumerate storage devices
            devices = self.enumerate_devices()
            
            if devices:
                self.devices[driver_name] = {
                    'path': driver_path,
                    'metadata': metadata,
                    'devices': devices
                }
                logger.info(f"Storage driver loaded: {driver_name} ({len(devices)} devices)")
                return True
            else:
                logger.warning(f"No storage devices found for driver: {driver_name}")
                # Still load the driver
                self.devices[driver_name] = {
                    'path': driver_path,
                    'metadata': metadata,
                    'devices': []
                }
                return True
                
        except Exception as e:
            logger.error(f"Failed to load storage driver {driver_name}: {e}")
            return False
    
    def unload(self, driver_name: str) -> bool:
        """
        Unload a storage driver
        
        Args:
            driver_name: Name of driver to unload
            
        Returns:
            True if successful, False otherwise
        """
        if driver_name not in self.devices:
            logger.error(f"Storage driver not loaded: {driver_name}")
            return False
        
        try:
            del self.devices[driver_name]
            logger.info(f"Storage driver unloaded: {driver_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unload storage driver {driver_name}: {e}")
            return False
    
    def enumerate_devices(self) -> List[Dict[str, Any]]:
        """
        Enumerate storage devices
        
        Returns:
            List of storage device information
        """
        devices = []
        
        try:
            # Use lsblk to enumerate block devices
            result = subprocess.run(
                ['lsblk', '-J', '-o', 'NAME,SIZE,TYPE,MOUNTPOINT,VENDOR,MODEL,SERIAL'],
                capture_output=True,
                text=True,
                check=True
            )
            
            import json
            data = json.loads(result.stdout)
            
            for device in data.get('blockdevices', []):
                if device['type'] in ['disk', 'part']:
                    devices.append({
                        'name': device['name'],
                        'path': f"/dev/{device['name']}",
                        'size': device.get('size', 'unknown'),
                        'type': device['type'],
                        'mountpoint': device.get('mountpoint', ''),
                        'vendor': device.get('vendor', 'unknown').strip(),
                        'model': device.get('model', 'unknown').strip(),
                        'serial': device.get('serial', 'unknown').strip()
                    })
            
            logger.debug(f"Enumerated {len(devices)} storage devices")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to enumerate storage devices: {e}")
        except FileNotFoundError:
            logger.error("lsblk command not found. Install util-linux package.")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse lsblk output: {e}")
        
        return devices
    
    def get_device_by_path(self, device_path: str) -> Dict[str, Any]:
        """
        Get information about a specific storage device
        
        Args:
            device_path: Path to device (e.g., /dev/sda)
            
        Returns:
            Device information dictionary
        """
        devices = self.enumerate_devices()
        for device in devices:
            if device['path'] == device_path:
                return device
        return {}
    
    def get_mounted_devices(self) -> List[Dict[str, Any]]:
        """
        Get all currently mounted storage devices
        
        Returns:
            List of mounted devices
        """
        devices = self.enumerate_devices()
        return [d for d in devices if d['mountpoint']]
