#!/usr/bin/env python3
"""Bundle Python, Qt and the settings editor into a portable application folder."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    subprocess.run([sys.executable, "-m", "PyInstaller", "--noconfirm", str(ROOT / "Shimeji.spec")],
                   cwd=ROOT, check=True)
    destination = ROOT / "dist" / "Shimeji"
    for folder in ("img", "characters", "docs"):
        shutil.copytree(ROOT / folder, destination / folder, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("*.jar", "__pycache__"))
    for name in ("window.conf", "titles.conf", "settings.properties", ".current_character",
                 "shimeji.ico", "README.md", "LICENSE", "LICENSE.de"):
        source = ROOT / name
        if source.exists():
            shutil.copy2(source, destination / name)
    print("Portable application created in " + str(destination))


if __name__ == "__main__":
    main()
