# Arch Linux — Hyprland Dotfiles Documentation

**Theme:** Catppuccin Mocha  
**WM:** Hyprland (Wayland)  
**Last updated:** 2026-04-19

---

## Table of Contents

1. [File Structure](#file-structure)
2. [Core Hyprland Config](#core-hyprland-config)
3. [Appearance Modules](#appearance-modules)
4. [Input Configuration](#input-configuration)
5. [Idle & Lock Screen](#idle--lock-screen)
6. [Wallpaper Management](#wallpaper-management)
7. [Status Bar — Waybar](#status-bar--waybar)
8. [Application Launcher — Wofi](#application-launcher--wofi)
9. [Logout Menu — Wlogout](#logout-menu--wlogout)
10. [Notifications — Dunst](#notifications--dunst)
11. [Terminal — Kitty](#terminal--kitty)
12. [All Keybindings](#all-keybindings)
13. [Dunst Shortcuts](#dunst-shortcuts)

---

## File Structure

```
~/.config/
├── hypr/
│   ├── hyprland.conf                  # Orchestrator — sources all modules
│   ├── hypridle.conf                  # Idle timers (dim / lock / sleep)
│   ├── hyprlock.conf                  # Lock screen layout and wallpaper
│   ├── hyprpaper/
│   │   └── hyprpaper.conf             # Wallpaper daemon config
│   ├── wallpapers/
│   │   └── main.png                   # Active wallpaper (rename to change)
│   ├── modules/
│   │   ├── variables.conf             # App shortcuts and $mainMod
│   │   ├── monitors.conf              # Monitor layout/resolution
│   │   ├── environment.conf           # Environment variables
│   │   ├── autostart.conf             # Startup programs (exec-once)
│   │   ├── appearance.conf            # Gaps, borders, blur, animations
│   │   ├── input.conf                 # Keyboard, mouse, touchpad
│   │   ├── keybindings.conf           # All hotkeys
│   │   └── rules.conf                 # Window rules and overrides
│   └── waybar/
│       ├── config.jsonc               # Waybar modules and layout
│       ├── style.css                  # Waybar styling (Catppuccin Mocha)
│       └── scripts/
│           ├── blue_ligth_filter      # Blue light toggle script
│           └── empty_window.sh        # Detects empty workspace
├── wofi/
│   ├── config                         # Wofi launcher settings
│   └── style.css                      # Wofi styling (Catppuccin Mocha)
├── wlogout/
│   └── layout                         # Logout menu buttons
├── dunst/
│   ├── dunstrc                        # Notification daemon config
│   └── scripts/
│       └── volume_brightness.sh       # OSD script for volume/brightness
└── kitty/
    └── kitty.conf                     # Terminal colors and font
```

---

## Core Hyprland Config

### `~/.config/hypr/hyprland.conf`
Orchestrator. Sources all modules in order:
1. `modules/variables.conf` — defines `$terminal`, `$fileManager`, `$menu`, `$mainMod`
2. `modules/monitors.conf` — monitor setup
3. `modules/environment.conf` — `XCURSOR_SIZE`, `HYPRCURSOR_SIZE`
4. `modules/autostart.conf` — starts waybar, hyprpaper, dunst, blueman-applet, hypridle
5. `modules/appearance.conf` — visual configuration
6. `modules/input.conf` — keyboard, mouse, touchpad
7. `modules/keybindings.conf` — all bindings
8. `modules/rules.conf` — window behavior overrides

### `modules/variables.conf`
Change default applications here. Affects all keybindings that use `$terminal`, `$fileManager`, `$menu`.

```conf
$terminal    = kitty
$fileManager = dolphin
$menu        = wofi --show drun
$mainMod     = SUPER
```

### `modules/monitors.conf`
Auto-detect by default. For multi-monitor setups, add explicit entries:
```conf
monitor = DP-1, 2560x1440@144, 0x0, 1
monitor = eDP-1, 1920x1080@60, 2560x0, 1
```

### `modules/appearance.conf`
Controls:
- **Gaps**: `gaps_in = 5`, `gaps_out = 20`
- **Borders**: `border_size = 2`, active border is flamingo→rosewater gradient
- **Rounding**: `rounding = 10`
- **Blur**: enabled, size 6, 1 pass
- **Animations**: custom bezier curves for windows, workspaces, layers
- **Layout**: `dwindle` (default)

### `modules/rules.conf`
Per-app window rules:
- `kitty` and `Brave-browser` have 90% opacity (active and inactive)
- XWayland phantom popup fix
- Maximize event suppression

---

## Appearance Modules

### Tiling Layouts

| Layout | Description |
|--------|-------------|
| `dwindle` | Default. Binary space partitioning, like i3/bspwm |
| `master` | Master window on the left, stack on the right |

Switch via `general.layout` in `modules/appearance.conf`.

### Transparency
Configured via `windowrulev2` in `modules/rules.conf`:
```conf
windowrulev2 = opacity <active> <inactive>, class:^(app-class)$
```
Current values: `0.90 0.90` for kitty and Brave.

---

## Input Configuration

**File:** `~/.config/hypr/modules/input.conf`

| Setting | Value | Description |
|---------|-------|-------------|
| `kb_layout` | `us,ru` | Two keyboard layouts |
| `kb_options` | `grp:win_space_toggle` | Toggle layout with Win+Space |
| `follow_mouse` | `1` | Focus follows cursor |
| `natural_scroll` | `true` | Touchpad natural scroll |
| `sensitivity` | `0` | No pointer acceleration |

**Per-device override:** `epic-mouse-v1` sensitivity set to `-0.5`.

---

## Idle & Lock Screen

**File:** `~/.config/hypr/hypridle.conf`

| Timeout | Action |
|---------|--------|
| 1m 50s | Dim screen to 50% |
| 2m | Lock screen (hyprlock) |
| 2m 30s | Turn off display (DPMS off) |
| 10m | Suspend to RAM |

**Lock screen config:** `~/.config/hypr/hyprlock.conf`  
Displays: blurred wallpaper, clock (95pt), date, input field, keyboard layout indicator.

---

## Wallpaper Management

### Quick change (rename method)
Replace `~/.config/hypr/wallpapers/main.png` with your image.  
Then reload hyprpaper:
```bash
killall hyprpaper && hyprpaper -c ~/.config/hypr/hyprpaper/hyprpaper.conf &
```

### Manual path change
Edit **both** files and update the path:

1. `~/.config/hypr/hyprpaper/hyprpaper.conf`
   - `preload = /path/to/image`
   - `wallpaper = eDP-1,/path/to/image`

2. `~/.config/hypr/hyprlock.conf`
   - `path = /path/to/image` (inside `background { }`)

> Both files have a clearly marked `TO CHANGE WALLPAPER:` comment at the top.

---

## Status Bar — Waybar

**Files:** `~/.config/hypr/waybar/`

### Layout
```
[workspaces]    [active window]    [tray|net|bt|audio|battery|blue-light|clock|lang|power]
```

### Modules

| Module | Description | Click action |
|--------|-------------|--------------|
| `hyprland/workspaces` | Workspace icons | Click to activate |
| `hyprland/window` | Active window class | — |
| `tray` | System tray | — |
| `network` | Wi-Fi/ethernet icon | Opens `nmtui` in kitty |
| `bluetooth` | BT status and battery | Opens `blueman-manager` |
| `pulseaudio` | Volume level | Opens `pavucontrol` |
| `battery` | Battery % with icon | — |
| `custom/blue-light-filter` | Toggle warm/cool display | Click to toggle hyprshade |
| `clock` | `HH:MM`, right-click for calendar | Right-click: month view |
| `hyprland/language` | Current keyboard layout | Click: switch to next layout |
| `custom/power` | Power menu button | Opens wlogout |

### Waybar Styling
Colors are defined as CSS variables at the top of `style.css` using Catppuccin Mocha palette.  
Bar height: 25px, margin-top: 10px, border-radius: 20px.

### Blue Light Filter Script
**File:** `~/.config/hypr/waybar/scripts/blue_ligth_filter`  
Uses `hyprshade` to toggle `blue-light-filter` shader.  
Signal `RTMIN+2` forces waybar module refresh after toggle.

---

## Application Launcher — Wofi

**Files:** `~/.config/wofi/`

| Setting | Value |
|---------|-------|
| Mode | `drun` (desktop app launcher) |
| Size | 750 × 400 |
| Columns | 2 |
| Case sensitive | No |
| Terminal | kitty |

Styled with full Catppuccin Mocha palette. Selected entries highlighted in mauve (`#cba6f7`).

---

## Logout Menu — Wlogout

**File:** `~/.config/wlogout/layout`  
Launched via: `wlogout -b 4 --layout ~/.config/wlogout/layout --protocol layer-shell`

| Button | Key | Action |
|--------|-----|--------|
| Lock | `L` | `hyprlock` |
| Logout | `E` | `hyprctl exit` |
| Reboot | `R` | `systemctl reboot` |
| Shutdown | `S` | `systemctl poweroff` |

---

## Notifications — Dunst

**File:** `~/.config/dunst/dunstrc`

| Setting | Value |
|---------|-------|
| Position | Bottom-center |
| Corner radius | 15 |
| Width | 300px |
| Font | Font Awesome 5 Free Regular 12 |
| Colors | Dark background `#131519`, white text, teal highlight |
| Low urgency timeout | 5s |
| Normal urgency timeout | 20s |
| Critical urgency | No timeout |

### Volume/Brightness OSD Script
**File:** `~/.config/dunst/scripts/volume_brightness.sh`

| Argument | Description |
|----------|-------------|
| `volume_up` | +5% volume (capped at 100%) |
| `volume_down` | -5% volume |
| `volume_mute` | Toggle mute |
| `brightness_up` | +5% brightness |
| `brightness_down` | -5% brightness (floor at 0%) |
| `next_track` | playerctl next + show notification |
| `prev_track` | playerctl previous + show notification |
| `play_pause` | playerctl play-pause + show notification |

Uses `pactl` for audio, `brightnessctl` for brightness, `notify-send` with dunst stack tags (replaces previous OSD instead of stacking).

---

## Terminal — Kitty

**File:** `~/.config/kitty/kitty.conf`

| Setting | Value |
|---------|-------|
| Font | JetBrainsMono Nerd Font |
| Window padding | 5px |
| Theme | Catppuccin Mocha |
| Tab bar background | `#11111b` (Crust) |

---

## All Keybindings

> `$mainMod` = **Super** (Windows key)

### Window Management

| Hotkey | Action |
|--------|--------|
| `Super + Enter` | Open terminal (kitty) |
| `Super + Q` | Close active window |
| `Super + M` | Exit Hyprland |
| `Super + E` | Open file manager (Dolphin) |
| `Super + V` | Toggle floating mode |
| `Super + D` | Open app launcher (Wofi) |
| `Super + P` | Dwindle: toggle pseudo-tiling |
| `Super + J` | Dwindle: toggle split direction |
| `Super + L` | Lock screen (hyprlock) |

### Focus Navigation

| Hotkey | Action |
|--------|--------|
| `Super + ←` | Move focus left |
| `Super + →` | Move focus right |
| `Super + ↑` | Move focus up |
| `Super + ↓` | Move focus down |

### Workspaces

| Hotkey | Action |
|--------|--------|
| `Super + 1–9` | Switch to workspace 1–9 |
| `Super + 0` | Switch to workspace 10 |
| `Super + Shift + 1–9` | Move window to workspace 1–9 |
| `Super + Shift + 0` | Move window to workspace 10 |
| `Super + S` | Toggle special (scratchpad) workspace |
| `Super + Shift + S` | Send window to scratchpad |
| `Super + Scroll Down` | Next workspace |
| `Super + Scroll Up` | Previous workspace |

### Mouse Bindings (hold Super)

| Binding | Action |
|---------|--------|
| `Super + LMB drag` | Move floating window |
| `Super + RMB drag` | Resize floating window |

### Media Keys

| Key | Action |
|-----|--------|
| `XF86AudioRaiseVolume` | Volume +5% |
| `XF86AudioLowerVolume` | Volume -5% |
| `XF86AudioMute` | Toggle mute |
| `XF86AudioMicMute` | Toggle microphone mute |
| `XF86MonBrightnessUp` | Brightness +5% |
| `XF86MonBrightnessDown` | Brightness -5% |
| `XF86AudioNext` | Next track |
| `XF86AudioPrev` | Previous track |
| `XF86AudioPlay` / `XF86AudioPause` | Play/Pause |

---

## Dunst Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Space` | Dismiss latest notification |
| `Ctrl + Shift + Space` | Dismiss all notifications |
| `Ctrl + \`` | Show notification history |
| `Ctrl + Shift + .` | Open notification context menu |

---

## Dependencies

| Tool | Purpose |
|------|---------|
| `hyprland` | Window manager |
| `hyprpaper` | Wallpaper daemon |
| `hyprlock` | Lock screen |
| `hypridle` | Idle manager |
| `hyprshade` | Screen shader (blue light filter) |
| `waybar` | Status bar |
| `wofi` | Application launcher |
| `wlogout` | Logout/power menu |
| `dunst` | Notification daemon |
| `kitty` | Terminal emulator |
| `dolphin` | File manager |
| `blueman` | Bluetooth manager |
| `pactl` / `pipewire` | Audio control |
| `brightnessctl` | Backlight control |
| `playerctl` | Media player control |
| `JetBrains Mono` | Primary font (Nerd Font variant) |
| `Font Awesome 5` | Icon font (dunst) |
| `Symbols Nerd Font` | Icon font (waybar, wofi) |
| `Catppuccin-Mocha` GTK theme | GTK app theming |
| `Catppuccin-Mocha-Alt2` icons | Icon theme |
