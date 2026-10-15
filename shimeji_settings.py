#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import tkinter as tk
import webbrowser
from tkinter import ttk, messagebox, filedialog

from character_import import import_characters, is_character_directory

APP_ROOT = (os.path.dirname(sys.executable) if getattr(sys, "frozen", False)
            else os.path.dirname(os.path.abspath(__file__)))
WINDOW_CONF = os.path.join(APP_ROOT, "window.conf")
TITLES_CONF = os.path.join(APP_ROOT, "titles.conf")
SETTINGS_PROPS = os.path.join(APP_ROOT, "settings.properties")
CHARACTERS_DIR = os.path.join(APP_ROOT, "characters")
IMG_DIR = os.path.join(APP_ROOT, "img")
CURRENT_CHARACTER = os.path.join(APP_ROOT, ".current_character")
import hashlib
LOCK_FILE = os.path.join(tempfile.gettempdir(), "shimeji-settings-" +
    hashlib.sha256(os.fsencode(os.path.normcase(APP_ROOT))).hexdigest()[:24] + ".lock")

IS_WINDOWS = platform.system() == "Windows"
RUN_SCRIPT = os.path.join(APP_ROOT, "launch.bat" if IS_WINDOWS else "launch.sh")

HEADER = "Enter window offsets on the following lines: x, y, extra width, extra height. Blank values mean 0."
DEFAULT_WINDOW = ["0", "0", "0", "0"]
_lock_handle = None


def acquire_single_instance_lock():
    global _lock_handle
    try:
        _lock_handle = open(LOCK_FILE, "a+")
        if IS_WINDOWS:
            import msvcrt
            try:
                msvcrt.locking(_lock_handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                return False
        else:
            import fcntl
            try:
                fcntl.flock(_lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                return False
        _lock_handle.seek(0)
        _lock_handle.truncate()
        _lock_handle.write(str(os.getpid()))
        _lock_handle.flush()
        return True
    except Exception:
        return True


def list_characters():
    if not os.path.isdir(CHARACTERS_DIR):
        return []
    names = []
    for name in sorted(os.listdir(CHARACTERS_DIR)):
        path = os.path.join(CHARACTERS_DIR, name)
        if os.path.isdir(path) and is_character_directory(path):
            names.append(name)
    return names


def detect_current_characters():
    installed = list_characters()
    if os.path.exists(CURRENT_CHARACTER):
        with open(CURRENT_CHARACTER, "r", encoding="utf-8", errors="replace") as stream:
            names = list(dict.fromkeys(line.strip() for line in stream if line.strip()))
        selected = [name for name in names if name in installed]
        if selected:
            return selected[:50]
    return ["Ayaka"] if "Ayaka" in installed else installed[:1]


def detect_current_character():
    return next(iter(detect_current_characters()), "Ayaka")


def set_current_characters(names):
    names = list(dict.fromkeys(names))
    installed = list_characters()
    if not names:
        raise ValueError("Please select at least one character.")
    if len(names) > 50:
        raise ValueError("Select at most 50 characters.")
    if any(name not in installed for name in names):
        raise ValueError("Please select complete, installed characters.")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=os.path.dirname(CURRENT_CHARACTER),
                                         delete=False) as stream:
            temporary = stream.name
            stream.write("\n".join(names) + "\n")
        os.replace(temporary, CURRENT_CHARACTER)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def set_current_character(name):
    set_current_characters([name])


def apply_character(name):
    src = os.path.join(CHARACTERS_DIR, name)
    if not is_character_directory(src):
        raise ValueError(f"Incomplete character: {name}. shime1.png through shime46.png are required.")
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR, exist_ok=True)
    for i in range(1, 47):
        shutil.copyfile(os.path.join(src, f"shime{i}.png"), os.path.join(IMG_DIR, f"shime{i}.png"))
    set_current_character(name)


def read_window_conf():
    vals = DEFAULT_WINDOW[:]
    if os.path.exists(WINDOW_CONF):
        with open(WINDOW_CONF, "r", encoding="utf-8", errors="replace") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]
        nums = [line.strip() for line in lines[1:] if line.strip()]
        for i in range(min(4, len(nums))):
            vals[i] = nums[i]
    return vals


def write_window_conf(vals):
    content = HEADER + "\n" + "\n".join(vals) + "\n"
    with open(WINDOW_CONF, "w", encoding="utf-8") as f:
        f.write(content)


