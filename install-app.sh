#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ICON_PATH="$APP_DIR/docs/images/linux-shimeji-icon.png"
BIN_DIR="$HOME/.local/bin"
APPS_DIR="$HOME/.local/share/applications"
DESKTOP_DIR="$HOME/Desktop"

echo "=== Đang thiết lập và cài đặt ứng dụng Shimeji ==="

# 1. Cấp quyền thực thi cho các script
chmod +x "$APP_DIR/launch.sh" "$APP_DIR/run-linux-shimeji.sh" "$APP_DIR/run-settings.sh" "$APP_DIR/shimeji_settings.py"

# 2. Build lại Shimeji.jar nếu chưa có hoặc cập nhật
if command -v ant >/dev/null 2>&1; then
    echo "-> Đang build Shimeji.jar bằng Ant..."
    (cd "$APP_DIR" && ant jar) || true
fi

# 3. Tạo thư mục bin nếu chưa có
mkdir -p "$BIN_DIR"
mkdir -p "$APPS_DIR"

# 4. Tạo wrapper command trong ~/.local/bin
cat <<EOF > "$BIN_DIR/shimeji"
#!/usr/bin/env bash
exec bash "$APP_DIR/run-linux-shimeji.sh" "\$@"
EOF
chmod +x "$BIN_DIR/shimeji"

cat <<EOF > "$BIN_DIR/shimeji-settings"
#!/usr/bin/env bash
exec bash "$APP_DIR/run-settings.sh" "\$@"
EOF
chmod +x "$BIN_DIR/shimeji-settings"

# 5. Tạo Desktop Entry trong menu ứng dụng (~/.local/share/applications)
cat <<EOF > "$APPS_DIR/shimeji.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=Shimeji Desktop Mascot
Comment=Desktop mascot pet for Linux
Exec=bash "$APP_DIR/run-linux-shimeji.sh"
Icon=$ICON_PATH
Path=$APP_DIR
Terminal=false
Categories=Utility;Amusement;
Keywords=shimeji;mascot;pet;anime;
StartupNotify=true
EOF
chmod +x "$APPS_DIR/shimeji.desktop"

cat <<EOF > "$APPS_DIR/shimeji-settings.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=Shimeji Settings & Characters
Comment=Settings, Dialogues, Reminders and Character Switcher for Shimeji
Exec=bash "$APP_DIR/run-settings.sh"
Icon=$ICON_PATH
Path=$APP_DIR
Terminal=false
Categories=Utility;Settings;
Keywords=shimeji;settings;character;
StartupNotify=true
EOF
chmod +x "$APPS_DIR/shimeji-settings.desktop"

# 6. Tạo Desktop Shortcut trên Desktop nếu có thư mục Desktop
if [ -d "$DESKTOP_DIR" ]; then
    cp "$APPS_DIR/shimeji.desktop" "$DESKTOP_DIR/shimeji.desktop"
    cp "$APPS_DIR/shimeji-settings.desktop" "$DESKTOP_DIR/shimeji-settings.desktop"
    chmod +x "$DESKTOP_DIR/shimeji.desktop" "$DESKTOP_DIR/shimeji-settings.desktop"

    if command -v gio >/dev/null 2>&1; then
        gio set "$DESKTOP_DIR/shimeji.desktop" metadata::trusted true 2>/dev/null || true
        gio set "$DESKTOP_DIR/shimeji-settings.desktop" metadata::trusted true 2>/dev/null || true
    fi
fi

# 7. Cập nhật cơ sở dữ liệu ứng dụng của hệ thống
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APPS_DIR" 2>/dev/null || true
fi

echo "=== Đã hoàn tất cài đặt ứng dụng Shimeji! ==="
echo "✔ Lệnh thực thi trong terminal: 'shimeji' hoặc 'shimeji-settings'"
echo "✔ Icon trong menu ứng dụng hệ thống (App Launcher)"
echo "✔ Shortcut trên Desktop (~/Desktop)"
