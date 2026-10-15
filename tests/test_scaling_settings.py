import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import shimeji_settings as settings


class ScalingSettingsTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name) / "settings.properties"
        self.patch = patch.object(settings, "SETTINGS_PROPS", str(self.path))
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.directory.cleanup()

    def test_old_settings_default_to_original_size(self):
        self.assertEqual(settings.read_settings_props()["scalePercent"], 100)
        self.path.write_text("selfCloningEnabled=false\n", encoding="utf-8")
        self.assertEqual(settings.read_settings_props(), {"selfCloningEnabled": False, "scalePercent": 100})

    def test_round_trip_and_preserve_other_settings(self):
        self.path.write_text("# preferences\nother=value\nselfCloningEnabled=true\nscalePercent=100\n", encoding="utf-8")
        for percent in (25, 100, 137, 200):
            settings.write_settings_props(False, percent)
            self.assertEqual(settings.read_settings_props(), {"selfCloningEnabled": False, "scalePercent": percent})
            text = self.path.read_text(encoding="utf-8")
            self.assertIn("# preferences\nother=value\n", text)
            self.assertEqual(text.count("scalePercent="), 1)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_invalid_saved_values_are_safe(self):
        for value, expected in (("0", 25), ("999", 200), ("bad", 100), ("75.5", 100)):
            self.path.write_text("scalePercent=" + value + "\n", encoding="utf-8")
            self.assertEqual(settings.read_settings_props()["scalePercent"], expected)

    def test_invalid_input_does_not_overwrite_settings(self):
        self.path.write_text("scalePercent=100\n", encoding="utf-8")
        for value in (24, 201, "bad"):
            with self.assertRaises(ValueError):
                settings.write_settings_props(True, value)
            self.assertEqual(self.path.read_text(encoding="utf-8"), "scalePercent=100\n")

    def test_ui_sync_and_save_validation(self):
        with patch.object(settings, "CURRENT_CHARACTER", str(self.path.parent / ".current_character")), \
             patch.object(settings, "WINDOW_CONF", str(self.path.parent / "window.conf")), \
             patch.object(settings, "TITLES_CONF", str(self.path.parent / "titles.conf")), \
             patch.object(settings.messagebox, "showinfo"), \
             patch.object(settings.messagebox, "showerror"):
            app = settings.App()
            app.withdraw()
            try:
                for percent in (25, 137, 200):
                    app.scale_var.set(str(percent))
                    self.assertEqual(app.scale_slider.get(), percent)
                    self.assertTrue(app.save())
                    self.assertEqual(settings.read_settings_props()["scalePercent"], percent)
                app.scale_slider.set(75.4)
                self.assertEqual(app.scale_var.get(), "75")
                previous = self.path.read_bytes()
                for value in ("24", "201", "", "no", "75.5"):
                    app.scale_var.set(value)
                    self.assertFalse(app.save())
                    self.assertEqual(self.path.read_bytes(), previous)
            finally:
                app.destroy()


if __name__ == "__main__":
    unittest.main()
