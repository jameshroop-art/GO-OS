#!/usr/bin/env python3
"""
Layout Presets Manager - Window ratio presets with draggable splitter
"""

from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QLabel,
                              QFrame, QSplitter)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class LayoutPresetsManager(QWidget):
    """Manager for window layout presets"""
    
    preset_changed = pyqtSignal(str, list)
    
    def __init__(self, splitter):
        super().__init__()
        self.splitter = splitter
        self.default_sizes = None
        self.setup_ui()
        
        # Save default sizes
        if splitter:
            self.default_sizes = splitter.sizes()
            
    def setup_ui(self):
        """Setup preset buttons"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        label = QLabel("Layout:")
        layout.addWidget(label)
        
        # Preset buttons
        presets = [
            ("Default 60/40", [60, 40]),
            ("Preview Focus 40/60", [40, 60]),
            ("Workspace 80/20", [80, 20]),
            ("Balanced 50/50", [50, 50]),
        ]
        
        for name, ratios in presets:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, n=name, r=ratios: self.apply_preset(n, r))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 1px solid #3d3d3d;
                    border-radius: 3px;
                    padding: 5px 10px;
                    font-size: 9pt;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                    border-color: #0078d4;
                }
                QPushButton:pressed {
                    background-color: #252525;
                }
            """)
            layout.addWidget(btn)
            
        layout.addStretch()
        
        # Reset button
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_to_default)
        reset_btn.setToolTip("Double-click splitter to reset as well")
        layout.addWidget(reset_btn)
        
    def apply_preset(self, name, ratios):
        """Apply a layout preset"""
        if not self.splitter:
            return
            
        # Calculate sizes based on total width
        total = self.splitter.width()
        sizes = [int(total * (r / 100)) for r in ratios]
        
        self.splitter.setSizes(sizes)
        self.preset_changed.emit(name, sizes)
        
    def reset_to_default(self):
        """Reset to default layout"""
        if self.splitter and self.default_sizes:
            self.splitter.setSizes(self.default_sizes)
            self.preset_changed.emit("Default", self.default_sizes)


class CustomSplitterHandle(QFrame):
    """Custom splitter handle with visual feedback"""
    
    def __init__(self, orientation, parent=None):
        super().__init__(parent)
        self.orientation = orientation
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setup_style()
        
    def setup_style(self):
        """Setup handle styling"""
        if self.orientation == Qt.Orientation.Horizontal:
            self.setFixedWidth(8)
            self.setCursor(Qt.CursorShape.SplitHCursor)
        else:
            self.setFixedHeight(8)
            self.setCursor(Qt.CursorShape.SplitVCursor)
            
        self.setStyleSheet("""
            QFrame {
                background-color: #3d3d3d;
                border-left: 1px solid #4d4d4d;
                border-right: 1px solid #4d4d4d;
            }
            QFrame:hover {
                background-color: #0078d4;
            }
        """)
        
    def enterEvent(self, event):
        """Handle hover enter"""
        self.setStyleSheet("""
            QFrame {
                background-color: #0078d4;
                border-left: 1px solid #1084d8;
                border-right: 1px solid #1084d8;
            }
        """)
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """Handle hover leave"""
        self.setStyleSheet("""
            QFrame {
                background-color: #3d3d3d;
                border-left: 1px solid #4d4d4d;
                border-right: 1px solid #4d4d4d;
            }
        """)
        super().leaveEvent(event)
