package com.group_finity.mascot.speech;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.group_finity.mascot.Main;
import com.group_finity.mascot.Mascot;

/**
 * Quản lý lịch nhắc nhở theo giờ, nhắc nhở định kỳ và hội thoại ngẫu nhiên.
 */
public class ReminderManager {

	private static final Logger log = Logger.getLogger(ReminderManager.class.getName());
	private static final ReminderManager instance = new ReminderManager();

	public static ReminderManager getInstance() {
		return instance;
	}

	private static final String APP_ROOT = System.getProperty("user.dir");
	private static final String REMINDERS_FILE = APP_ROOT + File.separator + "conf" + File.separator + "reminders.properties";
	private static final String DIALOGUES_FILE = APP_ROOT + File.separator + "conf" + File.separator + "dialogues.conf";

	private boolean enabled = true;
	private boolean soundEnabled = true;
	private boolean notifySendEnabled = true;
	private boolean randomIdleChatEnabled = true;
	private int randomChatIntervalMinutes = 15;
	private int bubbleDurationSeconds = 7;

	// Lịch nhắc cố định: Key là "HH:mm" (ví dụ "11:55"), Value là nội dung
	private final Map<String, String> scheduledReminders = new HashMap<String, String>();

	// Nhắc nhở theo chu kỳ
	private int waterIntervalMinutes = 60;
	private String waterMessage = "Anh nhớ uống một ngụm nước nhé! 💧";
	private long lastWaterReminderTime = System.currentTimeMillis();

	private int restIntervalMinutes = 45;
	private String restMessage = "Anh chớp mắt và vươn vai thư giãn 20 giây nha! 👀";
	private long lastRestReminderTime = System.currentTimeMillis();

	private long lastIdleChatTime = System.currentTimeMillis();

	// Danh sách câu thoại ngẫu nhiên
	private final List<String> dialogues = new ArrayList<String>();

	private long remindersFileLastModified = 0;
	private long dialoguesFileLastModified = 0;
	private String lastTriggeredMinute = "";

	private final Random random = new Random();
	private Thread daemonThread = null;
	private volatile boolean running = false;

	private ReminderManager() {
	}

	public synchronized void start() {
		if (running) {
			return;
		}
		loadConfig();
		loadDialogues();

		running = true;
		daemonThread = new Thread(new Runnable() {
			@Override
			public void run() {
				while (running) {
					try {
						Thread.sleep(10000); // Kiểm tra mỗi 10 giây
						if (!running) break;

						checkFileUpdates();
						checkAndTriggerReminders();
					} catch (final InterruptedException e) {
						Thread.currentThread().interrupt();
						break;
					} catch (final Exception e) {
						log.log(Level.WARNING, "Lỗi trong thread ReminderManager", e);
					}
				}
			}
		}, "Shimeji-ReminderDaemon");
		daemonThread.setDaemon(true);
		daemonThread.start();
		log.log(Level.INFO, "Đã khởi động ReminderManager");
	}

	public synchronized void stop() {
		running = false;
		if (daemonThread != null) {
			daemonThread.interrupt();
			daemonThread = null;
		}
	}

	public synchronized void loadConfig() {
		final File file = new File(REMINDERS_FILE);
		if (!file.exists()) {
			return;
		}

		remindersFileLastModified = file.lastModified();
		final Properties props = new Properties();
		try (InputStream in = new FileInputStream(file);
			 InputStreamReader reader = new InputStreamReader(in, StandardCharsets.UTF_8)) {
			props.load(reader);

			this.enabled = Boolean.parseBoolean(props.getProperty("enabled", "true"));
			this.soundEnabled = Boolean.parseBoolean(props.getProperty("soundEnabled", "true"));
			this.notifySendEnabled = Boolean.parseBoolean(props.getProperty("notifySendEnabled", "true"));
			this.randomIdleChatEnabled = Boolean.parseBoolean(props.getProperty("randomIdleChatEnabled", "true"));
			this.randomChatIntervalMinutes = Integer.parseInt(props.getProperty("randomChatIntervalMinutes", "15"));
			this.bubbleDurationSeconds = Integer.parseInt(props.getProperty("bubbleDurationSeconds", "7"));

			this.waterIntervalMinutes = Integer.parseInt(props.getProperty("interval.water_minutes", "60"));
			this.waterMessage = props.getProperty("interval.water_message", "Anh nhớ uống một ngụm nước nhé! 💧");

			this.restIntervalMinutes = Integer.parseInt(props.getProperty("interval.rest_minutes", "45"));
			this.restMessage = props.getProperty("interval.rest_message", "Anh chớp mắt và vươn vai thư giãn 20 giây nha! 👀");

			this.scheduledReminders.clear();
			for (final String key : props.stringPropertyNames()) {
				if (key.startsWith("reminder.")) {
					// Format key: reminder.11_55 hoặc reminder.11:55
					final String timePart = key.substring("reminder.".length()).replace('_', ':');
					final String msg = props.getProperty(key);
					if (timePart.matches("^\\d{1,2}:\\d{2}$") && msg != null && !msg.trim().isEmpty()) {
						final String normalizedTime = normalizeTime(timePart);
						this.scheduledReminders.put(normalizedTime, msg.trim());
					}
				}
			}

			log.log(Level.INFO, "Đã nạp {0} mốc nhắc nhở từ reminders.properties", scheduledReminders.size());

		} catch (final Exception e) {
			log.log(Level.WARNING, "Không thể đọc reminders.properties", e);
		}
	}

