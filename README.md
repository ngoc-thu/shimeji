# shimeji-ubuntu

<p align="center">
  <img src="docs/images/repo-banner.png" alt="shimeji-ubuntu banner" width="100%" />
</p>

<p align="center">
  <img src="docs/images/linux-shimeji-icon.png" alt="linux-shimeji icon" width="64" height="64" />
</p>

<p align="center">
  <a href="https://github.com/ngoc-thu/shimeji-ubuntu/releases/latest">⬇ Download latest release</a>
</p>

A practical Ubuntu-focused Shimeji project with:

- reduced flicker experiments for modern compositors
- X11 frame/layer behavior tweaks
- a small Settings GUI
- multi-character switching
- bundled character libraries for **Ayaka** and **Hatsune Miku**
- a toggle to enable or disable mascot self-cloning

This project is still based on an old Java/X11 codebase, so it is best treated as a hobby desktop-pet build rather than a perfectly modern desktop integration.

This project includes modified code from an older Shimeji codebase, with Ubuntu/X11-focused usability changes.

## What changed in this project

### 1. Flicker reduction experiment
This project removes an old visibility toggle in `src/com/group_finity/mascot/Mascot.java` that hid the mascot window on specific ticks.

That old behavior can show up as visible blinking/flicker on modern Ubuntu GNOME/X11 compositors.

### 2. Modern build compatibility
`build.xml` was updated so the project can be rebuilt with a current JDK + Ant toolchain instead of requiring an old Java 6 era setup.

### 3. X11 frame and layer behavior tweaks
This project includes experiments around:

- corrected `Rectangle` bounds handling
- `_NET_FRAME_EXTENTS` support for window frame calculations
- more consistent use of frame bounds in X11 environment logic
- disabling old `DOCK` forcing behavior that could place the mascot in an odd stacking layer
- reasserting `alwaysOnTop` / `toFront()` during apply

These changes are specifically aimed at improving behavior on Ubuntu GNOME/X11 where mascots may otherwise flicker, clip into bars, or appear on the wrong layer.

### 4. Built-in Settings GUI
A lightweight GUI settings tool is included:

- `shimeji_settings.py`
- `run-settings.sh`

It can:

- edit `window.conf`
- edit `titles.conf`
- apply a selected character
- enable or disable self-cloning
- restart Shimeji
- open the app folder

### 5. Multi-character switching
This project supports a simple character library layout:

```text
characters/
  Ayaka/
  Miku/
```

Each character folder contains `shime1.png` through `shime46.png`.

The Settings GUI can switch between bundled characters and apply them into the active `img/` set.

## Included characters

Currently bundled in this project:

- **Ayaka**
- **Hatsune Miku**

### Character previews

<table>
  <tr>
    <td align="center"><strong>Ayaka</strong></td>
    <td align="center"><strong>Hatsune Miku</strong></td>
  </tr>
  <tr>
    <td align="center"><img src="docs/images/ayaka-preview.png" alt="Ayaka preview" width="128" /></td>
    <td align="center"><img src="docs/images/miku-preview.png" alt="Hatsune Miku preview" width="128" /></td>
  </tr>
</table>

## Requirements

Recommended environment:

- **Windows**: Windows 10/11 with Java 8+ installed (JDK 19, 21 recommended) and Python 3.x for Settings GUI.
- **Linux**: Ubuntu or another Linux desktop using **X11**, `openjdk-21-jdk` (or another modern JDK), `ant`, and Python 3.x.

Example install on Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y openjdk-21-jdk ant python3 python3-tk
```

## Build

### On Windows
Run `build.bat` directly (no Ant required):

```cmd
build.bat
```

Or using Ant if installed: `ant clean jar`

### On Linux
```bash
ant clean jar
```

## Run

### On Windows
Double-click **[Shimeji.exe](file:///D:/Code/ngoc-tien/shimeji/Shimeji.exe)** (clean GUI launcher with custom icon, no terminal window) or run `launch.bat`.

### On Linux
```bash
./launch.sh
```

## Settings GUI

### On Windows
Double-click **[ShimejiSettings.exe](file:///D:/Code/ngoc-tien/shimeji/ShimejiSettings.exe)** (clean GUI launcher, no terminal window) or run `run-settings.bat`.

### On Linux
```bash
./run-settings.sh
```

From there you can:

- choose a character
- apply the selected character
- enable or disable self-cloning
- save window/title configuration
- restart the mascot

The self-cloning toggle is persisted in:

```text
settings.properties
```

Current property used by the app:

```properties
selfCloningEnabled=true
```

## Character switching

The Settings GUI uses the `characters/` directory as the source of truth.

To add a new character manually:

1. create a new folder under `characters/NAME/`
2. place `shime1.png` through `shime46.png` inside it
3. reopen the Settings GUI
4. select that character from the dropdown
5. click **Apply Character** or **Apply + Restart**

## Configuration

### `window.conf`
Controls manual offsets:

1. x offset
2. y offset
3. width add
4. height add

### `titles.conf`
One window title per line. Leave empty to allow interaction with all windows.

### `settings.properties`
Additional runtime behavior flags live here.

Currently supported:

- `selfCloningEnabled=true|false`

## Known limitations

- This is still legacy Java/X11 code.
- Rendering behavior may vary by compositor, theme, GPU, and desktop environment.
- Some Ubuntu GNOME setups may still need manual tuning in `window.conf`.
- Wayland support is not a goal of this project.

## Project intent

This project exists to make it easier to:

- rebuild on a modern Ubuntu machine
- test small targeted fixes
- use a friendlier local settings workflow
- swap characters without manually replacing the image set every time

## License

This project inherits the ZLIB/LIBPNG license of the original Shimeji.

The included Java Native Access library is licensed under the LGPL. The Mozilla Rhino Javascript Engine is licensed under the Mozilla Public License.
