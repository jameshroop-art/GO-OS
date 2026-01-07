"""Base device handler class"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

logger = logging.getLogger('DeviceHandler')


class DeviceHandler(ABC):
    """Abstract base class for device handlers"""
    
    def __init__(self, device_type: str):
        self.device_type = device_type
        self.devices = {}
        logger.info(f"Initialized {device_type} handler")
    
    @abstractmethod
    def load(self, driver_path: str, metadata: Dict[str, Any]) -> bool:
        """
        Load a driver
        
        Args:
            driver_path: Path to driver file
            metadata: Driver metadata
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def unload(self, driver_name: str) -> bool:
        """
        Unload a driver
        
        Args:
            driver_name: Name of driver to unload
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def enumerate_devices(self) -> list:
        """
        Enumerate devices of this type
        
        Returns:
            List of device information dictionaries
        """
        pass
    
    def get_device_count(self) -> int:
        """Get count of managed devices"""
        return len(self.devices)