	public synchronized void loadDialogues() {
		final File file = new File(DIALOGUES_FILE);
		if (!file.exists()) {
			return;
		}

		dialoguesFileLastModified = file.lastModified();
		final List<String> list = new ArrayList<String>();
		try (BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(file), StandardCharsets.UTF_8))) {
			String line;
			while ((line = reader.readLine()) != null) {
				line = line.trim();
				if (!line.isEmpty() && !line.startsWith("#")) {
					list.add(line);
				}
			}
			dialogues.clear();
			dialogues.addAll(list);
			log.log(Level.INFO, "Đã nạp {0} câu thoại từ dialogues.conf", dialogues.size());
		} catch (final Exception e) {
			log.log(Level.WARNING, "Không thể đọc dialogues.conf", e);
		}
	}

	private void checkFileUpdates() {
		final File rFile = new File(REMINDERS_FILE);
		if (rFile.exists() && rFile.lastModified() > remindersFileLastModified) {
			loadConfig();
		}
		final File dFile = new File(DIALOGUES_FILE);
		if (dFile.exists() && dFile.lastModified() > dialoguesFileLastModified) {
			loadDialogues();
		}
	}

	private String normalizeTime(final String timeStr) {
		final String[] parts = timeStr.split(":");
		int h = Integer.parseInt(parts[0]);
		int m = Integer.parseInt(parts[1]);
		return String.format("%02d:%02d", h, m);
	}

	private void checkAndTriggerReminders() {
		if (!enabled) {
			return;
		}

		final Mascot mascot = getActiveMascot();
		if (mascot == null) {
			return;
		}

		final SimpleDateFormat sdf = new SimpleDateFormat("HH:mm");
		final String currentMinute = sdf.format(new Date());

		// 1. Kiểm tra mốc giờ cố định (ví dụ 11:55)
		if (!currentMinute.equals(lastTriggeredMinute)) {
			if (scheduledReminders.containsKey(currentMinute)) {
				lastTriggeredMinute = currentMinute;
				final String message = scheduledReminders.get(currentMinute);
				SpeechManager.getInstance().say(mascot, "⏰ [" + currentMinute + "] Lời nhắc", message, bubbleDurationSeconds + 2);
				return;
			}
		}

		final long now = System.currentTimeMillis();

		// 2. Kiểm tra chu kỳ uống nước
		if (waterIntervalMinutes > 0 && (now - lastWaterReminderTime) >= (long) waterIntervalMinutes * 60 * 1000) {
			lastWaterReminderTime = now;
			SpeechManager.getInstance().say(mascot, "💧 Lời nhắc", waterMessage, bubbleDurationSeconds);
			return;
		}

		// 3. Kiểm tra chu kỳ nghỉ mắt
		if (restIntervalMinutes > 0 && (now - lastRestReminderTime) >= (long) restIntervalMinutes * 60 * 1000) {
			lastRestReminderTime = now;
			SpeechManager.getInstance().say(mascot, "👀 Lời nhắc", restMessage, bubbleDurationSeconds);
			return;
		}

		// 4. Kiểm tra trò chuyện ngẫu nhiên khi rảnh
		if (randomIdleChatEnabled && randomChatIntervalMinutes > 0 && (now - lastIdleChatTime) >= (long) randomChatIntervalMinutes * 60 * 1000) {
			lastIdleChatTime = now;
			sayRandomDialogue(mascot);
		}
	}

	public void sayRandomDialogue(final Mascot mascot) {
		final Mascot target = mascot != null ? mascot : getActiveMascot();
		if (target == null) return;

		final String line = getRandomDialogue();
		if (line != null && !line.isEmpty()) {
			SpeechManager.getInstance().say(target, "💬 Trò chuyện", line, bubbleDurationSeconds);
		}
	}

	public void sayNextReminderInfo(final Mascot mascot) {
		final Mascot target = mascot != null ? mascot : getActiveMascot();
		if (target == null) return;

		final SimpleDateFormat sdf = new SimpleDateFormat("HH:mm");
		final String currentMinute = sdf.format(new Date());

		final List<String> sortedTimes = new ArrayList<String>(scheduledReminders.keySet());
		Collections.sort(sortedTimes);

		String nextTime = null;
		for (final String t : sortedTimes) {
			if (t.compareTo(currentMinute) > 0) {
				nextTime = t;
				break;
			}
		}
		if (nextTime == null && !sortedTimes.isEmpty()) {
			nextTime = sortedTimes.get(0); // Vòng sang ngày mai
		}

		if (nextTime != null) {
			final String msg = scheduledReminders.get(nextTime);
			SpeechManager.getInstance().say(target, "⏰ Lời nhắc kế tiếp", "Lúc " + nextTime + ": " + msg, bubbleDurationSeconds);
		} else {
			SpeechManager.getInstance().say(target, "⏰ Lời nhắc", "Hiện chưa có lịch nhắc nhở nào được cài đặt!", bubbleDurationSeconds);
		}
	}

	public String getRandomDialogue() {
		if (dialogues.isEmpty()) {
			return "Chào anh! Chúc anh một ngày làm việc hiệu quả và vui vẻ nhé! ✨";
		}
		return dialogues.get(random.nextInt(dialogues.size()));
	}

	private Mascot getActiveMascot() {
		try {
			final Main main = Main.getInstance();
			if (main != null && main.getManager() != null && main.getManager().getCount() > 0) {
				return main.getManager().getFirstMascot();
			}
		} catch (final Exception e) {
		}
		return null;
	}

	public boolean isEnabled() {
		return enabled;
	}

	public boolean isSoundEnabled() {
		return soundEnabled;
	}

	public boolean isNotifySendEnabled() {
		return notifySendEnabled;
	}

	public int getBubbleDurationSeconds() {
		return bubbleDurationSeconds;
	}
}
