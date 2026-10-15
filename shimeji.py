#!/usr/bin/env python3
"""Python/Qt desktop mascots. Run with --settings for the Tk settings editor."""
import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import time

APP_ROOT = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent


def main(argv=None):
    parser = argparse.ArgumentParser(description="Java-free desktop mascots for Windows and Linux.")
    parser.add_argument("--settings", action="store_true", help="Open the settings editor")
    parser.add_argument("--restart", action="store_true", help="Reload this installation's running mascots")
    parser.add_argument("--quit", action="store_true", help="Stop this installation's running mascots")
    parser.add_argument("--smoke-test", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    os.chdir(APP_ROOT)
    if args.settings or (getattr(sys, "frozen", False) and Path(sys.executable).stem == "ShimejiSettings"):
        import shimeji_settings
        if args.smoke_test:
            editor = shimeji_settings.App()
            editor.withdraw()
            try:
                editor.update()
                assert editor.title() == "Shimeji Settings"
                assert editor.character_vars
                print("Settings smoke test: character discovery and English Python UI passed.")
            finally:
                editor.destroy()
        elif shimeji_settings.acquire_single_instance_lock():
            shimeji_settings.App().mainloop()
        return 0
    try:
        return run_mascots(args)
    except ImportError as error:
        message = "Shimeji requires Qt for Python. Run: python -m pip install -r requirements.txt"
        if os.name == "nt":
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, message + "\n\n" + str(error), "Shimeji", 0x10)
        else:
            print(message + "\n" + str(error), file=sys.stderr)
        return 1


