# Shimeji

<p align="center"><img src="docs/images/repo-banner.png" alt="Shimeji banner" width="100%" /></p>

Desktop mascots for **Windows 10/11 and Linux with X11**, written in **Python**. Java, JNA, Rhino, C# and a .NET compiler are no longer required. This is a modified successor to the original Shimeji application by Yuki Yamada (Group Finity).

The mascot engine uses Qt for Python; the settings editor uses Python's Tkinter. Portable builds bundle Python and their libraries, so end users do not need to install Python separately.

## Features

- Transparent, animated mascots with a tray menu and right-click menu.
- Walk, run, sit, lie down, crawl, spin, fall, climb screen sides and crawl along the screen ceiling.
- Drag and throw mascots; land on the taskbar work area or the foreground window's top edge.
- Run several different characters together; add mascots, gather at the cursor, keep one, or enable automatic cloning (maximum 50).
- Live **25–200%** scaling, including custom percentages, with monitor DPI handled by Qt.
- Import standard PNG sets, Shimeji-EE PNG/XML packs and `legacy_default_v1` JSON/WebP packs.
- English interface, error messages and documentation.
- Bundled characters: **Ayaka** and **Hatsune Miku**.

<table><tr><td align="center"><strong>Ayaka</strong></td><td align="center"><strong>Hatsune Miku</strong></td></tr>
<tr><td><img src="docs/images/ayaka-preview.png" alt="Ayaka preview" width="128" /></td>
<td><img src="docs/images/miku-preview.png" alt="Hatsune Miku preview" width="128" /></td></tr></table>

## Run from source

