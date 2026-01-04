# Ghost OS Files Report

## Overview
This document catalogs all "Ghost OS files" found in the Experimental-UI repository. Ghost OS files include hidden files, placeholder files, and system-level files that maintain the structure and configuration of the project.

## What are Ghost OS Files?

**Ghost OS files** are files that exist in the filesystem but may not be immediately visible or actively used during normal operations. They include:
1. **Hidden files** (files starting with `.`)
2. **Placeholder files** (`.gitkeep` files preserving empty directories)
3. **System configuration files** (git configuration, ignore patterns)

## Complete Inventory of Ghost OS Files

### 1. Git System Files

#### `.gitignore`
- **Location**: `/home/runner/work/Experimental-UI/Experimental-UI/.gitignore`
- **Purpose**: Specifies intentionally untracked files to ignore
- **Type**: Hidden Git Configuration
- **Visibility**: Hidden file (starts with `.`)

### 2. Placeholder Files (.gitkeep)

These "ghost" files exist solely to preserve empty directory structures in Git, as Git doesn't track empty directories.

#### Root Level Placeholders:
1. **`./models/.gitkeep`**
   - **Directory**: models/
   - **Purpose**: Preserves the models directory for AI generation models (FLUX, SDXL, etc.)
   - **Related**: Symlink target for user model directories

2. **`./outputs/.gitkeep`**
   - **Directory**: outputs/
   - **Purpose**: Preserves directory for generated images and videos

3. **`./extensions/.gitkeep`**
   - **Directory**: extensions/
   - **Purpose**: Preserves extension system directory for plugins

4. **`./llm_settings/.gitkeep`**
   - **Directory**: llm_settings/
   - **Purpose**: Preserves directory for LLM configuration profiles

5. **`./mtg_decks/.gitkeep`**
   - **Directory**: mtg_decks/
   - **Purpose**: Preserves directory for saved Magic: The Gathering decks

6. **`./mtg_data/.gitkeep`**
   - **Directory**: mtg_data/
   - **Purpose**: Preserves directory for MTG card databases and rules

7. **`./dnd_characters/.gitkeep`**
   - **Directory**: dnd_characters/
   - **Purpose**: Preserves directory for saved D&D 5e characters

#### MTG Playspace Placeholders (Cockatrice-Compatible):
8. **`./mtg_playspace/.gitkeep`**
   - **Directory**: mtg_playspace/
   - **Purpose**: Root directory for playspace resources

9. **`./mtg_playspace/rules/.gitkeep`**
   - **Directory**: mtg_playspace/rules/
   - **Purpose**: Preserves directory for game rules files (XML, JSON, TXT, PDF, DOC, DOCX)

10. **`./mtg_playspace/images/.gitkeep`**
    - **Directory**: mtg_playspace/images/
    - **Purpose**: Preserves directory for card images (PNG, JPG, GIF, BMP, WEBP)

11. **`./mtg_playspace/carddb/.gitkeep`**
    - **Directory**: mtg_playspace/carddb/
    - **Purpose**: Preserves directory for Cockatrice-compatible card databases (cards.xml, AllPrintings.json, SQL)

12. **`./mtg_playspace/sets/.gitkeep`**
    - **Directory**: mtg_playspace/sets/
    - **Purpose**: Preserves directory for set information (XML, JSON)

#### LLM Data Placeholders:
13. **`./llm_data/prepends/.gitkeep`**
    - **Directory**: llm_data/prepends/
    - **Purpose**: Preserves directory for system prepend files (up to 2000 characters)

14. **`./llm_data/bios/.gitkeep`**
    - **Directory**: llm_data/bios/
    - **Purpose**: Preserves directory for LLM behavior guidelines/bios (up to 2000 characters)

15. **`./llm_data/dnd_characters/.gitkeep`**
    - **Directory**: llm_data/dnd_characters/
    - **Purpose**: Preserves directory for D&D character LLM training data

## Ghost OS Files by Category

### Category 1: Version Control Ghosts
- `.gitignore` - Controls visibility of other files
- All `.gitkeep` files - Preserve directory structure

### Category 2: Structural Ghosts
These preserve the architecture of the application:
- Model storage directories (`models/`)
- Output directories (`outputs/`)
- Extension system (`extensions/`)

### Category 3: User Data Ghosts
These preserve directories for user-generated content:
- `mtg_decks/` - User MTG decks
- `dnd_characters/` - User D&D characters
- `llm_settings/` - User LLM configurations

### Category 4: Resource Ghosts (Cockatrice-Compatible)
These preserve directories for user-sourced resources (following copyright-safe approach):
- `mtg_playspace/rules/` - User-provided game rules
- `mtg_playspace/images/` - User-provided card images
- `mtg_playspace/carddb/` - User-provided card databases
- `mtg_playspace/sets/` - User-provided set data

## Total Ghost OS Files Count

- **Hidden Configuration Files**: 1 (`.gitignore`)
- **Placeholder Files (.gitkeep)**: 15
- **Total Ghost OS Files**: 16

## Ghost OS Files and Their Relationship to the System

### Offline/Privacy Mode Integration
Ghost OS files are essential for the privacy-focused architecture:
- They preserve directory structure without bundling copyrighted content
- They maintain separation between code and user data
- They enable the symlink-based model system (see `PLACEHOLDER_INSTRUCTIONS.txt`)

### Extension System Integration
The ghost files support the Extension Launcher system:
- `extensions/.gitkeep` preserves the extension directory
- Extensions can be added without modifying repository structure
- Whitelist system restricts access to `models/` and `extensions/` only

### Copyright-Safe Architecture
Following Cockatrice's approach:
- Ghost files preserve directories for user-sourced content
- No copyrighted MTG card data or images bundled
- Users provide their own resources

## Related Documentation

- **PLACEHOLDER_INSTRUCTIONS.txt**: Explains symlink system for models
- **EXTENSION_LAUNCHER.md**: Details extension system and whitelist
- **BESEECH-SETUP.md**: Virtual environment setup
- **README.md**: Project overview and features

## Technical Details

### Why .gitkeep Files?
Git doesn't track empty directories. The `.gitkeep` files are a convention to preserve directory structure in the repository. They:
- Are typically empty files
- Act as "ghosts" that Git can track
- Allow the directory to exist in the repository
- Can be removed once user adds actual files

### Ghost OS Files and Offline Mode
The Ghost OS file structure supports the 100% offline operation:
- Directories exist but remain empty until user populates them
- No external dependencies or downloads required
- User controls all content and models

## Verification Commands

To verify Ghost OS files exist:

```bash
# Find all hidden files
find . -name ".*" -type f ! -path "./.git/*"

# Find all .gitkeep files
find . -name ".gitkeep"

# Count ghost files
find . -name ".gitkeep" | wc -l
```

## Conclusion

The Experimental-UI repository contains **16 Ghost OS files** that preserve the project's directory structure while maintaining a copyright-safe, privacy-focused, offline-capable architecture. These files act as "ghosts" in the operating system, ensuring directories exist for user-provided content without bundling any proprietary or copyrighted materials.

---

**Report Generated**: January 4, 2026
**Repository**: jameshroop-art/Experimental-UI
**Branch**: copilot/find-ghost-os-files