def run_mascots(args):
    from PySide6.QtCore import QLockFile, QPoint, QRect, QStandardPaths, Qt, QTimer, QUrl
    from PySide6.QtGui import QCursor, QDesktopServices, QIcon, QImage, QPainter, QPixmap, QRegion
    from PySide6.QtNetwork import QLocalServer, QLocalSocket
    from PySide6.QtWidgets import QApplication, QMenu, QMessageBox, QSystemTrayIcon, QWidget
    from desktop_windows import DesktopWindows
    from mascot_physics import Mascot, Rect
    from shimeji_settings import detect_current_characters, read_settings_props, read_titles_conf, read_window_conf

    app = QApplication([sys.argv[0]])
    app.setApplicationName("Shimeji")
    app.setQuitOnLastWindowClosed(False)
    identity = hashlib.sha256(os.fsencode(str(APP_ROOT).casefold() if os.name == "nt" else str(APP_ROOT))).hexdigest()[:24]
    server_name = "shimeji-" + identity
    if args.smoke_test:
        server_name += "-smoke-" + str(os.getpid())
    # QLockFile closes the race between first launch and the local server listening.
    lock = QLockFile(str(Path(QStandardPaths.writableLocation(QStandardPaths.TempLocation)) / (server_name + ".lock")))
    if not lock.tryLock(0):
        client = QLocalSocket()
        client.connectToServer(server_name)
        if not client.waitForConnected(3000):
            raise RuntimeError("Shimeji is starting or is not responding. Please try again.")
        command = "quit" if args.quit else "restart" if args.restart else "add"
        client.write((command + "\n").encode())
        client.flush()
        client.waitForBytesWritten(1000)
        client.disconnectFromServer()
        return 0
    if args.quit:
        return 0
    server = QLocalServer()
    server.setSocketOptions(QLocalServer.UserAccessOption)
    QLocalServer.removeServer(server_name)
    if not server.listen(server_name):
        raise RuntimeError(server.errorString())

    class Sprite(QWidget):
        def __init__(self, manager, x, y, character):
            super().__init__(None, Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus)
            self.manager = manager
            self.character = character
            self.model = Mascot(x, y)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setAttribute(Qt.WA_ShowWithoutActivating)
            self.setWindowTitle("Shimeji mascot" + (": " + character if character else ""))
            self.drag_offset = None
            self.drag_sample = None
            self.velocity = (0, 0)
            self.last_image_key = None
            self.draw()
            self.show()

        def draw(self):
            key = (self.character, self.model.frame, self.model.direction > 0, self.manager.scale)
            image = self.manager.pixmap(*key)
            self.image = image
            if key != self.last_image_key:
                self.resize(image.size())
                # Transparent areas must not intercept clicks intended for other apps.
                self.setMask(QRegion(image.mask()))
                self.last_image_key = key
            scale = self.manager.scale / 100
            anchor_y = 48 if self.model.state == "ceiling" else 128
            self.move(round(self.model.x - 64 * scale), round(self.model.y - anchor_y * scale))
            self.update()

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.image)

        def mousePressEvent(self, event):
            if event.button() == Qt.LeftButton:
                pos = event.globalPosition()
                self.drag_offset = (self.model.x - pos.x(), self.model.y - pos.y())
                self.model.state = "drag"
                self.drag_sample = (pos.x(), pos.y(), time.monotonic())
                self.velocity = (0, 0)
                event.accept()

        def mouseMoveEvent(self, event):
            if self.drag_offset is None:
                return
            pos, now = event.globalPosition(), time.monotonic()
            x, y, previous = self.drag_sample
            dt = max(.001, now - previous)
            self.velocity = ((pos.x() - x) / dt, (pos.y() - y) / dt)
            self.drag_sample = (pos.x(), pos.y(), now)
            self.model.x = pos.x() + self.drag_offset[0]
            self.model.y = pos.y() + self.drag_offset[1]
            self.draw()

        def mouseReleaseEvent(self, event):
            if event.button() == Qt.LeftButton and self.drag_offset is not None:
                velocity = self.velocity if time.monotonic() - self.drag_sample[2] < .15 else (0, 0)
                self.drag_offset = None
                self.model.release(*velocity)

        def contextMenuEvent(self, event):
            menu = self.manager.menu(self)
            menu.exec(event.globalPos())

    class Manager:
        def __init__(self):
            self.sprites = []
            self.images = {}
            self.cache = {}
            self.scale = 100
            self.clone_enabled = True
            self.window = None
            self.desktop = DesktopWindows()
            self.previous_tick = time.monotonic()
            self.last_clone = self.previous_tick
            self.reload()
            self.tray = QSystemTrayIcon(QIcon(str(APP_ROOT / "shimeji.ico")), app)
            self.tray.setToolTip("Shimeji")
            self.tray.setContextMenu(self.menu())
            self.tray.activated.connect(lambda reason: self.add() if reason == QSystemTrayIcon.DoubleClick else None)
            if QSystemTrayIcon.isSystemTrayAvailable():
                self.tray.show()
            self.timer = QTimer()
            self.timer.timeout.connect(self.safe_tick)
            self.timer.start(20)
            self.preferences_timer = QTimer()
            self.preferences_timer.timeout.connect(self.safe_preferences)
            self.preferences_timer.start(500)
            self.windows_timer = QTimer()
            self.windows_timer.timeout.connect(self.refresh_window)
            self.windows_timer.start(250)

        def reload(self):
            images = {}
            # Load all sets before replacing the current sprites, so a failed reload
            # leaves the running characters intact. Old installations can use img/.
            for character in detect_current_characters() or [""]:
                directory = APP_ROOT / "characters" / character if character else APP_ROOT / "img"
                frames = {}
                for number in range(1, 47):
                    path = directory / f"shime{number}.png"
                    image = QImage(str(path))
                    if image.isNull():
                        raise ValueError(f"Cannot load {path}. Import a complete character in Settings first.")
                    frames[number] = image
                images[character] = frames
            self.preferences()
            for sprite in self.sprites:
                sprite.close()
                sprite.deleteLater()
            self.sprites.clear()
            self.images = images
            self.characters = list(images)
            self.next_character = 0
            self.cache.clear()
            self.last_clone = time.monotonic()
            for character in self.characters:
                self.add(character=character)

        def preferences(self):
            props = read_settings_props()
            scale = props["scalePercent"]
            if self.scale != scale:
                self.cache.clear()
            self.scale = scale
            self.clone_enabled = props["selfCloningEnabled"]
            self.titles = [line.strip() for line in read_titles_conf().splitlines() if line.strip()]
            try:
                self.offsets = tuple(map(int, read_window_conf()))
            except ValueError:
                self.offsets = (0, 0, 0, 0)

        def safe_preferences(self):
            try:
                self.preferences()
            except OSError:
                pass  # Keep the last preferences while a network folder is unavailable.

        def refresh_window(self):
            self.window = self.desktop.foreground(app.screens(), self.titles, self.offsets,
                {int(sprite.winId()) for sprite in self.sprites})

        def pixmap(self, character, frame, right, percent):
            key = (character, frame, right, percent)
            if key not in self.cache:
                original = self.images[character][frame]
                if right:
                    original = original.mirrored(True, False)
                self.cache[key] = QPixmap.fromImage(original.scaled(
                    max(1, round(original.width() * percent / 100)),
                    max(1, round(original.height() * percent / 100)),
                    Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            return self.cache[key]

        def add(self, x=None, y=None, character=None):
            if len(self.sprites) >= 50:
                return
            if character is None:
                character = self.characters[self.next_character % len(self.characters)]
                self.next_character += 1
            screen = app.screenAt(QCursor.pos()) or app.primaryScreen()
            area = screen.availableGeometry()
            if x is None:
                import random
                x = random.uniform(area.left() + area.width() * .25, area.left() + area.width() * .75)
            if y is None:
                y = area.top() + 128 * self.scale / 100
            sprite = Sprite(self, x, y, character)
            self.sprites.append(sprite)
            return sprite

        def clone(self, parent):
            return self.add(parent.model.x, parent.model.y - 20, character=parent.character)

        def safe_tick(self):
            try:
                self.tick()
            except Exception as error:
                self.timer.stop()
                QMessageBox.critical(None, "Shimeji stopped", str(error))
                app.exit(1)

        def tick(self):
            now = time.monotonic()
            dt, self.previous_tick = now - self.previous_tick, now
            for sprite in list(self.sprites):
                model = sprite.model
                point = QPoint(round(model.x), round(model.y - 1))
                screen = app.screenAt(point) or app.primaryScreen()
                geo = screen.availableGeometry()
                area = Rect(geo.left(), geo.top(), geo.left() + geo.width(), geo.top() + geo.height())
                model.step(dt, area, self.window, self.scale / 100)
                sprite.draw()
            # Automatic cloning is deliberately bounded, like the old maxCount.
            if self.clone_enabled and self.sprites and now - self.last_clone >= 30:
                self.last_clone = now
                parent = next((s for s in self.sprites if s.model.state not in ("drag", "fall", "climb", "ceiling")), None)
                if parent:
                    self.clone(parent)

        def remove(self, sprite):
            self.sprites.remove(sprite)
            sprite.close()
            sprite.deleteLater()
            if not self.sprites and not self.tray.isVisible():
                app.quit()

        def keep_one(self):
            for sprite in list(self.sprites[1:]):
                self.remove(sprite)

        def gather(self):
            cursor = QCursor.pos()
            for index, sprite in enumerate(self.sprites):
                sprite.model.x = cursor.x() + (index % 5 - 2) * 40
                sprite.model.y = cursor.y() - (index // 5) * 40
                sprite.model.release()

        def settings(self):
            if getattr(sys, "frozen", False):
                command = [sys.executable, "--settings"]
            else:
                command = [sys.executable, str(APP_ROOT / "shimeji.py"), "--settings"]
            subprocess.Popen(command, cwd=APP_ROOT,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)

        def open_path(self, path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

        def reset_offsets(self):
            from shimeji_settings import write_window_conf
            write_window_conf(["0"] * 4)
            self.preferences()

        def menu(self, sprite=None):
            menu = QMenu()
            if sprite:
                menu.addAction("Remove this mascot", lambda: self.remove(sprite))
                menu.addSeparator()
            menu.addAction("Add mascot", lambda: self.add(character=sprite.character if sprite else None))
            menu.addAction("Gather at cursor", self.gather)
            menu.addAction("Keep one mascot", self.keep_one)
            menu.addSeparator()
            menu.addAction("Settings…", self.settings)
            menu.addAction("Open window.conf", lambda: self.open_path(APP_ROOT / "window.conf"))
            menu.addAction("Open titles.conf", lambda: self.open_path(APP_ROOT / "titles.conf"))
            menu.addAction("Open application folder", lambda: self.open_path(APP_ROOT))
            menu.addAction("Reset window.conf", self.reset_offsets)
            menu.addSeparator()
            menu.addAction("Quit Shimeji", app.quit)
            return menu

    try:
        manager = Manager()
    except Exception as error:
        if args.smoke_test:
            raise
        QMessageBox.critical(None, "Shimeji could not start", str(error))
        return 1
    clients = set()

    def accept():
        while server.hasPendingConnections():
            client = server.nextPendingConnection()
            clients.add(client)
            client.setProperty("buffer", b"")

            def receive(client=client):
                data = client.property("buffer") + bytes(client.readAll())
                if len(data) > 64:
                    client.disconnectFromServer()
                    return
                if b"\n" not in data:
                    client.setProperty("buffer", data)
                    return
                command = data.split(b"\n", 1)[0]
                try:
                    if command == b"quit":
                        app.quit()
                    elif command == b"restart":
                        manager.reload()
                    elif command == b"add":
                        manager.add()
                except Exception as error:
                    QMessageBox.critical(None, "Shimeji", str(error))
                client.disconnectFromServer()

            client.readyRead.connect(receive)
            client.disconnected.connect(lambda client=client: (clients.discard(client), client.deleteLater()))
            QTimer.singleShot(3000, client.disconnectFromServer)
            if client.bytesAvailable():
                receive()

    server.newConnection.connect(accept)
    if args.smoke_test:
        # Exercise all selected image sets, cloning, restart and per-character caches.
        def smoke():
            try:
                assert [sprite.character for sprite in manager.sprites] == manager.characters
                for sprite in list(manager.sprites):
                    for percent in (25, 100, 137, 200):
                        manager.scale = percent
                        for right in (False, True):
                            sprite.model.direction = 1 if right else -1
                            for state in ("stand", "walk", "drag", "fall", "climb", "ceiling", "spin"):
                                sprite.model.state = state
                                sprite.draw()
                                original = manager.images[sprite.character][sprite.model.frame]
                                expected = original.mirrored(True, False) if right else original
                                expected = expected.scaled(
                                    max(1, round(original.width() * percent / 100)),
                                    max(1, round(original.height() * percent / 100)),
                                    Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                                assert sprite.image.toImage() == QPixmap.fromImage(expected).toImage()
                    if len(manager.sprites) < 50:
                        clone = manager.clone(sprite)
                        assert clone.character == sprite.character
                manager.reload()
                for character in manager.characters:
                    if len(manager.sprites) < 50:
                        assert manager.add().character == character
                manager.refresh_window()
                manager.keep_one()
                print("Qt smoke test: PNG loading, poses, scaling, menus, desktop query and "
                      f"{len(manager.characters)} independent character sets passed.")
            except Exception:
                import traceback
                traceback.print_exc()
                app.exit(1)
            else:
                app.quit()
        QTimer.singleShot(100, smoke)
    try:
        return app.exec()
    finally:
        manager.desktop.close()
        server.close()
        lock.unlock()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        if os.name == "nt" and "--smoke-test" not in sys.argv:
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, str(error), "Shimeji", 0x10)
        else:
            raise
