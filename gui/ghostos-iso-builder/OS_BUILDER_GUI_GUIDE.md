# HeckOS Builder GUI - Complete Visual Guide & User Manual

## Table of Contents
1. [GUI Appearance & Layout](#gui-appearance--layout)
2. [System Requirements](#system-requirements)
3. [Drag-and-Drop Interface](#drag-and-drop-interface)
4. [Window Ratios & Panels](#window-ratios--panels)
5. [Editable Previews with Element Movements](#editable-previews-with-element-movements)
6. [AI Assembly Integration](#ai-assembly-integration)
7. [Full Preview Mode](#full-preview-mode)
8. [Complete Instruction Manual](#complete-instruction-manual)

---

## GUI Appearance & Layout

### Overall Visual Design

**Window Dimensions:**
- Default size: 1400x900 pixels
- Minimum size: 1024x768 pixels
- Fully resizable and remembers last size
- Supports fullscreen mode (F11)

**Color Scheme:**
```
Primary Background:   #1e1e1e (Dark charcoal)
Secondary Background: #252525 (Slightly lighter)
Border Color:         #3d3d3d (Medium gray)
Accent Color:         #0078d4 (Microsoft blue)
Success Color:        #107c10 (Green)
Warning Color:        #ff8c00 (Orange)
Error Color:          #e81123 (Red)
Text Primary:         #ffffff (White)
Text Secondary:       #888888 (Light gray)
```

**Visual Structure:**
```
┌──────────────────────────────────────────────────────────────────┐
│ 👻 HeckOS Advanced ISO Builder    [🔑 Credentials] [⚙️ Settings] [⌨ Keyboard] │
├────────────────────────────────┬─────────────────────────────────┤
│                                │                                 │
│  Left Panel (60% width)        │  Right Panel (40% width)        │
│  ┌──────────────────────────┐  │  ┌───────────────────────────┐  │
│  │ 📀 ISO Loader            │  │  │ 👁️ Live Preview           │  │
│  │ 🎨 Theme Editor          │  │  │                           │  │
│  │ 📦 Repository Browser    │  │  │ [Preview Area]            │  │
│  │ 🔧 Driver Manager        │  │  │                           │  │
│  │ 🎮 UI Designer (NEW)     │  │  │ [Component Summary]       │  │
│  └──────────────────────────┘  │  │                           │  │
│                                │  │ [Build Summary]           │  │
│  [Component Selection Area]    │  └───────────────────────────┘  │
│                                │                                 │
│  [Drag-and-Drop Zone]          │  [AI Suggestions Panel]         │
│                                │                                 │
├────────────────────────────────┴─────────────────────────────────┤
│ Ready to build | [🔍 Validate] [💾 Export] [🚀 Build ISO]        │
└──────────────────────────────────────────────────────────────────┘
```

---

## System Requirements

### Hardware Requirements

**Minimum:**
- CPU: Dual-core 2.0 GHz
- RAM: 4 GB
- Storage: 20 GB free space
- Display: 1024x768 resolution
- Mouse/Touchpad or Touchscreen

**Recommended:**
- CPU: Quad-core 3.0 GHz or better
- RAM: 8 GB or more
- Storage: 50 GB+ free space (SSD preferred)
- Display: 1920x1080 or higher
- Touchscreen for drag-and-drop features
- GPU: Any modern GPU for preview rendering

### Software Requirements

**Operating System:**
- Linux: Ubuntu 20.04+, Debian 11+, Fedora 35+
- Windows 10/11 (via WSL2)
- macOS 11+ (experimental)

**Python Dependencies:**
```bash
# Install all requirements
pip install -r requirements.txt

# Core dependencies:
PyQt6 >= 6.4.0
Pillow >= 9.0.0
pyYAML >= 6.0
requests >= 2.28.0
```

**System Tools:**
```bash
# Debian/Ubuntu
sudo apt install genisoimage squashfs-tools xorriso

# Fedora
sudo dnf install genisoimage squashfs-tools xorriso

# Arch
sudo pacman -S cdrtools squashfs-tools xorriso
```

**Launch Command:**
```bash
cd gui/ghostos-iso-builder
./launch-menu.sh
```

---

## Drag-and-Drop Interface

### Button Placements & Widget Library

The GUI includes a comprehensive widget library accessible from the UI Designer tab:

#### Widget Categories

**1. Desktop Elements**
```
┌─ Panel Widgets ──────────────┐
│ • Top Panel                  │
│ • Bottom Panel               │
│ • Side Panel (Left/Right)    │
│ • Floating Panel             │
└──────────────────────────────┘

┌─ Launcher Widgets ───────────┐
│ • Application Menu           │
│ • Dock/Taskbar              │
│ • Quick Launch Bar          │
│ • System Tray               │
└──────────────────────────────┘

┌─ Window Widgets ─────────────┐
│ • Title Bar                  │
│ • Window Buttons             │
│ • Menu Bar                   │
│ • Status Bar                 │
└──────────────────────────────┘
```

**2. Control Elements**
```
┌─ Buttons ────────────────────┐
│ • Standard Button            │
│ • Icon Button                │
│ • Toggle Button              │
│ • Radio Button               │
│ • Checkbox                   │
└──────────────────────────────┘

┌─ Input Fields ───────────────┐
│ • Text Input                 │
│ • Number Input               │
│ • Password Field             │
│ • Search Box                 │
│ • Dropdown Menu              │
└──────────────────────────────┘

┌─ Containers ─────────────────┐
│ • Group Box                  │
│ • Tab Widget                 │
│ • Scroll Area                │
│ • Split Pane                 │
│ • Dialog Window              │
└──────────────────────────────┘
```

#### Drag-and-Drop Workflow

**Step 1: Select Widget**
1. Open "🎮 UI Designer" tab
2. Browse widget library in left sidebar
3. Click on desired widget to select

**Step 2: Drag to Canvas**
1. Hold left mouse button on selected widget
2. Drag widget to preview canvas
3. Visual guide shows drop zones (highlighted in blue)
4. Release to place widget

**Step 3: Configure Widget**
1. Right-click placed widget
2. Select "Properties" from context menu
3. Configure:
   - Size (width, height)
   - Position (x, y coordinates or snap-to-grid)
   - Appearance (colors, borders, shadows)
   - Behavior (click actions, hover effects)
   - Content (text, icons, images)

**Visual Feedback:**
```
Dragging Widget:
┌────────────────────┐
│ [Widget Icon] ↓    │  ← Semi-transparent preview
│  Button Widget     │
└────────────────────┘

Drop Zone Highlighting:
┌────────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Blue glow when hovering
│ ▓▓ Valid Drop Zone     ▓▓  │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
└────────────────────────────┘

Placed Widget:
┌────────────────────┐
│ [Button]           │  ← Solid appearance
│ ◉ ◉ ◉ ◉ ◉ ◉ ◉ ◉   │  ← Resize handles on corners/edges
└────────────────────┘
```

---

## Window Ratios & Panels

### Adjustable Panel System

All panels are adjustable with draggable splitters:

**Default Ratios:**
```
┌─────────────────────────────────┐
│  Main Window: 100%              │
│                                 │
│  ┌─────────┬──────────────────┐ │
│  │ Left    │ Right            │ │
│  │ 60%     │ 40%              │ │
│  │         │                  │ │
│  │         │  ┌──────────────┐│ │
│  │         │  │ Preview: 60% ││ │
│  │         │  └──────────────┘│ │
│  │         │  ┌──────────────┐│ │
│  │         │  │ Summary: 40% ││ │
│  │         │  └──────────────┘│ │
│  └─────────┴──────────────────┘ │
└─────────────────────────────────┘
```

**Adjustable Elements:**

1. **Main Horizontal Splitter**
   - Separates left workspace from right preview
   - Adjustable from 40%-80% left, 20%-60% right
   - Double-click splitter to reset to default (60/40)

2. **Vertical Splitters in Left Panel**
   - Tab area vs. Component selection
   - Configuration panels vs. Options
   - Adjustable heights

3. **Vertical Splitters in Right Panel**
   - Live Preview vs. Component Summary
   - Build Summary vs. AI Suggestions
   - Adjustable from 30%-70%

**Splitter Visual Indicators:**
```
Normal State:
│ Panel A │ │ Panel B │
          ↑
      Splitter (gray)

Hover State:
│ Panel A ║ │ Panel B │
          ↑
  Splitter (blue, thicker)

Dragging:
│ Panel A ┃ │ Panel B │
          ↑
  Splitter (white, animated)
```

**Saved Layouts:**
- Save current layout: File > Save Layout
- Load saved layout: File > Load Layout
- Preset layouts:
  - "Default" (60/40)
  - "Preview Focus" (40/60)
  - "Workspace Focus" (80/20)
  - "Balanced" (50/50)

---

## Editable Previews with Element Movements

### Interactive Preview Canvas

The preview area is fully interactive with real-time editing capabilities:

#### Preview Modes

**1. Static Preview (Default)**
- Shows visual representation of current configuration
- Updates automatically when changes are made
- Non-interactive (view-only)

**2. Interactive Preview (Edit Mode)**
- Enable: Click "🎮 Enable Edit Mode" button
- All elements become selectable and moveable
- Changes reflected in real-time
- Keyboard shortcuts active

**3. Live Preview (Runtime Simulation)**
- Enable: Click "▶️ Live Preview" button
- Simulates actual OS behavior
- Interactive widgets respond to clicks
- Performance monitoring active

#### Element Movement System

**Selection:**
```
Single Click: Select element
  ┌───────────────┐
  │ [Button]      │  ← Selected (blue border)
  └───────────────┘

Ctrl+Click: Multi-select
  ┌───────────────┐
  │ [Button 1]    │  ← Both selected
  └───────────────┘
  ┌───────────────┐
  │ [Button 2]    │
  └───────────────┘

Click-and-Drag: Lasso selection
  ╔═══════════════╗
  ║ ┌─────┐ ┌───┐ ║  ← All within box selected
  ║ └─────┘ └───┘ ║
  ╚═══════════════╝
```

**Movement Methods:**

1. **Freeform Drag**
   - Click and hold element
   - Drag to new position
   - Release to place
   - Visual guides show alignment

2. **Precision Movement (Arrow Keys)**
   ```
   ↑ : Move up 1 pixel
   ↓ : Move down 1 pixel
   ← : Move left 1 pixel
   → : Move right 1 pixel
   
   Shift+Arrow: Move 10 pixels
   Ctrl+Arrow: Snap to grid
   ```

3. **Snap-to-Grid**
   - Enable: View > Grid > Show Grid
   - Configure grid size: 5px, 10px, 20px
   - Elements snap to nearest grid point
   - Visual grid overlay

4. **Alignment Tools**
   ```
   Align Left:   [|||||||]
   Align Center: [||||||]
   Align Right:  [|||||||]
   
   Align Top:    ┬──────
   Align Middle: ┼──────
   Align Bottom: ┴──────
   
   Distribute Horizontally: [|] [|] [|]
   Distribute Vertically:   [|]
                           [|]
                           [|]
   ```

**Visual Feedback During Movement:**

```
Before Movement:
┌────────────────────┐
│  [Button]          │
└────────────────────┘

During Drag:
┌────────────────────┐
│                    │
│     ┊ ┊ ┊ ┊       │  ← Alignment guides
│  ┈┈┈[Button]┈┈┈   │  ← Ghost image at original
│     ┊ ┊ ┊ ┊       │
│  [Button]          │  ← Actual element being moved
└────────────────────┘

After Drop:
┌────────────────────┐
│                    │
│                    │
│  [Button]          │  ← New position
└────────────────────┘
```

#### Resize Handles

When an element is selected, resize handles appear:

```
┌─────◉─────◉─────◉─────┐
│                       │
◉      Element          ◉  ← Corner handles (resize proportionally)
│                       │
◉      Content          ◉  ← Edge handles (resize one dimension)
│                       │
└─────◉─────◉─────◉─────┘
```

**Resize Modes:**
- Drag corner: Proportional resize
- Drag edge: Resize width OR height
- Shift+Drag: Maintain aspect ratio
- Alt+Drag: Resize from center
- Ctrl+Drag: Snap to common sizes

#### Property Inspector

Real-time property editing panel shows:

```
┌─ Properties ─────────────────┐
│ Element: Button              │
│                              │
│ Position:                    │
│   X: [100] px                │
│   Y: [200] px                │
│                              │
│ Size:                        │
│   Width:  [120] px           │
│   Height: [40]  px           │
│                              │
│ Appearance:                  │
│   Background: [#0078d4] 🎨   │
│   Border:     [2]px          │
│   Radius:     [4]px          │
│                              │
│ Text:                        │
│   Content: [Click Me]        │
│   Font:    [Ubuntu 12pt]     │
│   Color:   [#ffffff] 🎨      │
│                              │
│ Actions:                     │
│   On Click: [⚙️ Configure]   │
│   On Hover: [⚙️ Configure]   │
│                              │
│ [ Apply ] [ Reset ]          │
└──────────────────────────────┘
```

---

## AI Assembly Integration

### AI-Powered Design Assistant

The AI Assembly system provides intelligent design suggestions and automated layout generation:

#### AI Features

**1. Smart Layout Suggestions**
```
┌─ AI Assistant ───────────────┐
│ 🤖 Analyzing your design...  │
│                              │
│ Suggestions:                 │
│ • Button too small for text  │
│   → Suggest: 140px width     │
│                              │
│ • Poor color contrast        │
│   → Suggest: #ffffff text    │
│                              │
│ • Elements overlap           │
│   → Auto-align: Enable       │
│                              │
│ [ Apply All ] [ Dismiss ]    │
└──────────────────────────────┘
```

**2. Auto-Arrangement**
- Click "🤖 AI Arrange"
- AI analyzes element relationships
- Automatically positions for optimal UX
- Suggests spacing and alignment
- Preserves user intentions

**3. Component Generation**
```
AI Prompt: "Create a login form with username, password, and login button"

Generated:
┌────────────────────────────┐
│ Username: [____________]   │
│ Password: [____________]   │
│           [   Login   ]    │
└────────────────────────────┘

User can then:
- Move components
- Resize elements
- Modify properties
- Request variations
```

**4. Theme Consistency Checker**
- Analyzes all UI elements
- Identifies color inconsistencies
- Suggests matching colors
- Validates accessibility (WCAG)
- Reports contrast ratios

**5. Layout Templates**
```
AI Library includes:
• Dashboard Layout
• Settings Panel
• File Browser
• Login Screen
• Application Menu
• Control Panel
• Media Player
• Terminal Interface
• System Monitor
• Calendar View
```

#### AI Integration Workflow

**Step-by-Step:**

1. **Activate AI Assistant**
   ```
   Click: View > AI Assistant
   Or: Press F12
   Or: Click 🤖 button in toolbar
   ```

2. **Describe Your Intent**
   ```
   AI Prompt Input:
   ┌─────────────────────────────────┐
   │ Describe what you want:         │
   │ [Create a system control panel] │
   │                                 │
   │ Include:                        │
   │ ☑ Volume control                │
   │ ☑ Brightness slider             │
   │ ☑ Network status                │
   │ ☐ Battery indicator             │
   │                                 │
   │ [ Generate ] [ Clear ]          │
   └─────────────────────────────────┘
   ```

3. **AI Generates Options**
   ```
   ┌─ Design Options ──────────────┐
   │ Option 1: [Preview]           │
   │ Compact vertical layout       │
   │ [ Select ]                    │
   │                               │
   │ Option 2: [Preview]           │
   │ Horizontal with icons         │
   │ [ Select ]                    │
   │                               │
   │ Option 3: [Preview]           │
   │ Grid-based layout             │
   │ [ Select ]                    │
   └───────────────────────────────┘
   ```

4. **Refine with AI**
   ```
   Selected Option 1
   
   AI Refinements:
   • "Make volume slider larger"
   • "Change icons to monochrome"
   • "Add labels below each control"
   • "Use Material Design style"
   ```

5. **Apply to Canvas**
   - AI places components on canvas
   - User can further adjust manually
   - AI watches for inconsistencies
   - Suggests improvements continuously

#### AI-Assisted Drag-and-Drop

When dragging elements, AI provides:

**Smart Snapping:**
```
Dragging [Button]:

AI detects nearby elements:
┌──────────┐
│ [Label]  │
└──────────┘
     ↓ Snap suggestion (10px gap)
┌──────────┐
│ [Button] │  ← Suggested position
└──────────┘
```

**Relationship Recognition:**
```
AI recognizes patterns:

[Label]        +  [Input]
   ↓               ↓
"Username"      [________]
                    ↓
         AI suggests alignment
              and spacing
```

**Automatic Grouping:**
```
Multiple related elements:
[Icon] [Label] [Button]
         ↓
   AI suggests:
   "Group these as 'Menu Item'?"
   [ Yes ] [ No ]
```

---

## Full Preview Mode

### Immersive Preview Experience

Full Preview Mode transforms the entire window into a live preview of the OS interface:

#### Entering Preview Mode

**Methods:**
```
1. Click: "👁️ Preview" button (top toolbar)
2. Press: F5 key
3. Menu: View > Full Preview Mode
4. Quick action: Ctrl+Shift+P
```

**Transition Animation:**
```
Normal View:
┌──────┬──────┐
│ Edit │Prev. │
└──────┴──────┘
     ↓ 300ms fade
┌──────────────┐
│   Preview    │  ← Full window
└──────────────┘
```

#### Preview Mode Interface

**Full-Screen Layout:**
```
┌─────────────────────────────────────────────┐
│ 🔙 Exit Preview    [Scale: 100%▼]  🎯 🔧 ℹ️ │  ← Minimal toolbar
├─────────────────────────────────────────────┤
│                                             │
│                                             │
│         Your OS Design Rendered Here        │
│             (Live & Interactive)            │
│                                             │
│                                             │
│                                             │
│                                             │
├─────────────────────────────────────────────┤
│ Simulation: Desktop | FPS: 60 | RAM: 45MB   │  ← Status bar
└─────────────────────────────────────────────┘
```

**Preview Toolbar (Minimal, Auto-Hide):**
```
┌─────────────────────────────────────────────┐
│ [🔙 Exit] [⚙️ Settings] [📏 Rulers] [ℹ️ Info]│
│                                             │
│ Zoom: [50%] [75%] [100%] [125%] [150%]      │
│                                             │
│ Resolution: [1920x1080▼] [Custom...]        │
└─────────────────────────────────────────────┘
```

#### Interactive Features in Preview Mode

**1. Click-Through Testing**
- All UI elements functional
- Buttons trigger configured actions
- Menus expand and collapse
- Forms accept input
- Dialogs open/close

**2. Hover Effects**
- Tooltips appear
- Highlighting works
- Animations play
- State changes visible

**3. Navigation**
- Switch between screens
- Tab through elements
- Navigate menus
- Test keyboard shortcuts

**4. Performance Monitoring**
```
┌─ Performance Overlay ─────┐
│ FPS:        60            │
│ Frame Time: 16ms          │
│ Memory:     45MB          │
│ CPU:        12%           │
│ GPU:        8%            │
└───────────────────────────┘
```

#### Viewport Scaling

**Scale Options:**
```
50%  - Overview mode (see entire layout)
75%  - Comfortable viewing
100% - Actual size (1:1 pixel)
125% - Magnified for detail work
150% - Maximum zoom
200% - Ultra zoom (detail inspection)

Custom: Enter any percentage
```

**Fit to Window:**
- Auto-scale to fit current window
- Maintains aspect ratio
- Updates on window resize

#### Resolution Simulation

Test different display resolutions:

```
┌─ Resolution Presets ─────────────┐
│ 📱 Mobile:                       │
│    • 360x640  (Phone Portrait)   │
│    • 640x360  (Phone Landscape)  │
│    • 768x1024 (Tablet Portrait)  │
│                                  │
│ 💻 Desktop:                      │
│    • 1366x768  (HD)              │
│    • 1920x1080 (Full HD)         │
│    • 2560x1440 (2K)              │
│    • 3840x2160 (4K)              │
│                                  │
│ 🖥️ Ultrawide:                    │
│    • 2560x1080 (21:9)            │
│    • 3440x1440 (21:9 WQHD)       │
│                                  │
│ 📐 Custom: [____] x [____]       │
└──────────────────────────────────┘
```

#### Exiting Preview Mode

**Methods:**
```
1. Click: "🔙 Exit Preview" button
2. Press: F5 key (toggle)
3. Press: Escape key
4. Click: Outside preview area
```

**Smooth Transition Back:**
```
Preview Mode:
┌──────────────┐
│   Preview    │
└──────────────┘
     ↓ 300ms fade
┌──────┬──────┐
│ Edit │Prev. │  ← Returns to split view
└──────┴──────┘
```

**Changes Preserved:**
- Any edits made in preview are saved
- All measurements recorded
- Performance data logged
- User interactions tracked

---

## Complete Instruction Manual

### Getting Started

#### Installation

**Quick Install:**
```bash
# Clone repository
git clone https://github.com/jameshroop-art/GO-OS.git
cd GO-OS/gui/ghostos-iso-builder

# Install dependencies
pip install -r requirements.txt

# Install system packages (Debian/Ubuntu)
sudo apt install genisoimage squashfs-tools xorriso

# Launch GUI
./launch-menu.sh
```

**Verify Installation:**
```bash
python3 -c "import PyQt6; print('PyQt6 OK')"
python3 -c "from PIL import Image; print('Pillow OK')"
which genisoimage && echo "genisoimage OK"
```

#### First Launch

**Welcome Screen:**
```
┌────────────────────────────────────────┐
│  Welcome to HeckOS Builder!            │
│                                        │
│  Quick Start Guide:                    │
│  1. Load an ISO source                 │
│  2. Select components                  │
│  3. Customize theme                    │
│  4. Build your OS                      │
│                                        │
│  ☑ Don't show this again               │
│                                        │
│  [ Tutorial ] [ Skip ] [ Start ]       │
└────────────────────────────────────────┘
```

### Basic Workflow

#### 1. Load ISO Source

**Step-by-Step:**

1. Click "📀 ISO Loader" tab
2. Click "Browse" button
3. Select source ISO file (Debian/Ubuntu)
4. Wait for analysis (progress bar shows)
5. Review detected components

**Supported Formats:**
- .iso files (standard ISO 9660)
- .img files (disk images)
- Folders (extracted ISO contents)

**Auto-Detection:**
- Distribution name and version
- Desktop environment
- Installed packages
- File system structure
- Boot configuration

#### 2. Select Components

**Component Categories:**
```
┌─ Select Components ─────────────────────┐
│                                         │
│ ☑ Base System (Required)               │
│   ☑ Kernel                              │
│   ☑ Core utilities                      │
│   ☑ System libraries                    │
│                                         │
│ ☐ Desktop Environment                   │
│   ☐ MATE Desktop                        │
│   ☐ XFCE                                │
│   ☐ GNOME (minimal)                     │
│                                         │
│ ☐ Applications                          │
│   ☐ Firefox                             │
│   ☐ LibreOffice                         │
│   ☐ GIMP                                │
│   ☐ VLC Media Player                    │
│                                         │
│ ☐ Development Tools                     │
│   ☐ GCC Compiler                        │
│   ☐ Python 3                            │
│   ☐ Git                                 │
│   ☐ VS Code                             │
│                                         │
│ Estimated Size: 2.4 GB                  │
│                                         │
│ [ Select All ] [ Deselect All ]         │
└─────────────────────────────────────────┘
```

**Smart Selection:**
- Auto-resolve dependencies
- Warn about conflicts
- Suggest related packages
- Show size impact

#### 3. Customize Theme

**Theme Editor Workflow:**

1. Click "🎨 Theme Editor" tab
2. Choose base theme:
   - Light
   - Dark
   - Auto (based on time)
   - Custom

3. Adjust colors:
   ```
   Primary:   [#0078d4] 🎨
   Secondary: [#2b2b2b] 🎨
   Accent:    [#107c10] 🎨
   Text:      [#ffffff] 🎨
   Background:[#1e1e1e] 🎨
   ```

4. Configure elements:
   - Window decorations
   - Panel appearance
   - Icon theme
   - Font family and size
   - Button styles
   - Menu layout

5. Preview changes in real-time

#### 4. Design UI Layout (New!)

**UI Designer Tab:**

1. Click "🎮 UI Designer" tab
2. Choose layout template or start blank
3. Drag widgets from library to canvas
4. Position and resize elements
5. Configure properties
6. Use AI for suggestions
7. Test in Preview Mode

**Widget Library Categories:**
- Panels & Containers
- Buttons & Controls
- Input Fields
- Labels & Text
- Icons & Images
- Menus & Navigation
- System Widgets

#### 5. Validate Configuration

**Before Building:**

1. Click "🔍 Validate Configuration"
2. Review validation report:
   ```
   ┌─ Validation Report ──────────────┐
   │ ✓ ISO source valid               │
   │ ✓ All dependencies resolved      │
   │ ✓ No conflicts detected          │
   │ ✓ Theme properly configured      │
   │ ✓ Sufficient disk space (25 GB)  │
   │ ⚠ Large build size (3.2 GB)      │
   │                                  │
   │ Status: Ready to Build           │
   │                                  │
   │ [ Fix Issues ] [ Continue ]      │
   └──────────────────────────────────┘
   ```

3. Fix any warnings or errors
4. Proceed to build

#### 6. Build ISO

**Build Process:**

1. Click "🚀 Build ISO"
2. Choose output location
3. Enter ISO label (optional)
4. Start build process

**Progress Tracking:**
```
┌─ Building ISO ───────────────────────┐
│                                      │
│ Current Stage: Extracting source    │
│ Progress: ████████░░░░░░░ 56%       │
│                                      │
│ Elapsed Time: 00:08:34               │
│ Estimated Remaining: 00:06:22        │
│                                      │
│ Recent Actions:                      │
│ • Extracted base system              │
│ • Copied desktop packages            │
│ • Applying theme customizations      │
│ • Installing drivers                 │
│                                      │
│ [ Pause ] [ Cancel ]                 │
└──────────────────────────────────────┘
```

**Build Stages:**
1. Extracting source ISO (15%)
2. Selecting components (25%)
3. Applying customizations (40%)
4. Installing additional packages (60%)
5. Generating filesystem (75%)
6. Creating bootloader (85%)
7. Building final ISO (95%)
8. Verification (100%)

**Completion:**
```
┌─ Build Complete! ────────────────────┐
│                                      │
│ ✓ ISO successfully created           │
│                                      │
│ Output: /path/to/heckos-custom.iso   │
│ Size: 2.8 GB                         │
│ MD5: a1b2c3d4...                     │
│                                      │
│ What's Next?                         │
│ • Test in virtual machine            │
│ • Write to USB drive                 │
│ • Share configuration                │
│                                      │
│ [ Open Folder ] [ Write USB ]        │
│ [ Create Another ] [ Exit ]          │
└──────────────────────────────────────┘
```

### Advanced Features

#### Keyboard Shortcuts

**Global:**
```
F1          - Help
F5          - Toggle Full Preview
F11         - Fullscreen
F12         - AI Assistant
Ctrl+S      - Save Configuration
Ctrl+O      - Open Configuration
Ctrl+Z      - Undo
Ctrl+Y      - Redo
Ctrl+Q      - Quit
```

**Canvas (Edit Mode):**
```
Arrow Keys     - Move selected element (1px)
Shift+Arrow    - Move selected element (10px)
Ctrl+Arrow     - Snap to grid
Delete         - Remove selected element
Ctrl+C         - Copy selected element
Ctrl+V         - Paste element
Ctrl+D         - Duplicate element
Ctrl+A         - Select all elements
Ctrl+G         - Group selected elements
Ctrl+U         - Ungroup
```

**View:**
```
Ctrl++         - Zoom in
Ctrl+-         - Zoom out
Ctrl+0         - Reset zoom
Ctrl+R         - Toggle rulers
Ctrl+G         - Toggle grid
Ctrl+L         - Toggle layers panel
```

#### Configuration Management

**Save Configuration:**
```
File > Save Configuration
  ↓
Choose format:
• JSON (recommended)
• YAML
• XML

Include:
☑ Selected components
☑ Theme settings
☑ UI layout
☑ Build options
☑ Custom files
```

**Load Configuration:**
```
File > Load Configuration
  ↓
Select saved configuration file
  ↓
Preview changes
  ↓
[ Apply ] [ Cancel ]
```

**Share Configurations:**
```
File > Export for Sharing
  ↓
Creates portable package:
• Configuration file
• Custom assets
• Theme resources
• Documentation
  ↓
Share as .heckpkg file
```

#### AI Assistant Commands

**Text Commands:**
```
"Create login screen"
"Add volume control"
"Change to dark theme"
"Align buttons vertically"
"Make text larger"
"Center all elements"
"Add shadow to panel"
"Generate system menu"
```

**AI Understands Context:**
```
User: "Add a button"
AI: "Where would you like the button?"
User: "Below the text field"
AI: [Places button, suggests label]
User: "Make it blue"
AI: [Changes to theme accent color]
```

### Troubleshooting

#### Common Issues

**Issue: GUI won't start**
```
Solution:
1. Check Python version: python3 --version
   (Must be 3.8 or higher)
2. Reinstall dependencies: pip install -r requirements.txt --force-reinstall
3. Check system packages: sudo apt install python3-pyqt6
4. Run with debug: python3 main.py --debug
```

**Issue: ISO build fails**
```
Solution:
1. Check disk space: df -h
2. Verify permissions: ls -l /tmp
3. Check source ISO integrity: md5sum source.iso
4. Review build log: cat build.log
5. Try with minimal components
```

**Issue: Preview not updating**
```
Solution:
1. Disable hardware acceleration: Settings > Rendering > Software
2. Update graphics drivers
3. Reduce animation frequency: Settings > Performance
4. Restart application
```

**Issue: Drag-and-drop not working**
```
Solution:
1. Check touch/mouse drivers
2. Calibrate touchscreen: Tools > Calibration
3. Try keyboard shortcuts instead
4. Restart in safe mode
```

#### Getting Help

**Built-in Help:**
- Press F1 for context-sensitive help
- Hover over any element for tooltip
- Click "?" icon for feature explanation

**Community Support:**
- GitHub Issues: [Link]
- Forum: [Link]
- Discord: [Link]
- Documentation: [Link]

**Report a Bug:**
```
Help > Report Issue
  ↓
Form includes:
• Description
• Steps to reproduce
• System information
• Error logs
• Screenshots (auto-capture)
  ↓
Submit to GitHub
```

### Tips and Best Practices

**Performance:**
- Close unused tabs
- Reduce animation frequency for low-end systems
- Use "Preview on demand" instead of live preview
- Build ISOs on SSD when possible

**Design:**
- Use grid snapping for aligned layouts
- Maintain consistent spacing (multiples of 8px)
- Follow desktop environment guidelines
- Test with different resolutions
- Use AI suggestions for accessibility

**Workflow:**
- Save configurations frequently
- Use templates for common designs
- Test builds in VM before writing to USB
- Keep source ISOs organized
- Document custom configurations

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│ HeckOS Builder GUI - Quick Reference                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ LAUNCH: ./launch-menu.sh                               │
│                                                         │
│ ESSENTIAL SHORTCUTS:                                    │
│   F1  - Help      F5  - Preview   F11 - Fullscreen    │
│   F12 - AI        Ctrl+S - Save   Ctrl+Z - Undo       │
│                                                         │
│ WORKFLOW:                                               │
│   1. Load ISO → 2. Select → 3. Theme → 4. Build       │
│                                                         │
│ DRAG-AND-DROP:                                          │
│   • Select widget → Drag → Drop → Configure           │
│   • Arrow keys move selected elements                  │
│   • Ctrl+Click for multi-select                        │
│                                                         │
│ PREVIEW MODE:                                           │
│   • F5 to enter/exit                                   │
│   • Esc to exit                                        │
│   • Interactive testing available                      │
│                                                         │
│ AI ASSISTANT:                                           │
│   • F12 to activate                                    │
│   • Describe intent in plain English                   │
│   • AI generates and refines layouts                   │
│                                                         │
│ SUPPORT:                                                │
│   • F1 for context help                                │
│   • Help > Documentation                               │
│   • Help > Report Issue                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Conclusion

The HeckOS Builder GUI provides a comprehensive, visual environment for creating custom operating system installations. With its drag-and-drop interface, real-time preview, AI-powered assistance, and full-screen preview mode, users can design professional-quality OS distributions without deep technical knowledge.

For the latest updates and detailed documentation, visit the [project repository](https://github.com/jameshroop-art/GO-OS).

**Version:** 1.0.0  
**Last Updated:** 2026-01-15  
**License:** MIT
