#!/usr/bin/env python3
"""
Touchscreen Keyboard Widget
Resizable, snapping virtual keyboard with calibration support
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional

try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                                  QPushButton, QLabel, QFrame, QSizeGrip, 
                                  QApplication, QMenu)
    from PyQt6.QtCore import Qt, QPoint, QRect, QSize, pyqtSignal, QTimer
    from PyQt6.QtGui import QFont, QCursor, QPalette, QColor, QPainter, QMouseEvent
except ImportError:
    print("Error: PyQt6 not found. Install with: pip3 install PyQt6")
    raise


class KeyboardKey(QPushButton):
    """Individual keyboard key with customization support"""
    
    def __init__(self, text: str, value: str = None, width_multiplier: float = 1.0):
        super().__init__(text)
        self.key_value = value or text
        self.width_multiplier = width_multiplier
        self.base_width = 50
        self.base_height = 50
        
        # Apply default styling
        self.apply_default_style()
        
    def apply_default_style(self):
        """Apply default key styling"""
        self.setMinimumSize(int(self.base_width * self.width_multiplier), self.base_height)
        self.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border: 1px solid #0078d4;
            }
            QPushButton:pressed {
                background-color: #0078d4;
                color: white;
            }
        """)


class TouchscreenKeyboard(QWidget):
    """Resizable and snappable touchscreen keyboard widget"""
    
    # Signals
    key_pressed = pyqtSignal(str)  # Emits the key value
    keyboard_hidden = pyqtSignal()
    position_changed = pyqtSignal(QPoint)
    
    # Snap settings
    SNAP_DISTANCE = 20  # pixels from edge to trigger snap
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Window flags for floating keyboard
        self.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # Keyboard state
        self.is_shift_active = False
        self.is_caps_lock = False
        self.current_layout = "qwerty"
        self.calibration_offset = QPoint(0, 0)
        self.is_dragging = False
        self.drag_position = QPoint()
        
        # Snapping state
        self.snapped_edge = None  # 'top', 'bottom', 'left', 'right', or None
        
        # Initialize UI
        self.setup_ui()
        self.load_calibration()
        
        # Set default size and position
        self.resize(800, 280)
        self.center_on_screen()
        
    def setup_ui(self):
        """Setup the keyboard UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(2)
        
        # Title bar with drag handle and controls
        title_bar = self.create_title_bar()
        main_layout.addWidget(title_bar)
        
        # Keyboard layout container
        self.keyboard_container = QWidget()
        self.keyboard_layout = QVBoxLayout(self.keyboard_container)
        self.keyboard_layout.setSpacing(2)
        self.keyboard_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create keyboard layouts
        self.create_qwerty_layout()
        
        main_layout.addWidget(self.keyboard_container)
        
        # Apply styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border: 2px solid #0078d4;
                border-radius: 6px;
            }
        """)
        
    def create_title_bar(self):
        """Create title bar with controls"""
        title_bar = QFrame()
        title_bar.setFixedHeight(30)
        title_bar.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: none;
                border-bottom: 1px solid #3d3d3d;
            }
        """)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(5, 0, 5, 0)
        
        # Drag handle
        drag_label = QLabel("⋮⋮ Virtual Keyboard")
        drag_label.setStyleSheet("color: #e0e0e0; font-weight: bold;")
        layout.addWidget(drag_label)
        
        layout.addStretch()
        
        # Layout selector
        layout_btn = QPushButton("⌨")
        layout_btn.setFixedSize(24, 24)
        layout_btn.setToolTip("Change Layout")
        layout_btn.clicked.connect(self.show_layout_menu)
        layout.addWidget(layout_btn)
        
        # Settings button
        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(24, 24)
        settings_btn.setToolTip("Keyboard Settings")
        settings_btn.clicked.connect(self.show_settings_menu)
        layout.addWidget(settings_btn)
        
        # Calibrate button
        calibrate_btn = QPushButton("🎯")
        calibrate_btn.setFixedSize(24, 24)
        calibrate_btn.setToolTip("Calibrate Touch")
        calibrate_btn.clicked.connect(self.start_calibration)
        layout.addWidget(calibrate_btn)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.setToolTip("Hide Keyboard")
        close_btn.clicked.connect(self.hide_keyboard)
        layout.addWidget(close_btn)
        
        return title_bar
        
    def create_qwerty_layout(self):
        """Create standard QWERTY keyboard layout"""
        # Clear existing layout
        while self.keyboard_layout.count():
            child = self.keyboard_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Row 1: Numbers
        row1 = QHBoxLayout()
        row1.setSpacing(2)
        for key in ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=']:
            btn = KeyboardKey(key)
            btn.clicked.connect(lambda checked, k=key: self.on_key_click(k))
            row1.addWidget(btn)
        
        backspace = KeyboardKey("⌫", "\b", 1.5)
        backspace.clicked.connect(lambda: self.on_key_click("\b"))
        row1.addWidget(backspace)
        self.keyboard_layout.addLayout(row1)
        
        # Row 2: QWERTY
        row2 = QHBoxLayout()
        row2.setSpacing(2)
        tab = KeyboardKey("Tab", "\t", 1.3)
        tab.clicked.connect(lambda: self.on_key_click("\t"))
        row2.addWidget(tab)
        
        for key in ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\']:
            btn = KeyboardKey(key.upper() if self.is_caps_lock or self.is_shift_active else key)
            btn.clicked.connect(lambda checked, k=key: self.on_letter_click(k))
            row2.addWidget(btn)
        self.keyboard_layout.addLayout(row2)
        
        # Row 3: ASDFGH
        row3 = QHBoxLayout()
        row3.setSpacing(2)
        caps = KeyboardKey("Caps", "", 1.5)
        caps.clicked.connect(self.toggle_caps_lock)
        if self.is_caps_lock:
            caps.setStyleSheet(caps.styleSheet() + "QPushButton { background-color: #0078d4; }")
        row3.addWidget(caps)
        
        for key in ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'']:
            btn = KeyboardKey(key.upper() if self.is_caps_lock or self.is_shift_active else key)
            btn.clicked.connect(lambda checked, k=key: self.on_letter_click(k))
            row3.addWidget(btn)
        
        enter = KeyboardKey("Enter", "\n", 1.8)
        enter.clicked.connect(lambda: self.on_key_click("\n"))
        row3.addWidget(enter)
        self.keyboard_layout.addLayout(row3)
        
        # Row 4: ZXCVBN
        row4 = QHBoxLayout()
        row4.setSpacing(2)
        shift = KeyboardKey("Shift", "", 2.0)
        shift.clicked.connect(self.toggle_shift)
        if self.is_shift_active:
            shift.setStyleSheet(shift.styleSheet() + "QPushButton { background-color: #0078d4; }")
        row4.addWidget(shift)
        
        for key in ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']:
            btn = KeyboardKey(key.upper() if self.is_caps_lock or self.is_shift_active else key)
            btn.clicked.connect(lambda checked, k=key: self.on_letter_click(k))
            row4.addWidget(btn)
        
        shift_r = KeyboardKey("Shift", "", 2.0)
        shift_r.clicked.connect(self.toggle_shift)
        row4.addWidget(shift_r)
        self.keyboard_layout.addLayout(row4)
        
        # Row 5: Space bar
        row5 = QHBoxLayout()
        row5.setSpacing(2)
        
        ctrl = KeyboardKey("Ctrl", "", 1.5)
        ctrl.setEnabled(False)  # Disabled - modifier key support coming soon
        row5.addWidget(ctrl)
        
        alt = KeyboardKey("Alt", "", 1.5)
        alt.setEnabled(False)  # Disabled - modifier key support coming soon
        row5.addWidget(alt)
        
        space = KeyboardKey("Space", " ", 7.0)
        space.clicked.connect(lambda: self.on_key_click(" "))
        row5.addWidget(space)
        
        alt_r = KeyboardKey("Alt", "", 1.5)
        alt_r.setEnabled(False)  # Disabled - modifier key support coming soon
        row5.addWidget(alt_r)
        
        ctrl_r = KeyboardKey("Ctrl", "", 1.5)
        ctrl_r.setEnabled(False)  # Disabled - modifier key support coming soon
        row5.addWidget(ctrl_r)
        
        self.keyboard_layout.addLayout(row5)
        
    def on_key_click(self, key: str):
        """Handle key click"""
        self.key_pressed.emit(key)
        
        # Reset shift after keypress (but not caps lock)
        if self.is_shift_active and not self.is_caps_lock:
            self.is_shift_active = False
            self.create_qwerty_layout()
            
    def on_letter_click(self, key: str):
        """Handle letter key click"""
        if self.is_caps_lock or self.is_shift_active:
            key = key.upper()
        self.on_key_click(key)
        
    def toggle_shift(self):
        """Toggle shift key"""
        self.is_shift_active = not self.is_shift_active
        self.create_qwerty_layout()
        
    def toggle_caps_lock(self):
        """Toggle caps lock"""
        self.is_caps_lock = not self.is_caps_lock
        self.is_shift_active = False
        self.create_qwerty_layout()
        
    def show_layout_menu(self):
        """Show layout selection menu"""
        menu = QMenu(self)
        menu.addAction("QWERTY", lambda: self.change_layout("qwerty"))
        menu.addAction("Numeric Keypad", lambda: self.change_layout("numpad"))
        menu.addAction("Custom Layout", lambda: self.open_layout_designer())
        menu.exec(QCursor.pos())
        
    def show_settings_menu(self):
        """Show settings menu"""
        menu = QMenu(self)
        menu.addAction("🎨 Customize Theme", self.customize_theme)
        menu.addAction("📐 Resize Keyboard", self.resize_keyboard)
        menu.addAction("🎯 Calibrate Touch", self.start_calibration)
        menu.addAction("💾 Save Layout", self.save_layout)
        menu.addAction("📂 Load Layout", self.load_layout)
        menu.exec(QCursor.pos())
        
    def change_layout(self, layout: str):
        """Change keyboard layout"""
        self.current_layout = layout
        if layout == "qwerty":
            self.create_qwerty_layout()
        elif layout == "numpad":
            self.create_numpad_layout()
            
    def create_numpad_layout(self):
        """Create numeric keypad layout"""
        # Clear existing layout
        while self.keyboard_layout.count():
            child = self.keyboard_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Numpad layout
        grid = QGridLayout()
        grid.setSpacing(2)
        
        keys = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ]
        
        for row_idx, row in enumerate(keys):
            for col_idx, key in enumerate(row):
                btn = KeyboardKey(key, width_multiplier=1.5)
                btn.clicked.connect(lambda checked, k=key: self.on_key_click(k))
                grid.addWidget(btn, row_idx, col_idx)
        
        # Enter key spans 2 rows
        enter = KeyboardKey("Enter", "\n", 1.5)
        enter.clicked.connect(lambda: self.on_key_click("\n"))
        grid.addWidget(enter, 2, 4, 2, 1)
        
        # Backspace
        backspace = KeyboardKey("⌫", "\b", 1.5)
        backspace.clicked.connect(lambda: self.on_key_click("\b"))
        grid.addWidget(backspace, 0, 4)
        
        # Clear
        clear = KeyboardKey("C", "", 1.5)
        clear.clicked.connect(lambda: self.on_key_click("\x08" * 10))  # Send 10 backspaces
        clear.setToolTip("Clear (10 backspaces)")
        grid.addWidget(clear, 1, 4)
        
        self.keyboard_layout.addLayout(grid)
        
    def hide_keyboard(self):
        """Hide the keyboard"""
        self.hide()
        self.keyboard_hidden.emit()
        
    def show_keyboard(self):
        """Show the keyboard"""
        self.show()
        self.raise_()
        self.activateWindow()
        
    def center_on_screen(self):
        """Center keyboard on screen"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = screen.height() - self.height() - 50  # 50px from bottom
        self.move(x, y)
        
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if clicking on title bar area (top 30px)
            if event.position().y() < 30:
                self.is_dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()
                
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move for dragging"""
        if self.is_dragging and event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_position
            
            # Apply calibration offset
            new_pos += self.calibration_offset
            
            # Check for edge snapping
            screen = QApplication.primaryScreen().geometry()
            snapped_pos = self.check_snap_edges(new_pos, screen)
            
            self.move(snapped_pos)
            self.position_changed.emit(snapped_pos)
            event.accept()
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            event.accept()
            
    def check_snap_edges(self, pos: QPoint, screen: QRect) -> QPoint:
        """Check if keyboard should snap to screen edges"""
        snapped = QPoint(pos)
        
        # Check left edge
        if pos.x() < self.SNAP_DISTANCE:
            snapped.setX(0)
            self.snapped_edge = 'left'
        # Check right edge
        elif pos.x() + self.width() > screen.width() - self.SNAP_DISTANCE:
            snapped.setX(screen.width() - self.width())
            self.snapped_edge = 'right'
        else:
            self.snapped_edge = None
            
        # Check top edge
        if pos.y() < self.SNAP_DISTANCE:
            snapped.setY(0)
            self.snapped_edge = 'top'
        # Check bottom edge
        elif pos.y() + self.height() > screen.height() - self.SNAP_DISTANCE:
            snapped.setY(screen.height() - self.height())
            self.snapped_edge = 'bottom'
            
        return snapped
        
    def start_calibration(self):
        """Start touch calibration process"""
        from ui.calibration_wizard import CalibrationWizard
        wizard = CalibrationWizard(self)
        if wizard.exec():
            self.calibration_offset = wizard.get_offset()
            self.save_calibration()
            
    def save_calibration(self):
        """Save calibration data"""
        config_dir = Path.home() / ".config" / "heckcheckos-builder"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        calibration_file = config_dir / "keyboard_calibration.json"
        calibration_data = {
            'offset_x': self.calibration_offset.x(),
            'offset_y': self.calibration_offset.y()
        }
        
        with open(calibration_file, 'w') as f:
            json.dump(calibration_data, f, indent=2)
            
    def load_calibration(self):
        """Load calibration data"""
        config_dir = Path.home() / ".config" / "heckcheckos-builder"
        calibration_file = config_dir / "keyboard_calibration.json"
        
        if calibration_file.exists():
            try:
                with open(calibration_file, 'r') as f:
                    data = json.load(f)
                    self.calibration_offset = QPoint(
                        data.get('offset_x', 0),
                        data.get('offset_y', 0)
                    )
            except Exception as e:
                print(f"Failed to load calibration: {e}")
                
    def save_layout(self):
        """Save current keyboard layout"""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        from pathlib import Path
        import json
        
        config_dir = Path.home() / ".config" / "heckcheckos-builder" / "keyboard_layouts"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Keyboard Layout",
            str(config_dir / "custom_layout.json"),
            "JSON Files (*.json)"
        )
        
        if file_path:
            layout_data = {
                'name': self.current_layout,
                'version': '1.0',
                'layout_type': self.current_layout
            }
            with open(file_path, 'w') as f:
                json.dump(layout_data, f, indent=2)
            QMessageBox.information(self, "Saved", f"Layout saved to:\n{file_path}")
        
    def load_layout(self):
        """Load keyboard layout"""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        from pathlib import Path
        import json
        
        config_dir = Path.home() / ".config" / "heckcheckos-builder" / "keyboard_layouts"
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Keyboard Layout",
            str(config_dir),
            "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    layout_data = json.load(f)
                layout_type = layout_data.get('layout_type', 'qwerty')
                self.change_layout(layout_type)
                QMessageBox.information(self, "Loaded", f"Layout loaded from:\n{file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load layout:\n{e}")
        
    def customize_theme(self):
        """Open theme customization"""
        # Placeholder for theme customization
        print("Theme customization not yet implemented")
        
    def resize_keyboard(self):
        """Resize keyboard"""
        # Placeholder for resize dialog
        print("Resize dialog not yet implemented")
        
    def open_layout_designer(self):
        """Open keyboard layout designer"""
        from ui.keyboard_designer import KeyboardLayoutDesigner
        designer = KeyboardLayoutDesigner(self)
        if designer.exec():
            # Apply the custom layout
            layout_data = designer.get_layout()
            # TODO: Implement custom layout rendering
            print(f"Custom layout created: {layout_data.get('name', 'Unnamed')}")
