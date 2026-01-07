# Heck-CheckOS Integrations

This directory contains curated external repository integrations for the Heck-CheckOS ISO Builder.

## Included Integrations

All integrated projects are properly licensed and credited to their original creators.

### Themes
- **Dracula Theme** (MIT License)
  - Repository: https://github.com/dracula/dracula-theme
  - Dark theme for 250+ applications

### Shell Enhancements
- **Oh My Zsh** (MIT License)
  - Repository: https://github.com/ohmyzsh/ohmyzsh
  - Framework for managing Zsh configuration
  
- **Powerlevel10k** (MIT License)
  - Repository: https://github.com/romkatv/powerlevel10k
  - Fast, flexible Zsh theme with instant prompt
  
- **Starship** (ISC License)
  - Repository: https://github.com/starship/starship
  - Minimal, fast, and customizable prompt

### Editors
- **NvChad** (GPLv3 License)
  - Repository: https://github.com/NvChad/NvChad
  - Blazing fast Neovim configuration

### Terminal
- **Alacritty** (Apache 2.0 License)
  - Repository: https://github.com/alacritty/alacritty
  - GPU-accelerated terminal emulator
  
- **Tmux Plugin Manager** (MIT License)
  - Repository: https://github.com/tmux-plugins/tpm
  - Plugin manager for tmux

### Launchers
- **Rofi** (MIT License)
  - Repository: https://github.com/davatorium/rofi
  - Window switcher and application launcher

## License Compliance

All integrations respect their original licenses. When building a custom ISO:

1. Each integration's license is preserved
2. Attribution is maintained in the final build
3. Source repositories are clearly documented
4. No license terms are violated

## Adding New Integrations

To add a new integration:

1. Add entry to `repos.json`
2. Create installation script in `scripts/`
3. Document license and attribution
4. Test integration in isolated environment

## Installation Scripts

The `scripts/` directory contains installation scripts for each integration:

- `install-dracula.sh` - Install Dracula theme
- `install-ohmyzsh.sh` - Install Oh My Zsh
- `install-powerlevel10k.sh` - Install Powerlevel10k
- `install-nvchad.sh` - Install NvChad
- `install-starship.sh` - Install Starship
- `install-alacritty.sh` - Install Alacritty
- `install-rofi.sh` - Install Rofi
- `install-tpm.sh` - Install Tmux Plugin Manager

## Credits

Heck-CheckOS ISO Builder integrates these amazing open-source projects.
All credit goes to the original authors and maintainers.

Thank you to the open-source community! 🎉
