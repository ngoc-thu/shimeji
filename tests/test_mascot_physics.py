import random
import unittest
from mascot_physics import Mascot, Rect


class MovementTest(unittest.TestCase):
    area = Rect(0, 0, 1920, 1040)

    def mascot(self, x=500, y=200):
        return Mascot(x, y, random.Random(1))

    def advance(self, mascot, frames=200, window=None, scale=1):
        for _ in range(frames):
            mascot.step(.02, self.area, window, scale)

    def test_falls_and_lands_above_taskbar_at_all_scales(self):
        for scale in (.25, 1, 1.37, 2):
            with self.subTest(scale=scale):
                m = self.mascot()
                for _ in range(500):
                    m.step(.02, self.area, scale=scale)
                    if m.state != 'fall':
                        break
                self.assertEqual(m.y, self.area.bottom)
                self.assertNotEqual(m.state, 'fall')

    def test_lands_on_window_top_without_tunnelling(self):
        m = self.mascot(y=490)
        m.vy = 900
        m.step(.05, self.area, Rect(400, 500, 800, 900))
        self.assertEqual(m.y, 500)
        self.assertNotEqual(m.state, 'fall')

    def test_falling_below_window_does_not_snap_up(self):
        m = self.mascot(y=600)
        m.step(.02, self.area, Rect(400, 500, 800, 900))
        self.assertGreater(m.y, 600)

    def test_removed_window_and_walking_off_window_start_falling(self):
        for window, x in ((None, 500), (Rect(400, 500, 800, 900), 900)):
            m = self.mascot(x=x, y=500)
            m.state, m.remaining = 'stand', 5
            m.step(.02, self.area, window)
            self.assertEqual(m.state, 'fall')

    def test_character_follows_same_window_but_not_new_foreground_window(self):
        for window_id, expected in ((1, (550, 450)), (2, (500, 500))):
            m = self.mascot(y=500)
            m.state, m.remaining = 'stand', 5
            m.previous_window = Rect(400, 500, 800, 900, 1)
            m.step(.02, self.area, Rect(450, 450, 850, 850, window_id))
            self.assertEqual((m.x, m.y), expected)

    def test_drag_ignores_gravity_and_release_clamps_throw_velocity(self):
        m = self.mascot()
        m.state = 'drag'
        self.advance(m)
        self.assertEqual((m.x, m.y), (500, 200))
        m.release(10000, -10000)
        self.assertEqual((m.vx, m.vy), (900, -900))
        self.assertEqual(m.state, 'fall')

    def test_climbing_reaches_ceiling_then_releases(self):
        m = self.mascot(x=0, y=5)
        m.state, m.wall = 'climb', 'left'
        self.advance(m, 10)
        self.assertEqual(m.state, 'ceiling')
        self.assertEqual(m.y, self.area.top)
        m.remaining = 0
        m.step(.02, self.area)
        self.assertEqual(m.state, 'fall')

    def test_negative_monitor_coordinates_and_changed_work_area(self):
        m = self.mascot(-1000, 1200)
        m.step(.02, Rect(-1920, 0, 0, 1000))
        self.assertEqual(m.x, -1000)
        self.assertEqual(m.y, 1000)
        self.assertNotEqual(m.state, 'fall')

    def test_pause_does_not_cause_huge_physics_jump(self):
        m = self.mascot()
        m.step(60, self.area)
        self.assertLess(m.y, 210)


if __name__ == '__main__':
    unittest.main()
