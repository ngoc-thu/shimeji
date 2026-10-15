#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ -x .venv/bin/python ]]; then
    exec .venv/bin/python shimeji.py "$@"
fi
exec python3 shimeji.py "$@"
