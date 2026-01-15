# HeckOS File Types Specification

## Overview

This document defines all file types, formats, and extensions used in the HeckOS operating system, the OS Builder application, and the overall ecosystem. It covers system files, configuration files, user data files, application files, and custom HeckOS-specific formats.

## Table of Contents

1. [File Type Categories](#file-type-categories)
2. [System File Types](#system-file-types)
3. [Configuration File Types](#configuration-file-types)
4. [User Data File Types](#user-data-file-types)
5. [Application File Types](#application-file-types)
6. [HeckOS Custom File Types](#heckos-custom-file-types)
7. [Implementation Guide](#implementation-guide)
8. [MIME Type Registry](#mime-type-registry)
9. [File Association System](#file-association-system)
10. [Creating New File Types](#creating-new-file-types)

---

## File Type Categories

### 1. System Files
- Boot and initialization files
- Kernel and driver files
- System libraries
- Core executables

### 2. Configuration Files
- System configuration
- Application settings
- User preferences
- Theme and appearance

### 3. User Data Files
- Documents and media
- Application data
- Saved projects
- User-created content

### 4. Application Files
- Executable programs
- Application packages
- Scripts and automation
- Plugins and extensions

### 5. Custom HeckOS Files
- HeckOS-specific formats
- OS Builder project files
- Layout and theme files
- Custom metadata files

---

## System File Types

### Boot & Initialization

| Extension | MIME Type | Description | Usage |
|-----------|-----------|-------------|-------|
| `.boot` | `application/x-heckos-boot` | Boot configuration | Bootloader settings |
| `.grub` | `text/x-grub-config` | GRUB configuration | Multi-boot setup |
| `.initrd` | `application/x-compressed-initrd` | Initial RAM disk | Boot initialization |
| `.vmlinuz` | `application/x-linux-kernel` | Linux kernel image | System kernel |

**Implementation:**
```python
BOOT_FILE_TYPES = {
    '.boot': {
        'mime': 'application/x-heckos-boot',
        'handler': 'system.boot.BootConfigHandler',
        'icon': 'boot-config.svg',
        'editable': True,
        'requires_root': True
    },
    '.grub': {
        'mime': 'text/x-grub-config',
        'handler': 'system.boot.GrubConfigHandler',
        'icon': 'grub.svg',
        'editable': True,
        'requires_root': True,
        'syntax_highlight': 'bash'
    }
}
```

### Drivers & Modules

| Extension | MIME Type | Description | Usage |
|-----------|-----------|-------------|-------|
| `.ko` | `application/x-kernel-module` | Kernel module | Linux drivers |
| `.sys` | `application/x-windows-driver` | Windows driver | Emulated drivers |
| `.inf` | `text/x-windows-inf` | Driver information | Driver metadata |
| `.fw` | `application/x-firmware` | Firmware image | Hardware firmware |

**Implementation:**
```python
DRIVER_FILE_TYPES = {
    '.ko': {
        'mime': 'application/x-kernel-module',
        'handler': 'system.drivers.KernelModuleHandler',
        'icon': 'driver.svg',
        'load_command': 'modprobe',
        'requires_root': True
    },
    '.sys': {
        'mime': 'application/x-windows-driver',
        'handler': 'emulator.WindowsDriverHandler',
        'icon': 'windows-driver.svg',
        'vm_required': True
    }
}
```

### Libraries & Dependencies

| Extension | MIME Type | Description | Usage |
|-----------|-----------|-------------|-------|
| `.so` | `application/x-sharedlib` | Shared library | Linux libraries |
| `.dll` | `application/x-ms-dll` | Dynamic link library | Windows libraries |
| `.a` | `application/x-archive` | Static library | Compiled libraries |
| `.dylib` | `application/x-dylib` | Dynamic library | macOS libraries |

---

## Configuration File Types

### System Configuration

| Extension | MIME Type | Description | Usage |
|-----------|-----------|-------------|-------|
| `.conf` | `text/x-config` | Generic configuration | System services |
| `.cfg` | `text/x-config` | Configuration file | Application config |
| `.ini` | `text/x-ini` | INI format config | Windows-style config |
| `.yaml` | `application/x-yaml` | YAML configuration | Modern config format |
| `.toml` | `application/toml` | TOML configuration | Rust-style config |
| `.json` | `application/json` | JSON configuration | Structured config |
| `.xml` | `application/xml` | XML configuration | Enterprise config |

**Implementation:**
```python
CONFIG_FILE_TYPES = {
    '.yaml': {
        'mime': 'application/x-yaml',
        'handler': 'config.YAMLHandler',
        'icon': 'yaml.svg',
        'validator': 'yaml.safe_load',
        'editor': 'config.YAMLEditor',
        'schema_support': True
    },
    '.json': {
        'mime': 'application/json',
        'handler': 'config.JSONHandler',
        'icon': 'json.svg',
        'validator': 'json.loads',
        'editor': 'config.JSONEditor',
        'schema_support': True,
        'pretty_print': True
    }
}
```

### User Preferences

| Extension | MIME Type | Description | Usage |
|-----------|-----------|-------------|-------|
| `.prefs` | `application/x-heckos-prefs` | HeckOS preferences | User settings |
| `.rc` | `text/x-rc-file` | Run control file | Shell configuration |
| `.desktop` | `application/x-desktop` | Desktop entry | Application launchers |
| `.theme` | `application/x-heckos-theme` | Theme package | UI themes |

**Implementation:**
```python
USER_PREF_FILE_TYPES = {
    '.prefs': {
        'mime': 'application/x-heckos-prefs',
        'handler': 'user.PreferencesHandler',
        'icon': 'preferences.svg',
        'format': 'json',
        'encrypted': False,
        'backup_enabled': True,
        'sync_cloud': True
    },
    '.desktop': {
        'mime': 'application/x-desktop',
        'handler': 'system.DesktopEntryHandler',
        'icon': 'desktop-entry.svg',
        'format': 'ini',
        'spec': 'freedesktop.org',
        'auto_register': True
    }
}
```

---

## User Data File Types

### Documents

| Extension | MIME Type | Description | Usage |
|-----------|-----------|-------------|-------|
| `.txt` | `text/plain` | Plain text | Notes, logs |
| `.md` | `text/markdown` | Markdown document | Documentation |
| `.rst` | `text/x-rst` | ReStructuredText | Documentation |
| `.odt` | `application/vnd.oasis.opendocument.text` | OpenDocument text | Word processor |
| `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | Word document | Microsoft Office |
| `.pdf` | `application/pdf` | PDF document | Portable docs |

### Media Files

| Extension | MIME Type | Description | Usage |
|-----------|-----------|-------------|-------|
| `.png` | `image/png` | PNG image | Lossless images |
| `.jpg`/`.jpeg` | `image/jpeg` | JPEG image | Photos |
| `.svg` | `image/svg+xml` | Vector image | Scalable graphics |
| `.gif` | `image/gif` | GIF image | Animated images |
| `.mp3` | `audio/mpeg` | MP3 audio | Music |
| `.mp4` | `video/mp4` | MP4 video | Videos |
| `.webm` | `video/webm` | WebM video | Web videos |

### Archives & Packages

| Extension | MIME Type | Description | Usage |
|-----------|-----------|-------------|-------|
| `.tar` | `application/x-tar` | TAR archive | Unix archives |
| `.gz` | `application/gzip` | GZIP compressed | Compression |
| `.tar.gz` | `application/x-compressed-tar` | Compressed TAR | Linux packages |
| `.zip` | `application/zip` | ZIP archive | Universal archives |
| `.7z` | `application/x-7z-compressed` | 7-Zip archive | High compression |
| `.deb` | `application/vnd.debian.binary-package` | Debian package | Debian/Ubuntu |
| `.rpm` | `application/x-rpm` | RPM package | RedHat/Fedora |

---

## Application File Types

### Executable Files

| Extension | MIME Type | Description | Usage |
|-----------|-----------|-------------|-------|
| `.sh` | `application/x-shellscript` | Shell script | Bash scripts |
| `.py` | `text/x-python` | Python script | Python programs |
| `.exe` | `application/x-msdownload` | Windows executable | Windows programs |
| `.app` | `application/x-application` | Application bundle | macOS apps |
| `.appimage` | `application/x-iso9660-appimage` | AppImage | Portable Linux apps |
| `.flatpak` | `application/vnd.flatpak` | Flatpak package | Sandboxed apps |
| `.snap` | `application/vnd.snap` | Snap package | Ubuntu apps |

**Implementation:**
```python
EXECUTABLE_FILE_TYPES = {
    '.sh': {
        'mime': 'application/x-shellscript',
        'handler': 'exec.ShellScriptHandler',
        'icon': 'shell-script.svg',
        'interpreter': '/bin/bash',
        'permissions': '755',
        'syntax_highlight': 'bash',
        'run_in_terminal': True
    },
    '.py': {
        'mime': 'text/x-python',
        'handler': 'exec.PythonScriptHandler',
        'icon': 'python.svg',
        'interpreter': '/usr/bin/python3',
        'syntax_highlight': 'python',
        'ide_support': True
    },
    '.appimage': {
        'mime': 'application/x-iso9660-appimage',
        'handler': 'exec.AppImageHandler',
        'icon': 'appimage.svg',
        'permissions': '755',
        'fuse_required': True,
        'auto_integrate': True
    }
}
```

### Scripts & Automation

| Extension | MIME Type | Description | Usage |
|-----------|-----------|-------------|-------|
| `.js` | `application/javascript` | JavaScript | Web scripts |
| `.lua` | `text/x-lua` | Lua script | Game scripts |
| `.rb` | `application/x-ruby` | Ruby script | Ruby programs |
| `.pl` | `application/x-perl` | Perl script | Perl programs |
| `.awk` | `text/x-awk` | AWK script | Text processing |

### Development Files

| Extension | MIME Type | Description | Usage |
|-----------|-----------|-------------|-------|
| `.c` | `text/x-c` | C source code | C programs |
| `.cpp` | `text/x-c++` | C++ source code | C++ programs |
| `.h` | `text/x-c-header` | C header file | C/C++ headers |
| `.rs` | `text/x-rust` | Rust source code | Rust programs |
| `.go` | `text/x-go` | Go source code | Go programs |
| `.java` | `text/x-java` | Java source code | Java programs |

---

## HeckOS Custom File Types

### OS Builder Project Files

#### `.heckproject` - HeckOS Project File
**MIME Type:** `application/x-heckos-project`

**Purpose:** Complete OS Builder project with all settings, layouts, and resources

**Format:** JSON-based with embedded resources

**Structure:**
```json
{
  "format_version": "1.0",
  "project": {
    "name": "My Custom OS",
    "version": "1.0.0",
    "author": "username",
    "created": "2026-01-15T10:00:00Z",
    "modified": "2026-01-15T15:00:00Z",
    "description": "Custom gaming OS",
    "tags": ["gaming", "entertainment"]
  },
  "os_configuration": {
    "base_os": "debian-12",
    "kernel_version": "6.1",
    "desktop_environment": "custom",
    "boot_mode": "uefi",
    "architecture": "x86_64"
  },
  "packages": [
    {"name": "firefox", "version": "latest", "repo": "official"},
    {"name": "steam", "version": "latest", "repo": "valve"}
  ],
  "layouts": [
    {"id": "layout_001", "name": "Main UI", "file": "layouts/main.hecklayout"}
  ],
  "themes": [
    {"id": "theme_001", "name": "Dark Theme", "file": "themes/dark.hecktheme"}
  ],
  "resources": {
    "icons": "resources/icons/",
    "wallpapers": "resources/wallpapers/",
    "sounds": "resources/sounds/"
  },
  "build_settings": {
    "iso_name": "heckos-gaming",
    "compression": "xz",
    "optimization": "size"
  }
}
```

**Implementation:**
```python
class HeckProjectHandler:
    """Handler for .heckproject files"""
    
    def __init__(self):
        self.mime_type = 'application/x-heckos-project'
        self.extension = '.heckproject'
        self.icon = 'heck-project.svg'
        
    def load(self, filepath):
        """Load project from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        self.validate(data)
        return Project(data)
        
    def save(self, project, filepath):
        """Save project to file"""
        data = project.to_dict()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
    def validate(self, data):
        """Validate project data"""
        required_fields = ['format_version', 'project', 'os_configuration']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
```

#### `.hecklayout` - HeckOS UI Layout File
**MIME Type:** `application/x-heckos-layout`

**Purpose:** UI layout definition with elements and properties

**Format:** JSON with embedded CSS/JavaScript

**Structure:**
```json
{
  "format_version": "1.0",
  "metadata": {
    "name": "Gaming Dashboard",
    "description": "Console-style gaming interface",
    "author": "username",
    "created": "2026-01-15T10:00:00Z",
    "modified": "2026-01-15T15:00:00Z",
    "tags": ["gaming", "dashboard", "console"],
    "thumbnail": "data:image/png;base64,..."
  },
  "canvas": {
    "width": 1920,
    "height": 1080,
    "background": "#1e1e1e",
    "grid_size": 10,
    "snap_enabled": true
  },
  "elements": [
    {
      "id": "elem_001",
      "type": "panel",
      "name": "Main Panel",
      "properties": {
        "x": 0,
        "y": 0,
        "width": 1920,
        "height": 1080,
        "background_color": "#1e1e1e",
        "border_width": 0,
        "z_index": 0
      },
      "children": ["elem_002", "elem_003"]
    },
    {
      "id": "elem_002",
      "type": "button",
      "name": "Play Button",
      "properties": {
        "x": 100,
        "y": 200,
        "width": 200,
        "height": 60,
        "text": "Play Game",
        "background_color": "#0078d4",
        "text_color": "#ffffff",
        "font_size": 18,
        "border_radius": 8,
        "z_index": 1
      },
      "states": {
        "hover": {
          "background_color": "#1084d8",
          "cursor": "pointer"
        },
        "active": {
          "background_color": "#006cbd"
        }
      },
      "actions": {
        "on_click": "launch_game('steam://rungameid/123')"
      }
    }
  ],
  "custom_css": ".custom-button { transition: all 0.3s; }",
  "custom_js": "function launch_game(url) { window.location = url; }",
  "responsive": {
    "breakpoints": [
      {"width": 1280, "layout_id": "layout_tablet"},
      {"width": 768, "layout_id": "layout_mobile"}
    ]
  }
}
```

**Implementation:**
```python
class HeckLayoutHandler:
    """Handler for .hecklayout files"""
    
    def __init__(self):
        self.mime_type = 'application/x-heckos-layout'
        self.extension = '.hecklayout'
        self.icon = 'layout.svg'
        
    def load(self, filepath):
        """Load layout from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return Layout(data)
        
    def save(self, layout, filepath):
        """Save layout to file"""
        data = layout.to_dict()
        # Generate thumbnail
        data['metadata']['thumbnail'] = self.generate_thumbnail(layout)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
    def generate_thumbnail(self, layout):
        """Generate base64 thumbnail"""
        # Render layout to image and encode
        pass
        
    def export_html(self, layout, filepath):
        """Export layout as standalone HTML"""
        html = self.render_to_html(layout)
        with open(filepath, 'w') as f:
            f.write(html)
```

#### `.hecktheme` - HeckOS Theme File
**MIME Type:** `application/x-heckos-theme`

**Purpose:** Complete theme definition with colors, fonts, and styling

**Format:** JSON with CSS extensions

**Structure:**
```json
{
  "format_version": "1.0",
  "metadata": {
    "name": "Dark Gaming Theme",
    "description": "Dark theme optimized for gaming",
    "author": "username",
    "version": "1.0.0",
    "created": "2026-01-15T10:00:00Z",
    "preview": "data:image/png;base64,..."
  },
  "colors": {
    "primary": "#0078d4",
    "secondary": "#2d2d2d",
    "accent": "#ffa500",
    "background": "#1e1e1e",
    "surface": "#2a2a2a",
    "text": "#e0e0e0",
    "text_secondary": "#b0b0b0",
    "success": "#4caf50",
    "warning": "#ff9800",
    "error": "#f44336",
    "info": "#2196f3"
  },
  "typography": {
    "font_family_primary": "Roboto, sans-serif",
    "font_family_monospace": "Fira Code, monospace",
    "font_size_small": 12,
    "font_size_medium": 14,
    "font_size_large": 18,
    "font_size_xlarge": 24,
    "line_height": 1.5,
    "letter_spacing": 0
  },
  "spacing": {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
    "xxl": 48
  },
  "borders": {
    "radius_small": 4,
    "radius_medium": 8,
    "radius_large": 16,
    "width_thin": 1,
    "width_medium": 2,
    "width_thick": 4
  },
  "shadows": {
    "small": "0 2px 4px rgba(0,0,0,0.1)",
    "medium": "0 4px 8px rgba(0,0,0,0.2)",
    "large": "0 8px 16px rgba(0,0,0,0.3)"
  },
  "animations": {
    "duration_fast": 150,
    "duration_normal": 300,
    "duration_slow": 500,
    "easing": "cubic-bezier(0.4, 0.0, 0.2, 1)"
  },
  "components": {
    "button": {
      "background": "$primary",
      "text_color": "#ffffff",
      "padding": "$spacing.md",
      "border_radius": "$borders.radius_medium",
      "font_size": "$typography.font_size_medium"
    },
    "panel": {
      "background": "$surface",
      "border": "1px solid $colors.secondary",
      "border_radius": "$borders.radius_large",
      "padding": "$spacing.lg"
    }
  }
}
```

**Implementation:**
```python
class HeckThemeHandler:
    """Handler for .hecktheme files"""
    
    def __init__(self):
        self.mime_type = 'application/x-heckos-theme'
        self.extension = '.hecktheme'
        self.icon = 'theme.svg'
        
    def load(self, filepath):
        """Load theme from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return Theme(data)
        
    def apply(self, theme):
        """Apply theme to system"""
        css = self.generate_css(theme)
        self.write_system_css(css)
        
    def generate_css(self, theme):
        """Generate CSS from theme"""
        css = [":root {"]
        for key, value in theme.colors.items():
            css.append(f"  --color-{key}: {value};")
        css.append("}")
        return "\n".join(css)
```

#### `.heckapp` - HeckOS Application Package
**MIME Type:** `application/x-heckos-app`

**Purpose:** Complete application package with executable, resources, and metadata

**Format:** Compressed archive (ZIP-based) with manifest

**Structure:**
```
myapp.heckapp/
├── manifest.json          # Application metadata
├── bin/
│   ├── myapp             # Main executable
│   └── myapp-helper      # Helper binaries
├── lib/
│   └── libmyapp.so       # Shared libraries
├── resources/
│   ├── icons/
│   │   ├── icon-16.png
│   │   ├── icon-32.png
│   │   └── icon-256.png
│   ├── images/
│   └── sounds/
├── config/
│   └── default.conf      # Default configuration
├── docs/
│   ├── README.md
│   └── LICENSE
└── desktop/
    └── myapp.desktop     # Desktop entry
```

**manifest.json:**
```json
{
  "format_version": "1.0",
  "app": {
    "id": "com.example.myapp",
    "name": "My Application",
    "version": "1.0.0",
    "author": "Developer Name",
    "description": "Application description",
    "category": "Games",
    "license": "GPL-3.0"
  },
  "executable": {
    "main": "bin/myapp",
    "type": "native",
    "architecture": ["x86_64", "arm64"]
  },
  "dependencies": [
    {"name": "gtk3", "version": ">=3.24"},
    {"name": "python3", "version": ">=3.8"}
  ],
  "permissions": [
    "network",
    "audio",
    "video",
    "files-home"
  ],
  "install": {
    "prefix": "/opt/heckos/apps/myapp",
    "integration": true,
    "create_launcher": true
  }
}
```

**Implementation:**
```python
class HeckAppHandler:
    """Handler for .heckapp files"""
    
    def __init__(self):
        self.mime_type = 'application/x-heckos-app'
        self.extension = '.heckapp'
        self.icon = 'heck-app.svg'
        
    def install(self, filepath):
        """Install HeckOS application"""
        # Extract archive
        temp_dir = self.extract(filepath)
        
        # Read manifest
        manifest = self.read_manifest(temp_dir)
        
        # Validate dependencies
        self.check_dependencies(manifest)
        
        # Install files
        install_dir = manifest['install']['prefix']
        self.copy_files(temp_dir, install_dir)
        
        # Create desktop entry
        if manifest['install']['create_launcher']:
            self.create_launcher(manifest, install_dir)
            
        # Register application
        self.register_app(manifest)
```

#### `.heckdata` - HeckOS User Data File
**MIME Type:** `application/x-heckos-data`

**Purpose:** Generic user data file with metadata and encryption support

**Format:** JSON with optional encryption

**Structure:**
```json
{
  "format_version": "1.0",
  "metadata": {
    "type": "user_data",
    "created": "2026-01-15T10:00:00Z",
    "modified": "2026-01-15T15:00:00Z",
    "encrypted": false,
    "compressed": true
  },
  "data": {
    // User-specific data structure
  }
}
```

---

## Implementation Guide

### File Type Registration System

**1. Central Registry (`/etc/heckos/filetypes.d/`)**

Create a modular file type registry system:

```python
# /usr/lib/heckos/filetypes/registry.py

class FileTypeRegistry:
    """Central registry for all file types"""
    
    def __init__(self):
        self.types = {}
        self.handlers = {}
        self.mime_map = {}
        self.extension_map = {}
        
    def register_file_type(self, file_type_def):
        """Register a new file type"""
        ext = file_type_def['extension']
        mime = file_type_def['mime_type']
        
        self.types[ext] = file_type_def
        self.mime_map[mime] = ext
        self.extension_map[ext] = mime
        
        # Register handler
        if 'handler' in file_type_def:
            self.register_handler(ext, file_type_def['handler'])
            
    def register_handler(self, extension, handler_class):
        """Register file handler"""
        self.handlers[extension] = handler_class
        
    def get_handler(self, filepath):
        """Get appropriate handler for file"""
        ext = os.path.splitext(filepath)[1]
        return self.handlers.get(ext)
        
    def get_mime_type(self, filepath):
        """Get MIME type for file"""
        ext = os.path.splitext(filepath)[1]
        return self.extension_map.get(ext, 'application/octet-stream')
        
    def load_definitions(self, directory):
        """Load file type definitions from directory"""
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                path = os.path.join(directory, filename)
                with open(path, 'r') as f:
                    definitions = json.load(f)
                for defn in definitions:
                    self.register_file_type(defn)

# Global registry instance
registry = FileTypeRegistry()
registry.load_definitions('/etc/heckos/filetypes.d/')
```

**2. File Type Definition Format (`/etc/heckos/filetypes.d/custom.json`)**

```json
{
  "file_types": [
    {
      "extension": ".heckproject",
      "mime_type": "application/x-heckos-project",
      "description": "HeckOS Project File",
      "category": "project",
      "icon": "heck-project.svg",
      "handler": "heckos.handlers.ProjectHandler",
      "default_app": "heckos-builder",
      "open_with": [
        {"app": "heckos-builder", "name": "OS Builder"},
        {"app": "text-editor", "name": "Text Editor"}
      ],
      "properties": {
        "editable": true,
        "compressed": false,
        "binary": false,
        "text_based": true
      },
      "magic_bytes": null,
      "file_signature": "^{\\s*\"format_version\"",
      "syntax_highlight": "json"
    }
  ]
}
```

**3. File Handler Base Class**

```python
# /usr/lib/heckos/filetypes/base_handler.py

from abc import ABC, abstractmethod

class FileHandler(ABC):
    """Base class for file type handlers"""
    
    def __init__(self):
        self.mime_type = None
        self.extension = None
        self.icon = None
        
    @abstractmethod
    def can_handle(self, filepath):
        """Check if handler can handle this file"""
        pass
        
    @abstractmethod
    def open(self, filepath):
        """Open file and return data"""
        pass
        
    @abstractmethod
    def save(self, data, filepath):
        """Save data to file"""
        pass
        
    def get_info(self, filepath):
        """Get file information"""
        return {
            'path': filepath,
            'size': os.path.getsize(filepath),
            'modified': os.path.getmtime(filepath),
            'mime_type': self.mime_type
        }
        
    def validate(self, data):
        """Validate file data"""
        return True
        
    def convert_to(self, data, target_format):
        """Convert to another format"""
        raise NotImplementedError("Conversion not supported")
```

**4. Example Custom Handler**

```python
# /usr/lib/heckos/handlers/project_handler.py

from heckos.filetypes.base_handler import FileHandler
import json

class ProjectHandler(FileHandler):
    """Handler for .heckproject files"""
    
    def __init__(self):
        super().__init__()
        self.mime_type = 'application/x-heckos-project'
        self.extension = '.heckproject'
        self.icon = 'heck-project.svg'
        
    def can_handle(self, filepath):
        """Check if this is a valid project file"""
        if not filepath.endswith(self.extension):
            return False
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return 'format_version' in data and 'project' in data
        except:
            return False
            
    def open(self, filepath):
        """Open project file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        self.validate(data)
        return data
        
    def save(self, data, filepath):
        """Save project file"""
        self.validate(data)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
    def validate(self, data):
        """Validate project data structure"""
        required = ['format_version', 'project', 'os_configuration']
        for field in required:
            if field not in data:
                raise ValueError(f"Invalid project file: missing {field}")
        return True
        
    def get_preview(self, filepath):
        """Get preview information"""
        data = self.open(filepath)
        return {
            'name': data['project']['name'],
            'version': data['project']['version'],
            'description': data['project'].get('description', ''),
            'created': data['project']['created'],
            'author': data['project'].get('author', 'Unknown')
        }
```

---

## MIME Type Registry

### System MIME Database (`/usr/share/mime/packages/heckos.xml`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
  
  <!-- HeckOS Project File -->
  <mime-type type="application/x-heckos-project">
    <comment>HeckOS Project File</comment>
    <glob pattern="*.heckproject"/>
    <magic priority="50">
      <match type="string" offset="0:256" value='{&quot;format_version&quot;'/>
    </magic>
    <icon name="heck-project"/>
  </mime-type>
  
  <!-- HeckOS Layout File -->
  <mime-type type="application/x-heckos-layout">
    <comment>HeckOS UI Layout File</comment>
    <glob pattern="*.hecklayout"/>
    <magic priority="50">
      <match type="string" offset="0:256" value='{&quot;format_version&quot;'/>
    </magic>
    <icon name="layout"/>
  </mime-type>
  
  <!-- HeckOS Theme File -->
  <mime-type type="application/x-heckos-theme">
    <comment>HeckOS Theme File</comment>
    <glob pattern="*.hecktheme"/>
    <icon name="theme"/>
  </mime-type>
  
  <!-- HeckOS Application Package -->
  <mime-type type="application/x-heckos-app">
    <comment>HeckOS Application Package</comment>
    <glob pattern="*.heckapp"/>
    <icon name="heck-app"/>
  </mime-type>
  
  <!-- HeckOS User Data File -->
  <mime-type type="application/x-heckos-data">
    <comment>HeckOS User Data File</comment>
    <glob pattern="*.heckdata"/>
    <icon name="heck-data"/>
  </mime-type>
  
</mime-info>
```

**Install MIME types:**
```bash
sudo cp heckos.xml /usr/share/mime/packages/
sudo update-mime-database /usr/share/mime
```

---

## File Association System

### Desktop Integration (`/usr/share/applications/heckos-builder.desktop`)

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=HeckOS Builder
Comment=Build and customize HeckOS
Exec=heckos-builder %F
Icon=heckos-builder
Terminal=false
Categories=Development;IDE;
MimeType=application/x-heckos-project;application/x-heckos-layout;application/x-heckos-theme;
StartupNotify=true
```

### Default Applications (`/etc/heckos/defaults.list`)

```ini
[Default Applications]
application/x-heckos-project=heckos-builder.desktop
application/x-heckos-layout=heckos-builder.desktop
application/x-heckos-theme=heckos-builder.desktop
application/x-heckos-app=heckos-installer.desktop
application/x-heckos-data=heckos-viewer.desktop
```

---

## Creating New File Types

### Step-by-Step Guide

**1. Define File Type Structure**

Decide on:
- File extension (e.g., `.myformat`)
- MIME type (e.g., `application/x-heckos-myformat`)
- File format (JSON, XML, binary, etc.)
- Data structure
- Metadata requirements

**2. Create File Type Definition**

```json
{
  "file_types": [
    {
      "extension": ".myformat",
      "mime_type": "application/x-heckos-myformat",
      "description": "My Custom Format",
      "category": "custom",
      "icon": "my-format.svg",
      "handler": "heckos.handlers.MyFormatHandler",
      "default_app": "my-format-editor",
      "properties": {
        "editable": true,
        "binary": false,
        "text_based": true
      }
    }
  ]
}
```

**3. Implement File Handler**

```python
from heckos.filetypes.base_handler import FileHandler

class MyFormatHandler(FileHandler):
    def __init__(self):
        super().__init__()
        self.mime_type = 'application/x-heckos-myformat'
        self.extension = '.myformat'
        
    def can_handle(self, filepath):
        return filepath.endswith(self.extension)
        
    def open(self, filepath):
        # Implement file opening logic
        pass
        
    def save(self, data, filepath):
        # Implement file saving logic
        pass
```

**4. Register MIME Type**

Create `/usr/share/mime/packages/myformat.xml`:
```xml
<mime-type type="application/x-heckos-myformat">
  <comment>My Custom Format</comment>
  <glob pattern="*.myformat"/>
  <icon name="my-format"/>
</mime-type>
```

**5. Create Desktop Application Entry**

Create `/usr/share/applications/my-format-editor.desktop`:
```ini
[Desktop Entry]
Name=My Format Editor
Exec=my-format-editor %F
MimeType=application/x-heckos-myformat;
Icon=my-format
```

**6. Install and Update**

```bash
# Copy file type definition
sudo cp myformat.json /etc/heckos/filetypes.d/

# Install MIME type
sudo cp myformat.xml /usr/share/mime/packages/
sudo update-mime-database /usr/share/mime

# Install desktop entry
sudo cp my-format-editor.desktop /usr/share/applications/
sudo update-desktop-database /usr/share/applications
```

---

## File Type Utilities

### Command-Line Tools

**`heckos-filetype` - File Type Management Tool**

```bash
# List all registered file types
heckos-filetype list

# Get info about a file type
heckos-filetype info .heckproject

# Register a new file type
heckos-filetype register /path/to/definition.json

# Unregister a file type
heckos-filetype unregister .myformat

# Validate a file
heckos-filetype validate myfile.heckproject

# Convert between formats
heckos-filetype convert input.hecklayout output.html
```

**Implementation:**
```python
#!/usr/bin/env python3
# /usr/bin/heckos-filetype

import sys
import argparse
from heckos.filetypes.registry import registry

def list_types():
    """List all registered file types"""
    for ext, info in registry.types.items():
        print(f"{ext:20} {info['mime_type']:40} {info['description']}")

def info(extension):
    """Show detailed info about a file type"""
    if extension in registry.types:
        info = registry.types[extension]
        for key, value in info.items():
            print(f"{key:15}: {value}")
    else:
        print(f"Unknown file type: {extension}")

def main():
    parser = argparse.ArgumentParser(description='HeckOS File Type Manager')
    subparsers = parser.add_subparsers(dest='command')
    
    subparsers.add_parser('list', help='List all file types')
    info_parser = subparsers.add_parser('info', help='Get file type info')
    info_parser.add_argument('extension', help='File extension')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_types()
    elif args.command == 'info':
        info(args.extension)

if __name__ == '__main__':
    main()
```

---

## Best Practices

### File Format Design

1. **Use Standard Formats When Possible**
   - JSON for structured data
   - YAML for configuration
   - XML for complex hierarchies
   - Binary only when necessary

2. **Include Version Information**
   - Always include `format_version` field
   - Support backward compatibility
   - Provide migration tools

3. **Add Comprehensive Metadata**
   - Creation/modification timestamps
   - Author information
   - Description and tags
   - Thumbnail/preview data

4. **Implement Validation**
   - Schema validation
   - Magic number checking
   - Data integrity verification

5. **Support Compression**
   - Use gzip/zlib for text data
   - Store thumbnails as base64
   - Optional compression flag

6. **Enable Extensibility**
   - Allow custom fields
   - Support plugins/extensions
   - Version-aware parsing

---

## Summary

This specification defines:

1. **System File Types** - Boot, drivers, libraries
2. **Configuration File Types** - System and user settings
3. **User Data File Types** - Documents, media, archives
4. **Application File Types** - Executables, scripts, packages
5. **HeckOS Custom File Types** - Project files, layouts, themes, apps, data
6. **Implementation System** - Registry, handlers, MIME types
7. **File Association** - Desktop integration, default apps
8. **Creation Guide** - Step-by-step for new file types
9. **Utilities** - Command-line tools for management

All file types are designed to be:
- **Extensible** - Easy to add new types
- **Interoperable** - Work with standard tools
- **User-friendly** - Clear associations and icons
- **Validated** - Built-in integrity checking
- **Versioned** - Support format evolution
