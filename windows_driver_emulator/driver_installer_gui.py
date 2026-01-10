#!/usr/bin/env python3
"""
Small Driver Installer GUI - Windows 10 22H2 Minimal Style
Lightweight GUI for managing drivers from Microsoft sources

LICENSE: MIT (see LICENSE file in repository root)
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QTableWidget, QTableWidgetItem, QGroupBox,
        QProgressBar, QMessageBox, QHeaderView, QComboBox, QTextEdit,
        QSplitter, QFrame
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal
    from PyQt6.QtGui import QFont, QColor, QIcon
except ImportError:
    print("Error: PyQt6 required. Install with: pip install PyQt6")
    sys.exit(1)

from driver_installer import (
    MinimalDriverInstaller,
    MicrosoftDriverSource,
    VMBridgeOptimizer
)


class DriverInstallThread(QThread):
    """Background thread for driver operations"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, action, device_id=None, category=None):
        super().__init__()
        self.action = action
        self.device_id = device_id
        self.category = category
        self.installer = MinimalDriverInstaller()
    
    def run(self):
        """Execute driver operation"""
        try:
            if self.action == 'list':
                self.progress.emit(50, "Scanning devices...")
                drivers = self.installer.list_required_drivers(self.category)
                self.progress.emit(100, "Scan complete")
                self.finished.emit(True, f"Found {len(drivers)} drivers")
            
            elif self.action == 'install':
                self.progress.emit(25, "Downloading driver...")
                self.progress.emit(50, "Verifying signature...")
                self.progress.emit(75, "Installing driver...")
                success, message = self.installer.install_driver(self.device_id)
                self.progress.emit(100, "Complete")
                self.finished.emit(success, message)
            
            elif self.action == 'uninstall':
                self.progress.emit(50, "Removing driver...")
                success, message = self.installer.uninstall_driver(self.device_id)
                self.progress.emit(100, "Complete")
                self.finished.emit(success, message)
        
        except Exception as e:
            self.finished.emit(False, str(e))


