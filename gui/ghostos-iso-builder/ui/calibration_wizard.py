#!/usr/bin/env python3
"""
Touch Calibration Wizard
Helps users calibrate touch input for accurate keyboard usage
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QProgressBar, QWidget)
from PyQt6.QtCore import Qt, QPoint, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QFont


class CalibrationTarget(QWidget):
    """Visual calibration target widget"""
    
    target_clicked = pyqtSignal(QPoint)
    
    def __init__(self, position: str):
        super().__init__()
        self.position = position  # 'top-left', 'top-right', 'center', 'bottom-left', 'bottom-right'
        self.target_size = 40
        self.is_active = False
        
    def paintEvent(self, event):
        """Draw calibration target"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get center point
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        if self.is_active:
            # Draw pulsing target
            painter.setPen(QPen(QColor(0, 120, 212), 3))
            painter.setBrush(QColor(0, 120, 212, 50))
            painter.drawEllipse(
                center_x - self.target_size // 2,
                center_y - self.target_size // 2,
                self.target_size,
                self.target_size
            )
            
            # Draw center crosshair
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            painter.drawLine(center_x - 10, center_y, center_x + 10, center_y)
            painter.drawLine(center_x, center_y - 10, center_x, center_y + 10)
            
            # Draw instruction text
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            text = "Tap the center"
            text_rect = painter.fontMetrics().boundingRect(text)
            painter.drawText(
                center_x - text_rect.width() // 2,
                center_y + self.target_size + 20,
                text
            )
        
    def mousePressEvent(self, event):
        """Handle touch/click on target"""
        if self.is_active and event.button() == Qt.MouseButton.LeftButton:
            self.target_clicked.emit(event.position().toPoint())
            event.accept()
            
    def activate(self):
        """Activate this target"""
        self.is_active = True
        self.update()
        
    def deactivate(self):
        """Deactivate this target"""
        self.is_active = False
        self.update()


