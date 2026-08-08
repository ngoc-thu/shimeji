package com.group_finity.mascot.win;

import java.awt.Color;
import java.awt.Component;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.AlphaComposite;

import javax.swing.JComponent;
import javax.swing.JPanel;
import javax.swing.JWindow;

import com.group_finity.mascot.image.NativeImage;
import com.group_finity.mascot.image.TranslucentWindow;

public class WindowsTranslucentWindow extends JWindow implements TranslucentWindow {

	private static final long serialVersionUID = 1L;

	private WindowsNativeImage image;
	private final JPanel panel;

	public WindowsTranslucentWindow() {
		super();
		this.init();

		this.panel = new JPanel() {
			private static final long serialVersionUID = 1L;

			@Override
			protected void paintComponent(final Graphics g) {
				super.paintComponent(g);
				if (getImage() != null && getImage().getManagedImage() != null) {
					final Graphics2D g2d = (Graphics2D) g.create();
					g2d.setComposite(AlphaComposite.Src);
					g2d.drawImage(getImage().getManagedImage(), 0, 0, null);
					g2d.dispose();
				}
			}
		};
		this.panel.setOpaque(false);
		this.setContentPane(this.panel);
	}

	private void init() {
		try {
			this.setBackground(new Color(0, 0, 0, 0));
		} catch (final Exception e) {
			// Fallback if per-pixel alpha background is restricted
		}
		this.setAlwaysOnTop(true);
	}

	@Override
	public JWindow asJWindow() {
		return this;
	}

	@Override
	public void setToDock(final int value) {
		// Not needed on Windows
	}

	public WindowsNativeImage getImage() {
		return this.image;
	}

	@Override
	public void setImage(final NativeImage image) {
		this.image = (WindowsNativeImage) image;
	}

	@Override
	public void updateImage() {
		if (this.getImage() != null) {
			this.setSize(this.getImage().getWidth(), this.getImage().getHeight());
		}
		this.revalidate();
		this.repaint();
	}

	@Override
	public String toString() {
		return "WindowsTranslucentWindow[hashCode=" + hashCode() + ",bounds=" + getBounds() + "]";
	}
}
