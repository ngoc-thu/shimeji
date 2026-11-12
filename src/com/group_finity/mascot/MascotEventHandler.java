package com.group_finity.mascot;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.swing.JMenuItem;
import javax.swing.JPopupMenu;
import javax.swing.JSeparator;
import javax.swing.SwingUtilities;
import javax.swing.event.PopupMenuEvent;
import javax.swing.event.PopupMenuListener;

import com.group_finity.mascot.exception.CantBeAliveException;

public class MascotEventHandler implements MouseListener {

	private static final Logger log = Logger.getLogger(MascotEventHandler.class.getName());

	/**
	 * トレイアイコンの分のメニューも表示するかどうか.
	 * トレイアイコンの作成に失敗した時はここでトレイアイコンの分のメニューも表示する必要がある.
	 */
	private static boolean showSystemTrayMenu = false;

	public static void setShowSystemTrayMenu(boolean showSystemTrayMenu) {
		MascotEventHandler.showSystemTrayMenu = showSystemTrayMenu;
	}

	public static boolean isShowSystemTrayMenu() {
		return showSystemTrayMenu;
	}

	private final Mascot mascot;

	public MascotEventHandler(Mascot mascot) {
		this.mascot = mascot;
	}

	public void mousePressed(final MouseEvent event) {

		if (SwingUtilities.isRightMouseButton(event) || event.isPopupTrigger()) {
			SwingUtilities.invokeLater(new Runnable() {
				@Override
				public void run() {
					showPopup(event.getComponent(), event.getX(), event.getY());
				}
			});
			return;
		}

		// マウスが押されたらドラッグアニメーションに切り替える
		if (getMascot().getBehavior() != null) {
			try {
				getMascot().getBehavior().mousePressed(event);
			} catch (final CantBeAliveException e) {
				log.log(Level.SEVERE, "生き続けることが出来ない状況", e);
				getMascot().dispose();
			}
		}

	}

	public void mouseReleased(final MouseEvent event) {

		if (SwingUtilities.isRightMouseButton(event) || event.isPopupTrigger()) {
			SwingUtilities.invokeLater(new Runnable() {
				@Override
				public void run() {
					showPopup(event.getComponent(), event.getX(), event.getY());
				}
			});
			return;
		}

		if (getMascot().getBehavior() != null) {
			try {
				getMascot().getBehavior().mouseReleased(event);
			} catch (final CantBeAliveException e) {
				log.log(Level.SEVERE, "生き続けることが出来ない状況", e);
				getMascot().dispose();
			}
		}

	}

