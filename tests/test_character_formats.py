"""Regression cases based on the structures of the DDLC and Megumin example ZIPs."""
import base64
import json
import os
import struct
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import character_formats
import character_import
import character_webp

PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=')
WEBP = (Path(__file__).parent / 'fixtures/pixel.webp').read_bytes()


def xml_actions(image='/stand.png'):
    return ('<Mascot xmlns="http://www.group-finity.com/Mascot"><ActionList>' + ''.join(
        '<Action Name="' + action + '"><Animation>' + ''.join('<Pose Image="' + name + '"/>' for name in names) +
        '</Animation></Action>' for action, names in (
            ('Stand', [image]), ('Walk', ['/stand.png', '/walk1.png', '/walk2.png']),
            ('Falling', ['/air.png']), ('GrabWall', ['/climb.png']), ('ClimbWall', ['/climb.png']),
            ('GrabCeiling', ['/ceiling.png']), ('ClimbCeiling', ['/ceiling.png']))) + '</ActionList></Mascot>')


def mobile_metadata():
    return ({'schemaVersion': 1, 'name': 'Megumin',
             'animationSchema': {'path': 'animation.json', 'schemaId': 'legacy_default_v1', 'version': 1},
             'sprites': {'type': 'SEQUENCE', 'basePath': 'sprites/', 'filePattern': '%04d.webp', 'spriteCount': 1}},
            {'schema_id': 'legacy_default_v1', 'version': 1, 'animations': [
                {'key': key, 'frames': [{'sprite': 0}]} for key in ('stand_left', 'walk_left', 'fall')]})


class CharacterFormatsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.zip = self.root / 'input.zip'
        self.characters = self.root / 'characters'

    def tearDown(self):
        self.temp.cleanup()

    def named_package(self, image='/stand.png', xml=None):
        with zipfile.ZipFile(self.zip, 'w') as archive:
            for character in ('Monika', 'Natsuki', 'Sayori', 'Yuri'):
                for number, name in enumerate(('stand', 'walk1', 'walk2', 'air', 'climb', 'ceiling')):
                    archive.writestr(f'img/{character}/{name}.png', PNG + bytes([number]))
                archive.writestr(f'img/{character}/conf/actions.xml', xml or xml_actions(image))
            archive.writestr('Shimeji-ee.jar', b'ignored')

    def mobile_package(self, manifest=None, animation=None, sprite=WEBP):
        default_manifest, default_animation = mobile_metadata()
        with zipfile.ZipFile(self.zip, 'w') as archive:
            archive.writestr('manifest.json', json.dumps(manifest or default_manifest))
            archive.writestr('animation.json', json.dumps(animation or default_animation))
            if sprite is not None:
                archive.writestr('sprites/0000.webp', sprite)

    def assert_rejected(self):
        with self.assertRaises(ValueError):
            character_import.import_characters(self.zip, self.characters)
        self.assertFalse(self.characters.exists() and list(self.characters.iterdir()))

    def test_named_xml_pack_maps_actions_to_standard_frames(self):
        self.named_package()
        self.assertEqual(character_import.import_characters(self.zip, self.characters), ['Monika', 'Natsuki', 'Sayori', 'Yuri'])
        for name in ('Monika', 'Natsuki', 'Sayori', 'Yuri'):
            figure = self.characters / name
            self.assertTrue(character_import.is_character_directory(figure))
            for frame, image in ((1, 0), (2, 1), (3, 2), (4, 3), (13, 4), (23, 5), (42, 0)):
                self.assertEqual((figure / f'shime{frame}.png').read_bytes(), PNG + bytes([image]))
            self.assertEqual(len(list(figure.iterdir())), 46)

    def test_named_xml_folder_import(self):
        self.named_package()
        with zipfile.ZipFile(self.zip) as archive:
            archive.extractall(self.root / 'unpacked')  # Only the synthetic fixture generated above.
        names = character_import.import_characters(self.root / 'unpacked', self.characters)
        self.assertEqual(names, ['Monika', 'Natsuki', 'Sayori', 'Yuri'])

    def test_named_xml_missing_and_unsafe_references(self):
        for image in ('/missing.png', '/../outside.png', 'https://example.invalid/image.png'):
            with self.subTest(image=image):
                self.named_package(image)
                self.assert_rejected()

    def test_xml_dtds_are_rejected(self):
        self.named_package(xml='<!DOCTYPE Mascot [<!ENTITY file SYSTEM "file:///private">]><Mascot/>')
        self.assert_rejected()

    def test_json_webp_bundle_is_converted_once_and_resized(self):
        self.mobile_package()
        with patch.object(character_webp.subprocess, 'run', wraps=character_webp.subprocess.run) as decoder:
            self.assertEqual(character_import.import_characters(self.zip, self.characters), ['Megumin'])
            self.assertEqual(decoder.call_count, 1)
        figure = self.characters / 'Megumin'
        self.assertEqual(len(list(figure.iterdir())), 46)
        png = (figure / 'shime1.png').read_bytes()
        self.assertEqual(png[:8], b'\x89PNG\r\n\x1a\n')
        self.assertEqual(struct.unpack('>II', png[16:24]), (128, 128))
        self.assertEqual((figure / 'shime46.png').read_bytes(), png)

    def test_json_unknown_schema_and_missing_sprites_are_rejected(self):
        manifest, animation = mobile_metadata()
        manifest['animationSchema']['schemaId'] = 'unknown'
        self.mobile_package(manifest=manifest)
        self.assert_rejected()
        self.mobile_package(sprite=None)
        self.assert_rejected()
        animation['animations'][0]['frames'][0]['sprite'] = 99
        self.mobile_package(animation=animation)
        self.assert_rejected()

    def test_json_paths_do_not_escape_package(self):
        for field in ('path', 'basePath', 'filePattern'):
            manifest, _ = mobile_metadata()
            manifest['animationSchema' if field == 'path' else 'sprites'][field] = '../outside'
            self.mobile_package(manifest=manifest)
            self.assert_rejected()

    def test_invalid_webp_and_oversized_metadata_leave_no_figures(self):
        self.mobile_package(sprite=b'RIFF-not-a-webp')
        self.assert_rejected()
        self.named_package()
        with patch.object(character_formats, 'MAX_METADATA_BYTES', 10):
            self.assert_rejected()


@unittest.skipUnless(os.environ.get('SHIMEJI_SAMPLE_DIR'), 'Set SHIMEJI_SAMPLE_DIR for the original example ZIPs')
class OriginalExampleTest(unittest.TestCase):
    def test_original_examples(self):
        for filename, expected in (('0fxxyxhc.zip', ['Monika', 'Natsuki', 'Sayori', 'Yuri']),
                                   ('7rkbhgkk.zip', ['Megumin'])):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as target:
                names = character_import.import_characters(Path(os.environ['SHIMEJI_SAMPLE_DIR']) / filename, target)
                self.assertEqual(names, expected)
                self.assertTrue(all(character_import.is_character_directory(Path(target) / n) for n in names))


if __name__ == '__main__':
    unittest.main()
