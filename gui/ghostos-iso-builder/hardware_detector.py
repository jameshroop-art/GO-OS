#!/usr/bin/env python3
"""
HeckOS Builder - Hardware Detection and Scaling
Automatically detects screen resolution, DPI, and configures optimal scaling
"""

import sys
import subprocess
from typing import Tuple, Dict, Optional

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QRect
    from PyQt6.QtGui import QScreen
except ImportError:
    print("PyQt6 not found. Hardware detection unavailable.")
    sys.exit(1)


class HardwareDetector:
    """Detects hardware capabilities and configures optimal settings"""
    
    def __init__(self):
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.primary_screen = self.app.primaryScreen()
        self.all_screens = self.app.screens()
        
    def get_screen_info(self) -> Dict:
        """Get detailed screen information"""
        if not self.primary_screen:
            return self._get_fallback_screen_info()
            
        geometry = self.primary_screen.geometry()
        physical_size = self.primary_screen.physicalSize()
        dpi = self.primary_screen.logicalDotsPerInch()
        device_pixel_ratio = self.primary_screen.devicePixelRatio()
        
        # Calculate aspect ratio
        width = geometry.width()
        height = geometry.height()
        aspect_ratio = self._calculate_aspect_ratio(width, height)
        
        # Determine screen category
        category = self._categorize_screen(width, height, physical_size.width())
        
        return {
            'width': width,
            'height': height,
            'physical_width_mm': physical_size.width(),
            'physical_height_mm': physical_size.height(),
            'dpi': dpi,
            'device_pixel_ratio': device_pixel_ratio,
            'aspect_ratio': aspect_ratio,
            'category': category,
            'refresh_rate': self.primary_screen.refreshRate(),
            'screens_count': len(self.all_screens)
        }
    
    def _get_fallback_screen_info(self) -> Dict:
        """Fallback screen info if PyQt6 detection fails"""
        try:
            # Try xrandr
            result = subprocess.run(
                ['xrandr'], 
                capture_output=True, 
                text=True,
                timeout=2
            )
            
            for line in result.stdout.split('\n'):
                if ' connected' in line and '*' in line:
                    parts = line.split()
                    for part in parts:
                        if 'x' in part and part[0].isdigit():
                            res = part.split('x')
                            width = int(res[0])
                            height = int(res[1].split('+')[0])
                            
                            return {
                                'width': width,
                                'height': height,
                                'physical_width_mm': 0,
                                'physical_height_mm': 0,
                                'dpi': 96,
                                'device_pixel_ratio': 1.0,
                                'aspect_ratio': self._calculate_aspect_ratio(width, height),
                                'category': self._categorize_screen(width, height, 0),
                                'refresh_rate': 60,
                                'screens_count': 1
                            }
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            pass
        
        # Ultimate fallback
        return {
            'width': 1920,
            'height': 1080,
            'physical_width_mm': 0,
            'physical_height_mm': 0,
            'dpi': 96,
            'device_pixel_ratio': 1.0,
            'aspect_ratio': '16:9',
            'category': 'desktop',
            'refresh_rate': 60,
            'screens_count': 1
        }
    
    def _calculate_aspect_ratio(self, width: int, height: int) -> str:
        """Calculate and return aspect ratio as string"""
        from math import gcd
        
        divisor = gcd(width, height)
        ratio_w = width // divisor
        ratio_h = height // divisor
        
        # Common aspect ratios
        common_ratios = {
            (16, 9): '16:9',
            (16, 10): '16:10',
            (4, 3): '4:3',
            (21, 9): '21:9',
            (32, 9): '32:9',
            (5, 4): '5:4',
            (3, 2): '3:2',
        }
        
        return common_ratios.get((ratio_w, ratio_h), f'{ratio_w}:{ratio_h}')
    
    def _categorize_screen(self, width: int, height: int, physical_width_mm: float) -> str:
        """Categorize screen type based on resolution and physical size"""
        total_pixels = width * height
        
        # Categorize by resolution
        if width <= 1024:
            return 'small'  # Small screen (netbook, old laptop)
        elif width <= 1366:
            return 'laptop'  # Standard laptop
        elif width <= 1920 and height <= 1080:
            return 'desktop'  # Full HD desktop
        elif width <= 2560 and height <= 1440:
            return 'high_res'  # QHD
        elif width <= 3840 and height <= 2160:
            return 'ultra_hd'  # 4K UHD
        elif width > 3840:
            return 'ultrawide'  # 5K+, ultrawide
        
        return 'desktop'
    
    def calculate_optimal_window_size(self, screen_info: Dict) -> Tuple[int, int]:
        """Calculate optimal window size based on screen resolution"""
        width = screen_info['width']
        height = screen_info['height']
        category = screen_info['category']
        
        # Calculate optimal size (leaving space for taskbar/panels)
        if category == 'small':
            # Small screens: use 95% of available space
            return (int(width * 0.95), int(height * 0.90))
        elif category == 'laptop':
            # Laptops: use 90% of available space
            return (int(width * 0.90), int(height * 0.85))
        elif category in ['desktop', 'high_res']:
            # Desktop: use fixed optimal size or 85%
            optimal_width = min(1400, int(width * 0.85))
            optimal_height = min(900, int(height * 0.85))
            return (optimal_width, optimal_height)
        elif category in ['ultra_hd', 'ultrawide']:
            # 4K+: use larger window but limit maximum
            optimal_width = min(1920, int(width * 0.70))
            optimal_height = min(1200, int(height * 0.70))
            return (optimal_width, optimal_height)
        
        # Default fallback
        return (1400, 900)
    
    def calculate_scaling_factor(self, screen_info: Dict) -> float:
        """Calculate UI scaling factor based on DPI and screen size"""
        dpi = screen_info['dpi']
        device_pixel_ratio = screen_info['device_pixel_ratio']
        category = screen_info['category']
        
        # Base scaling on DPI
        if dpi <= 96:
            base_scale = 1.0
        elif dpi <= 120:
            base_scale = 1.25
        elif dpi <= 144:
            base_scale = 1.5
        elif dpi <= 192:
            base_scale = 2.0
        else:
            base_scale = 2.5
        
        # Adjust for device pixel ratio
        if device_pixel_ratio > 1.0:
            base_scale *= device_pixel_ratio
        
        # Adjust for screen category
        if category == 'small':
            base_scale *= 0.85  # Smaller UI elements for small screens
        elif category == 'ultra_hd':
            base_scale *= 1.15  # Slightly larger for 4K
        
        # Clamp to reasonable range
        return max(0.75, min(base_scale, 3.0))
    
    def get_font_size_adjustments(self, screen_info: Dict) -> Dict[str, int]:
        """Calculate font size adjustments for different UI elements"""
        category = screen_info['category']
        dpi = screen_info['dpi']
        
        # Base sizes
        if category == 'small':
            base_multiplier = 0.85
        elif category in ['ultra_hd', 'ultrawide']:
            base_multiplier = 1.2
        else:
            base_multiplier = 1.0
        
        # DPI adjustment
        if dpi > 144:
            dpi_multiplier = 1.2
        elif dpi > 120:
            dpi_multiplier = 1.1
        else:
            dpi_multiplier = 1.0
        
        total_multiplier = base_multiplier * dpi_multiplier
        
        return {
            'title': int(16 * total_multiplier),
            'header': int(14 * total_multiplier),
            'body': int(11 * total_multiplier),
            'small': int(9 * total_multiplier),
            'button': int(11 * total_multiplier),
            'menu': int(10 * total_multiplier)
        }
    
    def detect_touchscreen(self) -> bool:
        """Detect if system has touchscreen capability"""
        try:
            # Check for touchscreen devices in /dev/input
            result = subprocess.run(
                ['ls', '/dev/input'],
                capture_output=True,
                text=True,
                timeout=1
            )
            
            # Look for touch devices
            if 'touchscreen' in result.stdout.lower() or 'event' in result.stdout:
                # Check xinput for touch devices
                xinput_result = subprocess.run(
                    ['xinput', 'list'],
                    capture_output=True,
                    text=True,
                    timeout=1
                )
                
                return 'touchscreen' in xinput_result.stdout.lower() or \
                       'touch' in xinput_result.stdout.lower()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return False
    
    def get_optimal_preview_resolution(self, screen_info: Dict) -> Tuple[int, int]:
        """Calculate optimal resolution for preview pane"""
        category = screen_info['category']
        
        # Preview pane resolutions based on screen category
        resolutions = {
            'small': (640, 480),
            'laptop': (800, 600),
            'desktop': (1024, 768),
            'high_res': (1280, 960),
            'ultra_hd': (1600, 1200),
            'ultrawide': (1920, 1080)
        }
        
        return resolutions.get(category, (1024, 768))
    
    def generate_config(self) -> Dict:
        """Generate complete hardware configuration"""
        screen_info = self.get_screen_info()
        window_size = self.calculate_optimal_window_size(screen_info)
        scaling_factor = self.calculate_scaling_factor(screen_info)
        font_sizes = self.get_font_size_adjustments(screen_info)
        has_touchscreen = self.detect_touchscreen()
        preview_resolution = self.get_optimal_preview_resolution(screen_info)
        
        return {
            'screen': screen_info,
            'window': {
                'width': window_size[0],
                'height': window_size[1],
                'scaling_factor': scaling_factor
            },
            'fonts': font_sizes,
            'preview': {
                'width': preview_resolution[0],
                'height': preview_resolution[1]
            },
            'features': {
                'touchscreen': has_touchscreen,
                'multi_monitor': screen_info['screens_count'] > 1,
                'high_dpi': screen_info['dpi'] > 144
            }
        }
    
    def print_config(self, config: Optional[Dict] = None):
        """Print hardware configuration (for debugging)"""
        if config is None:
            config = self.generate_config()
        
        print("\n" + "="*60)
        print("HeckOS Builder - Hardware Configuration")
        print("="*60)
        
        screen = config['screen']
        print(f"\nScreen:")
        print(f"  Resolution: {screen['width']}x{screen['height']}")
        print(f"  Aspect Ratio: {screen['aspect_ratio']}")
        print(f"  DPI: {screen['dpi']}")
        print(f"  Category: {screen['category']}")
        print(f"  Refresh Rate: {screen['refresh_rate']} Hz")
        print(f"  Multi-Monitor: {config['features']['multi_monitor']}")
        
        window = config['window']
        print(f"\nWindow:")
        print(f"  Size: {window['width']}x{window['height']}")
        print(f"  Scaling Factor: {window['scaling_factor']:.2f}x")
        
        fonts = config['fonts']
        print(f"\nFonts:")
        print(f"  Title: {fonts['title']}pt")
        print(f"  Header: {fonts['header']}pt")
        print(f"  Body: {fonts['body']}pt")
        
        features = config['features']
        print(f"\nFeatures:")
        print(f"  Touchscreen: {features['touchscreen']}")
        print(f"  High DPI: {features['high_dpi']}")
        
        print("="*60 + "\n")


if __name__ == '__main__':
    detector = HardwareDetector()
    config = detector.generate_config()
    detector.print_config(config)