class SmallDriverGUI(QMainWindow):
    """
    Small, focused driver management GUI
    Minimal Windows 10 22H2 style interface
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Driver Manager - Windows 10 22H2 Style")
        self.setGeometry(200, 200, 900, 600)
        
        self.installer = MinimalDriverInstaller()
        self.current_drivers = []
        
        self.setup_ui()
        self.apply_windows_10_style()
        self.refresh_drivers()
    
    def setup_ui(self):
        """Setup minimal user interface"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title bar
        title_bar = self.create_title_bar()
        layout.addWidget(title_bar)
        
        # Main content with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Driver categories
        left_panel = self.create_category_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Driver list and details
        right_panel = self.create_driver_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([200, 700])
        layout.addWidget(splitter)
        
        # Status bar
        status_bar = self.create_status_bar()
        layout.addWidget(status_bar)
    
    def create_title_bar(self) -> QWidget:
        """Create Windows 10 style title bar"""
        title_widget = QWidget()
        title_widget.setObjectName("titleBar")
        title_widget.setFixedHeight(40)
        
        layout = QHBoxLayout(title_widget)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Icon and title
        title_label = QLabel("🔧 Driver Manager")
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(False)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # Performance indicator
        perf_label = QLabel("Performance Impact: Low")
        perf_label.setObjectName("perfLabel")
        layout.addWidget(perf_label)
        
        return title_widget
    
    def create_category_panel(self) -> QWidget:
        """Create left category panel"""
        panel = QWidget()
        panel.setObjectName("categoryPanel")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Category label
        cat_label = QLabel("Driver Categories")
        cat_font = QFont()
        cat_font.setPointSize(10)
        cat_font.setBold(True)
        cat_label.setFont(cat_font)
        layout.addWidget(cat_label)
        
        # Category buttons
        categories = [
            ("All Drivers", None),
            ("Display", "display"),
            ("Network", "network"),
            ("Storage", "storage"),
            ("USB", "usb"),
            ("Audio", "audio"),
            ("Chipset", "chipset"),
        ]
        
        self.category_buttons = []
        for name, cat_id in categories:
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setObjectName("categoryButton")
            btn.clicked.connect(lambda checked, c=cat_id: self.filter_by_category(c))
            layout.addWidget(btn)
            self.category_buttons.append((btn, cat_id))
        
        # Set "All Drivers" as checked
        self.category_buttons[0][0].setChecked(True)
        
        layout.addStretch()
        
        return panel
    
    def create_driver_panel(self) -> QWidget:
        """Create main driver panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header with filter
        header_layout = QHBoxLayout()
        
        header_label = QLabel("System Drivers")
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_layout.addWidget(header_label)
        
        header_layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("actionButton")
        refresh_btn.clicked.connect(self.refresh_drivers)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Driver table
        self.driver_table = QTableWidget()
        self.driver_table.setColumnCount(5)
        self.driver_table.setHorizontalHeaderLabels([
            "Device Name", "Category", "Status", "Source", "Action"
        ])
        self.driver_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.driver_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.driver_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.driver_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.driver_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.driver_table.setColumnWidth(1, 100)
        self.driver_table.setColumnWidth(2, 120)
        self.driver_table.setColumnWidth(3, 100)
        self.driver_table.setColumnWidth(4, 100)
        self.driver_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.driver_table.setAlternatingRowColors(True)
        layout.addWidget(self.driver_table)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # Driver details panel
        details_group = QGroupBox("Performance Metrics")
        details_layout = QVBoxLayout(details_group)
        
        self.metrics_text = QTextEdit()
        self.metrics_text.setReadOnly(True)
        self.metrics_text.setMaximumHeight(120)
        details_layout.addWidget(self.metrics_text)
        
        layout.addWidget(details_group)
        
        # Update performance metrics
        self.update_performance_metrics()
        
        return panel
    
    def create_status_bar(self) -> QWidget:
        """Create status bar"""
        status_widget = QWidget()
        status_widget.setObjectName("statusBar")
        status_widget.setFixedHeight(30)
        
        layout = QHBoxLayout(status_widget)
        layout.setContentsMargins(15, 5, 15, 5)
        
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # Microsoft source indicator
        source_label = QLabel("Source: Microsoft Official")
        source_label.setObjectName("sourceLabel")
        layout.addWidget(source_label)
        
        return status_widget
    
    def filter_by_category(self, category):
        """Filter drivers by category"""
        # Update button states
        for btn, cat_id in self.category_buttons:
            btn.setChecked(cat_id == category)
        
        self.current_category = category
        self.refresh_drivers()
    
    def refresh_drivers(self):
        """Refresh driver list"""
        self.status_label.setText("Scanning for drivers...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Get current category filter
        category = getattr(self, 'current_category', None)
        
        # Start background thread
        self.scan_thread = DriverInstallThread('list', category=category)
        self.scan_thread.progress.connect(self.on_progress)
        self.scan_thread.finished.connect(self.on_scan_complete)
        self.scan_thread.start()
    
    def on_scan_complete(self, success, message):
        """Handle scan completion"""
        self.progress_bar.setVisible(False)
        
        if success:
            # Get drivers
            category = getattr(self, 'current_category', None)
            drivers = self.installer.list_required_drivers(category)
            self.current_drivers = drivers
            
            # Populate table
            self.driver_table.setRowCount(len(drivers))
            
            for row, driver in enumerate(drivers):
                # Device name
                name_item = QTableWidgetItem(driver.get('device_name', 'Unknown'))
                self.driver_table.setItem(row, 0, name_item)
                
                # Category
                cat_item = QTableWidgetItem(driver.get('category', 'other').capitalize())
                self.driver_table.setItem(row, 1, cat_item)
                
                # Status
                status = driver.get('status', 'unknown')
                status_item = QTableWidgetItem(
                    '✓ Installed' if status == 'installed' else '⚠ Needs Driver'
                )
                if status == 'installed':
                    status_item.setForeground(QColor(0, 128, 0))
                else:
                    status_item.setForeground(QColor(255, 140, 0))
                self.driver_table.setItem(row, 2, status_item)
                
                # Source
                source_item = QTableWidgetItem("Microsoft")
                self.driver_table.setItem(row, 3, source_item)
                
                # Action button (create widget)
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(5, 2, 5, 2)
                
                if status == 'needs_driver':
                    install_btn = QPushButton("Install")
                    install_btn.setObjectName("installButton")
                    install_btn.clicked.connect(
                        lambda checked, d=driver: self.install_driver(d)
                    )
                    action_layout.addWidget(install_btn)
                else:
                    uninstall_btn = QPushButton("Remove")
                    uninstall_btn.setObjectName("uninstallButton")
                    uninstall_btn.clicked.connect(
                        lambda checked, d=driver: self.uninstall_driver(d)
                    )
                    action_layout.addWidget(uninstall_btn)
                
                self.driver_table.setCellWidget(row, 4, action_widget)
            
            self.status_label.setText(f"Found {len(drivers)} drivers")
        else:
            self.status_label.setText(f"Scan failed: {message}")
    
    def install_driver(self, driver_info):
        """Install a driver"""
        device_id = driver_info.get('device_id')
        device_name = driver_info.get('device_name', 'Unknown')
        
        reply = QMessageBox.question(
            self,
            "Install Driver",
            f"Install driver for {device_name} from Microsoft?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.status_label.setText(f"Installing driver for {device_name}...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            self.install_thread = DriverInstallThread('install', device_id=device_id)
            self.install_thread.progress.connect(self.on_progress)
            self.install_thread.finished.connect(self.on_install_complete)
            self.install_thread.start()
    
    def on_install_complete(self, success, message):
        """Handle installation completion"""
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.refresh_drivers()
            self.update_performance_metrics()
        else:
            QMessageBox.warning(self, "Installation Failed", message)
        
        self.status_label.setText("Ready")
    
    def uninstall_driver(self, driver_info):
        """Uninstall a driver"""
        device_id = driver_info.get('device_id')
        device_name = driver_info.get('device_name', 'Unknown')
        
        reply = QMessageBox.question(
            self,
            "Remove Driver",
            f"Remove driver for {device_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.status_label.setText(f"Removing driver for {device_name}...")
            self.progress_bar.setVisible(True)
            
            self.uninstall_thread = DriverInstallThread('uninstall', device_id=device_id)
            self.uninstall_thread.progress.connect(self.on_progress)
            self.uninstall_thread.finished.connect(self.on_uninstall_complete)
            self.uninstall_thread.start()
    
    def on_uninstall_complete(self, success, message):
        """Handle uninstallation completion"""
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.refresh_drivers()
            self.update_performance_metrics()
        else:
            QMessageBox.warning(self, "Removal Failed", message)
        
        self.status_label.setText("Ready")
    
    def on_progress(self, value, message):
        """Handle progress updates"""
        self.progress_bar.setValue(value)
        self.progress_bar.setFormat(f"{message} - {value}%")
    
    def update_performance_metrics(self):
        """Update performance metrics display"""
        optimizer = VMBridgeOptimizer()
        metrics = optimizer.get_performance_impact()
        
        metrics_html = f"""
        <b>VM Bridge Performance Impact:</b><br>
        <table style="width: 100%; margin-top: 5px;">
        <tr><td>CPU Overhead:</td><td><b>{metrics['cpu_overhead_percent']:.1f}%</b></td></tr>
        <tr><td>Memory Overhead:</td><td><b>{metrics['memory_overhead_mb']:.0f} MB</b></td></tr>
        <tr><td>I/O Latency:</td><td><b>{metrics['io_latency_ms']:.1f} ms</b></td></tr>
        <tr><td>Cache Hit Rate:</td><td><b>{metrics['cache_hit_rate']*100:.0f}%</b></td></tr>
        </table>
        <p style="color: green; margin-top: 10px;">
        ✓ Optimized for low performance impact
        </p>
        """
        self.metrics_text.setHtml(metrics_html)
    
    def apply_windows_10_style(self):
        """Apply Windows 10 style to the GUI"""
        style = """
        QMainWindow {
            background-color: #f0f0f0;
        }
        
        #titleBar {
            background-color: #0078d4;
            color: white;
        }
        
        #titleBar QLabel {
            color: white;
        }
        
        #perfLabel {
            color: #e0e0e0;
            font-size: 9pt;
        }
        
        #categoryPanel {
            background-color: #f8f8f8;
            border-right: 1px solid #d0d0d0;
        }
        
        #categoryButton {
            text-align: left;
            padding: 8px 12px;
            background-color: transparent;
            border: none;
            border-radius: 4px;
        }
        
        #categoryButton:hover {
            background-color: #e5e5e5;
        }
        
        #categoryButton:checked {
            background-color: #0078d4;
            color: white;
            font-weight: bold;
        }
        
        #actionButton {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 6px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        #actionButton:hover {
            background-color: #005a9e;
        }
        
        #installButton {
            background-color: #107c10;
            color: white;
            border: none;
            padding: 4px 12px;
            border-radius: 3px;
        }
        
        #installButton:hover {
            background-color: #0e6b0e;
        }
        
        #uninstallButton {
            background-color: #d13438;
            color: white;
            border: none;
            padding: 4px 12px;
            border-radius: 3px;
        }
        
        #uninstallButton:hover {
            background-color: #a92c2c;
        }
        
        QTableWidget {
            background-color: white;
            border: 1px solid #d0d0d0;
            gridline-color: #e0e0e0;
        }
        
        QTableWidget::item:selected {
            background-color: #0078d4;
            color: white;
        }
        
        QHeaderView::section {
            background-color: #f8f8f8;
            padding: 6px;
            border: none;
            border-right: 1px solid #d0d0d0;
            border-bottom: 1px solid #d0d0d0;
            font-weight: bold;
        }
        
        QProgressBar {
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            text-align: center;
            background-color: #f0f0f0;
        }
        
        QProgressBar::chunk {
            background-color: #0078d4;
            border-radius: 3px;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
        
        #statusBar {
            background-color: #f8f8f8;
            border-top: 1px solid #d0d0d0;
        }
        
        #sourceLabel {
            color: #107c10;
            font-weight: bold;
        }
        
        QTextEdit {
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            padding: 5px;
            background-color: white;
        }
        """
        self.setStyleSheet(style)


def main():
    """Main entry point for GUI"""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    window = SmallDriverGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
