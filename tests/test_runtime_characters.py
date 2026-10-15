"""Render distinct character sets in an isolated installation with Qt offscreen."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


@unittest.skipUnless(importlib.util.find_spec("PySide6"), "Install requirements.txt for Qt tests")
class MultipleCharacterRuntimeTest(unittest.TestCase):
    def test_different_characters_render_clone_and_reload_with_their_own_images(self):
        from PySide6.QtGui import QColor, QImage
        source = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ("shimeji.py", "shimeji_settings.py", "mascot_physics.py", "desktop_windows.py",
                         "character_import.py", "character_formats.py", "character_webp.py", "character_frames.json"):
                shutil.copy2(source / name, root / name)
            # Different colors on each side expose both cache collisions and bad mirroring.
            for name, color in (("Red", "red"), ("Blue", "blue")):
                directory = root / "characters" / name
                directory.mkdir(parents=True)
                image = QImage(16, 16, QImage.Format_ARGB32)
                image.fill(QColor(color))
                image.setPixelColor(0, 0, QColor("green"))
                for number in range(1, 47):
                    self.assertTrue(image.save(str(directory / f"shime{number}.png")))
            (root / ".current_character").write_text("Red\nBlue\n", encoding="utf-8")
            (root / "settings.properties").write_text("selfCloningEnabled=false\nscalePercent=100\n")
            result = subprocess.run([sys.executable, "-B", str(root / "shimeji.py"), "--smoke-test"],
                cwd=root, env=dict(os.environ, QT_QPA_PLATFORM="offscreen"),
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("2 independent character sets passed", result.stdout)
            self.assertEqual((root / ".current_character").read_text(encoding="utf-8"), "Red\nBlue\n")


if __name__ == "__main__":
    unittest.main()
