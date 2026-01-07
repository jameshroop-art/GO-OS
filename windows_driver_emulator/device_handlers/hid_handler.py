"""HID device handler for Windows Driver Emulator"""

import os
import glob
import logging
from typing import Dict, Any, List
from .base_handler import DeviceHandler

logger = logging.getLogger('HIDHandler')


class HIDHandler(DeviceHandler):
    """Handler for HID (Human Interface Devices) - keyboards, mice, game controllers"""
    
    def __init__(self):
        super().__init__('hid')
        self.hid_devices = {}
    
    def load(self, driver_path: str, metadata: Dict[str, Any]) -> bool:
        """
        Load an HID driver
        
        Args:
            driver_path: Path to driver file
            metadata: Driver metadata
            
        Returns:
            True if successful, False otherwise
        """
        driver_name = os.path.basename(driver_path)
        logger.info(f"Loading HID driver: {driver_name}")
        
        try:
            # Enumerate HID devices
            devices = self.enumerate_devices()
            
            if devices:
                self.devices[driver_name] = {
                    'path': driver_path,
                    'metadata': metadata,
                    'devices': devices
                }
                logger.info(f"HID driver loaded: {driver_name} ({len(devices)} devices)")
                return True
            else:
                logger.warning(f"No HID devices found for driver: {driver_name}")
                # Still load the driver
                self.devices[driver_name] = {
                    'path': driver_path,
                    'metadata': metadata,
                    'devices': []
                }
                return True
                
        except Exception as e:
            logger.error(f"Failed to load HID driver {driver_name}: {e}")
            return False
    
    def unload(self, driver_name: str) -> bool:
        """
        Unload an HID driver
        
        Args:
            driver_name: Name of driver to unload
            
        Returns:
            True if successful, False otherwise
        """
        if driver_name not in self.devices:
            logger.error(f"HID driver not loaded: {driver_name}")
            return False
        
        try:
            del self.devices[driver_name]
            logger.info(f"HID driver unloaded: {driver_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unload HID driver {driver_name}: {e}")
            return False
    
    def enumerate_devices(self) -> List[Dict[str, Any]]:
        """
        Enumerate HID devices
        
        Returns:
            List of HID device information
        """
        devices = []
        
        try:
            # Look for HID devices in /dev/input
            input_devices = glob.glob('/dev/input/event*')
            
            for device_path in input_devices:
                try:
                    # Get device name from sysfs
                    device_num = os.path.basename(device_path).replace('event', '')
                    name_path = f'/sys/class/input/event{device_num}/device/name'
                    
                    if os.path.exists(name_path):
                        with open(name_path, 'r') as f:
                            device_name = f.read().strip()
                        
                        # Get device capabilities
                        capabilities_path = f'/sys/class/input/event{device_num}/device/capabilities/ev'
                        capabilities = ''
                        if os.path.exists(capabilities_path):
                            with open(capabilities_path, 'r') as f:
                                capabilities = f.read().strip()
                        
                        # Determine device type
                        device_type = self._determine_hid_type(device_name, capabilities)
                        
                        devices.append({
                            'path': device_path,
                            'name': device_name,
                            'type': device_type,
                            'capabilities': capabilities
                        })
                        
                except Exception as e:
                    logger.debug(f"Could not read device {device_path}: {e}")
                    continue
            
            logger.debug(f"Enumerated {len(devices)} HID devices")
            
        except Exception as e:
            logger.error(f"Failed to enumerate HID devices: {e}")
        
        return devices
    
    def _determine_hid_type(self, device_name: str, capabilities: str) -> str:
        """
        Determine HID device type from name and capabilities
        
        Args:
            device_name: Device name string
            capabilities: Capabilities hex string
            
        Returns:
            Device type string
        """
        name_lower = device_name.lower()
        
        # Check for specific device types
        if 'keyboard' in name_lower or 'kbd' in name_lower:
            return 'keyboard'
        elif 'mouse' in name_lower or 'pointing' in name_lower:
            return 'mouse'
        elif 'touchpad' in name_lower or 'trackpad' in name_lower:
            return 'touchpad'
        elif 'touchscreen' in name_lower or 'touch screen' in name_lower:
            return 'touchscreen'
        elif 'gamepad' in name_lower or 'joystick' in name_lower or 'controller' in name_lower:
            return 'gamepad'
        elif 'pen' in name_lower or 'stylus' in name_lower:
            return 'stylus'
        else:
            return 'generic_hid'
    
    def get_device_by_type(self, device_type: str) -> List[Dict[str, Any]]:
        """
        Get all HID devices of a specific type
        
        Args:
            device_type: Type of device (keyboard, mouse, etc.)
            
        Returns:
            List of matching devices
        """
        devices = self.enumerate_devices()
        return [d for d in devices if d['type'] == device_type]
