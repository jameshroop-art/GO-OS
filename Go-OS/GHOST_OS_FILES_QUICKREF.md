# Ghost OS Files - Quick Reference

## What are Ghost OS Files?
"Ghost OS files" are hidden or placeholder files that exist in the filesystem to maintain structure and configuration, but may not be immediately visible or actively used during normal operations.

## Quick List of All Ghost OS Files

### Hidden Configuration (1 file)
```
.gitignore                           # Git ignore patterns
```

### Placeholder Files - .gitkeep (15 files)

#### Main Directories
```
models/.gitkeep                      # AI models directory
outputs/.gitkeep                     # Generated content output
extensions/.gitkeep                  # Extension plugins
```

#### User Data Directories
```
llm_settings/.gitkeep                # LLM configuration profiles
mtg_decks/.gitkeep                   # MTG deck saves
mtg_data/.gitkeep                    # MTG databases
dnd_characters/.gitkeep              # D&D character saves
```

#### MTG Playspace (Cockatrice-Compatible)
```
mtg_playspace/.gitkeep               # Playspace root
mtg_playspace/rules/.gitkeep         # Game rules (XML, JSON, PDF, DOC)
mtg_playspace/images/.gitkeep        # Card images (PNG, JPG, GIF, BMP, WEBP)
mtg_playspace/carddb/.gitkeep        # Card databases (cards.xml, AllPrintings.json)
mtg_playspace/sets/.gitkeep          # Set information (XML, JSON)
```

#### LLM Data Directories
```
llm_data/prepends/.gitkeep           # System prepends (max 2000 chars)
llm_data/bios/.gitkeep               # LLM behavior guidelines (max 2000 chars)
llm_data/dnd_characters/.gitkeep     # D&D LLM training data
```

## Total Count: 16 Ghost OS Files

## Quick Commands

### Find all ghost files
```bash
# All hidden files (excluding .git directory)
find . -name ".*" -type f ! -path "./.git/*"

# All .gitkeep files
find . -name ".gitkeep"

# Count ghost files
find . -name ".gitkeep" | wc -l
```

### Verify directory structure
```bash
# Check all directories with .gitkeep
for f in $(find . -name ".gitkeep"); do
    echo "Directory: $(dirname $f)"
done
```

## Why Do These Files Exist?

1. **Git Limitation**: Git doesn't track empty directories
2. **Structure Preservation**: Maintains project architecture in version control
3. **Privacy Focus**: Directories exist but no copyrighted content bundled
4. **User Control**: Users populate directories with their own content
5. **Offline Capable**: No external dependencies required

## Categories

| Category | Count | Purpose |
|----------|-------|---------|
| Version Control | 1 | Git configuration |
| Structural | 3 | Core application structure |
| User Data | 3 | User-generated content storage |
| Cockatrice Resources | 5 | MTG playspace (user-sourced) |
| LLM Data | 3 | LLM configuration and training |

## Related Documentation

- **Full Report**: `GHOST_OS_FILES_REPORT.md` - Detailed analysis
- **Inventory**: `GHOST_OS_FILES_INVENTORY.json` - Structured data
- **Placeholders**: `PLACEHOLDER_INSTRUCTIONS.txt` - Symlink setup
- **Extensions**: `EXTENSION_LAUNCHER.md` - Extension system

## Key Architectural Principles

✅ **Copyright-Safe**: No proprietary content bundled
✅ **Privacy-Focused**: 100% offline operation
✅ **User-Controlled**: Users provide their own resources
✅ **Extensible**: Supports plugins and extensions
✅ **Symlink-Ready**: Models directory for user's actual models

---
**Generated**: January 4, 2026 | **Repository**: jameshroop-art/Experimental-UI
