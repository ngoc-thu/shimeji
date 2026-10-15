"""Desktop mascot movement in logical screen pixels; no GUI dependencies."""
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Rect:
    left: float
    top: float
    right: float
    bottom: float
    window_id: int = 0

    def contains_x(self, x):
        return self.left <= x <= self.right


class Mascot:
    def __init__(self, x, y, rng=None):
        self.x, self.y = x, y  # Feet, or hands while hanging from a ceiling.
        self.vx = self.vy = 0.0
        self.direction = -1
        self.state = "fall"
        self.elapsed = 0.0
        self.remaining = 0.0
        self.rng = rng or random.Random()
        self.previous_window = None
        self.wall = None

    def choose(self):
        self.state = self.rng.choices(
            ["stand", "walk", "run", "sit", "sprawl", "creep", "spin"],
            [2, 5, 2, 3, 1, 1, 1])[0]
        self.remaining = self.rng.uniform(2, 7)
        self.elapsed = 0
        if self.rng.random() < .3:
            self.direction *= -1

    def release(self, vx=0, vy=0):
        self.state = "fall"
        self.vx, self.vy = max(-900, min(900, vx)), max(-900, min(900, vy))
        self.elapsed = 0
        self.wall = None

    def step(self, dt, area, window=None, scale=1.0):
        dt = max(0, min(.05, dt))
        self.elapsed += dt
        if self.state == "drag":
            self.previous_window = window
            return
        # Follow a moving window while standing on its top edge.
        old = self.previous_window
        if (old and window and old.window_id == window.window_id and self.state not in ("fall", "climb", "ceiling")
                and abs(self.y - old.top) <= 2 and old.contains_x(self.x)):
            self.x += window.left - old.left
            self.y += window.top - old.top
        self.previous_window = window
        if self.state == "fall":
            previous_y = self.y
            self.vy = min(900 * scale, self.vy + 1200 * scale * dt)
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.x = max(area.left, min(area.right, self.x))
            floors = [area.bottom]
            if window and window.contains_x(self.x) and previous_y <= window.top + 2:
                floors.append(window.top)
            for floor in sorted(floors):
                if self.vy >= 0 and previous_y <= floor + 2 and self.y >= floor:
                    self.y = floor
                    self.vx = self.vy = 0
                    self.choose()
                    break
            # Recover from a removed monitor or a work area becoming smaller.
            if self.y > area.bottom:
                self.y = area.bottom
                self.choose()
            return
        if self.state == "climb":
            boundary = (area.left if self.wall == "left" else area.right)
            self.x = boundary
            self.y -= 55 * scale * dt
            if self.y <= area.top:
                self.y = area.top
                self.state = "ceiling"
                self.direction = 1 if self.wall == "left" else -1
                self.remaining = self.rng.uniform(3, 8)
                self.elapsed = 0
            return
        if self.state == "ceiling":
            self.y = area.top
            self.x += self.direction * 35 * scale * dt
            self.remaining -= dt
            if self.remaining <= 0 or self.x <= area.left or self.x >= area.right:
                self.release()
            return
        supported = abs(self.y - area.bottom) <= 2 or (
            window and window.contains_x(self.x) and abs(self.y - window.top) <= 2)
        if not supported:
            self.release()
            return
        self.remaining -= dt
        if self.remaining <= 0:
            self.choose()
        speed = {"walk": 100, "run": 200, "creep": 25}.get(self.state, 0)
        self.x += speed * self.direction * scale * dt
        if self.x <= area.left or self.x >= area.right:
            self.x = max(area.left, min(area.right, self.x))
            if speed and self.rng.random() < .6:
                self.wall = "left" if self.x == area.left else "right"
                self.state = "climb"
                self.elapsed = 0
            else:
                self.direction *= -1

    @property
    def frame(self):
        frames, delay = {
            "stand": ([1], .12), "walk": ([1, 2, 1, 3], .12),
            "run": ([1, 2, 1, 3], .05), "sit": ([11], .2),
            "sprawl": ([21], .2), "creep": ([20, 21], .4),
            "spin": ([26, 15, 27, 16, 28, 17, 29, 11], .1),
            "fall": ([4], .1), "drag": ([5, 6, 7, 8, 9, 10], .12),
            "climb": ([14, 13, 12, 13], .2), "ceiling": ([25, 23, 24, 23], .2),
        }[self.state]
        return frames[int(self.elapsed / delay) % len(frames)]
