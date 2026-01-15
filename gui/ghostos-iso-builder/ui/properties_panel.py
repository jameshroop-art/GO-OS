"""
Properties Panel - Inspector for selected UI elements
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QScrollArea, QLineEdit, QSpinBox, QComboBox,
                              QPushButton, QGroupBox, QColorDialog, QFrame,
                              QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor


class PropertyEditor(QWidget):
    """Base class for property editors"""
    
    value_changed = pyqtSignal(str, object)
    
    def __init__(self, property_name, label):
        super().__init__()
        self.property_name = property_name
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        
        label_widget = QLabel(label + ":")
        label_widget.setMinimumWidth(100)
        layout.addWidget(label_widget)
        
        self.setup_editor(layout)
        
    def setup_editor(self, layout):
        """Override to add editor widget"""
        pass
        
    def get_value(self):
        """Override to return current value"""
        return None
        
    def set_value(self, value):
        """Override to set value"""
        pass


class TextPropertyEditor(PropertyEditor):
    """Editor for text properties"""
    
    def setup_editor(self, layout):
        self.editor = QLineEdit()
        self.editor.textChanged.connect(lambda: self.value_changed.emit(
            self.property_name, self.editor.text()
        ))
        layout.addWidget(self.editor)
        
    def get_value(self):
        return self.editor.text()
        
    def set_value(self, value):
        self.editor.setText(str(value))


class NumberPropertyEditor(PropertyEditor):
    """Editor for numeric properties"""
    
    def setup_editor(self, layout):
        self.editor = QSpinBox()
        self.editor.setRange(-9999, 9999)
        self.editor.valueChanged.connect(lambda: self.value_changed.emit(
            self.property_name, self.editor.value()
        ))
        layout.addWidget(self.editor)
        
    def get_value(self):
        return self.editor.value()
        
    def set_value(self, value):
        self.editor.setValue(int(value))


class ColorPropertyEditor(PropertyEditor):
    """Editor for color properties"""
    
    def setup_editor(self, layout):
        self.color = QColor("#ffffff")
        
        self.color_display = QFrame()
        self.color_display.setFixedSize(30, 20)
        self.color_display.setStyleSheet(f"background-color: {self.color.name()}; border: 1px solid #3d3d3d;")
        layout.addWidget(self.color_display)
        
        pick_btn = QPushButton("Pick")
        pick_btn.clicked.connect(self.pick_color)
        layout.addWidget(pick_btn)
        
        layout.addStretch()
        
    def pick_color(self):
        color = QColorDialog.getColor(self.color, self, "Select Color")
        if color.isValid():
            self.color = color
            self.color_display.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #3d3d3d;")
            self.value_changed.emit(self.property_name, color.name())
            
    def get_value(self):
        return self.color.name()
        
    def set_value(self, value):
        self.color = QColor(value)
        self.color_display.setStyleSheet(f"background-color: {value}; border: 1px solid #3d3d3d;")


class ChoicePropertyEditor(PropertyEditor):
    """Editor for choice properties"""
    
    def __init__(self, property_name, label, choices):
        self.choices = choices
        super().__init__(property_name, label)
        
    def setup_editor(self, layout):
        self.editor = QComboBox()
        self.editor.addItems(self.choices)
        self.editor.currentTextChanged.connect(lambda: self.value_changed.emit(
            self.property_name, self.editor.currentText()
        ))
        layout.addWidget(self.editor)
        
    def get_value(self):
        return self.editor.currentText()
        
    def set_value(self, value):
        index = self.editor.findText(str(value))
        if index >= 0:
            self.editor.setCurrentIndex(index)


class BoolPropertyEditor(PropertyEditor):
    """Editor for boolean properties"""
    
    def setup_editor(self, layout):
        self.editor = QCheckBox()
        self.editor.stateChanged.connect(lambda: self.value_changed.emit(
            self.property_name, self.editor.isChecked()
        ))
        layout.addWidget(self.editor)
        layout.addStretch()
        
    def get_value(self):
        return self.editor.isChecked()
        
    def set_value(self, value):
        self.editor.setChecked(bool(value))


class PropertiesPanel(QWidget):
    """Properties inspector panel for selected elements"""
    
    property_changed = pyqtSignal(str, object)
    
    def __init__(self):
        super().__init__()
        self.current_element = None
        self.property_editors = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the properties panel interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QLabel("Properties")
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Scroll area for properties
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.properties_container = QWidget()
        self.properties_layout = QVBoxLayout(self.properties_container)
        self.properties_layout.setContentsMargins(5, 5, 5, 5)
        
        # No selection label
        self.no_selection_label = QLabel("No element selected")
        self.no_selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_selection_label.setStyleSheet("color: #888888; padding: 20px;")
        self.properties_layout.addWidget(self.no_selection_label)
        
        self.properties_layout.addStretch()
        
        scroll.setWidget(self.properties_container)
        layout.addWidget(scroll)
        
        # Style
        self.setStyleSheet("""
            QScrollArea {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
            }
            QLineEdit, QSpinBox, QComboBox {
                background-color: #252525;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
                padding: 3px;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
                padding: 3px 8px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)
        
    def set_element(self, element):
        """Set the element to display properties for"""
        self.current_element = element
        self.property_editors = {}
        
        # Clear existing properties
        for i in reversed(range(self.properties_layout.count())):
            widget = self.properties_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
                
        if not element:
            self.no_selection_label = QLabel("No element selected")
            self.no_selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.no_selection_label.setStyleSheet("color: #888888; padding: 20px;")
            self.properties_layout.addWidget(self.no_selection_label)
            self.properties_layout.addStretch()
            return
            
        # Element info
        info_group = QGroupBox(f"{element.get('type', 'Element')} Properties")
        info_layout = QVBoxLayout(info_group)
        
        # Add property editors based on element type
        self.add_common_properties(info_layout, element)
        self.add_type_specific_properties(info_layout, element)
        
        self.properties_layout.addWidget(info_group)
        self.properties_layout.addStretch()
        
    def add_common_properties(self, layout, element):
        """Add common properties for all elements"""
        # Position
        x_editor = NumberPropertyEditor("x", "X")
        x_editor.set_value(element.get('x', 0))
        x_editor.value_changed.connect(self.on_property_changed)
        layout.addWidget(x_editor)
        self.property_editors['x'] = x_editor
        
        y_editor = NumberPropertyEditor("y", "Y")
        y_editor.set_value(element.get('y', 0))
        y_editor.value_changed.connect(self.on_property_changed)
        layout.addWidget(y_editor)
        self.property_editors['y'] = y_editor
        
        # Size
        width_editor = NumberPropertyEditor("width", "Width")
        width_editor.set_value(element.get('width', 100))
        width_editor.value_changed.connect(self.on_property_changed)
        layout.addWidget(width_editor)
        self.property_editors['width'] = width_editor
        
        height_editor = NumberPropertyEditor("height", "Height")
        height_editor.set_value(element.get('height', 100))
        height_editor.value_changed.connect(self.on_property_changed)
        layout.addWidget(height_editor)
        self.property_editors['height'] = height_editor
        
    def add_type_specific_properties(self, layout, element):
        """Add properties specific to element type"""
        element_type = element.get('type', '')
        
        if element_type in ['button', 'label']:
            text_editor = TextPropertyEditor("text", "Text")
            text_editor.set_value(element.get('text', ''))
            text_editor.value_changed.connect(self.on_property_changed)
            layout.addWidget(text_editor)
            self.property_editors['text'] = text_editor
            
        if element_type == 'button':
            enabled_editor = BoolPropertyEditor("enabled", "Enabled")
            enabled_editor.set_value(element.get('enabled', True))
            enabled_editor.value_changed.connect(self.on_property_changed)
            layout.addWidget(enabled_editor)
            self.property_editors['enabled'] = enabled_editor
            
        # Background color
        bg_color_editor = ColorPropertyEditor("background_color", "Background")
        bg_color_editor.set_value(element.get('background_color', '#2d2d2d'))
        bg_color_editor.value_changed.connect(self.on_property_changed)
        layout.addWidget(bg_color_editor)
        self.property_editors['background_color'] = bg_color_editor
        
        # Border
        border_width_editor = NumberPropertyEditor("border_width", "Border Width")
        border_width_editor.set_value(element.get('border_width', 1))
        border_width_editor.value_changed.connect(self.on_property_changed)
        layout.addWidget(border_width_editor)
        self.property_editors['border_width'] = border_width_editor
        
        border_color_editor = ColorPropertyEditor("border_color", "Border Color")
        border_color_editor.set_value(element.get('border_color', '#3d3d3d'))
        border_color_editor.value_changed.connect(self.on_property_changed)
        layout.addWidget(border_color_editor)
        self.property_editors['border_color'] = border_color_editor
        
        # Border radius
        radius_editor = NumberPropertyEditor("border_radius", "Border Radius")
        radius_editor.set_value(element.get('border_radius', 0))
        radius_editor.value_changed.connect(self.on_property_changed)
        layout.addWidget(radius_editor)
        self.property_editors['border_radius'] = radius_editor
        
    def on_property_changed(self, property_name, value):
        """Handle property value change"""
        if self.current_element:
            self.current_element[property_name] = value
            self.property_changed.emit(property_name, value)
            
    def get_properties(self):
        """Get all current properties"""
        return {name: editor.get_value() for name, editor in self.property_editors.items()}
