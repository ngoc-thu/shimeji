package com.group_finity.mascot.win;

import java.awt.GraphicsEnvironment;
import java.awt.Point;
import java.awt.Rectangle;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;

import com.group_finity.mascot.environment.Area;
import com.group_finity.mascot.environment.Environment;
import com.group_finity.mascot.environment.WindowContainer;
import com.sun.jna.Native;
import com.sun.jna.Pointer;
import com.sun.jna.platform.win32.WinDef.HWND;
import com.sun.jna.platform.win32.WinDef.RECT;
import com.sun.jna.platform.win32.WinUser.WNDENUMPROC;

public class WindowsEnvironment extends Environment {

	public static final Area workArea = new Area();
	public WindowContainer IE = new WindowContainer();
	public Area activeIE = new Area();

	private int xoffset = 0;
	private int yoffset = 0;
	private int wmod = 0;
	private int hmod = 0;

	private final ArrayList<String> titles = new ArrayList<String>();
	private final ArrayList<Number> curActiveWin = new ArrayList<Number>();
	private final ArrayList<Number> curVisibleWin = new ArrayList<Number>();

	private int tickCount = 0;
	private HWND activeHwnd = null;

	public WindowsEnvironment() {
		loadConfig();
		updateWorkArea();
	}

	private void loadConfig() {
		try {
			final FileInputStream fstream = new FileInputStream("window.conf");
			final DataInputStream in = new DataInputStream(fstream);
			final BufferedReader br = new BufferedReader(new InputStreamReader(in));
			String strLine;
			int z = 0;
			while ((strLine = br.readLine()) != null) {
				z++;
				switch (z) {
					case 1: break;
					case 2: this.xoffset = Integer.parseInt(strLine.trim()); break;
					case 3: this.yoffset = Integer.parseInt(strLine.trim()); break;
					case 4: this.wmod = Integer.parseInt(strLine.trim()); break;
					case 5: this.hmod = Integer.parseInt(strLine.trim()); break;
					default: break;
				}
			}
			br.close();
			in.close();
		} catch (final Exception e) {
			// use defaults
		}

		try {
			final FileInputStream fstream = new FileInputStream("titles.conf");
			final DataInputStream in = new DataInputStream(fstream);
			final BufferedReader br = new BufferedReader(new InputStreamReader(in));
			String strLine;
			while ((strLine = br.readLine()) != null) {
				if (!strLine.trim().isEmpty()) {
					this.titles.add(strLine.trim().toLowerCase());
				}
			}
			br.close();
			in.close();
		} catch (final Exception e) {
			// use empty titles
		}
	}

	private void updateWorkArea() {
		try {
			final Rectangle maxBounds = GraphicsEnvironment.getLocalGraphicsEnvironment().getMaximumWindowBounds();
			workArea.set(maxBounds);
		} catch (final Exception e) {
			final int left = getScreen().getLeft();
			final int top = getScreen().getTop();
			final int width = getScreen().getRight() - left;
			final int height = getScreen().getBottom() - top;
			workArea.set(new Rectangle(left, top, width, height));
		}
	}

	@Override
	public void tick() {
		super.tick();
		updateWorkArea();

		tickCount++;
		if (tickCount % 20 == 0) {
			updateWindows();
		}
	}

	private double getScaleX() {
		final int physW = User32Extra.INSTANCE.GetSystemMetrics(0); // SM_CXSCREEN
		final int logW = getScreen().getRight() - getScreen().getLeft();
		if (physW > 0 && logW > 0) {
			return (double) logW / physW;
		}
		return 1.0;
	}

	private double getScaleY() {
		final int physH = User32Extra.INSTANCE.GetSystemMetrics(1); // SM_CYSCREEN
		final int logH = getScreen().getBottom() - getScreen().getTop();
		if (physH > 0 && logH > 0) {
			return (double) logH / physH;
		}
		return 1.0;
	}

