"""Import standard desktop Shimeji sprites without extracting executable package files."""
import os
import re
import shutil
import struct
import tempfile
import zipfile
from pathlib import Path

from character_formats import prepare_groups
from character_webp import convert_webp

FRAME_NAMES = tuple(f"shime{i}.png" for i in range(1, 47))
MAX_ENTRIES = 10000
MAX_FRAME_BYTES = 16 * 1024 * 1024
MAX_TOTAL_BYTES = 256 * 1024 * 1024


def is_character_directory(path):
    return all((Path(path) / name).is_file() for name in FRAME_NAMES)


def _safe_name(name):
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip(" .")[:100].strip(" .")
    if not name or name.upper().split(".")[0] in {
        "CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }:
        name = "Shimeji"
    return name


def _copy_frame(source, target):
    # Bound actual bytes as well as ZIP metadata; accept PNGs with reasonable dimensions.
    data = source.read(MAX_FRAME_BYTES + 1)
    if len(data) > MAX_FRAME_BYTES:
        raise ValueError("An image file exceeds 16 MiB.")
    if data[:4] == b"RIFF":
        data = convert_webp(data, target)
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("Invalid PNG image: " + target.name)
    width, height = struct.unpack(">II", data[16:24])
    if not (1 <= width <= 4096 and 1 <= height <= 4096):
        raise ValueError("Image dimensions must be between 1 and 4096 pixels.")
    target.write_bytes(data)
    return len(data)


def import_characters(source, characters_dir):
    """Return installed names. Import every complete sprite set, never overwrite a character."""
    source = Path(source)
    archive = None
    try:
        entries = []
        if source.is_dir():
            for base, dirs, files in os.walk(source, followlinks=False):
                dirs[:] = sorted(d for d in dirs if not (Path(base) / d).is_symlink())
                for name in sorted(files):
                    path = Path(base) / name
                    if path.is_symlink():
                        continue
                    entries.append((path.relative_to(source).as_posix(), path))
                    if len(entries) > MAX_ENTRIES:
                        raise ValueError("The package contains too many files (maximum 10000).")
            opener = lambda entry: entry.open("rb")
        else:
            if source.suffix.lower() != ".zip":
                raise ValueError("Please select a ZIP package or an extracted character folder.")
            archive = zipfile.ZipFile(source)
            if len(archive.infolist()) > MAX_ENTRIES:
                raise ValueError("The package contains too many files (maximum 10000).")
            for entry in archive.infolist():
                path = entry.filename.replace("\\", "/")
                if path.startswith("/") or ":" in path or ".." in path.split("/"):
                    raise ValueError("Unsafe file path in ZIP package: " + path)
                if not entry.is_dir():
                    entries.append((path, entry))
            opener = archive.open
        groups = [(_safe_name(label), frames) for label, frames in prepare_groups(
            entries, source.stem if source.is_file() else source.name, FRAME_NAMES, opener)]
        characters_dir = Path(characters_dir)
        characters_dir.mkdir(parents=True, exist_ok=True)
        installed = []
        with tempfile.TemporaryDirectory(prefix=".import-", dir=characters_dir) as staging:
            stage = Path(staging)
            total = 0
            for index, (_, frames) in enumerate(groups):
                target = stage / str(index)
                target.mkdir()
                copied = {}
                for name in FRAME_NAMES:
                    entry = frames[name]
                    if entry in copied:
                        shutil.copyfile(copied[entry], target / name)
                        total += (target / name).stat().st_size
                    else:
                        with opener(entry) as stream:
                            total += _copy_frame(stream, target / name)
                        copied[entry] = target / name
                    if total > MAX_TOTAL_BYTES:
                        raise ValueError("Character images exceed 256 MiB in total.")
            existing = {p.name.casefold() for p in characters_dir.iterdir()}
            try:
                for index, (label, _) in enumerate(groups):
                    name, suffix = label, 2
                    while name.casefold() in existing:
                        name = f"{label} ({suffix})"
                        suffix += 1
                    (stage / str(index)).rename(characters_dir / name)
                    installed.append(name)
                    existing.add(name.casefold())
            except Exception:
                for name in installed:
                    shutil.rmtree(characters_dir / name)
                raise
        return installed
    finally:
        if archive is not None:
            archive.close()
