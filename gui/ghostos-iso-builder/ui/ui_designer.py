"""
UI Designer - Main drag-and-drop canvas with full UI design capabilities
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QFrame, QScrollArea, QToolBar, QPushButton,
                              QSplitter, QMessageBox)
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal, QMimeData
from PyQt6.QtGui import (QPainter, QColor, QPen, QBrush, QFont, QDrag,
                         QKeySequence, QShortcut, QPainterPath)

from .widget_library import WidgetLibrary
from .properties_panel import PropertiesPanel
from .ai_assembly import AIAssembly
from .full_preview import FullPreviewMode
from .console_templates import ConsoleTemplates


class CanvasElement:
    """Represents an element on the canvas"""
    
    def __init__(self, element_type, x, y, width=100, height=30):
        self.type = element_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False
        self.properties = {
            'type': element_type,
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'text': self.get_default_text(),
            'background_color': '#2d2d2d',
            'border_color': '#3d3d3d',
            'border_width': 1,
            'border_radius': 4,
            'enabled': True
        }
        
    def get_default_text(self):
        """Get default text for element type"""
        defaults = {
            'button': 'Button',
            'label': 'Label',
            'text_input': 'Enter text...',
            'checkbox': 'Checkbox',
            'radio': 'Radio Button',
            'window': 'Window',
            'taskbar': 'Taskbar',
        }
        return defaults.get(self.type, self.type.replace('_', ' ').title())
        
    def contains(self, point):
        """Check if point is inside element"""
        return (self.x <= point.x() <= self.x + self.width and
                self.y <= point.y() <= self.y + self.height)
                
    def get_rect(self):
        """Get QRect for element"""
        return QRect(self.x, self.y, self.width, self.height)
        
    def move(self, dx, dy):
        """Move element by offset"""
        self.x += dx
        self.y += dy
        self.properties['x'] = self.x
        self.properties['y'] = self.y
        
    def resize(self, width, height):
        """Resize element"""
        self.width = max(20, width)
        self.height = max(20, height)
        self.properties['width'] = self.width
        self.properties['height'] = self.height
        
    def update_property(self, name, value):
        """Update element property"""
        self.properties[name] = value
        if name == 'x':
            self.x = int(value)
        elif name == 'y':
            self.y = int(value)
        elif name == 'width':
            self.width = max(20, int(value))
        elif name == 'height':
            self.height = max(20, int(value))


class DesignCanvas(QWidget):
    """Interactive canvas for UI design"""
    
    element_selected = pyqtSignal(object)
    elements_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.elements = []
        self.selected_elements = []
        self.drag_start = None
        self.drag_element = None
        self.resize_handle = None
        self.lasso_start = None
        self.lasso_end = None
        self.grid_size = 10
        self.grid_snap = True
        self.drop_zone_active = False
        
        self.setMinimumSize(800, 600)
        self.setAcceptDrops(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Keyboard shortcuts
        delete_shortcut = QShortcut(QKeySequence("Delete"), self)
        delete_shortcut.activated.connect(self.delete_selected)
        
        # Arrow key movement
        for key, dx, dy in [
            (Qt.Key.Key_Left, -1, 0),
            (Qt.Key.Key_Right, 1, 0),
            (Qt.Key.Key_Up, 0, -1),
            (Qt.Key.Key_Down, 0, 1)
        ]:
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(lambda dx=dx, dy=dy: self.move_selected(dx, dy))
            
        # Style
        self.setStyleSheet("""
            QWidget {
                background-color: #252525;
                border: 2px solid #3d3d3d;
            }
        """)
        
    def snap_to_grid(self, value):
        """Snap value to grid"""
        if self.grid_snap:
            return round(value / self.grid_size) * self.grid_size
        return value
        
    def add_element(self, element_type, x, y):
        """Add new element to canvas"""
        x = self.snap_to_grid(x)
        y = self.snap_to_grid(y)
        
        element = CanvasElement(element_type, x, y)
        self.elements.append(element)
        self.clear_selection()
        element.selected = True
        self.selected_elements = [element]
        self.element_selected.emit(element.properties)
        self.elements_changed.emit()
        self.update()
        
    def clear_selection(self):
        """Clear all selections"""
        for element in self.elements:
            element.selected = False
        self.selected_elements = []
        
    def delete_selected(self):
        """Delete selected elements"""
        if self.selected_elements:
            for element in self.selected_elements:
                if element in self.elements:
                    self.elements.remove(element)
            self.selected_elements = []
            self.element_selected.emit(None)
            self.elements_changed.emit()
            self.update()
            
    def move_selected(self, dx, dy, shift=False):
        """Move selected elements with arrow keys"""
        if not self.selected_elements:
            return
            
        multiplier = 10 if shift else 1
        for element in self.selected_elements:
            element.move(dx * multiplier, dy * multiplier)
            
        if self.selected_elements:
            self.element_selected.emit(self.selected_elements[0].properties)
        self.elements_changed.emit()
        self.update()
        
    def align_elements(self, alignment):
        """Align selected elements"""
        if len(self.selected_elements) < 2:
            return
            
        if alignment == 'left':
            x = min(e.x for e in self.selected_elements)
            for e in self.selected_elements:
                e.x = x
                e.properties['x'] = x
        elif alignment == 'right':
            x = max(e.x + e.width for e in self.selected_elements)
            for e in self.selected_elements:
                e.x = x - e.width
                e.properties['x'] = e.x
        elif alignment == 'top':
            y = min(e.y for e in self.selected_elements)
            for e in self.selected_elements:
                e.y = y
                e.properties['y'] = y
        elif alignment == 'bottom':
            y = max(e.y + e.height for e in self.selected_elements)
            for e in self.selected_elements:
                e.y = y - e.height
                e.properties['y'] = e.y
        elif alignment == 'center_h':
            center_x = sum(e.x + e.width / 2 for e in self.selected_elements) / len(self.selected_elements)
            for e in self.selected_elements:
                e.x = int(center_x - e.width / 2)
                e.properties['x'] = e.x
        elif alignment == 'center_v':
            center_y = sum(e.y + e.height / 2 for e in self.selected_elements) / len(self.selected_elements)
            for e in self.selected_elements:
                e.y = int(center_y - e.height / 2)
                e.properties['y'] = e.y
                
        self.elements_changed.emit()
        self.update()
        
    def distribute_elements(self, direction):
        """Distribute selected elements"""
        if len(self.selected_elements) < 3:
            return
            
        if direction == 'horizontal':
            sorted_elements = sorted(self.selected_elements, key=lambda e: e.x)
            left = sorted_elements[0].x
            right = sorted_elements[-1].x + sorted_elements[-1].width
            total_width = sum(e.width for e in sorted_elements)
            spacing = (right - left - total_width) / (len(sorted_elements) - 1)
            
            x = left
            for e in sorted_elements:
                e.x = int(x)
                e.properties['x'] = e.x
                x += e.width + spacing
        else:  # vertical
            sorted_elements = sorted(self.selected_elements, key=lambda e: e.y)
            top = sorted_elements[0].y
            bottom = sorted_elements[-1].y + sorted_elements[-1].height
            total_height = sum(e.height for e in sorted_elements)
            spacing = (bottom - top - total_height) / (len(sorted_elements) - 1)
            
            y = top
            for e in sorted_elements:
                e.y = int(y)
                e.properties['y'] = e.y
                y += e.height + spacing
                
        self.elements_changed.emit()
        self.update()
        
    def load_layout(self, layout_data):
        """Load layout from AI or template"""
        for element_data in layout_data.get('elements', []):
            element = CanvasElement(
                element_data['type'],
                element_data['x'],
                element_data['y'],
                element_data.get('width', 100),
                element_data.get('height', 30)
            )
            if 'text' in element_data:
                element.properties['text'] = element_data['text']
            if 'bg_color' in element_data:
                element.properties['background_color'] = element_data['bg_color']
            if 'color' in element_data:
                element.properties['text_color'] = element_data['color']
            if 'font_size' in element_data:
                element.properties['font_size'] = element_data['font_size']
            self.elements.append(element)
            
        self.elements_changed.emit()
        self.update()
    
    def clear_canvas(self):
        """Clear all elements from canvas"""
        self.elements.clear()
        self.selected_elements.clear()
        self.elements_changed.emit()
        self.update()
        
    def dragEnterEvent(self, event):
        """Handle drag enter"""
        self.drop_zone_active = True
        event.acceptProposedAction()
        self.update()
        
    def dragLeaveEvent(self, event):
        """Handle drag leave"""
        self.drop_zone_active = False
        self.update()
        
    def dropEvent(self, event):
        """Handle drop from widget library"""
        self.drop_zone_active = False
        # Widget type would be in mime data
        # For now, add a default button
        pos = event.position().toPoint()
        self.add_element('button', pos.x(), pos.y())
        event.acceptProposedAction()
        
    def mousePressEvent(self, event):
        """Handle mouse press"""
        pos = event.position().toPoint()
        
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if clicking on resize handle
            for element in self.selected_elements:
                handle = self.get_resize_handle(element, pos)
                if handle:
                    self.resize_handle = (element, handle)
                    self.drag_start = pos
                    return
                    
            # Check if clicking on element
            clicked_element = None
            for element in reversed(self.elements):
                if element.contains(pos):
                    clicked_element = element
                    break
                    
            if clicked_element:
                # Multi-select with Ctrl
                if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                    clicked_element.selected = not clicked_element.selected
                    if clicked_element.selected:
                        if clicked_element not in self.selected_elements:
                            self.selected_elements.append(clicked_element)
                    else:
                        if clicked_element in self.selected_elements:
                            self.selected_elements.remove(clicked_element)
                else:
                    if not clicked_element.selected:
                        self.clear_selection()
                        clicked_element.selected = True
                        self.selected_elements = [clicked_element]
                        
                self.drag_start = pos
                self.drag_element = clicked_element
                self.element_selected.emit(clicked_element.properties)
            else:
                # Start lasso selection
                self.clear_selection()
                self.lasso_start = pos
                self.element_selected.emit(None)
                
        self.update()
        
    def mouseMoveEvent(self, event):
        """Handle mouse move"""
        pos = event.position().toPoint()
        
        if self.resize_handle:
            # Resize element
            element, handle = self.resize_handle
            dx = pos.x() - self.drag_start.x()
            dy = pos.y() - self.drag_start.y()
            
            if 'e' in handle:
                element.resize(element.width + dx, element.height)
            elif 'w' in handle:
                element.x += dx
                element.resize(element.width - dx, element.height)
            if 's' in handle:
                element.resize(element.width, element.height + dy)
            elif 'n' in handle:
                element.y += dy
                element.resize(element.width, element.height - dy)
                
            self.drag_start = pos
            self.element_selected.emit(element.properties)
            self.elements_changed.emit()
            self.update()
            
        elif self.drag_element and self.drag_start:
            # Drag element(s)
            dx = pos.x() - self.drag_start.x()
            dy = pos.y() - self.drag_start.y()
            
            for element in self.selected_elements:
                element.move(dx, dy)
                
            self.drag_start = pos
            if self.selected_elements:
                self.element_selected.emit(self.selected_elements[0].properties)
            self.elements_changed.emit()
            self.update()
            
        elif self.lasso_start:
            # Update lasso
            self.lasso_end = pos
            self.update()
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if self.lasso_start and self.lasso_end:
            # Select elements in lasso
            lasso_rect = QRect(self.lasso_start, self.lasso_end).normalized()
            for element in self.elements:
                if lasso_rect.intersects(element.get_rect()):
                    element.selected = True
                    if element not in self.selected_elements:
                        self.selected_elements.append(element)
                        
        self.drag_start = None
        self.drag_element = None
        self.resize_handle = None
        self.lasso_start = None
        self.lasso_end = None
        self.update()
        
    def get_resize_handle(self, element, pos):
        """Get resize handle at position"""
        handle_size = 8
        x, y = element.x, element.y
        w, h = element.width, element.height
        
        handles = {
            'nw': QRect(x - handle_size, y - handle_size, handle_size * 2, handle_size * 2),
            'ne': QRect(x + w - handle_size, y - handle_size, handle_size * 2, handle_size * 2),
            'sw': QRect(x - handle_size, y + h - handle_size, handle_size * 2, handle_size * 2),
            'se': QRect(x + w - handle_size, y + h - handle_size, handle_size * 2, handle_size * 2),
            'n': QRect(x + w // 2 - handle_size, y - handle_size, handle_size * 2, handle_size * 2),
            's': QRect(x + w // 2 - handle_size, y + h - handle_size, handle_size * 2, handle_size * 2),
            'e': QRect(x + w - handle_size, y + h // 2 - handle_size, handle_size * 2, handle_size * 2),
            'w': QRect(x - handle_size, y + h // 2 - handle_size, handle_size * 2, handle_size * 2),
        }
        
        for handle, rect in handles.items():
            if rect.contains(pos):
                return handle
        return None
        
    def paintEvent(self, event):
        """Paint canvas"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw grid
        if self.grid_snap:
            painter.setPen(QPen(QColor("#2d2d2d"), 1))
            for x in range(0, self.width(), self.grid_size):
                painter.drawLine(x, 0, x, self.height())
            for y in range(0, self.height(), self.grid_size):
                painter.drawLine(0, y, self.width(), y)
                
        # Drop zone highlight
        if self.drop_zone_active:
            painter.fillRect(self.rect(), QColor(0, 120, 212, 30))
            painter.setPen(QPen(QColor("#0078d4"), 3, Qt.PenStyle.DashLine))
            painter.drawRect(self.rect().adjusted(10, 10, -10, -10))
            
        # Draw elements
        for element in self.elements:
            self.draw_element(painter, element)
            
        # Draw lasso
        if self.lasso_start and self.lasso_end:
            lasso_rect = QRect(self.lasso_start, self.lasso_end).normalized()
            painter.setPen(QPen(QColor("#0078d4"), 2, Qt.PenStyle.DashLine))
            painter.setBrush(QBrush(QColor(0, 120, 212, 30)))
            painter.drawRect(lasso_rect)
            
    def draw_element(self, painter, element):
        """Draw a single element"""
        rect = element.get_rect()
        
        # Background
        bg_color = QColor(element.properties.get('background_color', '#2d2d2d'))
        painter.fillRect(rect, bg_color)
        
        # Border
        border_width = element.properties.get('border_width', 1)
        border_color = QColor(element.properties.get('border_color', '#3d3d3d'))
        
        if element.selected:
            border_color = QColor("#0078d4")
            border_width = 2
            
        painter.setPen(QPen(border_color, border_width))
        painter.drawRect(rect)
        
        # Text
        text = element.properties.get('text', '')
        if text:
            painter.setPen(QColor('#e0e0e0'))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
            
        # Resize handles for selected elements
        if element.selected:
            self.draw_resize_handles(painter, element)
            
    def draw_resize_handles(self, painter, element):
        """Draw resize handles"""
        handle_size = 6
        painter.setBrush(QBrush(QColor("#0078d4")))
        painter.setPen(QPen(QColor("#ffffff"), 1))
        
        x, y = element.x, element.y
        w, h = element.width, element.height
        
        handles = [
            (x, y),  # nw
            (x + w, y),  # ne
            (x, y + h),  # sw
            (x + w, y + h),  # se
            (x + w // 2, y),  # n
            (x + w // 2, y + h),  # s
            (x, y + h // 2),  # w
            (x + w, y + h // 2),  # e
        ]
        
        for hx, hy in handles:
            painter.drawRect(hx - handle_size // 2, hy - handle_size // 2,
                           handle_size, handle_size)


class UIDesigner(QWidget):
    """Main UI Designer widget with full functionality"""
    
    def __init__(self):
        super().__init__()
        self.preview_mode = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI Designer interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # Main splitter (3 panels)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Widget Library + Console Templates + AI Assembly
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        self.widget_library = WidgetLibrary()
        self.widget_library.widget_selected.connect(self.on_widget_selected)
        left_layout.addWidget(self.widget_library, 2)
        
        self.console_templates = ConsoleTemplates()
        self.console_templates.template_loaded.connect(self.on_template_loaded)
        left_layout.addWidget(self.console_templates, 3)
        
        self.ai_assembly = AIAssembly()
        self.ai_assembly.layout_generated.connect(self.on_layout_generated)
        left_layout.addWidget(self.ai_assembly, 2)
        
        # Center panel - Canvas
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(5, 5, 5, 5)
        
        canvas_label = QLabel("Design Canvas")
        canvas_label_font = QFont()
        canvas_label_font.setBold(True)
        canvas_label.setFont(canvas_label_font)
        center_layout.addWidget(canvas_label)
        
        self.canvas = DesignCanvas()
        self.canvas.element_selected.connect(self.on_element_selected)
        center_layout.addWidget(self.canvas)
        
        # Right panel - Properties
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 5, 5, 5)
        
        self.properties_panel = PropertiesPanel()
        self.properties_panel.property_changed.connect(self.on_property_changed)
        right_layout.addWidget(self.properties_panel)
        
        # Add panels to splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(center_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([250, 550, 250])
        
        layout.addWidget(main_splitter)
        
        # F5 shortcut for full preview
        preview_shortcut = QShortcut(QKeySequence("F5"), self)
        preview_shortcut.activated.connect(self.show_full_preview)
        
    def create_toolbar(self):
        """Create designer toolbar"""
        toolbar = QFrame()
        toolbar.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-bottom: 1px solid #3d3d3d;
                padding: 5px;
            }
            QPushButton {
                background-color: #252525;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
                padding: 5px 10px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # Alignment tools
        align_label = QLabel("Align:")
        layout.addWidget(align_label)
        
        for name, alignment in [
            ("Left", "left"),
            ("Center", "center_h"),
            ("Right", "right"),
            ("Top", "top"),
            ("Middle", "center_v"),
            ("Bottom", "bottom")
        ]:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, a=alignment: self.canvas.align_elements(a))
            layout.addWidget(btn)
            
        layout.addSpacing(20)
        
        # Distribution tools
        dist_label = QLabel("Distribute:")
        layout.addWidget(dist_label)
        
        for name, direction in [("Horizontal", "horizontal"), ("Vertical", "vertical")]:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, d=direction: self.canvas.distribute_elements(d))
            layout.addWidget(btn)
            
        layout.addSpacing(20)
        
        # Grid snap
        grid_btn = QPushButton("Grid Snap")
        grid_btn.setCheckable(True)
        grid_btn.setChecked(True)
        grid_btn.clicked.connect(self.toggle_grid_snap)
        layout.addWidget(grid_btn)
        
        layout.addStretch()
        
        # Preview button
        preview_btn = QPushButton("🔍 Full Preview (F5)")
        preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
        """)
        preview_btn.clicked.connect(self.show_full_preview)
        layout.addWidget(preview_btn)
        
        return toolbar
        
    def on_widget_selected(self, widget_type):
        """Handle widget selection from library"""
        # Add to center of canvas
        self.canvas.add_element(widget_type, 300, 200)
        
    def on_element_selected(self, element):
        """Handle element selection on canvas"""
        self.properties_panel.set_element(element)
        
    def on_property_changed(self, property_name, value):
        """Handle property change"""
        if self.canvas.selected_elements:
            for element in self.canvas.selected_elements:
                element.update_property(property_name, value)
        self.canvas.update()
        
    def on_layout_generated(self, layout_data):
        """Handle AI-generated layout"""
        reply = QMessageBox.question(
            self,
            "Apply Layout",
            f"Apply AI-generated layout?\n\nThis will add {len(layout_data.get('elements', []))} elements to the canvas.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.canvas.load_layout(layout_data)
    
    def on_template_loaded(self, template_data):
        """Handle console template loading"""
        reply = QMessageBox.question(
            self,
            "Load Template",
            f"Load '{template_data['name']}' template?\n\n"
            f"Type: {template_data['type']}\n"
            f"Elements: {len(template_data.get('elements', []))}\n\n"
            f"This will replace the current canvas.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.canvas.clear_canvas()
            self.canvas.load_layout(template_data)
            
            # Show success message
            QMessageBox.information(
                self,
                "Template Loaded",
                f"'{template_data['name']}' template loaded successfully!\n\n"
                f"You can now customize all elements using the properties panel."
            )
            
    def show_full_preview(self):
        """Show full-screen preview"""
        if not self.preview_mode:
            self.preview_mode = FullPreviewMode(self.canvas.elements, self)
            self.preview_mode.closed.connect(self.on_preview_closed)
            self.preview_mode.showFullScreen()
        else:
            self.preview_mode.showFullScreen()
            
    def on_preview_closed(self):
        """Handle preview window closed"""
        self.preview_mode = None
    
    def toggle_grid_snap(self, checked):
        """Toggle grid snapping"""
        self.canvas.grid_snap = checked
        self.canvas.update()

