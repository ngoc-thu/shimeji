# shimeji

<p align="center">
  <img src="docs/images/repo-banner.png" alt="shimeji banner" width="100%" />
</p>

<p align="center">
  <img src="docs/images/linux-shimeji-icon.png" alt="shimeji icon" width="64" height="64" />
</p>

<p align="center">
  <a href="https://github.com/ngoc-thu/shimeji/releases/latest">⬇ Download latest release</a>
</p>

A modern, practical **Windows 10/11 & Linux** desktop mascot (Shimeji) application featuring native Windows API integration, standalone `.exe` GUI launchers, DPI scaling fixes, and a built-in Settings GUI.

---

## ✨ Features

- **Standalone Windows Executables**:
  - `Shimeji.exe`: Clean GUI executable launcher with mascot icon (runs silently without a black CMD window).
  - `ShimejiSettings.exe`: Dedicated GUI settings tool launcher.
- **Native Windows API Integration**:
  - Native window enumeration, active window detection, and taskbar collision handling via JNA (`User32` / `GDI32`).
- **High-DPI Display Scaling & Physics Fixes**:
  - Fixed floor collision and infinite falling bugs on scaled Windows displays (100%, 125%, 150%, 200%).
  - Added ±2px tolerance to floor/wall bounds checking for smooth landing.
- **Built-in Settings GUI**:
  - `ShimejiSettings.exe` / `shimeji_settings.py` (Python Tkinter).
  - Easy character switching, `window.conf` offset editing, `titles.conf` window filtering, and self-cloning toggle.
- **Bundled Character Libraries**:
  - **Ayaka** & **Hatsune Miku**.
- **Cross-Platform Compatibility**:
  - Full support for **Windows 10/11** and **Ubuntu / Linux X11**.

---

## 🎭 Included Characters

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

---

## 🚀 Quick Start

### On Windows
1. Make sure **Java 8 or higher** (JDK 19, 21 recommended) and **Python 3.x** are installed.
2. **Start Mascot**: Double-click `Shimeji.exe` (or `launch.bat`).
3. **Open Settings**: Double-click `ShimejiSettings.exe` (or `run-settings.bat`).

### On Linux
```bash
# Launch mascot
./launch.sh

# Launch settings GUI
./run-settings.sh
```

---

## 🛠️ Building from Source

### On Windows
Run `build.bat` directly from Command Prompt or PowerShell (no Ant installation required):

```cmd
build.bat
```

This compiles all Java sources (`src`, `src_generic`, `src_x11`, `src_win`), packages `Shimeji.jar`, and compiles `Shimeji.exe` & `ShimejiSettings.exe` using `csc.exe`.

### On Linux
```bash
ant clean jar
```

---

## 📁 Adding Custom Characters

To add a new character to Shimeji:

1. Create a new folder under `characters/YOUR_CHARACTER_NAME/`.
2. Place `shime1.png` through `shime46.png` inside that folder.
3. Open `ShimejiSettings.exe` (or `python shimeji_settings.py`).
4. Select your new character from the dropdown.
5. Click **Apply Character** or **Apply + Restart**.

---

## ⚙️ Configuration Files

- **`window.conf`**: Custom window offset adjustments (order: `x`, `y`, `width add`, `height add`).
- **`titles.conf`**: Filter target windows by title (one title per line; leave blank to allow interaction with all active windows).
- **`settings.properties`**: Persistence for behavior flags (e.g. `selfCloningEnabled=true|false`).

---

## 📜 License & Credits

This project inherits the ZLIB/LIBPNG license of the original Shimeji project by Yuki Yamada of Group Finity.

- **Java Native Access (JNA)**: Licensed under LGPL.
- **Mozilla Rhino JS Engine**: Licensed under MPL.
