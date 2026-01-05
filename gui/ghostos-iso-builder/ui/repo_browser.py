#!/usr/bin/env python3
"""
Repository Browser Widget - Browse and integrate external repositories
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QListWidget, QListWidgetItem,
                              QTextEdit, QGroupBox, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class RepoBrowserWidget(QWidget):
    """Widget for browsing and integrating external repositories"""
    
    integration_selected = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.repos_data = self.load_repos_data()
        self.setup_ui()
        
    def load_repos_data(self):
        """Load repository data"""
        # In production, this would load from integrations/repos.json
        return [
            {
                'name': 'Dracula Theme',
                'license': 'MIT',
                'url': 'https://github.com/dracula/dracula-theme',
                'description': 'Dark theme for 250+ apps and websites',
                'category': 'Themes',
            },
            {
                'name': 'Oh My Zsh',
                'license': 'MIT',
                'url': 'https://github.com/ohmyzsh/ohmyzsh',
                'description': 'Framework for managing Zsh configuration',
                'category': 'Shell',
            },
            {
                'name': 'Powerlevel10k',
                'license': 'MIT',
                'url': 'https://github.com/romkatv/powerlevel10k',
                'description': 'Fast, flexible Zsh theme with instant prompt',
                'category': 'Shell',
            },
            {
                'name': 'NvChad',
                'license': 'GPLv3',
                'url': 'https://github.com/NvChad/NvChad',
                'description': 'Blazing fast Neovim config',
                'category': 'Editor',
            },
            {
                'name': 'Starship',
                'license': 'ISC',
                'url': 'https://github.com/starship/starship',
                'description': 'Minimal, fast, and customizable prompt',
                'category': 'Shell',
            },
            {
                'name': 'Alacritty',
                'license': 'Apache 2.0',
                'url': 'https://github.com/alacritty/alacritty',
                'description': 'GPU-accelerated terminal emulator',
                'category': 'Terminal',
            },
            {
                'name': 'Rofi',
                'license': 'MIT',
                'url': 'https://github.com/davatorium/rofi',
                'description': 'Window switcher and application launcher',
                'category': 'Launcher',
            },
            {
                'name': 'Tmux Plugin Manager',
                'license': 'MIT',
                'url': 'https://github.com/tmux-plugins/tpm',
                'description': 'Plugin manager for tmux',
                'category': 'Terminal',
            },
        ]
        
    def setup_ui(self):
        """Setup the repository browser interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_label = QLabel("📦 Repository Integration Browser")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        info_label = QLabel("Browse and integrate popular tools and themes")
        info_label.setStyleSheet("color: #888888; font-size: 10pt;")
        layout.addWidget(info_label)
        
        layout.addSpacing(10)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("🔍 Search:"))
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search repositories...")
        self.search_input.textChanged.connect(self.filter_repos)
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)
        
        # Repository list
        repo_group = QGroupBox("Available Integrations")
        repo_layout = QVBoxLayout(repo_group)
        
        self.repo_list = QListWidget()
        self.repo_list.currentItemChanged.connect(self.on_repo_selected)
        self.populate_repo_list()
        repo_layout.addWidget(self.repo_list)
        
        layout.addWidget(repo_group)
        
        # Repository details
        details_group = QGroupBox("Repository Details")
        details_layout = QVBoxLayout(details_group)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(150)
        self.details_text.setPlainText("Select a repository to view details")
        details_layout.addWidget(self.details_text)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.preview_btn = QPushButton("👁️ Preview Changes")
        self.preview_btn.setEnabled(False)
        self.preview_btn.clicked.connect(self.preview_integration)
        button_layout.addWidget(self.preview_btn)
        
        self.install_btn = QPushButton("✓ Install Integration")
        self.install_btn.setEnabled(False)
        self.install_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #888888;
            }
        """)
        self.install_btn.clicked.connect(self.install_integration)
        button_layout.addWidget(self.install_btn)
        
        details_layout.addLayout(button_layout)
        
        layout.addWidget(details_group)
        
        layout.addStretch()
        
    def populate_repo_list(self, filter_text=""):
        """Populate the repository list"""
        self.repo_list.clear()
        
        for repo in self.repos_data:
            if filter_text.lower() in repo['name'].lower() or \
               filter_text.lower() in repo['description'].lower():
                item_text = f"{repo['name']} ({repo['license']})"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, repo)
                self.repo_list.addItem(item)
                
    def filter_repos(self, text):
        """Filter repositories by search text"""
        self.populate_repo_list(text)
        
    def on_repo_selected(self, current, previous):
        """Handle repository selection"""
        if current:
            repo = current.data(Qt.ItemDataRole.UserRole)
            
            details = f"""
<b>Name:</b> {repo['name']}<br>
<b>License:</b> {repo['license']}<br>
<b>Category:</b> {repo['category']}<br>
<b>URL:</b> <a href="{repo['url']}">{repo['url']}</a><br>
<br>
<b>Description:</b><br>
{repo['description']}
            """
            
            self.details_text.setHtml(details)
            self.preview_btn.setEnabled(True)
            self.install_btn.setEnabled(True)
            
            self.integration_selected.emit(repo)
        else:
            self.details_text.setPlainText("Select a repository to view details")
            self.preview_btn.setEnabled(False)
            self.install_btn.setEnabled(False)
            
    def preview_integration(self):
        """Preview integration changes"""
        current_item = self.repo_list.currentItem()
        if current_item:
            repo = current_item.data(Qt.ItemDataRole.UserRole)
            
            QMessageBox.information(
                self,
                "Preview Integration",
                f"Preview for {repo['name']}\n\n"
                "This would show:\n"
                "- Files to be added\n"
                "- Configuration changes\n"
                "- Dependencies required\n"
                "- Estimated disk space"
            )
            
    def install_integration(self):
        """Install selected integration"""
        current_item = self.repo_list.currentItem()
        if current_item:
            repo = current_item.data(Qt.ItemDataRole.UserRole)
            
            reply = QMessageBox.question(
                self,
                "Confirm Installation",
                f"Install {repo['name']}?\n\n"
                f"This will:\n"
                f"- Clone the repository\n"
                f"- Apply configurations\n"
                f"- Add to ISO build\n\n"
                f"License: {repo['license']}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # In production, would actually install the integration
                QMessageBox.information(
                    self,
                    "Installation Queued",
                    f"{repo['name']} has been queued for installation.\n\n"
                    "It will be included in the next ISO build."
                )