	private void updateWindows() {
		final WindowContainer newIE = new WindowContainer();
		final ArrayList<Number> newActiveWin = new ArrayList<Number>();
		final ArrayList<Number> newVisibleWin = new ArrayList<Number>();

		final HWND fgHwnd = User32Extra.INSTANCE.GetForegroundWindow();
		final double scaleX = getScaleX();
		final double scaleY = getScaleY();

		User32Extra.INSTANCE.EnumWindows(new WNDENUMPROC() {
			@Override
			public boolean callback(final HWND hwnd, final Pointer data) {
				if (!User32Extra.INSTANCE.IsWindowVisible(hwnd) || User32Extra.INSTANCE.IsIconic(hwnd)) {
					return true;
				}

				final RECT rect = new RECT();
				if (!User32Extra.INSTANCE.GetWindowRect(hwnd, rect)) {
					return true;
				}

				final int physW = rect.right - rect.left;
				final int physH = rect.bottom - rect.top;
				if (physW <= 50 || physH <= 50) {
					return true;
				}

				final char[] titleBuf = new char[512];
				User32Extra.INSTANCE.GetWindowText(hwnd, titleBuf, 512);
				final String title = Native.toString(titleBuf).trim();

				if (!titles.isEmpty()) {
					boolean match = false;
					final String lowerTitle = title.toLowerCase();
					for (final String t : titles) {
						if (lowerTitle.contains(t)) {
							match = true;
							break;
						}
					}
					if (!match) {
						return true;
					}
				}

				final int scaledLeft = (int) Math.round(rect.left * scaleX);
				final int scaledTop = (int) Math.round(rect.top * scaleY);
				final int scaledW = (int) Math.round(physW * scaleX);
				final int scaledH = (int) Math.round(physH * scaleY);

				final Rectangle winBounds = new Rectangle(
					scaledLeft + xoffset,
					scaledTop + yoffset,
					scaledW + wmod,
					scaledH + hmod
				);

				final long id = Pointer.nativeValue(hwnd.getPointer());
				final Area area = new Area(id);
				area.set(winBounds);
				newIE.put(id, area);
				newVisibleWin.add(id);

				if (fgHwnd != null && fgHwnd.equals(hwnd)) {
					newActiveWin.add(id);
				}
				return true;
			}
		}, null);

		this.IE = newIE;
		this.curVisibleWin.clear();
		this.curVisibleWin.addAll(newVisibleWin);

		this.curActiveWin.clear();
		this.curActiveWin.addAll(newActiveWin);

		if (fgHwnd != null && User32Extra.INSTANCE.IsWindowVisible(fgHwnd) && !User32Extra.INSTANCE.IsIconic(fgHwnd)) {
			final RECT rect = new RECT();
			if (User32Extra.INSTANCE.GetWindowRect(fgHwnd, rect)) {
				final int scaledLeft = (int) Math.round(rect.left * scaleX);
				final int scaledTop = (int) Math.round(rect.top * scaleY);
				final int scaledW = (int) Math.round((rect.right - rect.left) * scaleX);
				final int scaledH = (int) Math.round((rect.bottom - rect.top) * scaleY);

				final Rectangle winBounds = new Rectangle(
					scaledLeft + xoffset,
					scaledTop + yoffset,
					scaledW + wmod,
					scaledH + hmod
				);
				this.activeIE.set(winBounds);
				this.activeHwnd = fgHwnd;
			}
		}
	}

	@Override
	public Area getWorkArea() {
		return workArea;
	}

	@Override
	public Area getActiveIE() {
		return this.activeIE;
	}

	@Override
	public WindowContainer getIE() {
		return this.IE;
	}

	@Override
	public ArrayList<Number> getVisible() {
		return this.curVisibleWin;
	}

	@Override
	public int getDockValue() {
		return 0;
	}

	@Override
	public void moveActiveIE(final Point point) {
		if (this.activeHwnd != null && User32Extra.INSTANCE.IsWindowVisible(this.activeHwnd)) {
			final RECT rect = new RECT();
			if (User32Extra.INSTANCE.GetWindowRect(this.activeHwnd, rect)) {
				final int w = rect.right - rect.left;
				final int h = rect.bottom - rect.top;
				final double scaleX = getScaleX();
				final double scaleY = getScaleY();
				final int physX = (int) Math.round(point.x / scaleX);
				final int physY = (int) Math.round(point.y / scaleY);
				User32Extra.INSTANCE.MoveWindow(this.activeHwnd, physX, physY, w, h, true);
			}
		}
	}

	@Override
	public void restoreIE() {
		// Window restoration if needed
	}
}
