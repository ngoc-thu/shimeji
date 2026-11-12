#!/usr/bin/env python3
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import tkinter as tk
from tkinter import messagebox, ttk

IS_WINDOWS = os.name == "nt" or sys.platform.startswith("win")
IS_MAC = sys.platform == "darwin"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
WINDOW_CONF = os.path.join(APP_ROOT, "window.conf")
TITLES_CONF = os.path.join(APP_ROOT, "titles.conf")
SETTINGS_PROPS = os.path.join(APP_ROOT, "settings.properties")
REMINDERS_PROPS = os.path.join(APP_ROOT, "conf", "reminders.properties")
DIALOGUES_CONF = os.path.join(APP_ROOT, "conf", "dialogues.conf")
RUN_SCRIPT = os.path.join(APP_ROOT, "launch.bat" if IS_WINDOWS else "launch.sh")
CHARACTERS_DIR = os.path.join(APP_ROOT, "characters")
IMG_DIR = os.path.join(APP_ROOT, "img")
CURRENT_CHARACTER = os.path.join(APP_ROOT, ".current_character")
LOCK_FILE = os.path.join(tempfile.gettempdir(), "shimeji-settings.lock")

HEADER = "Put window offsets on the following lines in this order : x, y, width, height. No entry will default to 0."
DEFAULT_WINDOW = ["0", "0", "0", "0"]
_lock_handle = None


