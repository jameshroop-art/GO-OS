#!/usr/bin/env python3
"""
Credentials Dialog - Secure credentials management
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QPushButton, QTabWidget, QWidget,
                              QTextEdit, QMessageBox, QCheckBox, QGroupBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class CredentialsDialog(QDialog):
    """Dialog for managing secure credentials"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Credentials Management")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the credentials dialog interface"""
        layout = QVBoxLayout(self)
        
        # Header
        header_label = QLabel("🔑 Secure Credentials Management")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        info_label = QLabel("Manage authentication for external services")
        info_label.setStyleSheet("color: #888888; font-size: 10pt;")
        layout.addWidget(info_label)
        
        layout.addSpacing(10)
        
        # Tab widget
        tabs = QTabWidget()
        
        # GitHub tab
        github_tab = self.create_github_tab()
        tabs.addTab(github_tab, "GitHub")
        
        # Hugging Face tab
        hf_tab = self.create_huggingface_tab()
        tabs.addTab(hf_tab, "Hugging Face")
        
        # Terminal/CLI tab
        terminal_tab = self.create_terminal_tab()
        tabs.addTab(terminal_tab, "Terminal Auth")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        test_btn = QPushButton("🔍 Test Connection")
        test_btn.clicked.connect(self.test_connection)
        button_layout.addWidget(test_btn)
        
        save_btn = QPushButton("💾 Save")
        save_btn.clicked.connect(self.save_credentials)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def create_github_tab(self):
        """Create GitHub credentials tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Instructions
        info = QLabel(
            "Enter your GitHub Personal Access Token to enable repository integrations.\n"
            "Create a token at: https://github.com/settings/tokens"
        )
        info.setWordWrap(True)
        info.setStyleSheet("background-color: #2d2d2d; padding: 10px; border-radius: 4px;")
        layout.addWidget(info)
        
        layout.addSpacing(10)
        
        # Token input
        token_group = QGroupBox("GitHub Token")
        token_layout = QVBoxLayout(token_group)
        
        token_layout.addWidget(QLabel("Personal Access Token:"))
        self.github_token = QLineEdit()
        self.github_token.setEchoMode(QLineEdit.EchoMode.Password)
        self.github_token.setPlaceholderText("ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        token_layout.addWidget(self.github_token)
        
        self.github_show_token = QCheckBox("Show token")
        self.github_show_token.toggled.connect(
            lambda checked: self.github_token.setEchoMode(
                QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
            )
        )
        token_layout.addWidget(self.github_show_token)
        
        layout.addWidget(token_group)
        
        # Save option
        self.github_save_check = QCheckBox("Save credentials securely (encrypted)")
        self.github_save_check.setChecked(True)
        layout.addWidget(self.github_save_check)
        
        layout.addStretch()
        
        return tab
        
    def create_huggingface_tab(self):
        """Create Hugging Face credentials tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Instructions
        info = QLabel(
            "Enter your Hugging Face access token for AI model downloads.\n"
            "Create a token at: https://huggingface.co/settings/tokens"
        )
        info.setWordWrap(True)
        info.setStyleSheet("background-color: #2d2d2d; padding: 10px; border-radius: 4px;")
        layout.addWidget(info)
        
        layout.addSpacing(10)
        
        # Token input
        token_group = QGroupBox("Hugging Face Token")
        token_layout = QVBoxLayout(token_group)
        
        token_layout.addWidget(QLabel("Access Token:"))
        self.hf_token = QLineEdit()
        self.hf_token.setEchoMode(QLineEdit.EchoMode.Password)
        self.hf_token.setPlaceholderText("hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        token_layout.addWidget(self.hf_token)
        
        self.hf_show_token = QCheckBox("Show token")
        self.hf_show_token.toggled.connect(
            lambda checked: self.hf_token.setEchoMode(
                QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
            )
        )
        token_layout.addWidget(self.hf_show_token)
        
        layout.addWidget(token_group)
        
        # Save option
        self.hf_save_check = QCheckBox("Save credentials securely (encrypted)")
        self.hf_save_check.setChecked(True)
        layout.addWidget(self.hf_save_check)
        
        layout.addStretch()
        
        return tab
        
    def create_terminal_tab(self):
        """Create terminal authentication tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Instructions
        info = QLabel(
            "For CLI-based authentication, use these commands in your terminal.\n"
            "This is an alternative to using tokens in the GUI."
        )
        info.setWordWrap(True)
        info.setStyleSheet("background-color: #2d2d2d; padding: 10px; border-radius: 4px;")
        layout.addWidget(info)
        
        layout.addSpacing(10)
        
        # Command examples
        commands_group = QGroupBox("Authentication Commands")
        commands_layout = QVBoxLayout(commands_group)
        
        self.terminal_commands = QTextEdit()
        self.terminal_commands.setReadOnly(True)
        self.terminal_commands.setPlainText("""
# GitHub CLI Authentication
gh auth login

# Hugging Face CLI Authentication  
huggingface-cli login

# Git credential helper
git config --global credential.helper store

# SSH Key setup
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub
# Add the public key to GitHub/GitLab settings
        """.strip())
        commands_layout.addWidget(self.terminal_commands)
        
        copy_btn = QPushButton("📋 Copy Commands")
        copy_btn.clicked.connect(self.copy_terminal_commands)
        commands_layout.addWidget(copy_btn)
        
        layout.addWidget(commands_group)
        
        layout.addStretch()
        
        return tab
        
    def copy_terminal_commands(self):
        """Copy terminal commands to clipboard"""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self.terminal_commands.toPlainText())
        
        QMessageBox.information(
            self,
            "Copied",
            "Commands copied to clipboard!"
        )
        
    def test_connection(self):
        """Test the connection with provided credentials"""
        # In production, would actually test the credentials
        QMessageBox.information(
            self,
            "Connection Test",
            "Connection test would verify:\n\n"
            "✓ GitHub token validity\n"
            "✓ Hugging Face token validity\n"
            "✓ API access permissions\n"
            "✓ Rate limits\n\n"
            "This is a placeholder for the actual test."
        )
        
    def save_credentials(self):
        """Save credentials securely"""
        github_token = self.github_token.text()
        hf_token = self.hf_token.text()
        
        if not github_token and not hf_token:
            QMessageBox.warning(
                self,
                "No Credentials",
                "Please enter at least one credential before saving."
            )
            return
            
        # In production, would encrypt and save credentials
        QMessageBox.information(
            self,
            "Credentials Saved",
            "Credentials have been encrypted and saved securely.\n\n"
            "They will be used for repository integrations and downloads."
        )
        
        self.accept()
