package com.group_finity.mascot.win;

import com.sun.jna.Native;
import com.sun.jna.platform.win32.User32;
import com.sun.jna.platform.win32.WinDef.HWND;
import com.sun.jna.platform.win32.WinDef.RECT;

import com.sun.jna.win32.W32APIOptions;

public interface User32Extra extends User32 {
	User32Extra INSTANCE = (User32Extra) Native.loadLibrary("user32", User32Extra.class, W32APIOptions.DEFAULT_OPTIONS);

	int SPI_GETWORKAREA = 48;

	boolean IsIconic(HWND hWnd);

	boolean MoveWindow(HWND hWnd, int X, int Y, int nWidth, int nHeight, boolean bRepaint);

	boolean SystemParametersInfo(int uiAction, int uiParam, RECT pvParam, int fWinIni);

	int GetSystemMetrics(int nIndex);
}
