package com.group_finity.mascot.speech;

import java.awt.Toolkit;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.swing.SwingUtilities;

import com.group_finity.mascot.Mascot;

/**
 * Quản lý kích hoạt hiển thị bóng thoại, phát âm thanh và gửi thông báo hệ thống.
 */
public class SpeechManager {

	private static final Logger log = Logger.getLogger(SpeechManager.class.getName());
	private static final SpeechManager instance = new SpeechManager();

	public static SpeechManager getInstance() {
		return instance;
	}

	private SpeechManager() {
	}

	public void say(final Mascot mascot, final String message) {
		say(mascot, null, message, ReminderManager.getInstance().getBubbleDurationSeconds());
	}

	public void say(final Mascot mascot, final String title, final String message) {
		say(mascot, title, message, ReminderManager.getInstance().getBubbleDurationSeconds());
	}

	public void say(final Mascot mascot, final String title, final String message, final int durationSeconds) {
		if (mascot == null || message == null || message.trim().isEmpty()) {
			return;
		}

		SwingUtilities.invokeLater(new Runnable() {
			@Override
			public void run() {
				try {
					// Đóng bóng thoại cũ nếu có
					if (mascot.getSpeechBubble() != null) {
						mascot.getSpeechBubble().closeBubble();
						mascot.setSpeechBubble(null);
					}

					final SpeechBubble bubble = new SpeechBubble(mascot, title, message, durationSeconds);
					mascot.setSpeechBubble(bubble);
					bubble.updatePosition();
					bubble.setVisible(true);
					bubble.toFront();

					// Âm thanh thông báo
					if (ReminderManager.getInstance().isSoundEnabled()) {
						playNotificationSound();
					}

					// Thông báo hệ thống Linux desktop (notify-send)
					if (ReminderManager.getInstance().isNotifySendEnabled()) {
						sendDesktopNotification(title != null ? title : "Shimeji", message);
					}

				} catch (final Exception e) {
					log.log(Level.WARNING, "Không thể hiển thị bóng thoại", e);
				}
			}
		});
	}

	public void playNotificationSound() {
		try {
			Toolkit.getDefaultToolkit().beep();
		} catch (final Exception e) {
			log.log(Level.FINE, "Không thể phát âm thanh beep", e);
		}
	}

	public void sendDesktopNotification(final String title, final String message) {
		new Thread(new Runnable() {
			@Override
			public void run() {
				try {
					final ProcessBuilder pb = new ProcessBuilder("notify-send", "-a", "Shimeji", "-i", "dialog-information", title, message);
					pb.start();
				} catch (final Exception e) {
					log.log(Level.FINE, "Không thể gửi notify-send", e);
				}
			}
		}).start();
	}
}