def read_titles_conf():
    if not os.path.exists(TITLES_CONF):
        return ""
    with open(TITLES_CONF, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def write_titles_conf(text):
    with open(TITLES_CONF, "w", encoding="utf-8") as f:
        f.write(text)


def read_settings_props():
    props = {"selfCloningEnabled": True, "scalePercent": 100}
    if not os.path.exists(SETTINGS_PROPS):
        return props
    with open(SETTINGS_PROPS, "r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            key = k.strip()
            if key == "selfCloningEnabled":
                props[key] = v.strip().lower() == "true"
            elif key == "scalePercent":
                try:
                    props[key] = max(25, min(200, int(v.strip())))
                except ValueError:
                    props[key] = 100
    return props


def write_settings_props(self_cloning_enabled, scale_percent):
    scale_percent = int(scale_percent)
    if not 25 <= scale_percent <= 200:
        raise ValueError("Scale must be between 25 and 200 percent.")
    lines = []
    if os.path.exists(SETTINGS_PROPS):
        with open(SETTINGS_PROPS, "r", encoding="utf-8") as f:
            lines = [line for line in f if line.split("=", 1)[0].strip()
                     not in ("selfCloningEnabled", "scalePercent")]
    content = "".join(lines).rstrip("\n")
    if content:
        content += "\n"
    content += "selfCloningEnabled=%s\nscalePercent=%d\n" % (
        "true" if self_cloning_enabled else "false", scale_percent)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         dir=os.path.dirname(SETTINGS_PROPS), delete=False) as f:
            temp_path = f.name
            f.write(content)
        os.replace(temp_path, SETTINGS_PROPS)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


def restart_shimeji():
    if getattr(sys, "frozen", False):
        executable = os.path.join(APP_ROOT, "Shimeji.exe" if IS_WINDOWS else "Shimeji")
        command = [executable, "--restart"]
    else:
        command = [sys.executable, os.path.join(APP_ROOT, "shimeji.py"), "--restart"]
    subprocess.Popen(command, cwd=APP_ROOT,
                     creationflags=subprocess.CREATE_NO_WINDOW if IS_WINDOWS else 0)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shimeji Settings")
        self.geometry("820x790")
        self.minsize(780, 720)
        self.configure(padx=12, pady=12)
        self.option_add("*Font", "Sans 10")
        self.character_vars = {}
        self.self_clone_var = tk.BooleanVar(value=True)
        self.scale_var = tk.StringVar(value="100")
        self._syncing_scale = False
        self._build()
        self.load_values()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        top = ttk.Frame(self)
        top.grid(row=0, column=0, sticky="ew")
        top.grid_columnconfigure(0, weight=1)
        ttk.Label(top, text="Shimeji Settings", font=("Sans", 14, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(top, text="Choose characters, scale, window position, window titles and self-cloning.").grid(row=1, column=0, sticky="w", pady=(4, 10))

        chars = ttk.LabelFrame(self, text="Installed characters")
        chars.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        chars.grid_columnconfigure(1, weight=1)
        ttk.Label(chars, text="Check all characters you want to run together (one of each).").grid(
            row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(8, 4))
        list_wrap = ttk.Frame(chars)
        list_wrap.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        list_wrap.grid_columnconfigure(0, weight=1)
        self.character_canvas = tk.Canvas(list_wrap, height=135, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_wrap, orient="vertical", command=self.character_canvas.yview)
        self.character_canvas.configure(yscrollcommand=scrollbar.set)
        self.character_canvas.grid(row=0, column=0, sticky="ew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.character_list = ttk.Frame(self.character_canvas)
        list_window = self.character_canvas.create_window((0, 0), window=self.character_list, anchor="nw")
        self.character_list.bind("<Configure>", lambda event: self.character_canvas.configure(
            scrollregion=self.character_canvas.bbox("all")))
        self.character_canvas.bind("<Configure>", lambda event: self.character_canvas.itemconfigure(
            list_window, width=event.width))
        self.character_canvas.bind("<MouseWheel>", self._scroll_characters)
        self.character_canvas.bind("<Button-4>", lambda event: self.character_canvas.yview_scroll(-1, "units"))
        self.character_canvas.bind("<Button-5>", lambda event: self.character_canvas.yview_scroll(1, "units"))
        ttk.Button(chars, text="Start selected", command=self.apply_selection).grid(
            row=1, column=2, sticky="ne", padx=(0, 10))

        ttk.Label(chars, text="Scale").grid(row=2, column=0, sticky="w", padx=10, pady=(0, 8))
        self.scale_slider = ttk.Scale(chars, from_=25, to=200, command=self._scale_from_slider)
        self.scale_slider.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady=(0, 8))
        scale_input = ttk.Frame(chars)
        scale_input.grid(row=2, column=2, sticky="e", padx=(0, 10), pady=(0, 8))
        ttk.Spinbox(scale_input, from_=25, to=200, increment=1, textvariable=self.scale_var,
                    width=5).pack(side="left")
        ttk.Label(scale_input, text=" %").pack(side="left")
        self.scale_var.trace_add("write", self._scale_from_input)
        ttk.Label(chars, text="25–200% · 100% = original size · Save updates all running characters.").grid(
            row=3, column=0, columnspan=3, sticky="w", padx=10, pady=(0, 10))

        imports = ttk.Frame(chars)
        imports.grid(row=4, column=0, columnspan=3, sticky="w", padx=10, pady=(0, 10))
        ttk.Button(imports, text="Import ZIP …", command=self.import_zip).pack(side="left", padx=(0, 8))
        ttk.Button(imports, text="Download ZIPs from shimeji.org", command=self.open_character_site).pack(side="left")

        behavior = ttk.LabelFrame(self, text="Behavior")
        behavior.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        ttk.Checkbutton(behavior, text="Allow self-cloning", variable=self.self_clone_var).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        offsets = ttk.LabelFrame(self, text="window.conf")
        offsets.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        for i in range(2):
            offsets.grid_columnconfigure(i, weight=1)

        self.entries = {}
        fields = [
            ("X offset", "x"),
            ("Y offset", "y"),
            ("Extra width", "w"),
            ("Extra height", "h"),
        ]
        for idx, (label, key) in enumerate(fields):
            col = idx % 2
            row = idx // 2
            block = ttk.Frame(offsets)
            block.grid(row=row, column=col, sticky="ew", padx=10, pady=8)
            block.grid_columnconfigure(1, weight=1)
            ttk.Label(block, text=label, width=16).grid(row=0, column=0, sticky="w", padx=(0, 8))
            ent = ttk.Entry(block, width=12)
            ent.grid(row=0, column=1, sticky="w")
            self.entries[key] = ent

        ttk.Label(offsets, text="Save and restart Shimeji to see the changes.").grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10))

        titles = ttk.LabelFrame(self, text="titles.conf")
        titles.grid(row=4, column=0, sticky="nsew")
        titles.grid_columnconfigure(0, weight=1)
        titles.grid_rowconfigure(1, weight=1)
        ttk.Label(titles, text="One window title per line. Leave blank to use all windows.").grid(row=0, column=0, sticky="w", padx=10, pady=(8, 6))

        text_wrap = ttk.Frame(titles)
        text_wrap.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        text_wrap.grid_columnconfigure(0, weight=1)
        text_wrap.grid_rowconfigure(0, weight=1)
        self.text = tk.Text(text_wrap, height=10, wrap="word")
        yscroll = ttk.Scrollbar(text_wrap, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=yscroll.set)
        self.text.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")

        buttons = ttk.Frame(self)
        buttons.grid(row=5, column=0, sticky="ew", pady=(12, 0))
        actions = [
            ("Save", self.save),
            ("Apply + restart", self.apply_all),
            ("Reset window.conf", self.reset_window),
            ("Restart Shimeji", self.restart),
            ("Open application folder", self.open_folder),
            ("Close", self.destroy),
        ]
        for index, (label, command) in enumerate(actions):
            buttons.grid_columnconfigure(index % 3, weight=1)
            ttk.Button(buttons, text=label, command=command).grid(
                row=index // 3, column=index % 3, sticky="ew", padx=4, pady=4
            )

    def _scale_from_slider(self, value):
        if not self._syncing_scale:
            self.scale_var.set(str(round(float(value))))

    def _scale_from_input(self, *_):
        try:
            value = int(self.scale_var.get())
        except ValueError:
            return
        if 25 <= value <= 200:
            self._syncing_scale = True
            try:
                self.scale_slider.set(value)
            finally:
                self._syncing_scale = False

    def selected_characters(self):
        return [name for name, variable in self.character_vars.items() if variable.get()]

    def _scroll_characters(self, event):
        self.character_canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
        return "break"

    def refresh_characters(self, selected):
        for child in self.character_list.winfo_children():
            child.destroy()
        self.character_vars.clear()
        for name in list_characters():
            variable = tk.BooleanVar(value=name in selected)
            self.character_vars[name] = variable
            checkbox = ttk.Checkbutton(self.character_list, text=name, variable=variable)
            checkbox.pack(anchor="w", fill="x", padx=4, pady=2)
            checkbox.bind("<MouseWheel>", self._scroll_characters)
            checkbox.bind("<Button-4>", lambda event: self.character_canvas.yview_scroll(-1, "units"))
            checkbox.bind("<Button-5>", lambda event: self.character_canvas.yview_scroll(1, "units"))
        if not self.character_vars:
            ttk.Label(self.character_list, text="No characters installed. Import a ZIP to get started.").pack(
                anchor="w", padx=4, pady=4)

    def load_values(self):
        self.refresh_characters(detect_current_characters())
        props = read_settings_props()
        self.self_clone_var.set(bool(props.get("selfCloningEnabled", True)))
        self.scale_var.set(str(props.get("scalePercent", 100)))
        vals = read_window_conf()
        for key, val in zip(["x", "y", "w", "h"], vals):
            self.entries[key].delete(0, "end")
            self.entries[key].insert(0, val)
        self.text.delete("1.0", "end")
        self.text.insert("1.0", read_titles_conf())

    def save(self, show_message=True):
        vals = [self.entries[k].get().strip() or "0" for k in ["x", "y", "w", "h"]]
        try:
            [int(v) for v in vals]
        except ValueError:
            messagebox.showerror("Invalid number", "The four window.conf values must be integers.")
            return False
        try:
            scale_percent = int(self.scale_var.get().strip())
            if not 25 <= scale_percent <= 200:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid scale", "Enter an integer from 25 to 200 percent.")
            return False
        try:
            set_current_characters(self.selected_characters())
        except (OSError, ValueError) as error:
            messagebox.showerror("Character selection failed", str(error))
            return False
        write_window_conf(vals)
        write_titles_conf(self.text.get("1.0", "end").rstrip() + "\n" if self.text.get("1.0", "end").strip() else "")
        write_settings_props(self.self_clone_var.get(), scale_percent)
        if show_message:
            messagebox.showinfo("Saved", "Settings saved. Scale is applied to all running characters.\n"
                                "Use Start selected or Apply + restart to run the saved character selection.")
        return True

    def import_zip(self):
        path = filedialog.askopenfilename(title="Import Shimeji ZIP (e.g. from shimeji.org)",
                                          filetypes=[("Shimeji ZIP", "*.zip")])
        if path:
            self.import_package(path)

    def open_character_site(self):
        webbrowser.open("https://shimeji.org/")

    def import_package(self, path):
        try:
            names = import_characters(path, CHARACTERS_DIR)
            self.refresh_characters(self.selected_characters() + names)
            messagebox.showinfo("Characters imported", "Imported: " + ", ".join(names) +
                                "\nCheck the characters you want, then click Start selected to run them together.")
        except Exception as error:
            messagebox.showerror("Import failed", str(error))

    def apply_selection(self):
        try:
            set_current_characters(self.selected_characters())
        except (OSError, ValueError) as error:
            messagebox.showerror("Character selection failed", str(error))
            return
        self.restart()

    def apply_all(self):
        if self.save(show_message=False):
            self.restart()

    def reset_window(self):
        for key, val in zip(["x", "y", "w", "h"], DEFAULT_WINDOW):
            self.entries[key].delete(0, "end")
            self.entries[key].insert(0, val)

    def restart(self):
        try:
            restart_shimeji()
            messagebox.showinfo("Restarted", "Shimeji has been restarted.")
        except Exception as e:
            messagebox.showerror("Restart failed", str(e))

    def open_folder(self):
        if IS_WINDOWS:
            os.startfile(APP_ROOT)
        else:
            subprocess.Popen(["xdg-open", APP_ROOT])


if __name__ == "__main__":
    if not acquire_single_instance_lock():
        sys.exit(0)
    App().mainloop()