class CalibrationWizard(QDialog):
    """Multi-point touch calibration wizard"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Touch Calibration")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        
        # Calibration data
        self.calibration_points = []
        self.expected_points = []
        self.current_target = 0
        self.total_targets = 5
        
        # Calculated offset
        self.offset_x = 0
        self.offset_y = 0
        
        # Setup UI
        self.setup_ui()
        self.showFullScreen()
        
        # Start calibration after a short delay
        QTimer.singleShot(500, self.start_calibration)
        
    def setup_ui(self):
        """Setup calibration UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create semi-transparent overlay
        self.setStyleSheet("""
            QDialog {
                background-color: rgba(0, 0, 0, 200);
            }
            QLabel {
                color: white;
                font-size: 16pt;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
        """)
        
        # Top instruction panel
        instruction_widget = QWidget()
        instruction_layout = QVBoxLayout(instruction_widget)
        
        self.title_label = QLabel("Touch Calibration")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        instruction_layout.addWidget(self.title_label)
        
        self.instruction_label = QLabel("Tap each target as accurately as possible")
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_layout.addWidget(self.instruction_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.total_targets)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%v / %m targets")
        instruction_layout.addWidget(self.progress_bar)
        
        main_layout.addWidget(instruction_widget)
        
        # Calibration targets container
        self.targets_container = QWidget()
        self.targets_container.setMinimumSize(800, 600)
        main_layout.addWidget(self.targets_container, 1)
        
        # Create calibration targets at 5 points
        self.targets = []
        target_positions = [
            ('top-left', 50, 50),
            ('top-right', -90, 50),
            ('center', -40, -40),
            ('bottom-left', 50, -90),
            ('bottom-right', -90, -90)
        ]
        
        for pos_name, x_offset, y_offset in target_positions:
            target = CalibrationTarget(pos_name)
            target.setParent(self.targets_container)
            target.target_clicked.connect(self.on_target_clicked)
            self.targets.append(target)
            
        # Bottom control panel
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        
        self.skip_btn = QPushButton("Skip Calibration")
        self.skip_btn.clicked.connect(self.skip_calibration)
        control_layout.addWidget(self.skip_btn)
        
        control_layout.addStretch()
        
        self.restart_btn = QPushButton("Restart")
        self.restart_btn.clicked.connect(self.restart_calibration)
        self.restart_btn.setEnabled(False)
        control_layout.addWidget(self.restart_btn)
        
        self.finish_btn = QPushButton("Finish")
        self.finish_btn.clicked.connect(self.finish_calibration)
        self.finish_btn.setEnabled(False)
        control_layout.addWidget(self.finish_btn)
        
        main_layout.addWidget(control_widget)
        
    def resizeEvent(self, event):
        """Position targets when window is resized"""
        super().resizeEvent(event)
        self.position_targets()
        
    def position_targets(self):
        """Position calibration targets on screen"""
        if not self.targets:
            return
            
        container_width = self.targets_container.width()
        container_height = self.targets_container.height()
        
        positions = [
            (50, 50),  # top-left
            (container_width - 90, 50),  # top-right
            (container_width // 2 - 20, container_height // 2 - 20),  # center
            (50, container_height - 90),  # bottom-left
            (container_width - 90, container_height - 90)  # bottom-right
        ]
        
        for i, (x, y) in enumerate(positions):
            self.targets[i].setGeometry(x, y, 80, 80)
            
        # Store expected center points for calibration calculation
        self.expected_points = [
            QPoint(p[0] + 40, p[1] + 40) for p in positions
        ]
        
    def start_calibration(self):
        """Start the calibration process"""
        self.current_target = 0
        self.calibration_points = []
        self.progress_bar.setValue(0)
        self.restart_btn.setEnabled(False)
        self.finish_btn.setEnabled(False)
        
        # Position and activate first target
        self.position_targets()
        if self.targets:
            self.targets[0].activate()
            
    def on_target_clicked(self, point: QPoint):
        """Handle target click"""
        if self.current_target >= len(self.targets):
            return
            
        # Get the actual click position relative to container
        target = self.targets[self.current_target]
        global_pos = target.mapToGlobal(point)
        container_pos = self.targets_container.mapFromGlobal(global_pos)
        
        # Store calibration point
        self.calibration_points.append(container_pos)
        
        # Deactivate current target
        target.deactivate()
        
        # Move to next target
        self.current_target += 1
        self.progress_bar.setValue(self.current_target)
        
        if self.current_target < len(self.targets):
            # Activate next target
            self.targets[self.current_target].activate()
        else:
            # All targets completed
            self.complete_calibration()
            
    def complete_calibration(self):
        """Complete calibration and calculate offset"""
        if len(self.calibration_points) != len(self.expected_points):
            self.instruction_label.setText("Calibration incomplete. Please restart.")
            self.restart_btn.setEnabled(True)
            return
            
        # Calculate average offset
        total_offset_x = 0
        total_offset_y = 0
        
        for actual, expected in zip(self.calibration_points, self.expected_points):
            total_offset_x += expected.x() - actual.x()
            total_offset_y += expected.y() - actual.y()
            
        count = len(self.calibration_points)
        self.offset_x = total_offset_x // count
        self.offset_y = total_offset_y // count
        
        # Update UI
        self.instruction_label.setText(
            f"✓ Calibration Complete!\n"
            f"Offset: X={self.offset_x}px, Y={self.offset_y}px"
        )
        self.restart_btn.setEnabled(True)
        self.finish_btn.setEnabled(True)
        
    def restart_calibration(self):
        """Restart calibration process"""
        self.start_calibration()
        self.instruction_label.setText("Tap each target as accurately as possible")
        
    def skip_calibration(self):
        """Skip calibration and use no offset"""
        self.offset_x = 0
        self.offset_y = 0
        self.reject()
        
    def finish_calibration(self):
        """Finish and accept calibration"""
        self.accept()
        
    def get_offset(self) -> QPoint:
        """Get calculated calibration offset"""
        return QPoint(self.offset_x, self.offset_y)
