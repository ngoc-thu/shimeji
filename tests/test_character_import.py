import base64
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import character_import as importer
import shimeji_settings as settings

PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=')


class CharacterImportTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.characters = self.root / 'characters'
        self.archive = self.root / 'Download.zip'

    def tearDown(self):
        self.temp.cleanup()

    def make_zip(self, folders=('Package/img/Kinger',), missing=(), extra=(), invalid=False):
        with zipfile.ZipFile(self.archive, 'w') as archive:
            for folder in folders:
                for name in importer.FRAME_NAMES:
                    if name not in missing:
                        archive.writestr(f'{folder}/{name}', b'not png' if invalid else PNG)
            for name in extra:
                archive.writestr(name, b'ignored')

    def test_nested_zip_only_imports_required_sprites(self):
        self.make_zip(extra=('Package/Shimeji-ee.jar', 'Package/conf/actions.xml', 'Package/img/Kinger/shime47.png'))
        self.assertEqual(importer.import_characters(self.archive, self.characters), ['Kinger'])
        self.assertEqual(len(list((self.characters / 'Kinger').iterdir())), 46)
        self.assertEqual((self.characters / 'Kinger/shime1.png').read_bytes(), PNG)
        self.assertEqual(list(self.characters.iterdir()), [self.characters / 'Kinger'])

    def test_multiple_sets_and_name_collisions(self):
        self.make_zip(folders=('img/Ayaka', 'img/Miku'))
        self.assertEqual(importer.import_characters(self.archive, self.characters), ['Ayaka', 'Miku'])
        self.assertEqual(importer.import_characters(self.archive, self.characters), ['Ayaka (2)', 'Miku (2)'])
        self.assertEqual((self.characters / 'Ayaka/shime1.png').read_bytes(), PNG)

    def test_flat_zip_img_folder_and_folder_import(self):
        for folder, expected in (('', 'Download'), ('img', 'Download (2)'), ('Pack/img', 'Pack')):
            with self.subTest(folder=folder):
                with zipfile.ZipFile(self.archive, 'w') as archive:
                    for name in importer.FRAME_NAMES:
                        archive.writestr(f'{folder}/{name}' if folder else name, PNG)
                names = importer.import_characters(self.archive, self.characters)
                self.assertEqual(names, [expected])
                self.assertTrue(importer.is_character_directory(self.characters / names[0]))
        unpacked = self.root / 'Unpacked/img/Other'
        unpacked.mkdir(parents=True)
        for name in importer.FRAME_NAMES:
            (unpacked / name.upper()).write_bytes(PNG)
        self.assertEqual(importer.import_characters(self.root / 'Unpacked', self.characters), ['Other'])

    def test_invalid_incomplete_and_android_packages_leave_no_characters(self):
        for kwargs in ({'missing': ('shime46.png',)}, {'invalid': True}, {'folders': ()}):
            self.make_zip(**kwargs)
            with self.assertRaises(ValueError):
                importer.import_characters(self.archive, self.characters)
            self.assertFalse(self.characters.exists() and list(self.characters.iterdir()))

    def test_bad_second_set_does_not_install_first(self):
        self.make_zip(folders=('img/A',))
        with zipfile.ZipFile(self.archive, 'a') as archive:
            for name in importer.FRAME_NAMES:
                archive.writestr('img/B/' + name, b'bad')
        with self.assertRaises(ValueError):
            importer.import_characters(self.archive, self.characters)
        self.assertEqual(list(self.characters.iterdir()), [])

    def test_unsafe_paths_and_duplicate_frames_are_rejected(self):
        for path in ('../outside.txt', '/outside.txt', 'C:/outside.txt', r'..\outside.txt', 'Package/img/Kinger/SHIME1.PNG'):
            self.make_zip(extra=(path,))
            with self.assertRaises(ValueError):
                importer.import_characters(self.archive, self.characters)
            self.assertFalse(self.characters.exists() and list(self.characters.iterdir()))

    def test_import_limits(self):
        self.make_zip()
        for limit, value in (('MAX_ENTRIES', 3), ('MAX_FRAME_BYTES', 10), ('MAX_TOTAL_BYTES', 10)):
            with patch.object(importer, limit, value), self.assertRaises(ValueError):
                importer.import_characters(self.archive, self.characters)
            self.assertFalse(self.characters.exists() and list(self.characters.iterdir()))

    def test_invalid_dimensions_and_portable_names(self):
        large = PNG[:16] + (5000).to_bytes(4, 'big') + PNG[20:]
        with zipfile.ZipFile(self.archive, 'w') as archive:
            for name in importer.FRAME_NAMES:
                archive.writestr('img/Large/' + name, large)
        with self.assertRaises(ValueError):
            importer.import_characters(self.archive, self.characters)
        self.assertEqual(importer._safe_name('CON'), 'Shimeji')
        self.assertEqual(importer._safe_name('A:B'), 'A_B')
        self.make_zip(folders=('img/CON',))
        self.assertEqual(importer.import_characters(self.archive, self.characters), ['Shimeji'])

    def test_apply_imported_character_and_reject_incomplete_before_copying(self):
        self.make_zip()
        importer.import_characters(self.archive, self.characters)
        img = self.root / 'img'
        current = self.root / '.current_character'
        with patch.object(settings, 'CHARACTERS_DIR', str(self.characters)), \
             patch.object(settings, 'IMG_DIR', str(img)), patch.object(settings, 'CURRENT_CHARACTER', str(current)):
            self.assertEqual(settings.list_characters(), ['Kinger'])
            settings.apply_character('Kinger')
            self.assertEqual(current.read_text(), 'Kinger\n')
            self.assertEqual(len(list(img.iterdir())), 46)
            (self.characters / 'Kinger/shime46.png').unlink()
            (img / 'shime1.png').write_bytes(b'previous')
            with self.assertRaises(ValueError):
                settings.apply_character('Kinger')
            self.assertEqual((img / 'shime1.png').read_bytes(), b'previous')

    def test_ui_import_selects_character_without_changing_active_images(self):
        self.make_zip()
        with patch.object(settings, 'CHARACTERS_DIR', str(self.characters)), \
             patch.object(settings.messagebox, 'showinfo'), patch.object(settings.messagebox, 'showerror') as error:
            app = settings.App()
            app.withdraw()
            try:
                app.import_package(self.archive)
                self.assertEqual(app.selected_characters(), ['Kinger'])
                self.assertIn('Kinger', app.character_vars)
                error.assert_not_called()
            finally:
                app.destroy()


if __name__ == '__main__':
    unittest.main()
