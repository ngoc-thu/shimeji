"""Read the external foreground window through Win32 or X11, without Java/JNA."""
import ctypes
import ctypes.util
import os
from mascot_physics import Rect


class DesktopWindows:
    def __init__(self):
        self.last = None
        self.last_handle = None
        self.diagnostic = ""
        self.display = None
        if os.name == "nt":
            from ctypes import wintypes as w
            self.w = w
            self.user = ctypes.WinDLL("user32", use_last_error=True)
            self.user.GetForegroundWindow.restype = w.HWND
            self.user.GetWindowRect.argtypes = [w.HWND, ctypes.POINTER(w.RECT)]
            self.user.GetWindowThreadProcessId.argtypes = [w.HWND, ctypes.POINTER(w.DWORD)]
            self.user.GetWindowTextLengthW.argtypes = [w.HWND]
            self.user.GetWindowTextW.argtypes = [w.HWND, w.LPWSTR, ctypes.c_int]
            self.user.IsIconic.argtypes = [w.HWND]
            self.user.IsWindowVisible.argtypes = [w.HWND]
            self.user.GetClassNameW.argtypes = [w.HWND, w.LPWSTR, ctypes.c_int]
        elif os.environ.get("DISPLAY"):
            try:
                self.x = ctypes.CDLL(ctypes.util.find_library("X11") or "libX11.so.6")
                self.x.XOpenDisplay.argtypes = [ctypes.c_char_p]
                self.x.XOpenDisplay.restype = ctypes.c_void_p
                self.x.XDefaultRootWindow.argtypes = [ctypes.c_void_p]
                self.x.XDefaultRootWindow.restype = ctypes.c_ulong
                self.x.XInternAtom.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
                self.x.XInternAtom.restype = ctypes.c_ulong
                self.x.XGetWindowProperty.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong,
                    ctypes.c_long, ctypes.c_long, ctypes.c_int, ctypes.c_ulong,
                    ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong),
                    ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte))]
                self.x.XFree.argtypes = [ctypes.c_void_p]
                self.x.XGetGeometry.argtypes = [ctypes.c_void_p, ctypes.c_ulong,
                    ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_uint),
                    ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint),
                    ctypes.POINTER(ctypes.c_uint)]
                self.x.XTranslateCoordinates.argtypes = [ctypes.c_void_p, ctypes.c_ulong,
                    ctypes.c_ulong, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_ulong)]
                self.x.XCloseDisplay.argtypes = [ctypes.c_void_p]
                self.error_callback = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)(lambda *_: 0)
                self.x.XSetErrorHandler.argtypes = [type(self.error_callback)]
                self.x.XSetErrorHandler(self.error_callback)
                self.display = self.x.XOpenDisplay(None)
                if self.display:
                    self.root = self.x.XDefaultRootWindow(self.display)
            except (OSError, AttributeError) as error:
                self.diagnostic = str(error)
        else:
            self.diagnostic = "Window interaction requires an X11 session."

    def property(self, window, name):
        atom = self.x.XInternAtom(self.display, name.encode(), 1)
        if not atom:
            return None
        actual, fmt, count, rest = ctypes.c_ulong(), ctypes.c_int(), ctypes.c_ulong(), ctypes.c_ulong()
        data = ctypes.POINTER(ctypes.c_ubyte)()
        status = self.x.XGetWindowProperty(self.display, window, atom, 0, 4096, 0, 0,
            ctypes.byref(actual), ctypes.byref(fmt), ctypes.byref(count), ctypes.byref(rest), ctypes.byref(data))
        try:
            if status or not data:
                return None
            if fmt.value == 32:
                return list(ctypes.cast(data, ctypes.POINTER(ctypes.c_ulong))[:count.value])
            if fmt.value == 8:
                return ctypes.string_at(data, count.value).decode("utf-8", "replace")
        finally:
            if data:
                self.x.XFree(data)

    def foreground(self, screens, titles=(), offsets=(0, 0, 0, 0), own_ids=()):
        if os.name == "nt":
            w = self.w
            hwnd = self.user.GetForegroundWindow()
            if not hwnd:
                return None
            pid = w.DWORD()
            self.user.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if pid.value == os.getpid() or int(hwnd) in own_ids:
                hwnd = self.last_handle
                if not hwnd or not self.user.IsWindowVisible(hwnd):
                    return None
            if self.user.IsIconic(hwnd):
                return None
            window_class = ctypes.create_unicode_buffer(256)
            self.user.GetClassNameW(hwnd, window_class, len(window_class))
            if window_class.value in {"Progman", "WorkerW", "Shell_TrayWnd", "Shell_SecondaryTrayWnd"}:
                self.last_handle = None
                self.last = None
                return None
            title = ctypes.create_unicode_buffer(self.user.GetWindowTextLengthW(hwnd) + 1)
            self.user.GetWindowTextW(hwnd, title, len(title))
            bounds = w.RECT()
            if not self.user.GetWindowRect(hwnd, ctypes.byref(bounds)):
                return None
            # Qt uses logical coordinates; Win32 reports physical coordinates.
            # Match the monitor by its Win32 device name before converting.
            self.user.MonitorFromWindow.argtypes = [w.HWND, w.DWORD]
            self.user.MonitorFromWindow.restype = w.HANDLE
            class MonitorInfo(ctypes.Structure):
                _fields_ = [("size", w.DWORD), ("monitor", w.RECT), ("work", w.RECT),
                            ("flags", w.DWORD), ("device", w.WCHAR * 32)]
            info = MonitorInfo()
            info.size = ctypes.sizeof(info)
            self.user.GetMonitorInfoW.argtypes = [w.HANDLE, ctypes.POINTER(MonitorInfo)]
            self.user.GetMonitorInfoW(self.user.MonitorFromWindow(hwnd, 2), ctypes.byref(info))
            screen = next((s for s in screens if s.name() == info.device), screens[0])
            ratio, geo = screen.devicePixelRatio(), screen.geometry()
            rect = Rect(geo.left() + (bounds.left - info.monitor.left) / ratio,
                        geo.top() + (bounds.top - info.monitor.top) / ratio,
                        geo.left() + (bounds.right - info.monitor.left) / ratio,
                        geo.top() + (bounds.bottom - info.monitor.top) / ratio)
            label = title.value
        elif self.display:
            active = self.property(self.root, "_NET_ACTIVE_WINDOW")
            if not active or not active[0]:
                self.last = None
                return None
            hwnd = active[0]
            pid = self.property(hwnd, "_NET_WM_PID")
            if hwnd in own_ids or pid == [os.getpid()]:
                hwnd = self.last_handle
                if not hwnd:
                    return None
            root, child = ctypes.c_ulong(), ctypes.c_ulong()
            x, y = ctypes.c_int(), ctypes.c_int()
            width, height, border, depth = (ctypes.c_uint() for _ in range(4))
            if not self.x.XGetGeometry(self.display, hwnd, ctypes.byref(root), ctypes.byref(x),
                    ctypes.byref(y), ctypes.byref(width), ctypes.byref(height), ctypes.byref(border), ctypes.byref(depth)):
                return None
            self.x.XTranslateCoordinates(self.display, hwnd, self.root, 0, 0,
                ctypes.byref(x), ctypes.byref(y), ctypes.byref(child))
            extents = self.property(hwnd, "_NET_FRAME_EXTENTS") or [0, 0, 0, 0]
            ratio = screens[0].devicePixelRatio()
            rect = Rect((x.value - extents[0]) / ratio, (y.value - extents[2]) / ratio,
                        (x.value + width.value + extents[1]) / ratio,
                        (y.value + height.value + extents[3]) / ratio)
            label = self.property(hwnd, "_NET_WM_NAME") or self.property(hwnd, "WM_NAME") or ""
        else:
            return None
        if not label or (titles and not any(t.casefold() in label.casefold() for t in titles)):
            self.last = None
            return None
        dx, dy, dw, dh = offsets
        self.last_handle = int(hwnd)
        self.last = Rect(rect.left + dx, rect.top + dy, rect.right + dx + dw, rect.bottom + dy + dh, int(hwnd))
        return self.last

    def close(self):
        if self.display:
            self.x.XCloseDisplay(self.display)
            self.display = None
