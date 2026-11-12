#!/usr/bin/env bash
set -euo pipefail

BIN_DIR="$HOME/.local/bin"
APPS_DIR="$HOME/.local/share/applications"
DESKTOP_DIR="$HOME/Desktop"

echo "=== Đang gỡ bỏ shortcut và app wrapper của Shimeji ==="

rm -f "$BIN_DIR/shimeji" "$BIN_DIR/shimeji-settings"
rm -f "$APPS_DIR/shimeji.desktop" "$APPS_DIR/shimeji-settings.desktop"
if [ -d "$DESKTOP_DIR" ]; then
    rm -f "$DESKTOP_DIR/shimeji.desktop" "$DESKTOP_DIR/shimeji-settings.desktop"
fi

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APPS_DIR" 2>/dev/null || true
fi

echo "=== Đã gỡ bỏ thành công! ==="
