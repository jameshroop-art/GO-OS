"""
Full Preview Mode - F5 full-screen preview with auto-hide toolbar
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QComboBox, QSlider, QCheckBox,
                              QFrame, QToolBar, QScrollArea)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, pyqtSignal
from PyQt6.QtGui import QFont, QPainter, QColor, QKeySequence, QShortcut


class FullPreviewMode(QWidget):
    """Full-screen preview mode with auto-hide toolbar"""
    
    closed = pyqtSignal()
    
    def __init__(self, canvas_elements, parent=None):
        super().__init__(parent)
        self.canvas_elements = canvas_elements
        self.scale_factor = 1.0
        self.show_performance = False
        self.toolbar_visible = False
        self.setup_ui()
        
        # F5 to exit
        exit_shortcut = QShortcut(QKeySequence("F5"), self)
        exit_shortcut.activated.connect(self.close_preview)
        
        # ESC to exit
        esc_shortcut = QShortcut(QKeySequence("Esc"), self)
        esc_shortcut.activated.connect(self.close_preview)
        
    def setup_ui(self):
        """Setup full preview interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Auto-hide toolbar
        self.toolbar = QFrame()
        self.toolbar.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 30, 230);
                border-bottom: 1px solid #3d3d3d;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
                padding: 6px 12px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QComboBox, QSlider {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
                padding: 4px;
            }
            QLabel {
                color: #e0e0e0;
                margin: 0 5px;
            }
        """)
        
        toolbar_layout = QHBoxLayout(self.toolbar)
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        
        # Exit button
        exit_btn = QPushButton("✕ Exit Preview (F5)")
        exit_btn.clicked.connect(self.close_preview)
        toolbar_layout.addWidget(exit_btn)
        
        toolbar_layout.addSpacing(20)
        
        # Scale control
        scale_label = QLabel("Scale:")
        toolbar_layout.addWidget(scale_label)
        
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setMinimum(50)
        self.scale_slider.setMaximum(200)
        self.scale_slider.setValue(100)
        self.scale_slider.setMaximumWidth(150)
        self.scale_slider.valueChanged.connect(self.update_scale)
        toolbar_layout.addWidget(self.scale_slider)
        
        self.scale_value_label = QLabel("100%")
        toolbar_layout.addWidget(self.scale_value_label)
        
        # Resolution simulation
        res_label = QLabel("Resolution:")
        toolbar_layout.addWidget(res_label)
        
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems([
            "Native",
            "1920x1080 (Full HD)",
            "1366x768 (HD)",
            "1280x720 (HD)",
            "1024x768 (XGA)",
            "800x600 (SVGA)"
        ])
        self.resolution_combo.currentTextChanged.connect(self.update_resolution)
        toolbar_layout.addWidget(self.resolution_combo)
        
        # Performance overlay
        self.perf_check = QCheckBox("Performance Overlay")
        self.perf_check.stateChanged.connect(self.toggle_performance)
        toolbar_layout.addWidget(self.perf_check)
        
        toolbar_layout.addStretch()
        
        # Info label
        info_label = QLabel("Move mouse to top to show toolbar")
        info_label.setStyleSheet("color: #888888; font-size: 9pt;")
        toolbar_layout.addWidget(info_label)
        
        layout.addWidget(self.toolbar)
        
        # Preview canvas
        self.preview_canvas = PreviewCanvas(self.canvas_elements)
        layout.addWidget(self.preview_canvas)
        
        # Performance overlay
        self.performance_overlay = QLabel(self)
        self.performance_overlay.setStyleSheet("""
            background-color: rgba(0, 0, 0, 180);
            color: #0f0;
            font-family: monospace;
            font-size: 10pt;
            padding: 10px;
            border-radius: 5px;
        """)
        self.performance_overlay.hide()
        self.performance_overlay.setGeometry(10, 60, 200, 100)
        
        # Mouse tracking for auto-hide
        self.setMouseTracking(True)
        
        # Hide toolbar initially
        self.toolbar.hide()
        
        # Timer for updating performance
        self.perf_timer = QTimer()
        self.perf_timer.timeout.connect(self.update_performance_overlay)
        self.perf_timer.start(1000)
        
        # Style
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
            }
        """)
        
    def mouseMoveEvent(self, event):
        """Handle mouse movement for auto-hide toolbar"""
        if event.position().y() < 100:
            if not self.toolbar_visible:
                self.show_toolbar()
        else:
            if self.toolbar_visible:
                self.hide_toolbar()
        super().mouseMoveEvent(event)
        
    def show_toolbar(self):
        """Show toolbar with fade animation"""
        self.toolbar_visible = True
        self.toolbar.show()
        
    def hide_toolbar(self):
        """Hide toolbar with fade animation"""
        self.toolbar_visible = False
        QTimer.singleShot(500, lambda: self.toolbar.hide() if not self.toolbar_visible else None)
        
    def update_scale(self, value):
        """Update preview scale"""
        self.scale_factor = value / 100.0
        self.scale_value_label.setText(f"{value}%")
        self.preview_canvas.set_scale(self.scale_factor)
        
    def update_resolution(self, resolution):
        """Update resolution simulation"""
        if resolution == "Native":
            self.preview_canvas.set_resolution(None)
        else:
            # Parse resolution string
            res_part = resolution.split()[0]
            width, height = map(int, res_part.split('x'))
            self.preview_canvas.set_resolution((width, height))
            
    def toggle_performance(self, state):
        """Toggle performance overlay"""
        self.show_performance = bool(state)
        if self.show_performance:
            self.performance_overlay.show()
        else:
            self.performance_overlay.hide()
            
    def update_performance_overlay(self):
        """Update performance stats"""
        if self.show_performance:
            import time
            fps = 60  # Mock FPS
            elements = len(self.canvas_elements)
            memory = 45  # Mock memory MB
            
            perf_text = f"""FPS: {fps}
Elements: {elements}
Memory: {memory} MB
Scale: {int(self.scale_factor * 100)}%"""
            
            self.performance_overlay.setText(perf_text)
            
    def close_preview(self):
        """Close preview and return to editor"""
        self.closed.emit()
        self.close()


