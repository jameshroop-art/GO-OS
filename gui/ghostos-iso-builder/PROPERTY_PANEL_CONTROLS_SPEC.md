# Property Panel Visual & Interactable Controls Specification

## Overview

This document details all visual and interactable controls required for the Property Panel to provide comprehensive, user-friendly layout management in the HeckOS OS Builder.

## Table of Contents

1. [Element Properties](#element-properties)
2. [Layout Management](#layout-management)
3. [Visual Controls](#visual-controls)
4. [Interactive Controls](#interactive-controls)
5. [Save/Load System](#saveload-system)
6. [User Experience](#user-experience)

---

## Element Properties

### 1. Position & Transform Controls

**Numeric Spinboxes:**
- **X Position** (0-9999px) - Horizontal position with ±1px buttons
- **Y Position** (0-9999px) - Vertical position with ±1px buttons
- **Width** (20-9999px) - Element width with ±1px buttons
- **Height** (20-9999px) - Element height with ±1px buttons

**Visual Features:**
- Direct numeric entry (keyboard)
- Increment/decrement arrows (mouse)
- Drag-to-adjust slider option
- Unit display (px, %, em)
- Live preview as values change

**Advanced Transform:**
- **Rotation** (0-360°) - Circular dial + numeric input
- **Scale X** (0.1x-5.0x) - Horizontal scaling
- **Scale Y** (0.1x-5.0x) - Vertical scaling
- **Skew X/Y** (-45° to +45°) - Perspective distortion
- **Opacity** (0-100%) - Transparency slider

### 2. Appearance Controls

**Color Pickers:**
- **Background Color**
  - Color swatch preview (30x30px)
  - Click to open color picker dialog
  - Hex input field (#RRGGBB)
  - RGB sliders (R: 0-255, G: 0-255, B: 0-255)
  - HSV sliders (H: 0-360°, S: 0-100%, V: 0-100%)
  - Alpha channel (0-100% transparency)
  - Eyedropper tool (pick from screen)
  - Recently used colors palette
  - Preset color palette (material design, flat UI)

- **Text Color**
  - Same features as background color
  - Contrast checker (WCAG AA/AAA compliance)
  - Auto-suggest readable colors

- **Border Color**
  - Same features as background color

- **Gradient Support**
  - Linear gradient (start/end colors, angle)
  - Radial gradient (center color, edge color, radius)
  - Multiple color stops
  - Visual gradient editor

**Border Controls:**
- **Border Width** (0-50px) - Slider + numeric input
- **Border Style** - Dropdown: Solid, Dashed, Dotted, Double, Groove, Ridge, Inset, Outset
- **Border Radius** (0-500px) - Individual corner control:
  - Top-Left
  - Top-Right
  - Bottom-Right
  - Bottom-Left
  - Lock button (apply to all corners)
- **Border Radius Visual Editor** - Interactive corner handles

**Shadow Controls:**
- **Box Shadow**
  - X Offset (-100 to +100px)
  - Y Offset (-100 to +100px)
  - Blur Radius (0-100px)
  - Spread Radius (-50 to +50px)
  - Color picker
  - Multiple shadows support
  - Visual shadow preview

- **Text Shadow**
  - Same parameters as box shadow
  - Multiple shadows for effects

### 3. Typography Controls

**Font Selection:**
- **Font Family** - Dropdown with preview
  - System fonts list
  - Google Fonts integration
  - Custom font upload
  - Font preview in dropdown
  - Search/filter fonts

**Font Properties:**
- **Font Size** (8-200px) - Slider + numeric input
- **Font Weight** - Dropdown: Thin, Light, Regular, Medium, Bold, ExtraBold, Black
- **Font Style** - Buttons: Normal, Italic, Oblique
- **Text Decoration** - Multi-select: None, Underline, Overline, Line-through
- **Text Transform** - Dropdown: None, Uppercase, Lowercase, Capitalize
- **Letter Spacing** (-10 to +50px) - Slider + numeric
- **Line Height** (0.5-5.0) - Slider + numeric
- **Word Spacing** (-20 to +100px) - Slider + numeric

**Text Alignment:**
- Icon buttons:
  - Left align ⬅️
  - Center align ↔️
  - Right align ➡️
  - Justify ⬌
- Vertical alignment:
  - Top ⬆️
  - Middle ↕️
  - Bottom ⬇️

**Text Content:**
- **Single-line** - QLineEdit with placeholder
- **Multi-line** - QTextEdit with rich text support
- **Character counter** - Shows current/max length
- **Smart quotes** - Convert straight quotes to curly
- **Auto-capitalize** - Toggle option

### 4. Layout & Spacing Controls

**Padding:**
- **All Sides** (0-200px) - Quick set all
- **Individual Sides:**
  - Padding Top
  - Padding Right
  - Padding Bottom
  - Padding Left
- **Lock button** - Apply value to all sides
- **Visual padding editor** - Interactive box model

**Margin:**
- Same structure as Padding
- Support for auto margins
- Negative margins (-200 to +200px)

**Z-Index:**
- **Layer Order** (-100 to +100) - Spinbox
- **Quick buttons:**
  - Send to Back
  - Send Backward
  - Bring Forward
  - Bring to Front
- **Visual layer stack** - Drag-to-reorder list

**Display Properties:**
- **Display** - Dropdown: Block, Inline, Inline-Block, Flex, Grid, None
- **Visibility** - Dropdown: Visible, Hidden, Collapse
- **Overflow** - Dropdown: Visible, Hidden, Scroll, Auto
- **Position** - Dropdown: Static, Relative, Absolute, Fixed, Sticky

### 5. Interactive Properties

**State-Based Styling:**
- **Tabs for states:**
  - Normal (default)
  - Hover (mouse over)
  - Active (being clicked)
  - Focus (keyboard focus)
  - Disabled (inactive)
- Each state has its own property values
- Visual indicator of which state is being edited

**Animation Controls:**
- **Transition Property** - Multi-select: All, Background, Color, Transform, etc.
- **Duration** (0-10000ms) - Slider + numeric
- **Timing Function** - Dropdown: Linear, Ease, Ease-In, Ease-Out, Ease-In-Out, Cubic-Bezier
- **Delay** (0-5000ms) - Slider + numeric
- **Preview animation** button

**Interaction Settings:**
- **Cursor Style** - Dropdown: Default, Pointer, Move, Text, Wait, Help, etc.
- **User Select** - Dropdown: Auto, None, Text, All
- **Pointer Events** - Dropdown: Auto, None
- **Tooltip Text** - Text input
- **Tab Index** (0-999) - Spinbox for keyboard navigation order

### 6. Element-Specific Controls

**Button Properties:**
- **Button Type** - Dropdown: Primary, Secondary, Danger, Success, Warning, Info, Link
- **Button Size** - Dropdown: Small, Medium, Large, Extra Large
- **Icon** - Icon picker with search
- **Icon Position** - Dropdown: Left, Right, Top, Bottom
- **Click Action** - Dropdown: None, Open URL, Execute Command, Show Dialog, Close Window

**Input Field Properties:**
- **Input Type** - Dropdown: Text, Password, Email, Number, Tel, URL, Date, Time, etc.
- **Placeholder Text** - Text input
- **Max Length** (0-9999) - Spinbox
- **Pattern** - Regex validation pattern
- **Required** - Checkbox
- **Read-only** - Checkbox
- **Auto-complete** - Checkbox

**Image Properties:**
- **Image Source** - File picker button
- **Alt Text** - Text input (accessibility)
- **Object Fit** - Dropdown: Fill, Contain, Cover, Scale-Down, None
- **Image Filter:** Grayscale, Blur, Brightness, Contrast, Sepia sliders

**Container Properties:**
- **Flex Direction** - Dropdown: Row, Column, Row-Reverse, Column-Reverse
- **Justify Content** - Dropdown: Start, End, Center, Space-Between, Space-Around, Space-Evenly
- **Align Items** - Dropdown: Start, End, Center, Stretch, Baseline
- **Flex Wrap** - Dropdown: No-Wrap, Wrap, Wrap-Reverse
- **Gap** (0-100px) - Row and column gap controls

---

## Layout Management

### 1. Save Layout Controls

**Save Button Section:**
- **Save Layout** button (primary action)
  - Keyboard shortcut: Ctrl+S
  - Icon: 💾
  - Confirmation message on success

**Save Options:**
- **Layout Name** - Text input with validation
  - Character limit: 50
  - Auto-suggest based on content
  - Duplicate name warning

- **Description** - Multi-line text area
  - Character limit: 500
  - Optional field
  - Markdown support

- **Tags** - Multi-select/add custom tags
  - Quick filters: Dashboard, Login, Settings, Form, etc.
  - Create new tags on the fly
  - Tag autocomplete

- **Thumbnail** - Auto-generated preview
  - 280x200px canvas snapshot
  - Manual crop/adjust option
  - Upload custom thumbnail

**Save Location:**
- **Category** - Dropdown: My Layouts, Shared, Templates, Favorites
- **Folder** - Tree view selector
  - Create new folder option
  - Nested folder support
  - Recent folders quick access

### 2. Load Layout Controls

**Load Button Section:**
- **Load Layout** button
  - Keyboard shortcut: Ctrl+O
  - Icon: 📂
  - Shows load dialog

**Load Dialog:**
- **Layout Browser:**
  - Grid view with thumbnails
  - List view with details
  - Toggle view button
  - Sort options: Name, Date, Size, Rating
  - Filter by: Category, Tags, Date range
  - Search box with instant filtering

- **Layout Preview:**
  - Large thumbnail (400x300px)
  - Layout name and description
  - Creation date and modified date
  - Element count
  - File size
  - Author (if shared)
  - Star rating

- **Load Options:**
  - **Replace current** - Clear canvas and load
  - **Merge** - Add to existing elements
  - **Load as template** - Load but keep as unsaved

**Recent Layouts:**
- Quick access panel (sidebar)
- Last 10 opened layouts
- Pin favorite layouts
- One-click load

### 3. Export/Import Controls

**Export Options:**
- **Export as JSON** - Full layout data
  - Pretty-printed format
  - Compressed format option
  - Include metadata checkbox

- **Export as HTML** - Standalone HTML file
  - Inline CSS
  - External CSS option
  - Include JavaScript checkbox

- **Export as Image** - Screenshot of layout
  - PNG (lossless)
  - JPG (compressed)
  - SVG (vector)
  - Custom resolution

- **Export as PDF** - Printable documentation
  - Include properties table
  - Include screenshots
  - Page size: A4, Letter, Custom

**Import Options:**
- **Import JSON** - Load from file
  - Validation check
  - Error messages for invalid files
  - Migration for old format versions

- **Import from URL** - Fetch remote layout
  - URL input field
  - Authentication support
  - Download progress bar

- **Import from Clipboard** - Paste layout data
  - Auto-detect format
  - Validation

### 4. Version Control

**Layout Versions:**
- **Auto-save** - Every 5 minutes
  - Save to temp location
  - Auto-recovery on crash
  - Configurable interval

- **Version History:**
  - Timeline view of all saves
  - Compare versions (diff view)
  - Restore to previous version
  - Branch from version

- **Version Info:**
  - Version number (v1, v2, v3...)
  - Timestamp
  - Changes summary
  - Revert button

**Collaboration:**
- **Share Layout** button
  - Generate shareable link
  - Set permissions: View-only, Edit, Comment
  - Expiration date option

- **Comments** - Review feedback
  - Pin comments to elements
  - Resolve/archive comments
  - @mention users

---

## Visual Controls

### 1. Live Preview Panel

**Real-time Updates:**
- Preview updates instantly as properties change
- No manual refresh needed
- Smooth transitions

**Preview Options:**
- **Scale** - Dropdown: 25%, 50%, 75%, 100%, 150%, 200%, Fit
- **Background** - Toggle: Transparent, White, Dark, Custom color
- **Rulers** - Toggle horizontal/vertical rulers (shows px measurements)
- **Guides** - Toggle alignment guides
- **Grid** - Toggle grid overlay (configurable spacing)

**Interactive Preview:**
- **Click to select** - Click elements in preview to select
- **Hover highlight** - Highlight elements on hover
- **Context menu** - Right-click for quick actions

### 2. Visual Indicators

**Selection Feedback:**
- Blue outline around selected element
- Resize handles (8 points) on corners and edges
- Rotation handle at top center
- Bounding box measurements displayed

**Property Status:**
- **Modified indicator** - * next to changed properties
- **Default value** - Gray text for defaults
- **Custom value** - White text for user-set values
- **Invalid value** - Red border on invalid inputs

**Validation:**
- Real-time validation as user types
- Error icon ❌ for invalid values
- Warning icon ⚠️ for potentially problematic values
- Info icon ℹ️ for helpful tips
- Tooltip messages on hover

### 3. Color Coding

**Property Categories:**
- **Position/Size** - Blue theme
- **Appearance** - Green theme
- **Typography** - Orange theme
- **Layout** - Purple theme
- **Interactive** - Red theme

**State Indicators:**
- Enabled: Full color
- Disabled: Grayed out
- Hover: Highlighted
- Active: Bright accent

---

## Interactive Controls

### 1. Smart Input Fields

**Auto-completion:**
- Color names (red, blue, etc.) → hex values
- CSS units (10px, 1em, 50%, etc.)
- Font names with fuzzy matching

**Calculations:**
- Math expressions: "100 + 50" → 150
- Percentage calculations: "50% of 400" → 200
- Unit conversions: "2em" → "32px"

**Keyboard Shortcuts in Fields:**
- **↑/↓** - Increment/decrement by 1
- **Shift + ↑/↓** - Increment/decrement by 10
- **Ctrl + ↑/↓** - Increment/decrement by 0.1
- **Enter** - Apply and close
- **Esc** - Cancel changes

### 2. Drag Interactions

**Value Sliders:**
- Click-and-drag number labels to adjust
- Horizontal drag for numeric values
- Visual feedback bar showing value range
- Snap to common values (0, 50%, 100%)

**Color Dragging:**
- Drag color swatches to other color fields
- Drag from eyedropper tool
- Drag to create gradient

### 3. Multi-selection Editing

**Batch Edit:**
- When multiple elements selected
- Show only common properties
- **"Mixed"** indicator for different values
- Apply change to all selected elements

**Smart Defaults:**
- Preserve differences while editing
- Relative changes (e.g., +10px to all)
- Absolute changes (set all to same value)

### 4. Undo/Redo System

**Undo Stack:**
- **Undo** button (Ctrl+Z)
- **Redo** button (Ctrl+Y)
- History panel:
  - List of all actions
  - Jump to any point in history
  - Clear history option

**Action Types Tracked:**
- Property changes
- Element creation/deletion
- Move/resize operations
- Layout load/save

---

## Save/Load System

### 1. File Format

**JSON Structure:**
```json
{
  "metadata": {
    "name": "My Layout",
    "description": "Dashboard interface",
    "version": "1.0",
    "created": "2026-01-15T10:00:00Z",
    "modified": "2026-01-15T15:00:00Z",
    "author": "username",
    "tags": ["dashboard", "admin"],
    "thumbnail": "base64..."
  },
  "canvas": {
    "width": 1400,
    "height": 900,
    "background": "#1e1e1e",
    "grid_size": 10,
    "snap_enabled": true
  },
  "elements": [
    {
      "id": "elem_001",
      "type": "button",
      "properties": {
        "x": 100,
        "y": 200,
        "width": 150,
        "height": 40,
        "text": "Click Me",
        "background_color": "#0078d4",
        ...
      },
      "states": {
        "hover": {...},
        "active": {...}
      }
    }
  ],
  "custom_css": "...",
  "custom_js": "..."
}
```

### 2. Auto-save Features

**Auto-save Settings:**
- **Enable auto-save** - Checkbox
- **Interval** - Dropdown: 1, 5, 10, 15, 30 minutes
- **Max versions** - Keep last N auto-saves (1-20)
- **Location** - Local, Cloud, Both

**Recovery:**
- **Auto-recovery dialog** - Shows on startup if crash detected
- List of available auto-saves
- Preview available
- Choose to restore or discard

### 3. Cloud Sync (Optional)

**Cloud Storage:**
- **Account integration** - Sign in to cloud service
- **Sync status** - Indicator: Synced ✓, Syncing ⟳, Error ❌
- **Conflict resolution** - Choose local or remote version
- **Offline mode** - Cache locally, sync when online

**Collaboration Features:**
- Real-time co-editing
- See who's viewing/editing
- Lock elements being edited
- Chat/comments system

---

## User Experience

### 1. Keyboard Shortcuts

**General:**
- `Ctrl+S` - Save layout
- `Ctrl+Shift+S` - Save as...
- `Ctrl+O` - Open layout
- `Ctrl+N` - New layout
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+C` - Copy element
- `Ctrl+V` - Paste element
- `Ctrl+D` - Duplicate element
- `Delete` - Delete selected elements

**Navigation:**
- `Tab` - Next property field
- `Shift+Tab` - Previous property field
- `Enter` - Apply property
- `Esc` - Cancel edit
- `F2` - Rename selected element

**View:**
- `Ctrl++` - Zoom in
- `Ctrl+-` - Zoom out
- `Ctrl+0` - Reset zoom
- `F5` - Full preview mode

### 2. Tooltips & Help

**Interactive Help:**
- Hover tooltip on every control
- "?" icon for detailed help
- Context-sensitive help panel
- Video tutorials linked
- Example values shown

**Tooltips Include:**
- Control purpose
- Expected value range
- Keyboard shortcuts
- Common uses
- Related properties

### 3. Responsive Design

**Panel Resize:**
- Draggable splitters
- Collapsible sections
- Minimum/maximum widths
- Remember user preferences

**Compact Mode:**
- Toggle for smaller panel
- Hide less-used properties
- Icon-only buttons
- Accordion groups

### 4. Accessibility

**Screen Reader Support:**
- ARIA labels on all controls
- Keyboard navigation for everything
- Focus indicators
- Announce value changes

**High Contrast:**
- High contrast theme option
- Larger text option
- Keyboard-only mode
- Colorblind-friendly indicators

### 5. Customization

**User Preferences:**
- **Property order** - Drag to reorder property groups
- **Show/hide properties** - Checkbox list to toggle
- **Default values** - Set custom defaults
- **Quick actions** - Add favorite properties to toolbar
- **Theme** - Light, Dark, System, Custom

**Workspace Presets:**
- Beginner (simple properties)
- Advanced (all properties)
- Developer (CSS/code view)
- Designer (visual focus)

---

## Property Panel Sections Layout

### Visual Organization:

```
╔═══════════════════════════════════════╗
║ Properties Panel          [?] [⚙] [×] ║
╠═══════════════════════════════════════╣
║ Element Info                          ║
║ ─────────────────────────────────     ║
║ Type: Button    ID: btn_001           ║
║ Name: [Primary Button          ]      ║
╠═══════════════════════════════════════╣
║ 📐 Position & Size          [−]       ║
║ ┌─────────────────────────────────┐   ║
║ │ X: [100]  Y: [200]              │   ║
║ │ W: [150]  H: [40]               │   ║
║ │ [Lock aspect ratio ☐]           │   ║
║ └─────────────────────────────────┘   ║
╠═══════════════════════════════════════╣
║ 🎨 Appearance               [−]       ║
║ ┌─────────────────────────────────┐   ║
║ │ Background: [██] #0078d4  [Pick]│   ║
║ │ Text Color: [██] #ffffff  [Pick]│   ║
║ │ Border Width: ▬▬▬●────── 2px    │   ║
║ │ Border Radius: ▬▬●─────── 4px   │   ║
║ └─────────────────────────────────┘   ║
╠═══════════════════════════════════════╣
║ 📝 Typography               [−]       ║
║ 🔧 Layout                   [+]       ║
║ ⚡ Interactive              [+]       ║
║ 🎭 States                   [+]       ║
╠═══════════════════════════════════════╣
║ [💾 Save Layout] [📂 Load Layout]     ║
║ [📤 Export]      [📥 Import]          ║
╠═══════════════════════════════════════╣
║ Recent Layouts:                       ║
║ ├─ 🕐 Dashboard v2                    ║
║ ├─ 🕐 Login Screen                    ║
║ └─ 🕐 Settings Panel                  ║
╚═══════════════════════════════════════╝
```

---

## Implementation Priority

### Phase 1 (Essential):
1. ✅ Basic position/size controls
2. ✅ Color pickers (background, text, border)
3. ✅ Text property editor
4. ✅ Number spinboxes
5. ✅ Choice dropdowns
6. ⚠️ Save/Load buttons (add functionality)
7. ⚠️ File format (JSON)

### Phase 2 (Enhanced):
8. ⬜ Typography controls (font family, size, weight)
9. ⬜ Border radius controls
10. ⬜ Layout properties (padding, margin)
11. ⬜ Z-index/layering
12. ⬜ Auto-save system
13. ⬜ Version history
14. ⬜ Layout browser with thumbnails

### Phase 3 (Advanced):
15. ⬜ State-based styling (hover, active, focus)
16. ⬜ Animation controls
17. ⬜ Gradient editor
18. ⬜ Shadow controls
19. ⬜ Transform controls (rotate, scale, skew)
20. ⬜ Batch editing
21. ⬜ Cloud sync (optional)

### Phase 4 (Professional):
22. ⬜ Collaboration features
23. ⬜ Custom CSS editor
24. ⬜ Responsive breakpoints
25. ⬜ Component library
26. ⬜ Design tokens
27. ⬜ Export to multiple formats

---

## Summary

The Property Panel is the **central hub** for all element editing and layout management. It must provide:

1. **Comprehensive controls** for every element property
2. **Intuitive visual editors** (color pickers, sliders, visual editors)
3. **Robust save/load system** with versioning and collaboration
4. **Real-time feedback** with live preview
5. **Keyboard-friendly** operation with shortcuts
6. **Accessibility** features for all users
7. **Extensibility** for custom properties and controls

The goal is to make layout creation and management as **user-friendly as professional design tools** like Figma, Adobe XD, or Sketch, while being accessible to beginners.