Use **Python 3.10 or newer**. Install dependencies in a virtual environment.

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\launch.bat
.\run-settings.bat
```

The batch files find `.venv` automatically and also support a project folder on a network share. You can run `python shimeji.py` or `python shimeji.py --settings` directly with the dependencies installed. Batch launches use a console so setup errors remain visible; packaged executables launch without a console.

### Linux (X11)

On Ubuntu/Debian, install Tkinter, venv and the WebP decoder first:

```bash
sudo apt install python3-tk python3-venv webp
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
bash ./launch.sh
bash ./run-settings.sh
```

Qt also needs the distribution's usual X11/xcb libraries and an ARGB-capable compositing window manager for transparency. The engine reads the foreground window through `libX11`. Use an **X11 session**; native Wayland window interaction is not supported. `QT_QPA_PLATFORM=xcb` can select X11 under XWayland, but only X11 windows are visible to the window integration.

Launch scripts resolve their own directory; no machine-specific paths are required.

## Portable Windows and Linux builds

Build on the operating system you want to distribute for:

```bash
python -m pip install -r requirements-build.txt
python build.py
```

On Windows, `build.bat` runs the build with `.venv` if present. The result is `dist/Shimeji/`, containing `Shimeji.exe` and `ShimejiSettings.exe` on Windows, or `Shimeji` and `ShimejiSettings` on Linux. **Distribute the complete folder**, including `_internal`, sprites, configuration files and licenses. Both executables are bundled from the same Python entry point; there is no C# launcher or JVM.

The build copies your current `img/`, `characters/` and configuration into the output. Builds contain the current local settings and imported characters; review those before distribution. For a clean release, build into an empty `dist/Shimeji/` directory so removed characters are not retained from an earlier build.

## Settings and character imports

Open Settings from a mascot's right-click menu, the tray menu, `run-settings.bat` / `run-settings.sh`, or the packaged settings executable.

1. Download a character ZIP, for example from [shimeji.org](https://shimeji.org/).
2. Click **Import ZIP ...**. **Download ZIPs from shimeji.org** opens the download site in your browser.
3. Check one or more installed characters in the list and click **Start selected**. One mascot of each checked character starts together. **Apply + restart** also saves all other settings.

Nested image folders and multiple characters in a single package are detected automatically. Characters are stored in `characters/<Name>/`. Existing characters are preserved; duplicate names get suffixes such as ` (2)`.

Supported formats:

- **Standard PNG:** `shime1.png` through `shime46.png`.
- **Shimeji-EE named PNG/XML:** named images such as `stand.png` with `conf/actions.xml` inside the character folder. English `Action`/`Pose` image references are mapped to standard frames.
- **JSON/WebP:** `manifest.json`, `animation.json` and `sprites/*.webp` using **`legacy_default_v1`, version 1**. Selected poses are converted into 128 × 128 PNGs.

Imports use image references only; downloaded executables, Java archives, expressions and behavior scripts are never executed. Missing special poses fall back to suitable poses or the standing pose. The importer limits packages to 10,000 files, metadata to 4 MiB, individual images to 16 MiB / 4096 × 4096 pixels, and all imported images to 256 MiB.

The Python importer uses `lib/webp/dwebp.exe` on Windows, included in portable builds. Linux uses the system `dwebp` command. See [decoder provenance and licenses](lib/webp/README.md).

For manual installation, create `characters/YOUR_CHARACTER/` with all 46 standard PNGs, then select and apply it in Settings.

## Configuration and runtime behavior

- **`window.conf`**: header followed by four integers: x offset, y offset, extra width, extra height.
- **`titles.conf`**: one foreground-window title filter per line; blank means all titled foreground windows. Matching ignores case and allows partial titles.
- **`settings.properties`**: `selfCloningEnabled=true|false` and `scalePercent=25..200` (default `100`). Other keys are preserved by the editor.
- **`.current_character`**: selected character names, one per line. Existing single-name files remain compatible. Each mascot loads its own frames from `characters/<Name>/`; `img/` is a fallback for installations without a character library.

Save applies scale, cloning, title filters and window offsets to running mascots within a second. Character selection is saved with **Save** and takes effect with **Start selected** or **Apply + restart**. Clones keep their parent's character. The tray's **Add mascot** and a second normal launch cycle through the selected characters; **Add mascot** from a mascot's own menu adds the same character. `python shimeji.py --restart` reloads only the instance belonging to this installation. A second normal launch adds a mascot. `--quit` stops this installation's instance. Communication uses a local user-restricted socket and a per-installation lock; unrelated processes are never terminated.

The Python engine replaces the old Java/Rhino action interpreter with a built-in movement state machine. **Old `conf/Actions.xml` and `conf/Behavior.xml` scripts are no longer interpreted.** Imported sprites remain compatible, but exact Java action timings, window carrying/throwing, window-side climbing and arbitrary scripted behaviors are not reproduced. Foreground-window top edges and screen sides/ceiling are supported. Linux window integration and mixed-DPI multi-monitor behavior need testing on the target desktop.

## Tests

```bash
python -B -m unittest discover -s tests -p 'test_*.py' -v
python shimeji.py --smoke-test
```

The tests cover imports, XML/JSON restrictions, WebP conversion, settings persistence, UI scale validation, multiple-character selection and rendering, gravity, landing, dragging, window movement and screen climbing. The smoke test loads the actual character PNGs and exercises Qt rendering and scaling. A graphical desktop and Tkinter are needed; Linux also needs `dwebp`. For headless Qt rendering tests, set `QT_QPA_PLATFORM=offscreen` (Tk tests still need a display such as Xvfb).

Windows convenience command: `powershell -ExecutionPolicy Bypass -File tests/run_import_checks.ps1`.

Synthetic fixtures contain no downloaded character art. `tests/fixtures/pixel.webp` is a generated pixel with alpha 128. Optional original sample checks use `SHIMEJI_SAMPLE_DIR`, expecting `0fxxyxhc.zip` and `7rkbhgkk.zip`; on Windows the runner also accepts `-SampleDirectory`.

## License and credits

The project retains the original [ZLIB/LIBPNG license](LICENSE) from Yuki Yamada (Group Finity), with an optional [German translation](LICENSE.de). This Python edition is a modified implementation, not the original runtime. Character artwork remains subject to its respective owners' terms.

Qt for Python / PySide6 and Shiboken are available under LGPLv3/GPLv3 or commercial terms; review the [Qt for Python licensing documentation](https://doc.qt.io/qtforpython-6/licenses.html) before redistribution. Portable builds use shared Qt libraries. The bundled WebP decoder's notices are included in [lib/webp](lib/webp/README.md).
