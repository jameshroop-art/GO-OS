#!/usr/bin/env python3
"""
Keyboard Layout Designer
Visual editor for creating and customizing keyboard layouts
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
                              QPushButton, QLabel, QLineEdit, QSpinBox, 
                              QColorDialog, QFileDialog, QMessageBox, QFrame,
                              QScrollArea, QWidget, QComboBox, QGroupBox)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QColor, QFont


class KeyDesigner(QFrame):
    """Widget for designing individual key properties"""
    
    properties_changed = pyqtSignal(dict)
    
    def __init__(self, key_data: dict = None):
        super().__init__()
        self.key_data = key_data or {
            'label': 'Key',
            'value': 'k',
            'width': 1.0,
            'height': 1.0,
            'bg_color': '#2d2d2d',
            'fg_color': '#e0e0e0',
            'font_size': 11
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup key designer UI"""
        layout = QVBoxLayout(self)
        
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 10px;
            }
            QLabel {
                color: #e0e0e0;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        
        # Title
        title = QLabel("Key Properties")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Label
        label_layout = QHBoxLayout()
        label_layout.addWidget(QLabel("Label:"))
        self.label_input = QLineEdit(self.key_data['label'])
        self.label_input.textChanged.connect(self.on_property_changed)
        label_layout.addWidget(self.label_input)
        layout.addLayout(label_layout)
        
        # Value
        value_layout = QHBoxLayout()
        value_layout.addWidget(QLabel("Value:"))
        self.value_input = QLineEdit(self.key_data['value'])
        self.value_input.textChanged.connect(self.on_property_changed)
        value_layout.addWidget(self.value_input)
        layout.addLayout(value_layout)
        
        # Width
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width:"))
        self.width_input = QSpinBox()
        self.width_input.setRange(1, 10)
        self.width_input.setValue(int(self.key_data['width']))
        self.width_input.setSuffix("x")
        self.width_input.valueChanged.connect(self.on_property_changed)
        width_layout.addWidget(self.width_input)
        layout.addLayout(width_layout)
        
        # Font size
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font Size:"))
        self.font_input = QSpinBox()
        self.font_input.setRange(8, 20)
        self.font_input.setValue(self.key_data['font_size'])
        self.font_input.setSuffix("pt")
        self.font_input.valueChanged.connect(self.on_property_changed)
        font_layout.addWidget(self.font_input)
        layout.addLayout(font_layout)
        
        # Colors
        color_group = QGroupBox("Colors")
        color_layout = QVBoxLayout(color_group)
        
        bg_layout = QHBoxLayout()
        bg_layout.addWidget(QLabel("Background:"))
        self.bg_color_btn = QPushButton()
        self.bg_color_btn.setFixedSize(60, 25)
        self.update_color_button(self.bg_color_btn, self.key_data['bg_color'])
        self.bg_color_btn.clicked.connect(self.choose_bg_color)
        bg_layout.addWidget(self.bg_color_btn)
        bg_layout.addStretch()
        color_layout.addLayout(bg_layout)
        
        fg_layout = QHBoxLayout()
        fg_layout.addWidget(QLabel("Text:"))
        self.fg_color_btn = QPushButton()
        self.fg_color_btn.setFixedSize(60, 25)
        self.update_color_button(self.fg_color_btn, self.key_data['fg_color'])
        self.fg_color_btn.clicked.connect(self.choose_fg_color)
        fg_layout.addWidget(self.fg_color_btn)
        fg_layout.addStretch()
        color_layout.addLayout(fg_layout)
        
        layout.addWidget(color_group)
        
        layout.addStretch()
        
    def update_color_button(self, button: QPushButton, color: str):
        """Update color button appearance"""
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: 1px solid #3d3d3d;
                border-radius: 3px;
            }}
        """)
        
    def choose_bg_color(self):
        """Choose background color"""
        color = QColorDialog.getColor(
            QColor(self.key_data['bg_color']),
            self,
            "Choose Background Color"
        )
        if color.isValid():
            self.key_data['bg_color'] = color.name()
            self.update_color_button(self.bg_color_btn, color.name())
            self.on_property_changed()
            
    def choose_fg_color(self):
        """Choose foreground color"""
        color = QColorDialog.getColor(
            QColor(self.key_data['fg_color']),
            self,
            "Choose Text Color"
        )
        if color.isValid():
            self.key_data['fg_color'] = color.name()
            self.update_color_button(self.fg_color_btn, color.name())
            self.on_property_changed()
            
    def on_property_changed(self):
        """Handle property change"""
        self.key_data['label'] = self.label_input.text()
        self.key_data['value'] = self.value_input.text()
        self.key_data['width'] = float(self.width_input.value())
        self.key_data['font_size'] = self.font_input.value()
        
        self.properties_changed.emit(self.key_data)
        
    def get_key_data(self) -> dict:
        """Get current key data"""
        return self.key_data
        
    def refresh_properties(self, key_data: dict):
        """Refresh property fields without recreating UI"""
        self.key_data = key_data
        self.label_input.setText(key_data.get('label', ''))
        self.value_input.setText(key_data.get('value', ''))
        self.width_input.setValue(int(key_data.get('width', 1.0)))
        self.font_input.setValue(key_data.get('font_size', 11))
        self.update_color_button(self.bg_color_btn, key_data.get('bg_color', '#2d2d2d'))
        self.update_color_button(self.fg_color_btn, key_data.get('fg_color', '#e0e0e0'))


class KeyboardLayoutDesigner(QDialog):
    """Visual keyboard layout designer and editor"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Keyboard Layout Designer")
        self.setMinimumSize(1200, 700)
        
        # Layout data
        self.current_layout = {
            'name': 'Custom Layout',
            'rows': []
        }
        self.selected_key = None
        
        self.setup_ui()
        self.load_default_layout()
        
    def setup_ui(self):
        """Setup designer UI"""
        main_layout = QHBoxLayout(self)
        
        # Apply styling
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QGroupBox {
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        # Left panel - Layout canvas
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Layout info
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel("Layout Name:"))
        self.layout_name_input = QLineEdit("Custom Layout")
        info_layout.addWidget(self.layout_name_input)
        left_layout.addLayout(info_layout)
        
        # Canvas scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #252525;
                border: 1px solid #3d3d3d;
            }
        """)
        
        self.canvas = QWidget()
        self.canvas_layout = QVBoxLayout(self.canvas)
        self.canvas_layout.setSpacing(5)
        scroll_area.setWidget(self.canvas)
        
        left_layout.addWidget(scroll_area, 1)
        
        # Canvas controls
        canvas_controls = QHBoxLayout()
        
        add_row_btn = QPushButton("➕ Add Row")
        add_row_btn.clicked.connect(self.add_row)
        canvas_controls.addWidget(add_row_btn)
        
        remove_row_btn = QPushButton("➖ Remove Row")
        remove_row_btn.clicked.connect(self.remove_row)
        canvas_controls.addWidget(remove_row_btn)
        
        canvas_controls.addStretch()
        
        preview_btn = QPushButton("👁 Preview")
        preview_btn.clicked.connect(self.preview_layout)
        canvas_controls.addWidget(preview_btn)
        
        left_layout.addLayout(canvas_controls)
        
        main_layout.addWidget(left_panel, 2)
        
        # Right panel - Properties and tools
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_panel.setMaximumWidth(350)
        
        # Key designer
        self.key_designer = KeyDesigner()
        self.key_designer.properties_changed.connect(self.on_key_properties_changed)
        right_layout.addWidget(self.key_designer)
        
        # Preset layouts
        preset_group = QGroupBox("Load Preset")
        preset_layout = QVBoxLayout(preset_group)
        
        preset_combo = QComboBox()
        preset_combo.addItems([
            "QWERTY Full",
            "QWERTY Compact",
            "Numeric Keypad",
            "Gaming (WASD Focus)",
            "Programming",
            "Custom..."
        ])
        preset_combo.currentTextChanged.connect(self.load_preset)
        preset_layout.addWidget(preset_combo)
        
        right_layout.addWidget(preset_group)
        
        right_layout.addStretch()
        
        # Action buttons
        action_layout = QVBoxLayout()
        
        save_btn = QPushButton("💾 Save Layout")
        save_btn.clicked.connect(self.save_layout)
        action_layout.addWidget(save_btn)
        
        load_btn = QPushButton("📂 Load Layout")
        load_btn.clicked.connect(self.load_layout)
        action_layout.addWidget(load_btn)
        
        export_btn = QPushButton("📤 Export")
        export_btn.clicked.connect(self.export_layout)
        action_layout.addWidget(export_btn)
        
        apply_btn = QPushButton("✓ Apply & Close")
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
        """)
        apply_btn.clicked.connect(self.accept)
        action_layout.addWidget(apply_btn)
        
        cancel_btn = QPushButton("✕ Cancel")
        cancel_btn.clicked.connect(self.reject)
        action_layout.addWidget(cancel_btn)
        
        right_layout.addLayout(action_layout)
        
        main_layout.addWidget(right_panel)
        
    def load_default_layout(self):
        """Load default QWERTY layout"""
        self.current_layout = {
            'name': 'QWERTY Full',
            'rows': [
                [
                    {'label': '`', 'value': '`', 'width': 1.0},
                    {'label': '1', 'value': '1', 'width': 1.0},
                    {'label': '2', 'value': '2', 'width': 1.0},
                    {'label': '3', 'value': '3', 'width': 1.0},
                    {'label': '4', 'value': '4', 'width': 1.0},
                    {'label': '5', 'value': '5', 'width': 1.0},
                    {'label': '6', 'value': '6', 'width': 1.0},
                    {'label': '7', 'value': '7', 'width': 1.0},
                    {'label': '8', 'value': '8', 'width': 1.0},
                    {'label': '9', 'value': '9', 'width': 1.0},
                    {'label': '0', 'value': '0', 'width': 1.0},
                    {'label': '-', 'value': '-', 'width': 1.0},
                    {'label': '=', 'value': '=', 'width': 1.0},
                    {'label': '⌫', 'value': '\\b', 'width': 1.5},
                ]
            ]
        }
        self.render_canvas()
        
    def render_canvas(self):
        """Render keyboard layout on canvas"""
        # Clear existing widgets
        while self.canvas_layout.count():
            child = self.canvas_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # Render each row
        for row_idx, row in enumerate(self.current_layout.get('rows', [])):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setSpacing(2)
            row_layout.setContentsMargins(0, 0, 0, 0)
            
            for key_idx, key_data in enumerate(row):
                key_btn = QPushButton(key_data.get('label', ''))
                width = int(50 * key_data.get('width', 1.0))
                key_btn.setMinimumSize(width, 50)
                key_btn.setMaximumSize(width, 50)
                key_btn.clicked.connect(
                    lambda checked, r=row_idx, k=key_idx: self.select_key(r, k)
                )
                row_layout.addWidget(key_btn)
                
            row_layout.addStretch()
            self.canvas_layout.addWidget(row_widget)
            
        self.canvas_layout.addStretch()
        
    def update_single_key(self, row_idx: int, key_idx: int, key_data: dict):
        """Update a single key without recreating entire canvas"""
        # Find the specific key widget and update it
        if row_idx >= self.canvas_layout.count():
            # Row doesn't exist, fall back to full render
            self.render_canvas()
            return
        
        # Get the row widget
        row_item = self.canvas_layout.itemAt(row_idx)
        if not row_item or not row_item.widget():
            self.render_canvas()
            return
        
        row_widget = row_item.widget()
        row_layout = row_widget.layout()
        
        if not row_layout or key_idx >= row_layout.count():
            self.render_canvas()
            return
        
        # Get the key button
        key_item = row_layout.itemAt(key_idx)
        if not key_item or not key_item.widget():
            self.render_canvas()
            return
        
        key_btn = key_item.widget()
        if not isinstance(key_btn, QPushButton):
            self.render_canvas()
            return
        
        # Update the button properties efficiently
        key_btn.setText(key_data.get('label', ''))
        width = int(50 * key_data.get('width', 1.0))
        key_btn.setMinimumSize(width, 50)
        key_btn.setMaximumSize(width, 50)
        
        # Apply custom styling if colors are specified
        bg_color = key_data.get('bg_color', '#2d2d2d')
        fg_color = key_data.get('fg_color', '#e0e0e0')
        font_size = key_data.get('font_size', 11)
        
        key_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {fg_color};
                font-size: {font_size}pt;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #3d3d3d;
                border: 1px solid #0078d4;
            }}
            QPushButton:pressed {{
                background-color: #0078d4;
                color: white;
            }}
        """)
        
    def add_row(self):
        """Add new row to layout"""
        new_row = [
            {'label': 'A', 'value': 'a', 'width': 1.0},
            {'label': 'B', 'value': 'b', 'width': 1.0},
        ]
        self.current_layout['rows'].append(new_row)
        self.render_canvas()
        
    def remove_row(self):
        """Remove last row from layout"""
        if self.current_layout['rows']:
            self.current_layout['rows'].pop()
            self.render_canvas()
            
    def select_key(self, row_idx: int, key_idx: int):
        """Select a key for editing"""
        if row_idx < len(self.current_layout['rows']):
            row = self.current_layout['rows'][row_idx]
            if key_idx < len(row):
                self.selected_key = (row_idx, key_idx)
                key_data = row[key_idx]
                # Update key designer with selected key data
                self.key_designer.key_data = key_data
                self.key_designer.refresh_properties(key_data)
                
    def refresh_properties(self, key_data: dict):
        """Refresh property fields without recreating UI"""
        self.key_data = key_data
        self.label_input.setText(key_data.get('label', ''))
        self.value_input.setText(key_data.get('value', ''))
        self.width_input.setValue(int(key_data.get('width', 1.0)))
        self.font_input.setValue(key_data.get('font_size', 11))
        self.update_color_button(self.bg_color_btn, key_data.get('bg_color', '#2d2d2d'))
        self.update_color_button(self.fg_color_btn, key_data.get('fg_color', '#e0e0e0'))
                
    def on_key_properties_changed(self, key_data: dict):
        """Handle key property changes"""
        if self.selected_key:
            row_idx, key_idx = self.selected_key
            self.current_layout['rows'][row_idx][key_idx] = key_data
            # Update just the affected key button instead of recreating entire canvas
            self.update_single_key(row_idx, key_idx, key_data)
            
    def load_preset(self, preset_name: str):
        """Load preset layout"""
        # For now, just load default QWERTY
        if "QWERTY" in preset_name:
            self.load_default_layout()
        elif preset_name == "Numeric Keypad":
            self.load_numpad_preset()
            
    def load_numpad_preset(self):
        """Load numeric keypad preset"""
        self.current_layout = {
            'name': 'Numeric Keypad',
            'rows': [
                [
                    {'label': '7', 'value': '7', 'width': 1.0},
                    {'label': '8', 'value': '8', 'width': 1.0},
                    {'label': '9', 'value': '9', 'width': 1.0},
                    {'label': '/', 'value': '/', 'width': 1.0},
                ],
                [
                    {'label': '4', 'value': '4', 'width': 1.0},
                    {'label': '5', 'value': '5', 'width': 1.0},
                    {'label': '6', 'value': '6', 'width': 1.0},
                    {'label': '*', 'value': '*', 'width': 1.0},
                ],
                [
                    {'label': '1', 'value': '1', 'width': 1.0},
                    {'label': '2', 'value': '2', 'width': 1.0},
                    {'label': '3', 'value': '3', 'width': 1.0},
                    {'label': '-', 'value': '-', 'width': 1.0},
                ],
                [
                    {'label': '0', 'value': '0', 'width': 2.0},
                    {'label': '.', 'value': '.', 'width': 1.0},
                    {'label': '+', 'value': '+', 'width': 1.0},
                ]
            ]
        }
        self.render_canvas()
        
    def save_layout(self):
        """Save layout to file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Keyboard Layout",
            str(Path.home() / "keyboard_layout.json"),
            "JSON Files (*.json)"
        )
        
        if file_path:
            self.current_layout['name'] = self.layout_name_input.text()
            with open(file_path, 'w') as f:
                json.dump(self.current_layout, f, indent=2)
            QMessageBox.information(self, "Saved", f"Layout saved to:\n{file_path}")
            
    def load_layout(self):
        """Load layout from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Keyboard Layout",
            str(Path.home()),
            "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    self.current_layout = json.load(f)
                self.layout_name_input.setText(self.current_layout.get('name', 'Custom'))
                self.render_canvas()
                QMessageBox.information(self, "Loaded", f"Layout loaded from:\n{file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load layout:\n{e}")
                
    def export_layout(self):
        """Export layout for distribution"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Keyboard Layout",
            str(Path.home() / "keyboard_layout_export.json"),
            "JSON Files (*.json)"
        )
        
        if file_path:
            export_data = {
                'name': self.layout_name_input.text(),
                'version': '1.0',
                'layout': self.current_layout
            }
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            QMessageBox.information(self, "Exported", f"Layout exported to:\n{file_path}")
            
    def preview_layout(self):
        """Preview the keyboard layout"""
        # This would create a temporary keyboard widget to preview
        QMessageBox.information(
            self,
            "Preview",
            "Preview functionality coming soon!\n"
            "This will show your keyboard in a separate window."
        )
        
    def get_layout(self) -> dict:
        """Get the current layout"""
        return self.current_layout
