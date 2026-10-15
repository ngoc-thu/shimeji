# Build on each target OS. Both executables share the same Python-only entry point.
from pathlib import Path
import sys

root = Path(SPECPATH)
datas = [(str(root / 'character_frames.json'), '.')]
if sys.platform == 'win32':
    datas += [(str(root / 'lib' / 'webp' / 'dwebp.exe'), 'lib/webp')]
for notice in (root / 'lib' / 'webp').iterdir():
    if notice.name != 'dwebp.exe':
        datas.append((str(notice), 'lib/webp'))
a = Analysis([str(root / 'shimeji.py')], pathex=[str(root)], datas=datas,
             hiddenimports=[], excludes=['PySide6.QtQml', 'PySide6.QtQuick', 'PySide6.QtOpenGL'])
pyz = PYZ(a.pure)
options = dict(exclude_binaries=True, console=False,
               icon=str(root / 'shimeji.ico') if sys.platform == 'win32' else None)
mascot = EXE(pyz, a.scripts, [], name='Shimeji', **options)
settings = EXE(pyz, a.scripts, [], name='ShimejiSettings', **options)
collection = COLLECT(mascot, settings, a.binaries, a.datas, name='Shimeji')
