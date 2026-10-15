# WebP decoder

`dwebp.exe` is the unmodified Windows x64 decoder from **libwebp 1.6.0**.

- Official download: https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.6.0-windows-x64.zip
- Archive member: `libwebp-1.6.0-windows-x64/bin/dwebp.exe`
- SHA-256 of `dwebp.exe`: `17c1488bf84b7834e9aa908bb40afd0be2e55d57567d210e96336c56bb6ae993`
- Source: https://chromium.googlesource.com/webm/libwebp/+/v1.6.0/
- Usage: https://developers.google.com/speed/webp/docs/dwebp
- License and patent grant: [COPYING](COPYING), [PATENTS](PATENTS).
- PNG/zlib notices for the decoder's PNG output: [LICENSE.libpng](LICENSE.libpng), [LICENSE.zlib](LICENSE.zlib).

Portable builds bundle the decoder and `character_frames.json`; imported WebP sprites are decoded locally in the temporary import directory. The decoder never comes from the character archive. The settings editor and importer are written in Python; portable builds include the Python runtime.

The Python importer uses this executable on Windows. On Linux install the distribution's `dwebp` command (Ubuntu/Debian: `sudo apt install webp`). No Pillow dependency is required.

The importer converts the selected WebP poses to transparent PNGs at 128 x 128 pixels, matching this application's default pose anchors. Original animation scripts are not executed.