	private void showPopup(final java.awt.Component invoker, final int x, final int y) {
		final JPopupMenu popup = new JPopupMenu();

		popup.addPopupMenuListener(new PopupMenuListener() {
			@Override
			public void popupMenuCanceled(final PopupMenuEvent e) {
			}

			@Override
			public void popupMenuWillBecomeInvisible(final PopupMenuEvent e) {
				getMascot().setAnimating(true);
			}

			@Override
			public void popupMenuWillBecomeVisible(final PopupMenuEvent e) {
				getMascot().setAnimating(false);
			}
		});

		// Mục trò chuyện ngay
		final JMenuItem talkMenu = new JMenuItem("💬 Trò chuyện (Nói chuyện)");
		talkMenu.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(final ActionEvent e) {
				com.group_finity.mascot.speech.ReminderManager.getInstance().sayRandomDialogue(getMascot());
			}
		});

		// Mục xem lời nhắc tiếp theo
		final JMenuItem reminderMenu = new JMenuItem("⏰ Lời nhắc tiếp theo");
		reminderMenu.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(final ActionEvent e) {
				com.group_finity.mascot.speech.ReminderManager.getInstance().sayNextReminderInfo(getMascot());
			}
		});

		popup.add(talkMenu);
		popup.add(reminderMenu);
		popup.add(new JSeparator());

		final JMenuItem disposeMenu = new JMenuItem("Quit");
		disposeMenu.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(final ActionEvent e) {
				getMascot().dispose();
			}
		});

		popup.add(disposeMenu);

		popup.add(new JSeparator());

		final JMenuItem openWindowConfMenu = new JMenuItem("Settings: Open window.conf");
		final JMenuItem openSettingsGuiMenu = new JMenuItem("Settings: Open Settings GUI");
		openSettingsGuiMenu.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(final ActionEvent e) {
				Main.getInstance().launchSettingsGui();
			}
		});

		openWindowConfMenu.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(final ActionEvent e) {
				Main.getInstance().openPath(System.getProperty("user.dir") + java.io.File.separator + "window.conf");
			}
		});

		final JMenuItem openTitlesConfMenu = new JMenuItem("Settings: Open titles.conf");
		openTitlesConfMenu.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(final ActionEvent e) {
				Main.getInstance().openPath(System.getProperty("user.dir") + java.io.File.separator + "titles.conf");
			}
		});

		final JMenuItem openAppFolderMenu = new JMenuItem("Settings: Open app folder");
		openAppFolderMenu.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(final ActionEvent e) {
				Main.getInstance().openPath(System.getProperty("user.dir"));
			}
		});

		final JMenuItem resetWindowConfMenu = new JMenuItem("Settings: Reset window.conf");
		resetWindowConfMenu.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(final ActionEvent e) {
				Main.getInstance().resetWindowConf();
			}
		});

		popup.add(openSettingsGuiMenu);
		popup.add(openWindowConfMenu);
		popup.add(openTitlesConfMenu);
		popup.add(openAppFolderMenu);
		popup.add(resetWindowConfMenu);

		if (MascotEventHandler.isShowSystemTrayMenu()) {

			popup.add(new JSeparator());

			// 「増やす」メニューアイテム
			final JMenuItem increaseMenu = new JMenuItem("Add 1");
			increaseMenu.addActionListener(new ActionListener() {
				public void actionPerformed(final ActionEvent event) {
					Main.getInstance().createMascot();
				}
			});

			// 「あつまれ！」メニューアイテム
			final JMenuItem gatherMenu = new JMenuItem("Gather！");
			gatherMenu.addActionListener(new ActionListener() {
				public void actionPerformed(final ActionEvent event) {
					getMascot().getManager().setBehaviorAll(Main.getInstance().getConfiguration(), Main.BEHAVIOR_GATHER);
				}
			});

			// 「一匹だけ残す」メニューアイテム
			final JMenuItem oneMenu = new JMenuItem("Reduce to 1");
			oneMenu.addActionListener(new ActionListener() {
				public void actionPerformed(final ActionEvent event) {
					getMascot().getManager().remainOne();
				}
			});

			// 「IEを元に戻す」メニューアイテム
		/*	final JMenuItem restoreMenu = new JMenuItem("IEを元に戻す");
			restoreMenu.addActionListener(new ActionListener() {
				public void actionPerformed(final ActionEvent event) {
					NativeFactory.getInstance().getEnvironment().restoreIE();
				}
			}); */

			// 「全部ばいばい」メニューアイテム
			final JMenuItem closeMenu = new JMenuItem("Quit");
			closeMenu.addActionListener(new ActionListener() {
				public void actionPerformed(final ActionEvent e) {
					Main.getInstance().exit();
				}
			});

			popup.add(increaseMenu);
			popup.add(gatherMenu);
			popup.add(oneMenu);
	//		popup.add(restoreMenu);
			popup.add(new JSeparator());
			popup.add(closeMenu);
		}

		final java.awt.Component targetComp = invoker != null ? invoker : getMascot().getWindow().asJWindow();
		popup.show(targetComp, x, y);
	}

	@Override
	public void mouseClicked(final MouseEvent e) {
		if (SwingUtilities.isLeftMouseButton(e) && e.getClickCount() == 1) {
			// Click chuột trái vào nhân vật -> nhân vật nói chuyện ngay
			com.group_finity.mascot.speech.ReminderManager.getInstance().sayRandomDialogue(getMascot());
		}
	}

	@Override
	public void mouseEntered(MouseEvent e) {
		// TODO 自動生成されたメソッド・スタブ

	}

	@Override
	public void mouseExited(MouseEvent e) {
		// TODO 自動生成されたメソッド・スタブ

	}

	private Mascot getMascot() {
		return mascot;
	}

}
