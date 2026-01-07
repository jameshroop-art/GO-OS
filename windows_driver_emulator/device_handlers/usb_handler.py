"""USB device handler for Windows Driver Emulator"""

import os
import subprocess
import logging
from typing import Dict, Any, List
from .base_handler import DeviceHandler

logger = logging.getLogger('USBHandler')


class USBHandler(DeviceHandler):
    """Handler for USB devices"""
    
    def __init__(self):
        super().__init__('usb')
        self.usb_devices = {}
    
    def load(self, driver_path: str, metadata: Dict[str, Any]) -> bool:
        """
        Load a USB driver
        
        Args:
            driver_path: Path to driver file
            metadata: Driver metadata
            
        Returns:
            True if successful, False otherwise
        """
        driver_name = os.path.basename(driver_path)
        logger.info(f"Loading USB driver: {driver_name}")
        
        try:
            # Enumerate USB devices
            devices = self.enumerate_devices()
            
            # Match devices with driver
            matched_devices = self._match_devices(devices, metadata)
            
            if matched_devices:
                self.devices[driver_name] = {
                    'path': driver_path,
                    'metadata': metadata,
                    'devices': matched_devices
                }
                logger.info(f"USB driver loaded: {driver_name} ({len(matched_devices)} devices)")
                return True
            else:
                logger.warning(f"No matching devices for driver: {driver_name}")
                # Still load the driver for future device connections
                self.devices[driver_name] = {
                    'path': driver_path,
                    'metadata': metadata,
                    'devices': []
                }
                return True
                
        except Exception as e:
            logger.error(f"Failed to load USB driver {driver_name}: {e}")
            return False
    
    def unload(self, driver_name: str) -> bool:
        """
        Unload a USB driver
        
        Args:
            driver_name: Name of driver to unload
            
        Returns:
            True if successful, False otherwise
        """
        if driver_name not in self.devices:
            logger.error(f"USB driver not loaded: {driver_name}")
            return False
        
        try:
            # Cleanup device associations
            del self.devices[driver_name]
            logger.info(f"USB driver unloaded: {driver_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unload USB driver {driver_name}: {e}")
            return False
    
    def enumerate_devices(self) -> List[Dict[str, Any]]:
        """
        Enumerate USB devices
        
        Returns:
            List of USB device information
        """
        devices = []
        
        try:
            # Use lsusb to enumerate USB devices
            result = subprocess.run(
                ['lsusb'],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.strip().split('\n'):
                if line:
                    # Parse lsusb output
                    parts = line.split()
                    if len(parts) >= 6:
                        bus = parts[1]
                        device = parts[3].rstrip(':')
                        vendor_product = parts[5]
                        
                        try:
                            vendor_id, product_id = vendor_product.split(':')
                            devices.append({
                                'bus': bus,
                                'device': device,
                                'vendor_id': vendor_id,
                                'product_id': product_id,
                                'description': ' '.join(parts[6:]) if len(parts) > 6 else ''
                            })
                        except ValueError:
                            continue
            
            logger.debug(f"Enumerated {len(devices)} USB devices")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to enumerate USB devices: {e}")
        except FileNotFoundError:
            logger.error("lsusb command not found. Install usbutils package.")
        
        return devices
    
    def _match_devices(self, devices: List[Dict[str, Any]], 
                      metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Match devices with driver metadata
        
        Args:
            devices: List of device dictionaries
            metadata: Driver metadata
            
        Returns:
            List of matched devices
        """
        matched = []
        compatible_ids = metadata.get('compatible_ids', [])
        
        # If no compatible IDs specified, match all devices
        if not compatible_ids:
            return devices
        
        for device in devices:
            device_id = f"{device['vendor_id']}:{device['product_id']}"
            if device_id in compatible_ids:
                matched.append(device)
        
        return matched
    
    def get_device_info(self, vendor_id: str, product_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a USB device
        
        Args:
            vendor_id: USB vendor ID (hex)
            product_id: USB product ID (hex)
            
        Returns:
            Device information dictionary
        """
        devices = self.enumerate_devices()
        for device in devices:
            if device['vendor_id'] == vendor_id and device['product_id'] == product_id:
                return device
        return {}
