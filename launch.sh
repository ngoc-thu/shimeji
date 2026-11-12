#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

JAVA_OPTS=()
JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}' | cut -d'.' -f1)

OS_NAME="$(uname -s)"

if [ -n "$JAVA_VERSION" ] && [ "$JAVA_VERSION" -ge 9 ] 2>/dev/null; then
    JAVA_OPTS=(
        --add-opens java.desktop/sun.awt=ALL-UNNAMED
        --add-opens java.desktop/sun.java2d=ALL-UNNAMED
        --add-opens java.desktop/java.awt=ALL-UNNAMED
        --add-opens java.desktop/java.awt.peer=ALL-UNNAMED
        --add-opens java.base/java.lang=ALL-UNNAMED
        --add-opens java.base/java.lang.reflect=ALL-UNNAMED
    )
    if [ "$OS_NAME" = "Linux" ]; then
        JAVA_OPTS+=(--add-opens java.desktop/sun.awt.X11=ALL-UNNAMED)
    elif [ "$OS_NAME" = "Darwin" ]; then
        JAVA_OPTS+=(
            --add-opens java.desktop/sun.lwawt=ALL-UNNAMED
            --add-opens java.desktop/sun.lwawt.macosx=ALL-UNNAMED
        )
    fi
fi

exec java "${JAVA_OPTS[@]}" -classpath Shimeji.jar -Xmx1000m -Djava.util.logging.config.file=./conf/logging.properties com.group_finity.mascot.Main "$@"
