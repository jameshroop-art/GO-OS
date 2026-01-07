#!/usr/bin/env python3
"""
Heck-CheckOS ISO Builder - Integration Test
Tests keyboard and GUI integration
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        print("✓ PyQt6.QtWidgets")
    except ImportError as e:
        print(f"✗ PyQt6.QtWidgets: {e}")
        return False
    
    try:
        from PyQt6.QtCore import Qt, QPoint
        print("✓ PyQt6.QtCore")
    except ImportError as e:
        print(f"✗ PyQt6.QtCore: {e}")
        return False
    
    try:
        from ui.touchscreen_keyboard import TouchscreenKeyboard
        print("✓ TouchscreenKeyboard")
    except ImportError as e:
        print(f"✗ TouchscreenKeyboard: {e}")
        return False
    
    try:
        from ui.calibration_wizard import CalibrationWizard
        print("✓ CalibrationWizard")
    except ImportError as e:
        print(f"✗ CalibrationWizard: {e}")
        return False
    
    try:
        from ui.keyboard_designer import KeyboardLayoutDesigner
        print("✓ KeyboardLayoutDesigner")
    except ImportError as e:
        print(f"✗ KeyboardLayoutDesigner: {e}")
        return False
    
    return True

def test_keyboard_creation():
    """Test keyboard widget creation"""
    print("\nTesting keyboard creation...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.touchscreen_keyboard import TouchscreenKeyboard
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        keyboard = TouchscreenKeyboard()
        print("✓ Keyboard widget created")
        
        # Test basic properties
        assert keyboard.current_layout == "qwerty", "Default layout should be qwerty"
        print("✓ Default layout is qwerty")
        
        assert keyboard.SNAP_DISTANCE == 20, "Snap distance should be 20px"
        print("✓ Snap distance configured")
        
        assert not keyboard.is_visible(), "Keyboard should be hidden by default"
        print("✓ Initial visibility state correct")
        
        return True
        
    except Exception as e:
        print(f"✗ Keyboard creation failed: {e}")
        return False

def test_calibration():
    """Test calibration wizard"""
    print("\nTesting calibration wizard...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QPoint
        from ui.calibration_wizard import CalibrationWizard
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Create wizard (won't show in headless mode)
        wizard = CalibrationWizard()
        print("✓ CalibrationWizard created")
        
        # Test offset
        offset = wizard.get_offset()
        assert isinstance(offset, QPoint), "Offset should be QPoint"
        print("✓ Offset calculation works")
        
        return True
        
    except Exception as e:
        print(f"✗ Calibration test failed: {e}")
        return False

def test_layout_designer():
    """Test layout designer"""
    print("\nTesting layout designer...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.keyboard_designer import KeyboardLayoutDesigner
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        designer = KeyboardLayoutDesigner()
        print("✓ KeyboardLayoutDesigner created")
        
        # Test layout data
        layout = designer.get_layout()
        assert 'name' in layout, "Layout should have name"
        assert 'rows' in layout, "Layout should have rows"
        print("✓ Layout structure valid")
        
        return True
        
    except Exception as e:
        print(f"✗ Layout designer test failed: {e}")
        return False

def test_main_gui_integration():
    """Test main GUI integration"""
    print("\nTesting main GUI integration...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from main import HeckCheckOSBuilderGUI
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Create main window (won't show in headless mode)
        window = HeckCheckOSBuilderGUI()
        print("✓ Main GUI created")
        
        # Test keyboard integration
        assert hasattr(window, 'touchscreen_keyboard'), "Main GUI should have keyboard attribute"
        print("✓ Keyboard attribute present")
        
        assert hasattr(window, 'toggle_touchscreen_keyboard'), "Main GUI should have keyboard toggle"
        print("✓ Keyboard toggle method present")
        
        return True
        
    except Exception as e:
        print(f"✗ Main GUI integration test failed: {e}")
        return False

def run_all_tests():
    """Run all integration tests"""
    print("="*60)
    print("Heck-CheckOS ISO Builder - Integration Test Suite")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Import Test", test_imports()))
    results.append(("Keyboard Creation", test_keyboard_creation()))
    results.append(("Calibration Wizard", test_calibration()))
    results.append(("Layout Designer", test_layout_designer()))
    results.append(("Main GUI Integration", test_main_gui_integration()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{name:30s} {status}")
    
    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
