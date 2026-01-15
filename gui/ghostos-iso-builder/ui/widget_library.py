#!/usr/bin/env python3
"""
Widget Library - Drag-and-drop widget library for UI Designer
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QTreeWidget, QTreeWidgetItem, QScrollArea, 
                              QLineEdit, QPushButton, QFrame)
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal, QByteArray
from PyQt6.QtGui import QDrag, QPixmap, QPainter, QColor, QFont


class WidgetLibraryItem(QTreeWidgetItem):
    """Custom tree widget item for draggable widgets"""
    
    def __init__(self, parent, widget_type, display_name, icon=""):
        super().__init__(parent, [f"{icon} {display_name}"])
        self.widget_type = widget_type
        self.display_name = display_name
        self.setToolTip(0, f"Drag to canvas to add {display_name}")


class WidgetLibrary(QWidget):
    """Widget library panel with categories and drag-and-drop"""
    
    widget_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the widget library interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QLabel("Widget Library")
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Search box
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search widgets...")
        self.search_box.textChanged.connect(self.filter_widgets)
        search_layout.addWidget(self.search_box)
        
        clear_btn = QPushButton("×")
        clear_btn.setMaximumWidth(30)
        clear_btn.clicked.connect(lambda: self.search_box.clear())
        search_layout.addWidget(clear_btn)
        
        layout.addLayout(search_layout)
        
        # Widget tree
        self.widget_tree = QTreeWidget()
        self.widget_tree.setHeaderHidden(True)
        self.widget_tree.setDragEnabled(True)
        self.widget_tree.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)
        self.widget_tree.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.widget_tree)
        
        # Populate widgets
        self.populate_widgets()
        
        # Style
        self.setStyleSheet("""
            QTreeWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:hover {
                background-color: #3d3d3d;
            }
            QTreeWidget::item:selected {
                background-color: #0078d4;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        
    def populate_widgets(self):
        """Populate widget library with categories"""
        self.widget_tree.clear()
        
        # Desktop Elements
        desktop_category = QTreeWidgetItem(self.widget_tree, ["🖥️ Desktop Elements"])
        desktop_category.setExpanded(True)
        
        WidgetLibraryItem(desktop_category, "taskbar", "Taskbar", "📊")
        WidgetLibraryItem(desktop_category, "system_tray", "System Tray", "🔔")
        WidgetLibraryItem(desktop_category, "desktop_icon", "Desktop Icon", "📁")
        WidgetLibraryItem(desktop_category, "window", "Window", "🪟")
        WidgetLibraryItem(desktop_category, "menu_bar", "Menu Bar", "☰")
        WidgetLibraryItem(desktop_category, "dock", "Application Dock", "⬜")
        WidgetLibraryItem(desktop_category, "wallpaper", "Wallpaper", "🖼️")
        
        # Control Elements
        control_category = QTreeWidgetItem(self.widget_tree, ["🎛️ Control Elements"])
        control_category.setExpanded(True)
        
        WidgetLibraryItem(control_category, "button", "Button", "🔘")
        WidgetLibraryItem(control_category, "slider", "Slider", "🎚️")
        WidgetLibraryItem(control_category, "checkbox", "Checkbox", "☑️")
        WidgetLibraryItem(control_category, "radio", "Radio Button", "⭕")
        WidgetLibraryItem(control_category, "dropdown", "Dropdown", "▼")
        WidgetLibraryItem(control_category, "text_input", "Text Input", "✏️")
        WidgetLibraryItem(control_category, "toggle", "Toggle Switch", "🔀")
        WidgetLibraryItem(control_category, "spinner", "Spinner", "🔃")
        
        # Containers
        container_category = QTreeWidgetItem(self.widget_tree, ["📦 Containers"])
        container_category.setExpanded(True)
        
        WidgetLibraryItem(container_category, "panel", "Panel", "▭")
        WidgetLibraryItem(container_category, "group_box", "Group Box", "▢")
        WidgetLibraryItem(container_category, "tab_widget", "Tab Widget", "📑")
        WidgetLibraryItem(container_category, "scroll_area", "Scroll Area", "📜")
        WidgetLibraryItem(container_category, "splitter", "Splitter", "⬌")
        WidgetLibraryItem(container_category, "frame", "Frame", "▭")
        
        # Display Elements
        display_category = QTreeWidgetItem(self.widget_tree, ["📺 Display Elements"])
        display_category.setExpanded(True)
        
        WidgetLibraryItem(display_category, "label", "Label", "🏷️")
        WidgetLibraryItem(display_category, "image", "Image", "🖼️")
        WidgetLibraryItem(display_category, "progress_bar", "Progress Bar", "▬")
        WidgetLibraryItem(display_category, "status_bar", "Status Bar", "📊")
        WidgetLibraryItem(display_category, "notification", "Notification", "🔔")
        WidgetLibraryItem(display_category, "tooltip", "Tooltip", "💬")
        
        # Media Elements
        media_category = QTreeWidgetItem(self.widget_tree, ["🎵 Media Elements"])
        media_category.setExpanded(False)
        
        WidgetLibraryItem(media_category, "volume_control", "Volume Control", "🔊")
        WidgetLibraryItem(media_category, "media_player", "Media Player", "▶️")
        WidgetLibraryItem(media_category, "equalizer", "Equalizer", "🎚️")
        
    def filter_widgets(self, text):
        """Filter widgets based on search text"""
        text = text.lower()
        
        for i in range(self.widget_tree.topLevelItemCount()):
            category = self.widget_tree.topLevelItem(i)
            category_visible = False
            
            for j in range(category.childCount()):
                item = category.child(j)
                item_text = item.text(0).lower()
                
                if text in item_text:
                    item.setHidden(False)
                    category_visible = True
                else:
                    item.setHidden(True)
                    
            category.setHidden(not category_visible)
            
            if category_visible:
                category.setExpanded(True)
                
    def on_item_clicked(self, item, column):
        """Handle item click"""
        if isinstance(item, WidgetLibraryItem):
            self.widget_selected.emit(item.widget_type)
