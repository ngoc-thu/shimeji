from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import shimeji_settings as settings


class CharacterSelectionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.current = self.root / ".current_character"
        self.characters = self.root / "characters"
        for name in ("Ayaka", "Miku", "Megumin"):
            directory = self.characters / name
            directory.mkdir(parents=True)
            for number in range(1, 47):
                (directory / f"shime{number}.png").write_bytes(b"fixture")
        for attribute, path in (("CHARACTERS_DIR", self.characters), ("CURRENT_CHARACTER", self.current),
                                ("SETTINGS_PROPS", self.root / "settings.properties"),
                                ("WINDOW_CONF", self.root / "window.conf"), ("TITLES_CONF", self.root / "titles.conf")):
            patcher = patch.object(settings, attribute, str(path))
            patcher.start()
            self.addCleanup(patcher.stop)

    def editor(self):
        app = settings.App()
        app.withdraw()
        self.addCleanup(app.destroy)
        return app

    def test_legacy_selection_round_trip_and_removed_characters(self):
        self.current.write_text("Miku\n", encoding="utf-8")
        self.assertEqual(settings.detect_current_characters(), ["Miku"])
        settings.set_current_characters(["Miku", "Ayaka", "Miku"])
        self.assertEqual(self.current.read_text(encoding="utf-8"), "Miku\nAyaka\n")
        self.assertEqual(settings.detect_current_characters(), ["Miku", "Ayaka"])
        (self.characters / "Miku" / "shime46.png").unlink()
        self.assertEqual(settings.detect_current_characters(), ["Ayaka"])
        self.current.write_text("Missing\n../outside\n", encoding="utf-8")
        self.assertEqual(settings.detect_current_characters(), ["Ayaka"])

    def test_invalid_selection_preserves_saved_selection(self):
        settings.set_current_characters(["Miku"])
        for names in ([], ["Missing"], ["../outside"], ["Ayaka", "Missing"],
                      [str(number) for number in range(51)]):
            with self.assertRaises(ValueError):
                settings.set_current_characters(names)
            self.assertEqual(self.current.read_text(encoding="utf-8"), "Miku\n")
        with patch.object(settings.os, "replace", side_effect=OSError("unavailable")):
            with self.assertRaises(OSError):
                settings.set_current_characters(["Ayaka"])
        self.assertEqual(set(self.root.iterdir()), {self.characters, self.current})

    def test_ui_saves_and_restores_multiple_checks_and_starts_once(self):
        app = self.editor()
        for checkbox in app.character_list.winfo_children():
            if checkbox.cget("text") == "Miku":
                checkbox.invoke()
        self.assertEqual(app.selected_characters(), ["Ayaka", "Miku"])
        with patch.object(settings.messagebox, "showinfo"), patch.object(settings.messagebox, "showerror") as error:
            self.assertTrue(app.save())
            app.character_vars["Ayaka"].set(False)
            app.load_values()
            self.assertEqual(app.selected_characters(), ["Ayaka", "Miku"])
            with patch.object(settings, "restart_shimeji") as restart:
                app.apply_all()
                restart.assert_called_once_with()
            self.assertEqual(settings.detect_current_characters(), ["Ayaka", "Miku"])
            error.assert_not_called()

    def test_empty_selection_does_not_save_or_restart(self):
        settings.set_current_characters(["Miku"])
        app = self.editor()
        app.character_vars["Miku"].set(False)
        with patch.object(settings.messagebox, "showerror") as error, \
             patch.object(settings, "restart_shimeji") as restart:
            self.assertFalse(app.save())
            app.apply_selection()
            restart.assert_not_called()
            self.assertEqual(error.call_count, 2)
        self.assertEqual(settings.detect_current_characters(), ["Miku"])
        self.assertFalse((self.root / "settings.properties").exists())

    def test_import_adds_checks_and_website_opens_browser(self):
        app = self.editor()
        with patch.object(settings, "import_characters", return_value=["Miku", "Megumin"]), \
             patch.object(settings.messagebox, "showinfo"), patch.object(settings.messagebox, "showerror") as error:
            app.import_package("download.zip")
            self.assertEqual(app.selected_characters(), ["Ayaka", "Megumin", "Miku"])
            self.assertFalse(self.current.exists())
            error.assert_not_called()
        with patch.object(settings.webbrowser, "open") as browser:
            app.open_character_site()
            browser.assert_called_once_with("https://shimeji.org/")

    def test_empty_library_is_explained_and_no_selection_is_saved(self):
        with patch.object(settings, "CHARACTERS_DIR", str(self.root / "empty")):
            self.assertEqual(settings.detect_current_characters(), [])
            app = self.editor()
            self.assertEqual(app.selected_characters(), [])
            self.assertIn("No characters installed", app.character_list.winfo_children()[0].cget("text"))


if __name__ == "__main__":
    unittest.main()
