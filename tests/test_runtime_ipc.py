"""Check that lifecycle commands target only the same installation."""
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest


@unittest.skipUnless(importlib.util.find_spec("PySide6"), "Install requirements.txt for Qt lifecycle tests")
class RuntimeIpcTest(unittest.TestCase):
    def test_restart_add_and_quit_are_isolated_between_installations(self):
        from PySide6.QtCore import QCoreApplication
        from PySide6.QtNetwork import QLocalSocket
        app = QCoreApplication.instance() or QCoreApplication([])
        source = Path(__file__).resolve().parents[1]
        processes = []
        env = dict(os.environ, QT_QPA_PLATFORM="offscreen")
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        with tempfile.TemporaryDirectory() as temporary:
            roots = [Path(temporary) / name for name in ("first", "second")]
            try:
                for root in roots:
                    root.mkdir()
                    for name in ("shimeji.py", "shimeji_settings.py", "mascot_physics.py", "desktop_windows.py",
                                 "character_import.py", "character_formats.py", "character_webp.py", "character_frames.json"):
                        shutil.copy2(source / name, root / name)
                    shutil.copytree(source / "img", root / "img", ignore=shutil.ignore_patterns("*.jar"))
                    (root / "settings.properties").write_text("selfCloningEnabled=false\nscalePercent=100\n")
                    process = subprocess.Popen([sys.executable, str(root / "shimeji.py")], cwd=root,
                        env=env, creationflags=flags, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    processes.append(process)
                    identity = hashlib.sha256(os.fsencode(str(root.resolve()).casefold() if os.name == "nt" else str(root.resolve()))).hexdigest()[:24]
                    deadline = time.monotonic() + 20
                    while time.monotonic() < deadline:
                        if process.poll() is not None:
                            self.fail(process.communicate()[1].decode(errors="replace"))
                        socket = QLocalSocket()
                        socket.connectToServer("shimeji-" + identity)
                        if socket.waitForConnected(100):
                            socket.disconnectFromServer()
                            break
                        time.sleep(.05)
                    else:
                        self.fail("Runtime did not open its local socket")
                for args in (("--restart",), ()):
                    result = subprocess.run([sys.executable, str(roots[0] / "shimeji.py"), *args],
                        env=env, creationflags=flags, capture_output=True, timeout=20)
                    self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
                    self.assertIsNone(processes[0].poll())
                result = subprocess.run([sys.executable, str(roots[0] / "shimeji.py"), "--quit"],
                    env=env, creationflags=flags, capture_output=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
                self.assertEqual(processes[0].wait(timeout=10), 0)
                self.assertIsNone(processes[1].poll(), "Quitting one installation stopped another")
            finally:
                for root, process in zip(roots, processes):
                    if process.poll() is None:
                        subprocess.run([sys.executable, str(root / "shimeji.py"), "--quit"],
                            env=env, creationflags=flags, capture_output=True, timeout=20)
                        try:
                            process.wait(timeout=10)
                        except subprocess.TimeoutExpired:
                            process.terminate()  # Only this test's own child process.
                            process.wait(timeout=10)
                    output, error = process.communicate()
                    if process.returncode != 0:
                        self.fail(error.decode(errors="replace"))


if __name__ == '__main__':
    unittest.main()
