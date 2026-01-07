#!/usr/bin/env python3
"""
Basic tests for Windows Driver Emulator
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from emulator import DriverEmulator


class TestDriverEmulator(unittest.TestCase):
    """Test cases for DriverEmulator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.emulator = DriverEmulator()
    
    def test_initialization(self):
        """Test emulator initializes correctly"""
        self.assertIsNotNone(self.emulator)
        self.assertIsNotNone(self.emulator.config)
        self.assertIsInstance(self.emulator.loaded_drivers, dict)
        self.assertIsInstance(self.emulator.device_handlers, dict)
    
    def test_config_loading(self):
        """Test configuration loading"""
        config = self.emulator.config
        self.assertIn('driver_search_paths', config)
        self.assertIn('supported_device_types', config)
        self.assertIn('security', config)
        self.assertIn('logging', config)
    
    def test_device_handlers_initialized(self):
        """Test device handlers are initialized"""
        handlers = self.emulator.device_handlers
        self.assertIn('usb', handlers)
        self.assertIn('hid', handlers)
        self.assertIn('storage', handlers)
    
    def test_list_drivers_empty(self):
        """Test listing drivers when none loaded"""
        drivers = self.emulator.list_drivers()
        self.assertIsInstance(drivers, list)
        self.assertEqual(len(drivers), 0)
    
    def test_parse_driver_metadata(self):
        """Test driver metadata parsing"""
        # Test with different filename patterns
        test_cases = [
            ('usb_device.sys', 'usb'),
            ('hid_keyboard.sys', 'hid'),
            ('storage_driver.sys', 'storage'),
            ('network_adapter.sys', 'network'),
            ('audio_device.sys', 'audio'),
        ]
        
        for filename, expected_type in test_cases:
            with self.subTest(filename=filename):
                # Create a fake path
                fake_path = f'/tmp/{filename}'
                metadata = self.emulator._parse_driver(fake_path)
                self.assertEqual(metadata['device_type'], expected_type)


class TestUSBHandler(unittest.TestCase):
    """Test cases for USB handler"""
    
    def setUp(self):
        """Set up test fixtures"""
        from device_handlers.usb_handler import USBHandler
        self.handler = USBHandler()
    
    def test_initialization(self):
        """Test handler initializes correctly"""
        self.assertIsNotNone(self.handler)
        self.assertEqual(self.handler.device_type, 'usb')
    
    def test_enumerate_devices(self):
        """Test device enumeration (may return empty if no USB devices)"""
        devices = self.handler.enumerate_devices()
        self.assertIsInstance(devices, list)
        # Can't guarantee devices present, just check format if any exist
        if devices:
            device = devices[0]
            self.assertIn('vendor_id', device)
            self.assertIn('product_id', device)


class TestHIDHandler(unittest.TestCase):
    """Test cases for HID handler"""
    
    def setUp(self):
        """Set up test fixtures"""
        from device_handlers.hid_handler import HIDHandler
        self.handler = HIDHandler()
    
    def test_initialization(self):
        """Test handler initializes correctly"""
        self.assertIsNotNone(self.handler)
        self.assertEqual(self.handler.device_type, 'hid')
    
    def test_determine_hid_type(self):
        """Test HID device type determination"""
        test_cases = [
            ('USB Keyboard', '', 'keyboard'),
            ('Logitech Mouse', '', 'mouse'),
            ('Touchpad Device', '', 'touchpad'),
            ('Xbox Controller', '', 'gamepad'),
            ('Generic HID', '', 'generic_hid'),
        ]
        
        for name, caps, expected in test_cases:
            with self.subTest(name=name):
                result = self.handler._determine_hid_type(name, caps)
                self.assertEqual(result, expected)


class TestStorageHandler(unittest.TestCase):
    """Test cases for Storage handler"""
    
    def setUp(self):
        """Set up test fixtures"""
        from device_handlers.storage_handler import StorageHandler
        self.handler = StorageHandler()
    
    def test_initialization(self):
        """Test handler initializes correctly"""
        self.assertIsNotNone(self.handler)
        self.assertEqual(self.handler.device_type, 'storage')


if __name__ == '__main__':
    unittest.main()