def acquire_single_instance_lock():
    global _lock_handle
    try:
        _lock_handle = open(LOCK_FILE, "a+")
        if IS_WINDOWS:
            try:
                import msvcrt
                msvcrt.locking(_lock_handle.fileno(), msvcrt.LK_NBLCK, 1)
            except (OSError, IOError):
                return False
            except ImportError:
                pass
        else:
            try:
                import fcntl
                fcntl.flock(_lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except (OSError, IOError):
                return False
            except ImportError:
                pass
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
        if os.path.isdir(path) and os.path.exists(os.path.join(path, "shime1.png")):
            names.append(name)
    return names


def detect_current_character():
    if os.path.exists(CURRENT_CHARACTER):
        with open(CURRENT_CHARACTER, "r", encoding="utf-8", errors="replace") as f:
            val = f.read().strip()
        if val:
            return val
    return "Ayaka"


def set_current_character(name):
    with open(CURRENT_CHARACTER, "w", encoding="utf-8") as f:
        f.write(name + "\n")


def apply_character(name):
    src = os.path.join(CHARACTERS_DIR, name)
    if not os.path.isdir(src):
        raise FileNotFoundError(f"Character not found: {name}")
    os.makedirs(IMG_DIR, exist_ok=True)
    for i in range(1, 47):
        src_file = os.path.join(src, f"shime{i}.png")
        dst_file = os.path.join(IMG_DIR, f"shime{i}.png")
        if os.path.exists(src_file):
            shutil.copyfile(src_file, dst_file)
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
    props = {"selfCloningEnabled": True}
    if not os.path.exists(SETTINGS_PROPS):
        return props
    with open(SETTINGS_PROPS, "r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            props[k.strip()] = v.strip().lower() == "true"
    return props


def write_settings_props(self_cloning_enabled):
    with open(SETTINGS_PROPS, "w", encoding="utf-8") as f:
        f.write("selfCloningEnabled=%s\n" % ("true" if self_cloning_enabled else "false"))


def read_reminders_conf():
    data = {
        "enabled": True,
        "soundEnabled": True,
        "notifySendEnabled": True,
        "randomIdleChatEnabled": True,
        "randomChatIntervalMinutes": 15,
        "bubbleDurationSeconds": 7,
        "water_minutes": 60,
        "water_message": "Anh nhớ uống một ngụm nước nhé! 💧",
        "rest_minutes": 45,
        "rest_message": "Anh chớp mắt và vươn vai thư giãn 20 giây nha! 👀",
        "reminders": {
            "11:55": "11h55 rồi, anh đi ăn cơm trưa thôi nào! 🍚🍛",
            "12:00": "12h00 rồi, nghỉ ngơi một lát cho khỏe nhé anh! 💤",
            "14:00": "Bắt đầu buổi chiều tràn đầy năng lượng nào! ⚡",
            "17:30": "Hết giờ làm việc rồi, chuẩn bị nghỉ ngơi thôi anh! 🎉",
            "23:00": "Đã 23h00 rồi, ngủ sớm giữ gìn sức khỏe nha anh! 🌙",
        }
    }
    if not os.path.exists(REMINDERS_PROPS):
        return data

    with open(REMINDERS_PROPS, "r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()
            if k == "enabled":
                data["enabled"] = v.lower() == "true"
            elif k == "soundEnabled":
                data["soundEnabled"] = v.lower() == "true"
            elif k == "notifySendEnabled":
                data["notifySendEnabled"] = v.lower() == "true"
            elif k == "randomIdleChatEnabled":
                data["randomIdleChatEnabled"] = v.lower() == "true"
            elif k == "randomChatIntervalMinutes":
                try:
                    data["randomChatIntervalMinutes"] = int(v)
                except ValueError:
                    pass
            elif k == "bubbleDurationSeconds":
                try:
                    data["bubbleDurationSeconds"] = int(v)
                except ValueError:
                    pass
            elif k == "interval.water_minutes":
                try:
                    data["water_minutes"] = int(v)
                except ValueError:
                    pass
            elif k == "interval.water_message":
                data["water_message"] = v
            elif k == "interval.rest_minutes":
                try:
                    data["rest_minutes"] = int(v)
                except ValueError:
                    pass
            elif k == "interval.rest_message":
                data["rest_message"] = v
            elif k.startswith("reminder."):
                time_key = k[len("reminder."):].replace("_", ":")
                if re.match(r"^\d{1,2}:\d{2}$", time_key):
                    parts = time_key.split(":")
                    formatted_time = f"{int(parts[0]):02d}:{int(parts[1]):02d}"
                    data["reminders"][formatted_time] = v

    return data


def write_reminders_conf(data):
    lines = [
        "# Cấu hình tính năng Lời nhắc & Trò chuyện cho Shimeji",
        f"enabled={'true' if data.get('enabled', True) else 'false'}",
        f"soundEnabled={'true' if data.get('soundEnabled', True) else 'false'}",
        f"notifySendEnabled={'true' if data.get('notifySendEnabled', True) else 'false'}",
        f"randomIdleChatEnabled={'true' if data.get('randomIdleChatEnabled', True) else 'false'}",
        f"randomChatIntervalMinutes={data.get('randomChatIntervalMinutes', 15)}",
        f"bubbleDurationSeconds={data.get('bubbleDurationSeconds', 7)}",
        "",
        "# Scheduled Reminders (Lịch nhắc nhở cố định theo giờ HH:mm)",
    ]

    reminders = data.get("reminders", {})
    for t in sorted(reminders.keys()):
        formatted_key = t.replace(":", "_")
        lines.append(f"reminder.{formatted_key}={reminders[t]}")

    lines.extend([
        "",
        "# Interval Reminders (Nhắc nhở theo chu kỳ phút)",
        f"interval.water_minutes={data.get('water_minutes', 60)}",
        f"interval.water_message={data.get('water_message', 'Anh nhớ uống một ngụm nước nhé! 💧')}",
        f"interval.rest_minutes={data.get('rest_minutes', 45)}",
        f"interval.rest_message={data.get('rest_message', 'Anh chớp mắt và vươn vai thư giãn 20 giây nha! 👀')}",
        "",
    ])

    os.makedirs(os.path.dirname(REMINDERS_PROPS), exist_ok=True)
    with open(REMINDERS_PROPS, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def read_dialogues_conf():
    if not os.path.exists(DIALOGUES_CONF):
        return ""
    with open(DIALOGUES_CONF, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def write_dialogues_conf(text):
    os.makedirs(os.path.dirname(DIALOGUES_CONF), exist_ok=True)
    with open(DIALOGUES_CONF, "w", encoding="utf-8") as f:
        f.write(text)


def get_java_add_opens():
    java_opts = []
    try:
        check_bin = "java"
        if IS_WINDOWS and os.environ.get("JAVA_HOME"):
            jh_bin = os.path.join(os.environ["JAVA_HOME"], "bin", "java.exe")
            if os.path.exists(jh_bin):
                check_bin = jh_bin
        res = subprocess.run([check_bin, "-version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        version_line = ""
        for line in res.stdout.splitlines():
            if "version" in line.lower():
                version_line = line
                break
        match = re.search(r'"(\d+)', version_line)
        if match:
            major_ver = int(match.group(1))
            if major_ver == 1:
                match8 = re.search(r'"1\.(\d+)', version_line)
                if match8:
                    major_ver = int(match8.group(1))
            if major_ver >= 9:
                java_opts.extend([
                    "--add-opens", "java.desktop/sun.awt=ALL-UNNAMED",
                    "--add-opens", "java.desktop/sun.java2d=ALL-UNNAMED",
                    "--add-opens", "java.desktop/java.awt=ALL-UNNAMED",
                    "--add-opens", "java.desktop/java.awt.peer=ALL-UNNAMED",
                    "--add-opens", "java.base/java.lang=ALL-UNNAMED",
                    "--add-opens", "java.base/java.lang.reflect=ALL-UNNAMED",
                ])
                if IS_WINDOWS:
                    java_opts.extend(["--add-opens", "java.desktop/sun.awt.windows=ALL-UNNAMED"])
                elif IS_MAC:
                    java_opts.extend([
                        "--add-opens", "java.desktop/sun.lwawt=ALL-UNNAMED",
                        "--add-opens", "java.desktop/sun.lwawt.macosx=ALL-UNNAMED",
                    ])
                else:
                    java_opts.extend(["--add-opens", "java.desktop/sun.awt.X11=ALL-UNNAMED"])
    except Exception:
        pass
    return java_opts


def spawn_character(name):
    char_dir = os.path.join(CHARACTERS_DIR, name)
    if not os.path.isdir(char_dir):
        return
    cp = f"{char_dir}{os.pathsep}{os.path.join(APP_ROOT, 'Shimeji.jar')}"
    logging_file = os.path.join(APP_ROOT, "conf", "logging.properties")

    java_cmd = "java"
    if IS_WINDOWS:
        java_cmd = "javaw"
        if os.environ.get("JAVA_HOME"):
            jh_javaw = os.path.join(os.environ["JAVA_HOME"], "bin", "javaw.exe")
            if os.path.exists(jh_javaw):
                java_cmd = jh_javaw

    java_opts = get_java_add_opens()

    cmd = [
        java_cmd,
        *java_opts,
        "-Xmx64m",
        "-classpath",
        cp,
        "-Djava.util.logging.config.file=" + logging_file,
        "com.group_finity.mascot.Main",
    ]
    if IS_WINDOWS:
        creation_flags = 0
        if hasattr(subprocess, "DETACHED_PROCESS"):
            creation_flags |= subprocess.DETACHED_PROCESS
        if hasattr(subprocess, "CREATE_NEW_PROCESS_GROUP"):
            creation_flags |= subprocess.CREATE_NEW_PROCESS_GROUP
        subprocess.Popen(cmd, cwd=APP_ROOT, creationflags=creation_flags)
    else:
        subprocess.Popen(cmd, cwd=APP_ROOT)


def kill_all_mascots():
    if IS_WINDOWS:
        ps_cmd = 'Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -like "*com.group_finity.mascot.Main*" -or $_.CommandLine -like "*Shimeji.jar*" } | ForEach-Object { $_.Terminate() }'
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True)
        except Exception:
            pass
        subprocess.run('taskkill /f /fi "WINDOWTITLE eq Shimeji*"', shell=True, capture_output=True)
    else:
        subprocess.run("pkill -f 'com.group_finity.mascot.Main'", shell=True)


def restart_shimeji():
    kill_all_mascots()
    if IS_WINDOWS:
        subprocess.Popen([RUN_SCRIPT], cwd=APP_ROOT, shell=True)
    else:
        subprocess.Popen(["bash", RUN_SCRIPT], cwd=APP_ROOT)


def open_folder():
    if IS_WINDOWS:
        os.startfile(APP_ROOT)
    elif IS_MAC:
        subprocess.Popen(["open", APP_ROOT])
    else:
        subprocess.Popen(["xdg-open", APP_ROOT])


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shimeji Master Control - Cài đặt & Lời nhắc")
        self.geometry("920x800")
        self.minsize(820, 700)
        self.configure(padx=12, pady=12)
        self.option_add("*Font", "Sans 10")

        self._all_characters = list_characters()

        icon_png = os.path.join(IMG_DIR, "icon.png")
        icon_ico = os.path.join(APP_ROOT, "shimeji.ico")
        if IS_WINDOWS and os.path.exists(icon_ico):
            try:
                self.iconbitmap(icon_ico)
            except Exception:
                pass
        elif os.path.exists(icon_png):
            try:
                self._app_icon = tk.PhotoImage(file=icon_png)
                self.iconphoto(True, self._app_icon)
            except Exception:
                pass

        # Variables
        self.character_var = tk.StringVar()
        self.self_clone_var = tk.BooleanVar(value=True)

        # Reminder Variables
        self.reminder_enabled_var = tk.BooleanVar(value=True)
        self.sound_enabled_var = tk.BooleanVar(value=True)
        self.notify_send_var = tk.BooleanVar(value=True)
        self.random_chat_enabled_var = tk.BooleanVar(value=True)
        self.random_chat_interval_var = tk.StringVar(value="15")
        self.bubble_duration_var = tk.StringVar(value="7")

        self.water_minutes_var = tk.StringVar(value="60")
        self.water_msg_var = tk.StringVar(value="Anh nhớ uống một ngụm nước nhé! 💧")
        self.rest_minutes_var = tk.StringVar(value="45")
        self.rest_msg_var = tk.StringVar(value="Anh chớp mắt và vươn vai thư giãn 20 giây nha! 👀")

        self.time_input_var = tk.StringVar(value="11:55")
        self.msg_input_var = tk.StringVar(value="11h55 rồi, anh đi ăn cơm trưa thôi nào! 🍚🍛")

        self.scheduled_reminders_dict = {}

        self._build_ui()
        self.load_values()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        top = ttk.Frame(self)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        top.grid_columnconfigure(0, weight=1)
        ttk.Label(top, text="Shimeji Master Control", font=("Sans", 15, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(top, text="Quản lý nhân vật desktop, bóng thoại trò chuyện & lịch nhắc nhở thông minh.").grid(row=1, column=0, sticky="w", pady=(2, 6))

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky="nsew")

        # Tab 1: Characters & Windows
        self.tab_char = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_char, text="🎭 Nhân vật & Cửa sổ")
        self._build_tab_char()

        # Tab 2: Speech & Reminders
        self.tab_speech = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_speech, text="💬 Trò chuyện & Lời nhắc")
        self._build_tab_speech()

        # Bottom Buttons
        bottom = ttk.Frame(self)
        bottom.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        ttk.Button(bottom, text="💾 Lưu cài đặt (Save)", command=self.save).pack(side="left")
        ttk.Button(bottom, text="⚡ Apply + Restart", command=self.apply_all).pack(side="left", padx=4)
        ttk.Button(bottom, text="🔄 Restart Shimeji", command=self.restart).pack(side="left", padx=4)
        ttk.Button(bottom, text="🛑 Tắt TẤT CẢ NV", command=self.kill_all).pack(side="left", padx=4)
        ttk.Button(bottom, text="📁 Open Folder", command=self.open_folder).pack(side="left", padx=4)
        ttk.Button(bottom, text="❌ Đóng", command=self.destroy).pack(side="right")

    def _build_tab_char(self):
        self.tab_char.grid_columnconfigure(0, weight=1)
        self.tab_char.grid_rowconfigure(3, weight=1)

        # Character Library Frame
        chars = ttk.LabelFrame(self.tab_char, text=f"Nhân vật ({len(self._all_characters)} Characters Library)", padding=8)
        chars.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        chars.grid_columnconfigure(1, weight=1)

        ttk.Label(chars, text="Tìm kiếm / Lọc:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(chars, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=6, pady=4)
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_characters())

        ttk.Label(chars, text="Nhân vật hiện tại:").grid(row=1, column=0, sticky="w", padx=6, pady=4)
        self.character_combo = ttk.Combobox(chars, textvariable=self.character_var, state="readonly", values=self._all_characters)
        self.character_combo.grid(row=1, column=1, sticky="ew", padx=6, pady=4)
        self.character_combo.bind("<<ComboboxSelected>>", lambda e: self.update_preview())

        char_btn_frame = ttk.Frame(chars)
        char_btn_frame.grid(row=1, column=2, sticky="e", padx=6, pady=4)
        ttk.Button(char_btn_frame, text="Áp dụng NV", command=self.apply_character_only).pack(side="left", padx=2)
        ttk.Button(char_btn_frame, text="Thả NV này", command=self.spawn_selected).pack(side="left", padx=2)
        ttk.Button(char_btn_frame, text="Thả TẤT CẢ NV", command=self.spawn_all).pack(side="left", padx=2)

        # Preview
        preview_frame = ttk.Frame(chars)
        preview_frame.grid(row=2, column=0, columnspan=3, pady=(4, 4))
        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack()
        self._preview_img = None

        # Behavior
        behavior = ttk.LabelFrame(self.tab_char, text="Hành vi nhân bản", padding=8)
        behavior.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        ttk.Checkbutton(behavior, text="Cho phép tự nhân bản (Self-cloning / đẻ thêm con)", variable=self.self_clone_var).grid(row=0, column=0, sticky="w", padx=6, pady=4)

        # Window Offsets
        offsets = ttk.LabelFrame(self.tab_char, text="Tọa độ bám cửa sổ (window.conf)", padding=8)
        offsets.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        for i in range(2):
            offsets.grid_columnconfigure(i, weight=1)

        self.entries = {}
        fields = [
            ("x offset", "x"),
            ("y offset", "y"),
            ("width add", "w"),
            ("height add", "h"),
        ]
        for idx, (label, key) in enumerate(fields):
            col = idx % 2
            row = idx // 2
            block = ttk.Frame(offsets)
            block.grid(row=row, column=col, sticky="ew", padx=6, pady=4)
            block.grid_columnconfigure(1, weight=1)
            ttk.Label(block, text=label, width=12).grid(row=0, column=0, sticky="w", padx=(0, 6))
            ent = ttk.Entry(block, width=12)
            ent.grid(row=0, column=1, sticky="w")
            self.entries[key] = ent

        # Titles conf
        titles = ttk.LabelFrame(self.tab_char, text="Danh sách cửa sổ bám vào (titles.conf)", padding=8)
        titles.grid(row=3, column=0, sticky="nsew")
        titles.grid_columnconfigure(0, weight=1)
        titles.grid_rowconfigure(1, weight=1)
        ttk.Label(titles, text="Mỗi dòng một tiêu đề cửa sổ. Để trống = bám mọi cửa sổ.").grid(row=0, column=0, sticky="w", padx=6, pady=(0, 4))

        text_wrap = ttk.Frame(titles)
        text_wrap.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 4))
        text_wrap.grid_columnconfigure(0, weight=1)
        text_wrap.grid_rowconfigure(0, weight=1)
        self.text_titles = tk.Text(text_wrap, height=6, wrap="word")
        yscroll = ttk.Scrollbar(text_wrap, orient="vertical", command=self.text_titles.yview)
        self.text_titles.configure(yscrollcommand=yscroll.set)
        self.text_titles.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")

    def _build_tab_speech(self):
        self.tab_speech.grid_columnconfigure(0, weight=1)
        self.tab_speech.grid_rowconfigure(2, weight=1)

        # Option flags frame
        opts = ttk.LabelFrame(self.tab_speech, text="Thiết lập Chung", padding=8)
        opts.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        opts.grid_columnconfigure(0, weight=1)
        opts.grid_columnconfigure(1, weight=1)

        row0 = ttk.Frame(opts)
        row0.grid(row=0, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(row0, text="Bật hệ thống nhắc nhở & bóng thoại", variable=self.reminder_enabled_var).pack(side="left", padx=(0, 15))
        ttk.Checkbutton(row0, text="Âm thanh chuông báo (Beep)", variable=self.sound_enabled_var).pack(side="left", padx=(0, 15))
        ttk.Checkbutton(row0, text="Thông báo Desktop hệ thống (Desktop notification)", variable=self.notify_send_var).pack(side="left")

        row1 = ttk.Frame(opts)
        row1.grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 2))
        ttk.Checkbutton(row1, text="Tự động nói chuyện vu vơ khi rảnh rỗi (Idle chat) mỗi", variable=self.random_chat_enabled_var).pack(side="left")
        ttk.Entry(row1, textvariable=self.random_chat_interval_var, width=5).pack(side="left", padx=4)
        ttk.Label(row1, text="phút.").pack(side="left", padx=(0, 20))

        ttk.Label(row1, text="Thời gian bóng thoại hiện:").pack(side="left")
        ttk.Entry(row1, textvariable=self.bubble_duration_var, width=4).pack(side="left", padx=4)
        ttk.Label(row1, text="giây.").pack(side="left")

        # Scheduled Reminders Frame
        sched = ttk.LabelFrame(self.tab_speech, text="⏰ Lịch Nhắc Nhở Cố Định Theo Giờ (Ví dụ: 11:55 Nhắc ăn cơm trưa)", padding=8)
        sched.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        sched.grid_columnconfigure(0, weight=1)

        # Treeview
        tree_wrap = ttk.Frame(sched)
        tree_wrap.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        tree_wrap.grid_columnconfigure(0, weight=1)

        self.tree_reminders = ttk.Treeview(tree_wrap, columns=("time", "message"), show="headings", height=5)
        self.tree_reminders.heading("time", text="Giờ (HH:mm)")
        self.tree_reminders.heading("message", text="Nội dung lời nhắc")
        self.tree_reminders.column("time", width=110, anchor="center")
        self.tree_reminders.column("message", width=620, anchor="w")

        tree_scroll = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.tree_reminders.yview)
        self.tree_reminders.configure(yscrollcommand=tree_scroll.set)
        self.tree_reminders.grid(row=0, column=0, sticky="nsew")
        tree_scroll.grid(row=0, column=1, sticky="ns")

        self.tree_reminders.bind("<<TreeviewSelect>>", self._on_reminder_selected)

        # Add/Edit Controls
        ctrl = ttk.Frame(sched)
        ctrl.grid(row=1, column=0, sticky="ew")
        ctrl.grid_columnconfigure(3, weight=1)

        ttk.Label(ctrl, text="Giờ:").grid(row=0, column=0, sticky="w", padx=(0, 4))
        ttk.Entry(ctrl, textvariable=self.time_input_var, width=8).grid(row=0, column=1, sticky="w", padx=(0, 8))

        ttk.Label(ctrl, text="Nội dung:").grid(row=0, column=2, sticky="w", padx=(0, 4))
        ttk.Entry(ctrl, textvariable=self.msg_input_var).grid(row=0, column=3, sticky="ew", padx=(0, 8))

        ttk.Button(ctrl, text="➕ Thêm / Cập nhật", command=self._add_or_update_reminder).grid(row=0, column=4, padx=2)
        ttk.Button(ctrl, text="❌ Xóa mốc chọn", command=self._delete_reminder).grid(row=0, column=5, padx=2)

        # Lower Split: Interval reminders & Dialogues
        lower = ttk.Frame(self.tab_speech)
        lower.grid(row=2, column=0, sticky="nsew")
        lower.grid_columnconfigure(0, weight=1)
        lower.grid_columnconfigure(1, weight=1)
        lower.grid_rowconfigure(0, weight=1)

        # Interval reminders
        inter = ttk.LabelFrame(lower, text="💧 Lời Nhắc Theo Chu Kỳ", padding=8)
        inter.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        inter.grid_columnconfigure(1, weight=1)

        ttk.Label(inter, text="Nhắc uống nước mỗi (phút):").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(inter, textvariable=self.water_minutes_var, width=6).grid(row=0, column=1, sticky="w", pady=4)
        ttk.Label(inter, text="Câu nhắc:").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Entry(inter, textvariable=self.water_msg_var).grid(row=1, column=1, sticky="ew", pady=2)

        ttk.Label(inter, text="Nhắc nghỉ mắt/vươn vai mỗi (phút):").grid(row=2, column=0, sticky="w", pady=(8, 4))
        ttk.Entry(inter, textvariable=self.rest_minutes_var, width=6).grid(row=2, column=1, sticky="w", pady=(8, 4))
        ttk.Label(inter, text="Câu nhắc:").grid(row=3, column=0, sticky="w", pady=2)
        ttk.Entry(inter, textvariable=self.rest_msg_var).grid(row=3, column=1, sticky="ew", pady=2)

        # Dialogues
        dlg = ttk.LabelFrame(lower, text="💬 Danh Sách Câu Thoại Ngẫu Nhiên (dialogues.conf)", padding=8)
        dlg.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        dlg.grid_columnconfigure(0, weight=1)
        dlg.grid_rowconfigure(1, weight=1)

        ttk.Label(dlg, text="Mỗi dòng là một câu thoại khi click chuột phải chọn 'Trò chuyện':").grid(row=0, column=0, sticky="w", pady=(0, 4))

        dlg_wrap = ttk.Frame(dlg)
        dlg_wrap.grid(row=1, column=0, sticky="nsew")
        dlg_wrap.grid_columnconfigure(0, weight=1)
        dlg_wrap.grid_rowconfigure(0, weight=1)

        self.text_dialogues = tk.Text(dlg_wrap, height=6, wrap="word")
        dlg_scroll = ttk.Scrollbar(dlg_wrap, orient="vertical", command=self.text_dialogues.yview)
        self.text_dialogues.configure(yscrollcommand=dlg_scroll.set)
        self.text_dialogues.grid(row=0, column=0, sticky="nsew")
        dlg_scroll.grid(row=0, column=1, sticky="ns")

    def _on_reminder_selected(self, event):
        sel = self.tree_reminders.selection()
        if sel:
            item = self.tree_reminders.item(sel[0])
            vals = item.get("values", [])
            if len(vals) >= 2:
                self.time_input_var.set(str(vals[0]))
                self.msg_input_var.set(str(vals[1]))

    def _add_or_update_reminder(self):
        t = self.time_input_var.get().strip()
        msg = self.msg_input_var.get().strip()
        if not re.match(r"^\d{1,2}:\d{2}$", t):
            messagebox.showerror("Lỗi định dạng giờ", "Giờ nhắc phải có dạng HH:mm (ví dụ 11:55 hoặc 08:30).")
            return
        if not msg:
            messagebox.showerror("Thiếu nội dung", "Vui lòng nhập nội dung lời nhắc.")
            return

        parts = t.split(":")
        h = int(parts[0])
        m = int(parts[1])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            messagebox.showerror("Giờ không hợp lệ", "Giờ phải từ 00 đến 23, phút từ 00 đến 59.")
            return

        formatted_time = f"{h:02d}:{m:02d}"
        self.scheduled_reminders_dict[formatted_time] = msg
        self._refresh_reminders_tree()

    def _delete_reminder(self):
        sel = self.tree_reminders.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng bấm chọn một dòng mốc giờ trong bảng để xóa.")
            return
        item = self.tree_reminders.item(sel[0])
        vals = item.get("values", [])
        if vals:
            t = str(vals[0])
            if t in self.scheduled_reminders_dict:
                del self.scheduled_reminders_dict[t]
                self._refresh_reminders_tree()

    def _refresh_reminders_tree(self):
        for item in self.tree_reminders.get_children():
            self.tree_reminders.delete(item)
        for t in sorted(self.scheduled_reminders_dict.keys()):
            self.tree_reminders.insert("", "end", values=(t, self.scheduled_reminders_dict[t]))

    def filter_characters(self):
        query = self.search_var.get().strip().lower()
        if not hasattr(self, "_all_characters") or not self._all_characters:
            self._all_characters = list_characters()
        all_chars = self._all_characters
        if not query:
            filtered = all_chars
        else:
            filtered = [c for c in all_chars if query in c.lower()]
        self.character_combo["values"] = filtered
        if filtered:
            if self.character_var.get() not in filtered:
                self.character_var.set(filtered[0])
            self.update_preview()
        else:
            self.character_var.set("")
            self.update_preview()

    def update_preview(self):
        name = self.character_var.get().strip()
        img_path = os.path.join(CHARACTERS_DIR, name, "shime1.png")
        if os.path.exists(img_path):
            try:
                img = tk.PhotoImage(file=img_path)
                self.preview_label.configure(image=img, text="")
                self._preview_img = img
                return
            except Exception:
                pass
        self.preview_label.configure(image="", text="[No preview available]")
        self._preview_img = None

    def load_values(self):
        # Character
        self._all_characters = list_characters()
        self.character_combo["values"] = self._all_characters
        current = detect_current_character()
        if current not in self._all_characters and self._all_characters:
            current = self._all_characters[0]
        self.character_var.set(current)
        self.update_preview()

        # Settings props
        props = read_settings_props()
        self.self_clone_var.set(bool(props.get("selfCloningEnabled", True)))

        # Window conf
        vals = read_window_conf()
        for key, val in zip(["x", "y", "w", "h"], vals):
            self.entries[key].delete(0, "end")
            self.entries[key].insert(0, val)

        # Titles conf
        self.text_titles.delete("1.0", "end")
        self.text_titles.insert("1.0", read_titles_conf())

        # Reminders conf
        rem_data = read_reminders_conf()
        self.reminder_enabled_var.set(rem_data.get("enabled", True))
        self.sound_enabled_var.set(rem_data.get("soundEnabled", True))
        self.notify_send_var.set(rem_data.get("notifySendEnabled", True))
        self.random_chat_enabled_var.set(rem_data.get("randomIdleChatEnabled", True))
        self.random_chat_interval_var.set(str(rem_data.get("randomChatIntervalMinutes", 15)))
        self.bubble_duration_var.set(str(rem_data.get("bubbleDurationSeconds", 7)))

        self.water_minutes_var.set(str(rem_data.get("water_minutes", 60)))
        self.water_msg_var.set(rem_data.get("water_message", "Anh nhớ uống một ngụm nước nhé! 💧"))
        self.rest_minutes_var.set(str(rem_data.get("rest_minutes", 45)))
        self.rest_msg_var.set(rem_data.get("rest_message", "Anh chớp mắt và vươn vai thư giãn 20 giây nha! 👀"))

        self.scheduled_reminders_dict = dict(rem_data.get("reminders", {}))
        self._refresh_reminders_tree()

        # Dialogues conf
        self.text_dialogues.delete("1.0", "end")
        self.text_dialogues.insert("1.0", read_dialogues_conf())

    def save(self):
        # 1. Window conf
        vals = [self.entries[k].get().strip() or "0" for k in ["x", "y", "w", "h"]]
        try:
            [int(v) for v in vals]
        except ValueError:
            messagebox.showerror("Invalid number", "4 ô window.conf phải là số nguyên.")
            return False
        write_window_conf(vals)
        write_titles_conf(self.text_titles.get("1.0", "end").rstrip() + "\n" if self.text_titles.get("1.0", "end").strip() else "")
        write_settings_props(self.self_clone_var.get())

        # 2. Reminders conf
        try:
            chat_interval = int(self.random_chat_interval_var.get().strip() or "15")
            bubble_dur = int(self.bubble_duration_var.get().strip() or "7")
            water_m = int(self.water_minutes_var.get().strip() or "60")
            rest_m = int(self.rest_minutes_var.get().strip() or "45")
        except ValueError:
            messagebox.showerror("Số không hợp lệ", "Khoảng thời gian phút và giây phải là số nguyên dương.")
            return False

        rem_data = {
            "enabled": self.reminder_enabled_var.get(),
            "soundEnabled": self.sound_enabled_var.get(),
            "notifySendEnabled": self.notify_send_var.get(),
            "randomIdleChatEnabled": self.random_chat_enabled_var.get(),
            "randomChatIntervalMinutes": chat_interval,
            "bubbleDurationSeconds": bubble_dur,
            "water_minutes": water_m,
            "water_message": self.water_msg_var.get().strip(),
            "rest_minutes": rest_m,
            "rest_message": self.rest_msg_var.get().strip(),
            "reminders": self.scheduled_reminders_dict,
        }
        write_reminders_conf(rem_data)

        # 3. Dialogues conf
        write_dialogues_conf(self.text_dialogues.get("1.0", "end").strip() + "\n")

        messagebox.showinfo("Đã lưu", "Đã lưu cài đặt nhân vật và lời nhắc thành công!\n(Nhân vật đang chạy sẽ tự động cập nhật ngay mà không cần restart).")
        return True

    def apply_character_only(self):
        name = self.character_var.get().strip()
        if not name:
            messagebox.showerror("No character", "Chưa chọn nhân vật.")
            return False
        try:
            apply_character(name)
            messagebox.showinfo("Character applied", f"Đã áp dụng nhân vật: {name}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi áp dụng nhân vật: {e}")
            return False

    def apply_all(self):
        if not self.save():
            return
        if not self.apply_character_only():
            return
        self.restart()

    def restart(self):
        try:
            restart_shimeji()
            messagebox.showinfo("Restarted", "Đã restart Shimeji.")
        except Exception as e:
            messagebox.showerror("Restart failed", str(e))

    def spawn_selected(self):
        name = self.character_var.get().strip()
        if not name:
            messagebox.showerror("No character", "Chưa chọn nhân vật.")
            return
        spawn_character(name)
        messagebox.showinfo("Spawned", f"Đã thả nhân vật '{name}' ra màn hình!")

    def spawn_all(self):
        chars = list_characters()
        if not chars:
            messagebox.showerror("No characters", "Không tìm thấy nhân vật nào.")
            return
        res = messagebox.askyesnocancel(
            "Thả tất cả nhân vật",
            f"Tìm thấy {len(chars)} nhân vật trong thư viện.\n\n"
            f"• Bấm 'YES' để thả TẤT CẢ {len(chars)} nhân vật ra màn hình.\n"
            f"• Bấm 'NO' để thả 20 nhân vật ngẫu nhiên.\n"
            f"• Bấm 'CANCEL' để hủy."
        )
        if res is True:
            for name in chars:
                spawn_character(name)
            messagebox.showinfo("Spawn All", f"Đã kích hoạt thả {len(chars)} nhân vật ra màn hình!")
        elif res is False:
            import random
            sample = random.sample(chars, min(20, len(chars)))
            for name in sample:
                spawn_character(name)
            messagebox.showinfo("Spawn 20", f"Đã thả 20 nhân vật ngẫu nhiên ra màn hình!")

    def kill_all(self):
        try:
            kill_all_mascots()
            messagebox.showinfo("Cleared", "Đã đóng tất cả nhân vật trên màn hình.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_folder(self):
        open_folder()


if __name__ == "__main__":
    if not acquire_single_instance_lock():
        sys.exit(0)
    App().mainloop()
