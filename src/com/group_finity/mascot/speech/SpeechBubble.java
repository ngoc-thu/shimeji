package com.group_finity.mascot.speech;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Cursor;
import java.awt.Font;
import java.awt.Point;
import java.awt.Dimension;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.geom.RoundRectangle2D;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JWindow;
import javax.swing.SwingUtilities;
import javax.swing.Timer;
import javax.swing.border.CompoundBorder;
import javax.swing.border.EmptyBorder;
import javax.swing.border.LineBorder;

import com.group_finity.mascot.Mascot;

/**
 * Hiển thị bóng thoại (Speech Bubble) trên đầu nhân vật Mascot.
 * Hỗ trợ hiển thị đầy đủ văn bản tiếng Việt nhiều dòng, tự động xuống dòng và tự co giãn chiều cao.
 */
public class SpeechBubble extends JWindow {

	private static final long serialVersionUID = 1L;

	private static final int TEXT_WRAP_WIDTH = 220;
	private static final int ARC_SIZE = 16;

	private static final Color BG_COLOR = new Color(255, 255, 255);
	private static final Color BORDER_COLOR = new Color(44, 62, 80);
	private static final Color TITLE_COLOR = new Color(30, 136, 229);
	private static final Color CLOSE_HOVER_COLOR = new Color(231, 76, 60);

	private final Mascot mascot;
	private final String title;
	private final String message;
	private Timer autoCloseTimer;

	public SpeechBubble(final Mascot mascot, final String title, final String message, final int durationSeconds) {
		super();
		this.mascot = mascot;
		this.title = (title != null && !title.trim().isEmpty()) ? title.trim() : "💬 Shimeji";
		this.message = (message != null && !message.trim().isEmpty()) ? message.trim() : "...";

		initUI(durationSeconds);
	}

	private void initUI(final int durationSeconds) {
		try {
			setType(Type.POPUP);
		} catch (final Exception ignored) {
		}

		setAlwaysOnTop(true);
		setFocusableWindowState(false);

		final JPanel mainPanel = new JPanel(new BorderLayout(0, 6));
		mainPanel.setBackground(BG_COLOR);
		mainPanel.setOpaque(true);
		mainPanel.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));

		// Viền bo tròn với khoảng đệm thoải mái
		mainPanel.setBorder(new CompoundBorder(
				new LineBorder(BORDER_COLOR, 2, true),
				new EmptyBorder(8, 12, 10, 12)
		));

		// Header: Title + Nút đóng (X)
		final JPanel headerPanel = new JPanel(new BorderLayout());
		headerPanel.setBackground(BG_COLOR);
		headerPanel.setOpaque(false);

		final JLabel titleLabel = new JLabel(title);
		titleLabel.setFont(new Font("SansSerif", Font.BOLD, 12));
		titleLabel.setForeground(TITLE_COLOR);
		headerPanel.add(titleLabel, BorderLayout.CENTER);

		final JLabel closeBtn = new JLabel(" ✕ ");
		closeBtn.setFont(new Font("SansSerif", Font.BOLD, 11));
		closeBtn.setForeground(new Color(160, 160, 160));
		closeBtn.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
		closeBtn.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseEntered(final MouseEvent e) {
				closeBtn.setForeground(CLOSE_HOVER_COLOR);
			}

			@Override
			public void mouseExited(final MouseEvent e) {
				closeBtn.setForeground(new Color(160, 160, 160));
			}

			@Override
			public void mouseClicked(final MouseEvent e) {
				closeBubble();
			}
		});
		headerPanel.add(closeBtn, BorderLayout.EAST);
		mainPanel.add(headerPanel, BorderLayout.NORTH);

		// Body: Message Text dạng HTML tự động xuống dòng và tự co giãn chiều cao
		final JLabel messageLabel = new JLabel(formatHtml(message, TEXT_WRAP_WIDTH));
		messageLabel.setOpaque(false);
		mainPanel.add(messageLabel, BorderLayout.CENTER);

		// Click vào bất cứ đâu để đóng
		final MouseAdapter clickCloser = new MouseAdapter() {
			@Override
			public void mouseClicked(final MouseEvent e) {
				closeBubble();
			}
		};
		mainPanel.addMouseListener(clickCloser);
		titleLabel.addMouseListener(clickCloser);
		messageLabel.addMouseListener(clickCloser);

		setContentPane(mainPanel);

		// Tự động tính toán kích thước bao trọn toàn bộ nội dung
		pack();

		// Cắt góc bo tròn cửa sổ
		try {
			setShape(new RoundRectangle2D.Double(0, 0, getWidth(), getHeight(), ARC_SIZE, ARC_SIZE));
		} catch (final Exception ignored) {
		}

		updatePosition();

		if (durationSeconds > 0) {
			autoCloseTimer = new Timer(durationSeconds * 1000, new ActionListener() {
				@Override
				public void actionPerformed(final ActionEvent e) {
					closeBubble();
				}
			});
			autoCloseTimer.setRepeats(false);
			autoCloseTimer.start();
		}
	}

	private static String formatHtml(final String text, final int wrapWidthPx) {
		final String escaped = text.replace("&", "&amp;")
				.replace("<", "&lt;")
				.replace(">", "&gt;")
				.replace("\"", "&quot;")
				.replace("\n", "<br/>");
		return "<html><div style='width: " + wrapWidthPx + "px; font-family: sans-serif; font-size: 11pt; color: #1F2937; line-height: 1.35;'>"
				+ escaped
				+ "</div></html>";
	}

	public void updatePosition() {
		if (mascot == null || !isVisible()) {
			return;
		}

		final Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
		final Point anchor = mascot.getAnchor();
		final int mascotHeight = (mascot.getImage() != null && mascot.getImage().getSize() != null)
				? mascot.getImage().getSize().height : 128;

		final int bubbleW = getWidth();
		final int bubbleH = getHeight();

		int targetX = anchor.x - (bubbleW / 2);
		int targetY = anchor.y - mascotHeight - bubbleH - 10;

		// Nếu nhân vật ở gần mép trên màn hình, đưa bóng thoại xuống dưới chân
		if (targetY < 25) {
			targetY = anchor.y + 12;
		}

		// Giữ bóng thoại luôn nằm trọn vẹn trong màn hình
		targetX = Math.max(12, Math.min(screenSize.width - bubbleW - 12, targetX));
		targetY = Math.max(12, Math.min(screenSize.height - bubbleH - 45, targetY));

		if (getX() != targetX || getY() != targetY) {
			setLocation(targetX, targetY);
		}
	}

	public void closeBubble() {
		SwingUtilities.invokeLater(new Runnable() {
			@Override
			public void run() {
				if (autoCloseTimer != null) {
					autoCloseTimer.stop();
				}
				setVisible(false);
				dispose();
			}
		});
	}
}