class PreviewCanvas(QWidget):
    """Canvas for rendering preview"""
    
    def __init__(self, elements):
        super().__init__()
        self.elements = elements
        self.scale = 1.0
        self.resolution = None
        self.setMouseTracking(True)
        
    def set_scale(self, scale):
        """Set rendering scale"""
        self.scale = scale
        self.update()
        
    def set_resolution(self, resolution):
        """Set resolution simulation"""
        self.resolution = resolution
        self.update()
        
    def paintEvent(self, event):
        """Render preview"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate canvas area
        if self.resolution:
            canvas_width = int(self.resolution[0] * self.scale)
            canvas_height = int(self.resolution[1] * self.scale)
            
            # Center the canvas
            x_offset = (self.width() - canvas_width) // 2
            y_offset = (self.height() - canvas_height) // 2
            
            # Draw border around simulated resolution
            painter.setPen(QColor("#666666"))
            painter.drawRect(x_offset, y_offset, canvas_width, canvas_height)
        else:
            x_offset = 0
            y_offset = 0
            
        # Render elements
        for element in self.elements:
            self.render_element(painter, element, x_offset, y_offset)
            
    def render_element(self, painter, element, x_offset, y_offset):
        """Render a single element"""
        x = int(element.get('x', 0) * self.scale) + x_offset
        y = int(element.get('y', 0) * self.scale) + y_offset
        width = int(element.get('width', 100) * self.scale)
        height = int(element.get('height', 30) * self.scale)
        
        # Background
        bg_color = QColor(element.get('background_color', '#2d2d2d'))
        painter.fillRect(x, y, width, height, bg_color)
        
        # Border
        border_width = element.get('border_width', 1)
        border_color = QColor(element.get('border_color', '#3d3d3d'))
        painter.setPen(border_color)
        painter.drawRect(x, y, width, height)
        
        # Text
        if 'text' in element:
            painter.setPen(QColor('#e0e0e0'))
            text_rect = QRect(x, y, width, height)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, element['text'])
