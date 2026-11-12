# Shimeji — Cross-Platform Desktop Mascot (Windows • Linux • macOS)

<p align="center">
  <img src="docs/images/repo-banner.png" alt="shimeji banner" width="100%" />
</p>

<p align="center">
  <img src="docs/images/linux-shimeji-icon.png" alt="shimeji icon" width="64" height="64" />
</p>

<p align="center">
  <a href="#-tiếng-việt">🇻🇳 <strong>Tiếng Việt</strong></a> &nbsp;|&nbsp; <a href="#-english">🇬🇧 <strong>English</strong></a> &nbsp;|&nbsp; <a href="#-danh-sách-toàn-bộ-400-nhân-vật--full-400-character-gallery">🎭 <strong>400+ Characters Gallery</strong></a>
</p>

---

# 🇻🇳 Tiếng Việt

**Shimeji** là ứng dụng thú cưng màn hình (Desktop Mascot / Pet) mã nguồn mở, hoạt động mượt mà trên cả 3 hệ điều hành **Windows 10/11**, **Linux** (Ubuntu, Debian, Arch...) và **macOS**. 

Phiên bản này được nâng cấp toàn diện với kho **hơn 400 nhân vật anime & game**, hệ thống **bong bóng thoại & lời nhắc sức khỏe** thông minh, cùng giao diện cài đặt (**Settings GUI**) trực quan hỗ trợ tìm kiếm và xem trước hình ảnh thời gian thực.

---

## ✨ Tính Năng Nổi Bật

- 🎭 **Kho 400+ Nhân Vật Đa Dạng**: Bao gồm Genshin Impact (Xiao Catboy, Ayaka...), Vocaloid (Hatsune Miku, Rin, Len...), Pokemon, Naruto, One Piece, Undertale, Marvel, v.v.
- 💬 **Hệ Thống Trò Chuyện & Bong Bóng Thoại**:
  - Bong bóng thoại hiển thị nổi trên đầu nhân vật, hỗ trợ tiếng Việt đầy đủ và tự động co giãn.
  - **Click chuột trái** vào nhân vật để trò chuyện ngay lập tức.
  - Thư viện câu thoại phong phú, dễ dàng tự thêm câu thoại yêu thích.
- ⏰ **Hệ Thống Lời Nhắc Sức Khỏe Thông Minh**:
  - Nhắc nhở định kỳ: uống nước, nghỉ mắt ngơi sau thời gian dài nhìn màn hình, vận động nhẹ, ăn đúng giờ.
  - Hỗ trợ chuông báo (beep) và thông báo desktop (Desktop Notification).
  - Click chuột phải chọn **⏰ Lời nhắc tiếp theo** để xem lịch nhắc sắp tới.
- 🖥️ **Giao Diện Cài Đặt Hiện Đại (Settings GUI)**:
  - **Live Search**: Tìm kiếm và lọc tên nhân vật tức thì.
  - **Image Preview**: Xem trước hình ảnh nhân vật trực tiếp trước khi áp dụng.
  - **Thao tác nhanh**: Nút *Thả NV này* (`Spawn Selected`), *Thả TẤT CẢ* (`Spawn ALL`), *Tắt TẤT CẢ* (`Kill All Mascots`).
  - Tùy chỉnh thông số bám cửa sổ (`window.conf`), lọc tiêu đề cửa sổ (`titles.conf`) và bật/tắt tự nhân bản (Self-cloning).
- ⚙️ **Tương Thích Đa Nền Tảng & Màn Hình Độ Phân Giải Cao (High-DPI)**:
  - **Windows**: Hỗ trợ launcher độc lập `.exe` (`Shimeji.exe`, `ShimejiSettings.exe`), fix triệt để lỗi rơi xuyên sàn và lỗi màn hình phóng to (125%, 150%, 200%).
  - **Linux**: Bộ script cài đặt tự động 1 lệnh, tích hợp icon menu ứng dụng và phím tắt toàn cục.
  - **macOS**: Hỗ trợ cả chip Intel và Apple Silicon (M1/M2/M3/M4) qua AWT/Swing fallback.
  - Hỗ trợ các bản Java mới nhất: **Java 8, 11, 17, 21+** (với các cờ `--add-opens` tối ưu).

---

## 🎭 Một Số Nhân Vật Tiêu Biểu

<table>
  <tr>
    <td align="center"><strong>Ayaka (Genshin)</strong></td>
    <td align="center"><strong>Hatsune Miku</strong></td>
    <td align="center"><strong>Xiao Catboy (Genshin)</strong></td>
  </tr>
  <tr>
    <td align="center"><img src="docs/images/ayaka-preview.png" alt="Ayaka preview" width="128" /></td>
    <td align="center"><img src="docs/images/miku-preview.png" alt="Hatsune Miku preview" width="128" /></td>
    <td align="center"><img src="docs/images/xiao-catboy-preview.png" alt="Xiao Catboy preview" width="128" /></td>
  </tr>
</table>

*(Cùng hơn 400 nhân vật khác có sẵn trong thư mục `characters/`)*

---

## 📋 Yêu Cầu Hệ Thống

1. **Java**: Phiên bản Java 8 trở lên (Khuyến nghị **OpenJDK 17** hoặc **21**).
2. **Python**: Python 3.x kèm module `tkinter` (để chạy giao diện cài đặt `shimeji_settings.py`).

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Theo Hệ Điều Hành

### 🪟 1. Trên Windows (10/11)

#### Cách 1: Chạy trực tiếp (Nhanh nhất)
1. Tải bản release mới nhất hoặc clone repository này về máy.
2. Cài đặt **Java** (nếu máy chưa có Java, tải tại [Adoptium Temurin](https://adoptium.net/)).
3. **Khởi động Shimeji**:
   - Double-click vào file **`Shimeji.exe`** (chạy ẩn ngầm không hiện cửa sổ đen) hoặc **`launch.bat`**.
4. **Mở Cài Đặt & Đổi Nhân Vật**:
   - Double-click vào file **`ShimejiSettings.exe`** hoặc **`run-settings.bat`**.

---

### 🐧 2. Trên Linux (Ubuntu / Debian / Fedora / Arch)

#### Cài đặt các gói phụ thuộc:
```bash
# Ubuntu / Debian / Linux Mint:
sudo apt update
sudo apt install -y openjdk-17-jre python3 python3-tk

# Arch Linux:
sudo pacman -S jre17-openjdk python tk

# Fedora:
sudo dnf install java-17-openjdk python3 python3-tkinter
```

#### Cài đặt ứng dụng vào hệ thống (1 Lệnh duy nhất):
Chạy script cài đặt để tự động tích hợp Shimeji vào hệ thống:
```bash
./install-app.sh
```
Script này sẽ tự động:
- Cấp quyền thực thi cho các file script.
- Tạo lệnh chạy toàn cục trong Terminal: `shimeji` và `shimeji-settings`.
- Tạo biểu tượng ứng dụng trong **Menu Ứng Dụng (Application Launcher)** và ngoài **Desktop**.

#### Chạy thủ công không cần cài đặt:
```bash
# Khởi động mascot:
./launch.sh

# Mở giao diện cài đặt & đổi nhân vật:
./run-settings.sh
```

#### Gỡ cài đặt:
```bash
./uninstall-app.sh
```

> **Lưu ý với Wayland**: Mascot Shimeji tương tác tốt nhất trên giao diện **X11 / XOrg**. Nếu đang dùng Wayland (mặc định trên một số bản Ubuntu mới), bạn có thể chọn phiên bản *"Ubuntu on Xorg"* ở màn hình đăng nhập để mascot có thể nhảy bám lên các mép cửa sổ ứng dụng khác.

---

### 🍎 3. Trên macOS (Intel & Apple Silicon M1/M2/M3/M4)

#### Cài đặt các gói phụ thuộc qua Homebrew:
```bash
brew install openjdk@17 python-tk
```

#### Cấp quyền và khởi chạy:
1. Mở Terminal và điều hướng vào thư mục dự án:
   ```bash
   cd /path/to/shimeji
   chmod +x launch.sh run-settings.sh
   ```
2. **Khởi động Shimeji**:
   ```bash
   ./launch.sh
   ```
3. **Mở giao diện Cài Đặt**:
   ```bash
   ./run-settings.sh
   ```

> **Lưu ý trên macOS**: Trong lần đầu chạy, macOS có thể yêu cầu cấp quyền **Trợ năng (Accessibility)** và **Ghi màn hình (Screen Recording)** cho Terminal/Java trong *Cài đặt hệ thống > Quyền riêng tư & Bảo mật* để hiển thị cửa sổ trong suốt bám màn hình.

---

## 🎮 Hướng Dẫn Sử Dụng & Tương Tác

### Thao Tác Chuột Trực Tiếp Lên Nhân Vật:
- **Click chuột trái (1 lần)**: Nhân vật sẽ nói chuyện ngay lập tức (hiển thị câu thoại ngẫu nhiên qua bong bóng thoại).
- **Nhấn giữ chuột trái & Kéo**: Nhấc bổng và ném nhân vật bay lượn khắp màn hình!
- **Click chuột phải**: Mở menu thao tác:
  - `💬 Trò chuyện (Nói chuyện)`: Kích hoạt nói ngẫu nhiên.
  - `⏰ Lời nhắc tiếp theo`: Xem nội dung và thời gian còn lại của lời nhắc sắp tới.
  - `Quit / Dismiss`: Tắt riêng nhân vật này.
  - `Restore Window`: Khôi phục lại cửa sổ nếu nhân vật ném mất.

### Menu Biểu Tượng Khay Hệ Thống (System Tray):
Click chuột phải vào icon Shimeji ở góc thanh tác vụ (Taskbar) để:
- **Thêm nhân vật**: Tăng thêm mascot cùng loại trên màn hình.
- **Gom tụ nhân vật**: Gọi tất cả mascot tập trung về vị trí con trỏ chuột.
- **Giữ lại 1 nhân vật**: Giải tán tất cả mascot, chỉ giữ lại một bé duy nhất.
- **Mở Cài Đặt**: Khởi chạy nhanh cửa sổ Settings GUI.
- **Mở file cấu hình**: Mở nhanh `reminders.properties` và `dialogues.conf`.
- **Thoát**: Tắt hoàn toàn ứng dụng.

---

## ⚙️ Cấu Hình Nâng Cao

### 1. Cấu hình Lời Nhắc Sức Khỏe (`conf/reminders.properties`)
File này lưu các thiết lập nhắc nhở tự động:
- `reminders.enabled=true`: Bật/tắt toàn bộ lời nhắc.
- `reminders.sound.enabled=true`: Bật âm thanh beep khi có lời nhắc.
- `water.enabled=true` & `water.interval.minutes=45`: Nhắc uống nước sau mỗi 45 phút.
- `rest.enabled=true` & `rest.interval.minutes=60`: Nhắc nghỉ ngơi sau mỗi 60 phút.
- `fixed.time.X`: Đặt lịch nhắc cố định theo giờ trong ngày (ví dụ: `12:00` ăn trưa, `18:00` tan làm).

### 2. Tùy Chỉnh Câu Thoại (`conf/dialogues.conf`)
Mỗi dòng là một câu thoại ngẫu nhiên của mascot khi người dùng click vào bé. Bạn có thể tự do chỉnh sửa, thêm các câu thoại hài hước, động viên hoặc ghi nhớ công việc của riêng mình!

---

## 🎨 Hướng Dẫn Thêm Nhân Vật Mới (Custom Characters)

Để thêm nhân vật yêu thích của riêng bạn vào Shimeji:
1. Tạo một thư mục mới tại: `characters/TÊN_NHÂN_VẬT/`.
2. Đặt bộ ảnh sprite gồm 46 file ảnh định dạng PNG từ `shime1.png` đến `shime46.png` vào thư mục vừa tạo.
3. Mở **Settings GUI** (`./run-settings.sh` hoặc `ShimejiSettings.exe`).
4. Tìm tên nhân vật bạn vừa thêm từ danh sách, bấm **Áp dụng NV** hoặc **Thả NV này** để trải nghiệm ngay!

---

## 🛠️ Biên Dịch Từ Mã Nguồn (Build from Source)

### Trên Linux / macOS:
Yêu cầu đã cài đặt `ant` (`sudo apt install ant` hoặc `brew install ant`):
```bash
ant clean jar
```
File thực thi `Shimeji.jar` sẽ được đóng gói sẵn sàng trong thư mục gốc.

### Trên Windows:
Chạy trực tiếp file `build.bat` trong Command Prompt hoặc PowerShell (tự động biên dịch mã nguồn Java và C#):
```cmd
build.bat
```

---
---

# 🇬🇧 English

**Shimeji** is an open-source desktop mascot/pet application designed to run smoothly on **Windows 10/11**, **Linux** (Ubuntu, Debian, Fedora, Arch...), and **macOS**.

This edition features an extensive collection of **400+ anime & game characters**, an intelligent **speech bubble & health reminder system**, and a modern **cross-platform Settings GUI** with real-time search and live sprite previews.

---

## ✨ Features

- 🎭 **400+ Characters Library**: Genshin Impact, Vocaloid, Pokemon, Naruto, One Piece, Undertale, Marvel, and hundreds more.
- 💬 **Interactive Speech & Speech Bubbles**:
  - Smooth rounded speech bubbles over mascot heads with full text auto-wrapping.
  - **Left-click** on any mascot to chat instantly with randomized witty dialogues.
- ⏰ **Health & Productivity Reminders**:
  - Timed periodic reminders: drink water, eye rest breaks, stretching, meal times.
  - Optional sound alerts (beeps) and desktop notifications.
  - Right-click menu option **⏰ Next Reminder** to check pending alerts.
- 🖥️ **Modern Cross-Platform Settings GUI**:
  - **Live Search**: Instant filtering through 400+ characters.
  - **Live Sprite Preview**: Instant visual preview (`shime1.png`) before applying.
  - **Quick Controls**: *Spawn Selected*, *Spawn ALL*, *Kill All Mascots*.
  - Full configuration for window offsets (`window.conf`), window title filtering (`titles.conf`), and self-cloning toggles.
- ⚙️ **Cross-Platform & High-DPI Display Support**:
  - **Windows**: Native executables (`Shimeji.exe`, `ShimejiSettings.exe`), JNA Windows API integration, and fixed infinite falling bugs on scaled displays (125%, 150%, 200%).
  - **Linux**: One-command automated installer (`install-app.sh`), application menu shortcuts, and global terminal wrappers.
  - **macOS**: Native AWT/Swing compatibility across both Intel and Apple Silicon (M1/M2/M3/M4) chips.
  - Modern Java support: Fully compatible with **Java 8, 11, 17, and 21+**.

---

## 📋 Requirements

1. **Java**: JRE/JDK 8 or higher (Recommended: **OpenJDK 17** or **21**).
2. **Python**: Python 3.x with `tkinter` (for the Settings GUI).

---

## 🚀 Quick Start Guide by Operating System

### 🪟 1. Windows (10/11)

1. Download or clone this repository.
2. Ensure **Java** is installed ([Adoptium Temurin](https://adoptium.net/)).
3. **Run Mascot**:
   - Double-click **`Shimeji.exe`** (runs cleanly in background) or **`launch.bat`**.
4. **Open Settings**:
   - Double-click **`ShimejiSettings.exe`** or **`run-settings.bat`**.

---

### 🐧 2. Linux (Ubuntu / Debian / Fedora / Arch)

#### Install prerequisites:
```bash
# Ubuntu / Debian / Linux Mint:
sudo apt update
sudo apt install -y openjdk-17-jre python3 python3-tk

# Arch Linux:
sudo pacman -S jre17-openjdk python tk

# Fedora:
sudo dnf install java-17-openjdk python3 python3-tkinter
```

#### One-command system installation:
```bash
./install-app.sh
```
This script will automatically:
- Set execution permissions.
- Create global terminal commands: `shimeji` and `shimeji-settings`.
- Add desktop entries to your **Application Menu** and **Desktop**.

#### Run manually without installing:
```bash
./launch.sh
./run-settings.sh
```

#### Uninstall:
```bash
./uninstall-app.sh
```

---

### 🍎 3. macOS (Intel & Apple Silicon)

#### Install prerequisites via Homebrew:
```bash
brew install openjdk@17 python-tk
```

#### Launching:
```bash
cd /path/to/shimeji
chmod +x launch.sh run-settings.sh

# Start mascot:
./launch.sh

# Open settings:
./run-settings.sh
```

---

## 🎮 Mascot Controls & Interactions

- **Left-Click (1x)**: Mascot speaks a random dialogue in a speech bubble.
- **Left-Click & Drag**: Pick up and toss the mascot across your screen.
- **Right-Click**: Context menu (Quit, Next Reminder, Talk, Clone, Gather).
- **System Tray Icon**: Add mascots, gather mascots, keep only one, or open configurations.

---

## ⚙️ Configuration Files

- `conf/reminders.properties`: Configure hydration, rest intervals, sound alerts, and scheduled reminder times.
- `conf/dialogues.conf`: List of randomized speech lines shown when clicking on mascots.
- `window.conf`: Custom window offset adjustments.
- `titles.conf`: Target window title filter (leave blank to interact with all active windows).
- `settings.properties`: Mascot behavior settings (e.g., `selfCloningEnabled=true|false`).

---

## 🎨 Adding Custom Characters

1. Create a folder: `characters/YOUR_CHARACTER_NAME/`.
2. Add sprites `shime1.png` through `shime46.png` inside the folder.
3. Open Settings GUI (`./run-settings.sh` or `ShimejiSettings.exe`).
4. Select your character from the list and click **Apply Character** or **Spawn Selected**.

---

## 🛠️ Building from Source

- **Linux / macOS**:
  ```bash
  ant clean jar
  ```
- **Windows**:
  ```cmd
  build.bat
  ```

---


---

## 🎭 Danh Sách Toàn Bộ 400+ Nhân Vật / Full 400+ Character Gallery

Dưới đây là bộ sưu tập đầy đủ hơn **400 nhân vật** có sẵn trong dự án. Bạn có thể chọn bất kỳ nhân vật nào thông qua giao diện **Settings GUI** ( / ):

<table>
  <tr>
    <td align="center" width="16%"><img src="characters/Adventure_Time_Beemo/shime1.png" alt="Adventure Time Beemo" width="80" /><br/><sub><b>Adventure Time Beemo</b></sub></td>
    <td align="center" width="16%"><img src="characters/Adventure_Time_Finn/shime1.png" alt="Adventure Time Finn" width="80" /><br/><sub><b>Adventure Time Finn</b></sub></td>
    <td align="center" width="16%"><img src="characters/Adventure_Time_Fionna/shime1.png" alt="Adventure Time Fionna" width="80" /><br/><sub><b>Adventure Time Fionna</b></sub></td>
    <td align="center" width="16%"><img src="characters/Adventure_Time_Jake/shime1.png" alt="Adventure Time Jake" width="80" /><br/><sub><b>Adventure Time Jake</b></sub></td>
    <td align="center" width="16%"><img src="characters/Adventure_Time_Lumpy_Space_Princess/shime1.png" alt="Adventure Time Lumpy Space Princess" width="80" /><br/><sub><b>Adventure Time Lumpy Space Princess</b></sub></td>
    <td align="center" width="16%"><img src="characters/Adventure_Time_Marceline/shime1.png" alt="Adventure Time Marceline" width="80" /><br/><sub><b>Adventure Time Marceline</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Adventure_Time_Marshall_Lee/shime1.png" alt="Adventure Time Marshall Lee" width="80" /><br/><sub><b>Adventure Time Marshall Lee</b></sub></td>
    <td align="center" width="16%"><img src="characters/Alice_In_The_Country_Of_Hearts_Ace/shime1.png" alt="Alice In The Country Of Hearts Ace" width="80" /><br/><sub><b>Alice In The Country Of Hearts Ace</b></sub></td>
    <td align="center" width="16%"><img src="characters/Alice_In_The_Country_Of_Hearts_Boris/shime1.png" alt="Alice In The Country Of Hearts Boris" width="80" /><br/><sub><b>Alice In The Country Of Hearts Boris</b></sub></td>
    <td align="center" width="16%"><img src="characters/Alice_In_The_Country_Of_Hearts_Julius/shime1.png" alt="Alice In The Country Of Hearts Julius" width="80" /><br/><sub><b>Alice In The Country Of Hearts Julius</b></sub></td>
    <td align="center" width="16%"><img src="characters/Apex_Legends_Bangalore/shime1.png" alt="Apex Legends Bangalore" width="80" /><br/><sub><b>Apex Legends Bangalore</b></sub></td>
    <td align="center" width="16%"><img src="characters/Apex_Legends_Bloodhound/shime1.png" alt="Apex Legends Bloodhound" width="80" /><br/><sub><b>Apex Legends Bloodhound</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Apex_Legends_Caustic/shime1.png" alt="Apex Legends Caustic" width="80" /><br/><sub><b>Apex Legends Caustic</b></sub></td>
    <td align="center" width="16%"><img src="characters/Apex_Legends_Crypto/shime1.png" alt="Apex Legends Crypto" width="80" /><br/><sub><b>Apex Legends Crypto</b></sub></td>
    <td align="center" width="16%"><img src="characters/Apex_Legends_Lifeline/shime1.png" alt="Apex Legends Lifeline" width="80" /><br/><sub><b>Apex Legends Lifeline</b></sub></td>
    <td align="center" width="16%"><img src="characters/Apex_Legends_Loba/shime1.png" alt="Apex Legends Loba" width="80" /><br/><sub><b>Apex Legends Loba</b></sub></td>
    <td align="center" width="16%"><img src="characters/Apex_Legends_Octane/shime1.png" alt="Apex Legends Octane" width="80" /><br/><sub><b>Apex Legends Octane</b></sub></td>
    <td align="center" width="16%"><img src="characters/Apex_Legends_Pathfinder/shime1.png" alt="Apex Legends Pathfinder" width="80" /><br/><sub><b>Apex Legends Pathfinder</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Apex_Legends_Revenant/shime1.png" alt="Apex Legends Revenant" width="80" /><br/><sub><b>Apex Legends Revenant</b></sub></td>
    <td align="center" width="16%"><img src="characters/Apex_Legends_Wattson/shime1.png" alt="Apex Legends Wattson" width="80" /><br/><sub><b>Apex Legends Wattson</b></sub></td>
    <td align="center" width="16%"><img src="characters/Apex_Legends_Wraith/shime1.png" alt="Apex Legends Wraith" width="80" /><br/><sub><b>Apex Legends Wraith</b></sub></td>
    <td align="center" width="16%"><img src="characters/Assassins_Creed_Cesare/shime1.png" alt="Assassins Creed Cesare" width="80" /><br/><sub><b>Assassins Creed Cesare</b></sub></td>
    <td align="center" width="16%"><img src="characters/Assassins_Creed_Desmond/shime1.png" alt="Assassins Creed Desmond" width="80" /><br/><sub><b>Assassins Creed Desmond</b></sub></td>
    <td align="center" width="16%"><img src="characters/Assassins_Creed_Ezio/shime1.png" alt="Assassins Creed Ezio" width="80" /><br/><sub><b>Assassins Creed Ezio</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Assassins_Creed_Kadar/shime1.png" alt="Assassins Creed Kadar" width="80" /><br/><sub><b>Assassins Creed Kadar</b></sub></td>
    <td align="center" width="16%"><img src="characters/Assassins_Creed_Leonardo_Da_Vinci/shime1.png" alt="Assassins Creed Leonardo Da Vinci" width="80" /><br/><sub><b>Assassins Creed Leonardo Da Vinci</b></sub></td>
    <td align="center" width="16%"><img src="characters/Assassins_Creed_Malik/shime1.png" alt="Assassins Creed Malik" width="80" /><br/><sub><b>Assassins Creed Malik</b></sub></td>
    <td align="center" width="16%"><img src="characters/Assassins_Creed_Yusuf/shime1.png" alt="Assassins Creed Yusuf" width="80" /><br/><sub><b>Assassins Creed Yusuf</b></sub></td>
    <td align="center" width="16%"><img src="characters/Attack_On_Titan_Annie_Leonhardt/shime1.png" alt="Attack On Titan Annie Leonhardt" width="80" /><br/><sub><b>Attack On Titan Annie Leonhardt</b></sub></td>
    <td align="center" width="16%"><img src="characters/Attack_On_Titan_Armin_Arlert/shime1.png" alt="Attack On Titan Armin Arlert" width="80" /><br/><sub><b>Attack On Titan Armin Arlert</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Attack_On_Titan_Connie_Springer/shime1.png" alt="Attack On Titan Connie Springer" width="80" /><br/><sub><b>Attack On Titan Connie Springer</b></sub></td>
    <td align="center" width="16%"><img src="characters/Attack_On_Titan_Eren_Jaeger/shime1.png" alt="Attack On Titan Eren Jaeger" width="80" /><br/><sub><b>Attack On Titan Eren Jaeger</b></sub></td>
    <td align="center" width="16%"><img src="characters/Attack_On_Titan_Hanji_Zoe/shime1.png" alt="Attack On Titan Hanji Zoe" width="80" /><br/><sub><b>Attack On Titan Hanji Zoe</b></sub></td>
    <td align="center" width="16%"><img src="characters/Attack_On_Titan_Jean_Kirschtein/shime1.png" alt="Attack On Titan Jean Kirschtein" width="80" /><br/><sub><b>Attack On Titan Jean Kirschtein</b></sub></td>
    <td align="center" width="16%"><img src="characters/Attack_On_Titan_Mikasa_Ackerman/shime1.png" alt="Attack On Titan Mikasa Ackerman" width="80" /><br/><sub><b>Attack On Titan Mikasa Ackerman</b></sub></td>
    <td align="center" width="16%"><img src="characters/Attack_On_Titan_Sasha_Braus/shime1.png" alt="Attack On Titan Sasha Braus" width="80" /><br/><sub><b>Attack On Titan Sasha Braus</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Attack_On_Titan_Ymir/shime1.png" alt="Attack On Titan Ymir" width="80" /><br/><sub><b>Attack On Titan Ymir</b></sub></td>
    <td align="center" width="16%"><img src="characters/Ayaka/shime1.png" alt="Ayaka" width="80" /><br/><sub><b>Ayaka</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bbc_Sherlock_Jim_Moriarty/shime1.png" alt="Bbc Sherlock Jim Moriarty" width="80" /><br/><sub><b>Bbc Sherlock Jim Moriarty</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bbc_Sherlock_John_Watson/shime1.png" alt="Bbc Sherlock John Watson" width="80" /><br/><sub><b>Bbc Sherlock John Watson</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bbc_Sherlock_Mycroft/shime1.png" alt="Bbc Sherlock Mycroft" width="80" /><br/><sub><b>Bbc Sherlock Mycroft</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bbc_Sherlock_Sherlock/shime1.png" alt="Bbc Sherlock Sherlock" width="80" /><br/><sub><b>Bbc Sherlock Sherlock</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Bendy_And_The_Ink_Machine_Bendy/shime1.png" alt="Bendy And The Ink Machine Bendy" width="80" /><br/><sub><b>Bendy And The Ink Machine Bendy</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bioshock_Big_Daddy/shime1.png" alt="Bioshock Big Daddy" width="80" /><br/><sub><b>Bioshock Big Daddy</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bioshock_Fontaine/shime1.png" alt="Bioshock Fontaine" width="80" /><br/><sub><b>Bioshock Fontaine</b></sub></td>
    <td align="center" width="16%"><img src="characters/Black_Butler_Alois_Trancy/shime1.png" alt="Black Butler Alois Trancy" width="80" /><br/><sub><b>Black Butler Alois Trancy</b></sub></td>
    <td align="center" width="16%"><img src="characters/Black_Butler_Ciel_Phantomhive/shime1.png" alt="Black Butler Ciel Phantomhive" width="80" /><br/><sub><b>Black Butler Ciel Phantomhive</b></sub></td>
    <td align="center" width="16%"><img src="characters/Black_Butler_Grell/shime1.png" alt="Black Butler Grell" width="80" /><br/><sub><b>Black Butler Grell</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Black_Butler_Maylene/shime1.png" alt="Black Butler Maylene" width="80" /><br/><sub><b>Black Butler Maylene</b></sub></td>
    <td align="center" width="16%"><img src="characters/Black_Butler_Sebastian_Michaelis/shime1.png" alt="Black Butler Sebastian Michaelis" width="80" /><br/><sub><b>Black Butler Sebastian Michaelis</b></sub></td>
    <td align="center" width="16%"><img src="characters/Black_Butler_Undertaker/shime1.png" alt="Black Butler Undertaker" width="80" /><br/><sub><b>Black Butler Undertaker</b></sub></td>
    <td align="center" width="16%"><img src="characters/Black_Butler_William/shime1.png" alt="Black Butler William" width="80" /><br/><sub><b>Black Butler William</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bleach_Aizen/shime1.png" alt="Bleach Aizen" width="80" /><br/><sub><b>Bleach Aizen</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bleach_Byakuya_Kuchiki/shime1.png" alt="Bleach Byakuya Kuchiki" width="80" /><br/><sub><b>Bleach Byakuya Kuchiki</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Bleach_Gin_Ichimaru/shime1.png" alt="Bleach Gin Ichimaru" width="80" /><br/><sub><b>Bleach Gin Ichimaru</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bleach_Grimmjow/shime1.png" alt="Bleach Grimmjow" width="80" /><br/><sub><b>Bleach Grimmjow</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bleach_Hisagi_Shuuhei/shime1.png" alt="Bleach Hisagi Shuuhei" width="80" /><br/><sub><b>Bleach Hisagi Shuuhei</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bleach_Ichigo/shime1.png" alt="Bleach Ichigo" width="80" /><br/><sub><b>Bleach Ichigo</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bleach_Inoue_Orihime/shime1.png" alt="Bleach Inoue Orihime" width="80" /><br/><sub><b>Bleach Inoue Orihime</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bleach_Jushiro_Ukitake/shime1.png" alt="Bleach Jushiro Ukitake" width="80" /><br/><sub><b>Bleach Jushiro Ukitake</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Bleach_Renji_Abarai/shime1.png" alt="Bleach Renji Abarai" width="80" /><br/><sub><b>Bleach Renji Abarai</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bleach_Rukia/shime1.png" alt="Bleach Rukia" width="80" /><br/><sub><b>Bleach Rukia</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bleach_Shirosaki_Hichigo/shime1.png" alt="Bleach Shirosaki Hichigo" width="80" /><br/><sub><b>Bleach Shirosaki Hichigo</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bleach_Starrk/shime1.png" alt="Bleach Starrk" width="80" /><br/><sub><b>Bleach Starrk</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bleach_Szayel_Aporro/shime1.png" alt="Bleach Szayel Aporro" width="80" /><br/><sub><b>Bleach Szayel Aporro</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bleach_Ulquiorra/shime1.png" alt="Bleach Ulquiorra" width="80" /><br/><sub><b>Bleach Ulquiorra</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Bleach_Uryuu_Ishida/shime1.png" alt="Bleach Uryuu Ishida" width="80" /><br/><sub><b>Bleach Uryuu Ishida</b></sub></td>
    <td align="center" width="16%"><img src="characters/Blobs_Blob/shime1.png" alt="Blobs Blob" width="80" /><br/><sub><b>Blobs Blob</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bts_Bangtan_Boys_J_Hope_Hobi_Hyyh/shime1.png" alt="Bts Bangtan Boys J Hope Hobi Hyyh" width="80" /><br/><sub><b>Bts Bangtan Boys J Hope Hobi Hyyh</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bts_Bangtan_Boys_J_Hope_Hobi_Summer/shime1.png" alt="Bts Bangtan Boys J Hope Hobi Summer" width="80" /><br/><sub><b>Bts Bangtan Boys J Hope Hobi Summer</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bts_Bangtan_Boys_Jimin/shime1.png" alt="Bts Bangtan Boys Jimin" width="80" /><br/><sub><b>Bts Bangtan Boys Jimin</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bts_Bangtan_Boys_Jin/shime1.png" alt="Bts Bangtan Boys Jin" width="80" /><br/><sub><b>Bts Bangtan Boys Jin</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Bts_Bangtan_Boys_Jungkook_Kookie_Baby/shime1.png" alt="Bts Bangtan Boys Jungkook Kookie Baby" width="80" /><br/><sub><b>Bts Bangtan Boys Jungkook Kookie Baby</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bts_Bangtan_Boys_Suga/shime1.png" alt="Bts Bangtan Boys Suga" width="80" /><br/><sub><b>Bts Bangtan Boys Suga</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bts_Bangtan_Boys_V_Tae_Tae_Not_Today/shime1.png" alt="Bts Bangtan Boys V Tae Tae Not Today" width="80" /><br/><sub><b>Bts Bangtan Boys V Tae Tae Not Today</b></sub></td>
    <td align="center" width="16%"><img src="characters/Bts_Bangtan_Boys_V_Tae_Tae_Puppy/shime1.png" alt="Bts Bangtan Boys V Tae Tae Puppy" width="80" /><br/><sub><b>Bts Bangtan Boys V Tae Tae Puppy</b></sub></td>
    <td align="center" width="16%"><img src="characters/Creepypasta_Ben_Drowned/shime1.png" alt="Creepypasta Ben Drowned" width="80" /><br/><sub><b>Creepypasta Ben Drowned</b></sub></td>
    <td align="center" width="16%"><img src="characters/Creepypasta_Eyeless_Jack/shime1.png" alt="Creepypasta Eyeless Jack" width="80" /><br/><sub><b>Creepypasta Eyeless Jack</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Creepypasta_Hoody/shime1.png" alt="Creepypasta Hoody" width="80" /><br/><sub><b>Creepypasta Hoody</b></sub></td>
    <td align="center" width="16%"><img src="characters/Creepypasta_Jeff_The_Killer/shime1.png" alt="Creepypasta Jeff The Killer" width="80" /><br/><sub><b>Creepypasta Jeff The Killer</b></sub></td>
    <td align="center" width="16%"><img src="characters/Creepypasta_Kagekao/shime1.png" alt="Creepypasta Kagekao" width="80" /><br/><sub><b>Creepypasta Kagekao</b></sub></td>
    <td align="center" width="16%"><img src="characters/Creepypasta_Laughing_Jack/shime1.png" alt="Creepypasta Laughing Jack" width="80" /><br/><sub><b>Creepypasta Laughing Jack</b></sub></td>
    <td align="center" width="16%"><img src="characters/Creepypasta_Lost_Silver/shime1.png" alt="Creepypasta Lost Silver" width="80" /><br/><sub><b>Creepypasta Lost Silver</b></sub></td>
    <td align="center" width="16%"><img src="characters/Creepypasta_Masky/shime1.png" alt="Creepypasta Masky" width="80" /><br/><sub><b>Creepypasta Masky</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Creepypasta_Rake/shime1.png" alt="Creepypasta Rake" width="80" /><br/><sub><b>Creepypasta Rake</b></sub></td>
    <td align="center" width="16%"><img src="characters/Creepypasta_Ticci_Toby/shime1.png" alt="Creepypasta Ticci Toby" width="80" /><br/><sub><b>Creepypasta Ticci Toby</b></sub></td>
    <td align="center" width="16%"><img src="characters/Creepypasta_Zehnder/shime1.png" alt="Creepypasta Zehnder" width="80" /><br/><sub><b>Creepypasta Zehnder</b></sub></td>
    <td align="center" width="16%"><img src="characters/Danganronpa_Kokichi_Oma/shime1.png" alt="Danganronpa Kokichi Oma" width="80" /><br/><sub><b>Danganronpa Kokichi Oma</b></sub></td>
    <td align="center" width="16%"><img src="characters/Deathnote_Beyond_Birthday/shime1.png" alt="Deathnote Beyond Birthday" width="80" /><br/><sub><b>Deathnote Beyond Birthday</b></sub></td>
    <td align="center" width="16%"><img src="characters/Deathnote_Matt/shime1.png" alt="Deathnote Matt" width="80" /><br/><sub><b>Deathnote Matt</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Digimon_Agumon/shime1.png" alt="Digimon Agumon" width="80" /><br/><sub><b>Digimon Agumon</b></sub></td>
    <td align="center" width="16%"><img src="characters/Digimon_Culumon/shime1.png" alt="Digimon Culumon" width="80" /><br/><sub><b>Digimon Culumon</b></sub></td>
    <td align="center" width="16%"><img src="characters/Digimon_Gatomon/shime1.png" alt="Digimon Gatomon" width="80" /><br/><sub><b>Digimon Gatomon</b></sub></td>
    <td align="center" width="16%"><img src="characters/Digimon_Patamon/shime1.png" alt="Digimon Patamon" width="80" /><br/><sub><b>Digimon Patamon</b></sub></td>
    <td align="center" width="16%"><img src="characters/Digimon_Tanemon/shime1.png" alt="Digimon Tanemon" width="80" /><br/><sub><b>Digimon Tanemon</b></sub></td>
    <td align="center" width="16%"><img src="characters/Digimon_Terriemon/shime1.png" alt="Digimon Terriemon" width="80" /><br/><sub><b>Digimon Terriemon</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Disney_Movies_Ariel_And_Meg/shime1.png" alt="Disney Movies Ariel And Meg" width="80" /><br/><sub><b>Disney Movies Ariel And Meg</b></sub></td>
    <td align="center" width="16%"><img src="characters/Disney_Movies_Clopin_Trouillefou/shime1.png" alt="Disney Movies Clopin Trouillefou" width="80" /><br/><sub><b>Disney Movies Clopin Trouillefou</b></sub></td>
    <td align="center" width="16%"><img src="characters/Disney_Movies_Flynn_Rider/shime1.png" alt="Disney Movies Flynn Rider" width="80" /><br/><sub><b>Disney Movies Flynn Rider</b></sub></td>
    <td align="center" width="16%"><img src="characters/Disney_Movies_Rapunzel_Braided_Hair/shime1.png" alt="Disney Movies Rapunzel Braided Hair" width="80" /><br/><sub><b>Disney Movies Rapunzel Braided Hair</b></sub></td>
    <td align="center" width="16%"><img src="characters/Disney_Movies_Rapunzel_Brunette/shime1.png" alt="Disney Movies Rapunzel Brunette" width="80" /><br/><sub><b>Disney Movies Rapunzel Brunette</b></sub></td>
    <td align="center" width="16%"><img src="characters/Dragon_Ball_Z_Goku/shime1.png" alt="Dragon Ball Z Goku" width="80" /><br/><sub><b>Dragon Ball Z Goku</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Dragon_Ball_Z_Vegeta/shime1.png" alt="Dragon Ball Z Vegeta" width="80" /><br/><sub><b>Dragon Ball Z Vegeta</b></sub></td>
    <td align="center" width="16%"><img src="characters/Dream_Smp_Bad_Boy_Halo/shime1.png" alt="Dream Smp Bad Boy Halo" width="80" /><br/><sub><b>Dream Smp Bad Boy Halo</b></sub></td>
    <td align="center" width="16%"><img src="characters/Dream_Smp_Dream/shime1.png" alt="Dream Smp Dream" width="80" /><br/><sub><b>Dream Smp Dream</b></sub></td>
    <td align="center" width="16%"><img src="characters/Dream_Smp_Fundy/shime1.png" alt="Dream Smp Fundy" width="80" /><br/><sub><b>Dream Smp Fundy</b></sub></td>
    <td align="center" width="16%"><img src="characters/Dream_Smp_George/shime1.png" alt="Dream Smp George" width="80" /><br/><sub><b>Dream Smp George</b></sub></td>
    <td align="center" width="16%"><img src="characters/Dream_Smp_Ghostbur/shime1.png" alt="Dream Smp Ghostbur" width="80" /><br/><sub><b>Dream Smp Ghostbur</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Dream_Smp_Ranboo/shime1.png" alt="Dream Smp Ranboo" width="80" /><br/><sub><b>Dream Smp Ranboo</b></sub></td>
    <td align="center" width="16%"><img src="characters/Dream_Smp_Sapnap/shime1.png" alt="Dream Smp Sapnap" width="80" /><br/><sub><b>Dream Smp Sapnap</b></sub></td>
    <td align="center" width="16%"><img src="characters/Dream_Smp_Technoblade/shime1.png" alt="Dream Smp Technoblade" width="80" /><br/><sub><b>Dream Smp Technoblade</b></sub></td>
    <td align="center" width="16%"><img src="characters/Durarara_Celty_Sturluson/shime1.png" alt="Durarara Celty Sturluson" width="80" /><br/><sub><b>Durarara Celty Sturluson</b></sub></td>
    <td align="center" width="16%"><img src="characters/Durarara_Delic_Heiwajima/shime1.png" alt="Durarara Delic Heiwajima" width="80" /><br/><sub><b>Durarara Delic Heiwajima</b></sub></td>
    <td align="center" width="16%"><img src="characters/Durarara_Hachimenroppi_Orihara/shime1.png" alt="Durarara Hachimenroppi Orihara" width="80" /><br/><sub><b>Durarara Hachimenroppi Orihara</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Durarara_Hibiya_Orihara/shime1.png" alt="Durarara Hibiya Orihara" width="80" /><br/><sub><b>Durarara Hibiya Orihara</b></sub></td>
    <td align="center" width="16%"><img src="characters/Durarara_Izaya_Orihara/shime1.png" alt="Durarara Izaya Orihara" width="80" /><br/><sub><b>Durarara Izaya Orihara</b></sub></td>
    <td align="center" width="16%"><img src="characters/Durarara_Izaya_Orihara_05/shime1.png" alt="Durarara Izaya Orihara 05" width="80" /><br/><sub><b>Durarara Izaya Orihara 05</b></sub></td>
    <td align="center" width="16%"><img src="characters/Durarara_Izaya_Orihara_06/shime1.png" alt="Durarara Izaya Orihara 06" width="80" /><br/><sub><b>Durarara Izaya Orihara 06</b></sub></td>
    <td align="center" width="16%"><img src="characters/Durarara_Masaomi_Kida/shime1.png" alt="Durarara Masaomi Kida" width="80" /><br/><sub><b>Durarara Masaomi Kida</b></sub></td>
    <td align="center" width="16%"><img src="characters/Durarara_Mikado_Ryuugamine/shime1.png" alt="Durarara Mikado Ryuugamine" width="80" /><br/><sub><b>Durarara Mikado Ryuugamine</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Durarara_Psyche_Orihara/shime1.png" alt="Durarara Psyche Orihara" width="80" /><br/><sub><b>Durarara Psyche Orihara</b></sub></td>
    <td align="center" width="16%"><img src="characters/Durarara_Shinra_Kishitani/shime1.png" alt="Durarara Shinra Kishitani" width="80" /><br/><sub><b>Durarara Shinra Kishitani</b></sub></td>
    <td align="center" width="16%"><img src="characters/Durarara_Shizuo_And_Izaya/shime1.png" alt="Durarara Shizuo And Izaya" width="80" /><br/><sub><b>Durarara Shizuo And Izaya</b></sub></td>
    <td align="center" width="16%"><img src="characters/Durarara_Shizuo_Hejiwama/shime1.png" alt="Durarara Shizuo Hejiwama" width="80" /><br/><sub><b>Durarara Shizuo Hejiwama</b></sub></td>
    <td align="center" width="16%"><img src="characters/Durarara_Shizuo_Hejiwama_05/shime1.png" alt="Durarara Shizuo Hejiwama 05" width="80" /><br/><sub><b>Durarara Shizuo Hejiwama 05</b></sub></td>
    <td align="center" width="16%"><img src="characters/Durarara_Tsugaru_Kaikyo_Fuyu_Geshiki/shime1.png" alt="Durarara Tsugaru Kaikyo Fuyu Geshiki" width="80" /><br/><sub><b>Durarara Tsugaru Kaikyo Fuyu Geshiki</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Eddsworld_Edd/shime1.png" alt="Eddsworld Edd" width="80" /><br/><sub><b>Eddsworld Edd</b></sub></td>
    <td align="center" width="16%"><img src="characters/Eddsworld_Future_Edd/shime1.png" alt="Eddsworld Future Edd" width="80" /><br/><sub><b>Eddsworld Future Edd</b></sub></td>
    <td align="center" width="16%"><img src="characters/Eddsworld_Jon/shime1.png" alt="Eddsworld Jon" width="80" /><br/><sub><b>Eddsworld Jon</b></sub></td>
    <td align="center" width="16%"><img src="characters/Eddsworld_Matt/shime1.png" alt="Eddsworld Matt" width="80" /><br/><sub><b>Eddsworld Matt</b></sub></td>
    <td align="center" width="16%"><img src="characters/Eddsworld_Paul/shime1.png" alt="Eddsworld Paul" width="80" /><br/><sub><b>Eddsworld Paul</b></sub></td>
    <td align="center" width="16%"><img src="characters/Eddsworld_Tom/shime1.png" alt="Eddsworld Tom" width="80" /><br/><sub><b>Eddsworld Tom</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Eddsworld_Tord/shime1.png" alt="Eddsworld Tord" width="80" /><br/><sub><b>Eddsworld Tord</b></sub></td>
    <td align="center" width="16%"><img src="characters/Fairy_Tail_Erza_Scarlet/shime1.png" alt="Fairy Tail Erza Scarlet" width="80" /><br/><sub><b>Fairy Tail Erza Scarlet</b></sub></td>
    <td align="center" width="16%"><img src="characters/Fairy_Tail_Freed/shime1.png" alt="Fairy Tail Freed" width="80" /><br/><sub><b>Fairy Tail Freed</b></sub></td>
    <td align="center" width="16%"><img src="characters/Fairy_Tail_Jackal/shime1.png" alt="Fairy Tail Jackal" width="80" /><br/><sub><b>Fairy Tail Jackal</b></sub></td>
    <td align="center" width="16%"><img src="characters/Fairy_Tail_Natsu/shime1.png" alt="Fairy Tail Natsu" width="80" /><br/><sub><b>Fairy Tail Natsu</b></sub></td>
    <td align="center" width="16%"><img src="characters/Fairy_Tail_Rogue/shime1.png" alt="Fairy Tail Rogue" width="80" /><br/><sub><b>Fairy Tail Rogue</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Fairy_Tail_Sting/shime1.png" alt="Fairy Tail Sting" width="80" /><br/><sub><b>Fairy Tail Sting</b></sub></td>
    <td align="center" width="16%"><img src="characters/Fairy_Tail_Zeref/shime1.png" alt="Fairy Tail Zeref" width="80" /><br/><sub><b>Fairy Tail Zeref</b></sub></td>
    <td align="center" width="16%"><img src="characters/Five_Nights_At_Freddys_Chica/shime1.png" alt="Five Nights At Freddys Chica" width="80" /><br/><sub><b>Five Nights At Freddys Chica</b></sub></td>
    <td align="center" width="16%"><img src="characters/Five_Nights_At_Freddys_Foxy/shime1.png" alt="Five Nights At Freddys Foxy" width="80" /><br/><sub><b>Five Nights At Freddys Foxy</b></sub></td>
    <td align="center" width="16%"><img src="characters/Five_Nights_At_Freddys_Mangle/shime1.png" alt="Five Nights At Freddys Mangle" width="80" /><br/><sub><b>Five Nights At Freddys Mangle</b></sub></td>
    <td align="center" width="16%"><img src="characters/Five_Nights_At_Freddys_Purple_Guy/shime1.png" alt="Five Nights At Freddys Purple Guy" width="80" /><br/><sub><b>Five Nights At Freddys Purple Guy</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Five_Nights_At_Freddys_Pyro_Foxy/shime1.png" alt="Five Nights At Freddys Pyro Foxy" width="80" /><br/><sub><b>Five Nights At Freddys Pyro Foxy</b></sub></td>
    <td align="center" width="16%"><img src="characters/Five_Nights_At_Freddys_The_Puppet/shime1.png" alt="Five Nights At Freddys The Puppet" width="80" /><br/><sub><b>Five Nights At Freddys The Puppet</b></sub></td>
    <td align="center" width="16%"><img src="characters/Five_Nights_At_Freddys_Toy_Bonnie/shime1.png" alt="Five Nights At Freddys Toy Bonnie" width="80" /><br/><sub><b>Five Nights At Freddys Toy Bonnie</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Aether/shime1.png" alt="Genshin Impact Aether" width="80" /><br/><sub><b>Genshin Impact Aether</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Albedo/shime1.png" alt="Genshin Impact Albedo" width="80" /><br/><sub><b>Genshin Impact Albedo</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Ayaka/shime1.png" alt="Genshin Impact Ayaka" width="80" /><br/><sub><b>Genshin Impact Ayaka</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Childe/shime1.png" alt="Genshin Impact Childe" width="80" /><br/><sub><b>Genshin Impact Childe</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Chongyun/shime1.png" alt="Genshin Impact Chongyun" width="80" /><br/><sub><b>Genshin Impact Chongyun</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Diluc/shime1.png" alt="Genshin Impact Diluc" width="80" /><br/><sub><b>Genshin Impact Diluc</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Hu_Tao/shime1.png" alt="Genshin Impact Hu Tao" width="80" /><br/><sub><b>Genshin Impact Hu Tao</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Kaeya/shime1.png" alt="Genshin Impact Kaeya" width="80" /><br/><sub><b>Genshin Impact Kaeya</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Kazuha/shime1.png" alt="Genshin Impact Kazuha" width="80" /><br/><sub><b>Genshin Impact Kazuha</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Klee/shime1.png" alt="Genshin Impact Klee" width="80" /><br/><sub><b>Genshin Impact Klee</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Lumine/shime1.png" alt="Genshin Impact Lumine" width="80" /><br/><sub><b>Genshin Impact Lumine</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Razor/shime1.png" alt="Genshin Impact Razor" width="80" /><br/><sub><b>Genshin Impact Razor</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Thoma/shime1.png" alt="Genshin Impact Thoma" width="80" /><br/><sub><b>Genshin Impact Thoma</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Venti/shime1.png" alt="Genshin Impact Venti" width="80" /><br/><sub><b>Genshin Impact Venti</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Xiao/shime1.png" alt="Genshin Impact Xiao" width="80" /><br/><sub><b>Genshin Impact Xiao</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Xiao_Catboy/shime1.png" alt="Genshin Impact Xiao Catboy" width="80" /><br/><sub><b>Genshin Impact Xiao Catboy</b></sub></td>
    <td align="center" width="16%"><img src="characters/Genshin_Impact_Zhongli/shime1.png" alt="Genshin Impact Zhongli" width="80" /><br/><sub><b>Genshin Impact Zhongli</b></sub></td>
    <td align="center" width="16%"><img src="characters/Gravity_Falls_Bill_Cipher/shime1.png" alt="Gravity Falls Bill Cipher" width="80" /><br/><sub><b>Gravity Falls Bill Cipher</b></sub></td>
    <td align="center" width="16%"><img src="characters/Gravity_Falls_Mabel_Pines/shime1.png" alt="Gravity Falls Mabel Pines" width="80" /><br/><sub><b>Gravity Falls Mabel Pines</b></sub></td>
    <td align="center" width="16%"><img src="characters/Group_Finity_Blank_Guy/shime1.png" alt="Group Finity Blank Guy" width="80" /><br/><sub><b>Group Finity Blank Guy</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_America/shime1.png" alt="Hetalia America" width="80" /><br/><sub><b>Hetalia America</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Hetalia_Austria/shime1.png" alt="Hetalia Austria" width="80" /><br/><sub><b>Hetalia Austria</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Belarus/shime1.png" alt="Hetalia Belarus" width="80" /><br/><sub><b>Hetalia Belarus</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Belgium/shime1.png" alt="Hetalia Belgium" width="80" /><br/><sub><b>Hetalia Belgium</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Canada/shime1.png" alt="Hetalia Canada" width="80" /><br/><sub><b>Hetalia Canada</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_China/shime1.png" alt="Hetalia China" width="80" /><br/><sub><b>Hetalia China</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Denmark/shime1.png" alt="Hetalia Denmark" width="80" /><br/><sub><b>Hetalia Denmark</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Hetalia_England/shime1.png" alt="Hetalia England" width="80" /><br/><sub><b>Hetalia England</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Estonia/shime1.png" alt="Hetalia Estonia" width="80" /><br/><sub><b>Hetalia Estonia</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Finland/shime1.png" alt="Hetalia Finland" width="80" /><br/><sub><b>Hetalia Finland</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_France/shime1.png" alt="Hetalia France" width="80" /><br/><sub><b>Hetalia France</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Germany/shime1.png" alt="Hetalia Germany" width="80" /><br/><sub><b>Hetalia Germany</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Greece/shime1.png" alt="Hetalia Greece" width="80" /><br/><sub><b>Hetalia Greece</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Hetalia_Hong_Kong/shime1.png" alt="Hetalia Hong Kong" width="80" /><br/><sub><b>Hetalia Hong Kong</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Hre/shime1.png" alt="Hetalia Hre" width="80" /><br/><sub><b>Hetalia Hre</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Hungary/shime1.png" alt="Hetalia Hungary" width="80" /><br/><sub><b>Hetalia Hungary</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Iceland/shime1.png" alt="Hetalia Iceland" width="80" /><br/><sub><b>Hetalia Iceland</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Italy/shime1.png" alt="Hetalia Italy" width="80" /><br/><sub><b>Hetalia Italy</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Japan/shime1.png" alt="Hetalia Japan" width="80" /><br/><sub><b>Hetalia Japan</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Hetalia_Kugelmugel/shime1.png" alt="Hetalia Kugelmugel" width="80" /><br/><sub><b>Hetalia Kugelmugel</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Latvia/shime1.png" alt="Hetalia Latvia" width="80" /><br/><sub><b>Hetalia Latvia</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Liechtenstein/shime1.png" alt="Hetalia Liechtenstein" width="80" /><br/><sub><b>Hetalia Liechtenstein</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Lithuania/shime1.png" alt="Hetalia Lithuania" width="80" /><br/><sub><b>Hetalia Lithuania</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Netherlands/shime1.png" alt="Hetalia Netherlands" width="80" /><br/><sub><b>Hetalia Netherlands</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Norway/shime1.png" alt="Hetalia Norway" width="80" /><br/><sub><b>Hetalia Norway</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Hetalia_Poland/shime1.png" alt="Hetalia Poland" width="80" /><br/><sub><b>Hetalia Poland</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Prussia/shime1.png" alt="Hetalia Prussia" width="80" /><br/><sub><b>Hetalia Prussia</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Romano/shime1.png" alt="Hetalia Romano" width="80" /><br/><sub><b>Hetalia Romano</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Russia/shime1.png" alt="Hetalia Russia" width="80" /><br/><sub><b>Hetalia Russia</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Scotland/shime1.png" alt="Hetalia Scotland" width="80" /><br/><sub><b>Hetalia Scotland</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Sealand/shime1.png" alt="Hetalia Sealand" width="80" /><br/><sub><b>Hetalia Sealand</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Hetalia_Seychelles/shime1.png" alt="Hetalia Seychelles" width="80" /><br/><sub><b>Hetalia Seychelles</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_South_Korea/shime1.png" alt="Hetalia South Korea" width="80" /><br/><sub><b>Hetalia South Korea</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Spain/shime1.png" alt="Hetalia Spain" width="80" /><br/><sub><b>Hetalia Spain</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Sweden/shime1.png" alt="Hetalia Sweden" width="80" /><br/><sub><b>Hetalia Sweden</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Switzerland/shime1.png" alt="Hetalia Switzerland" width="80" /><br/><sub><b>Hetalia Switzerland</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hetalia_Thailand/shime1.png" alt="Hetalia Thailand" width="80" /><br/><sub><b>Hetalia Thailand</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Hetalia_Vietnam/shime1.png" alt="Hetalia Vietnam" width="80" /><br/><sub><b>Hetalia Vietnam</b></sub></td>
    <td align="center" width="16%"><img src="characters/Homestuck_Dave_Strider/shime1.png" alt="Homestuck Dave Strider" width="80" /><br/><sub><b>Homestuck Dave Strider</b></sub></td>
    <td align="center" width="16%"><img src="characters/Homestuck_Equius/shime1.png" alt="Homestuck Equius" width="80" /><br/><sub><b>Homestuck Equius</b></sub></td>
    <td align="center" width="16%"><img src="characters/Homestuck_Eridan/shime1.png" alt="Homestuck Eridan" width="80" /><br/><sub><b>Homestuck Eridan</b></sub></td>
    <td align="center" width="16%"><img src="characters/Homestuck_Feferi/shime1.png" alt="Homestuck Feferi" width="80" /><br/><sub><b>Homestuck Feferi</b></sub></td>
    <td align="center" width="16%"><img src="characters/Homestuck_Gamzee_Makara/shime1.png" alt="Homestuck Gamzee Makara" width="80" /><br/><sub><b>Homestuck Gamzee Makara</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Homestuck_Kanaya/shime1.png" alt="Homestuck Kanaya" width="80" /><br/><sub><b>Homestuck Kanaya</b></sub></td>
    <td align="center" width="16%"><img src="characters/Homestuck_Sollux/shime1.png" alt="Homestuck Sollux" width="80" /><br/><sub><b>Homestuck Sollux</b></sub></td>
    <td align="center" width="16%"><img src="characters/Homestuck_Terezi/shime1.png" alt="Homestuck Terezi" width="80" /><br/><sub><b>Homestuck Terezi</b></sub></td>
    <td align="center" width="16%"><img src="characters/Homestuck_Vriska/shime1.png" alt="Homestuck Vriska" width="80" /><br/><sub><b>Homestuck Vriska</b></sub></td>
    <td align="center" width="16%"><img src="characters/Hunter_X_Hunter_Killua/shime1.png" alt="Hunter X Hunter Killua" width="80" /><br/><sub><b>Hunter X Hunter Killua</b></sub></td>
    <td align="center" width="16%"><img src="characters/It_2017_Pennywise/shime1.png" alt="It 2017 Pennywise" width="80" /><br/><sub><b>It 2017 Pennywise</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Jojos_Bizarre_Adventure_Dio/shime1.png" alt="Jojos Bizarre Adventure Dio" width="80" /><br/><sub><b>Jojos Bizarre Adventure Dio</b></sub></td>
    <td align="center" width="16%"><img src="characters/Jojos_Bizarre_Adventure_Kakyoin_Noriaki/shime1.png" alt="Jojos Bizarre Adventure Kakyoin Noriaki" width="80" /><br/><sub><b>Jojos Bizarre Adventure Kakyoin Noriaki</b></sub></td>
    <td align="center" width="16%"><img src="characters/Kingdom_Hearts_Aqua/shime1.png" alt="Kingdom Hearts Aqua" width="80" /><br/><sub><b>Kingdom Hearts Aqua</b></sub></td>
    <td align="center" width="16%"><img src="characters/Kingdom_Hearts_Axel/shime1.png" alt="Kingdom Hearts Axel" width="80" /><br/><sub><b>Kingdom Hearts Axel</b></sub></td>
    <td align="center" width="16%"><img src="characters/Kingdom_Hearts_Demyx/shime1.png" alt="Kingdom Hearts Demyx" width="80" /><br/><sub><b>Kingdom Hearts Demyx</b></sub></td>
    <td align="center" width="16%"><img src="characters/Kingdom_Hearts_Ienzo/shime1.png" alt="Kingdom Hearts Ienzo" width="80" /><br/><sub><b>Kingdom Hearts Ienzo</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Kingdom_Hearts_Riku/shime1.png" alt="Kingdom Hearts Riku" width="80" /><br/><sub><b>Kingdom Hearts Riku</b></sub></td>
    <td align="center" width="16%"><img src="characters/Kingdom_Hearts_Roxas/shime1.png" alt="Kingdom Hearts Roxas" width="80" /><br/><sub><b>Kingdom Hearts Roxas</b></sub></td>
    <td align="center" width="16%"><img src="characters/Kingdom_Hearts_Sora/shime1.png" alt="Kingdom Hearts Sora" width="80" /><br/><sub><b>Kingdom Hearts Sora</b></sub></td>
    <td align="center" width="16%"><img src="characters/Kingdom_Hearts_Terra/shime1.png" alt="Kingdom Hearts Terra" width="80" /><br/><sub><b>Kingdom Hearts Terra</b></sub></td>
    <td align="center" width="16%"><img src="characters/Kingdom_Hearts_Vanitas/shime1.png" alt="Kingdom Hearts Vanitas" width="80" /><br/><sub><b>Kingdom Hearts Vanitas</b></sub></td>
    <td align="center" width="16%"><img src="characters/Kingdom_Hearts_Xemnas/shime1.png" alt="Kingdom Hearts Xemnas" width="80" /><br/><sub><b>Kingdom Hearts Xemnas</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Mario_Bowser/shime1.png" alt="Mario Bowser" width="80" /><br/><sub><b>Mario Bowser</b></sub></td>
    <td align="center" width="16%"><img src="characters/Mario_Luigi/shime1.png" alt="Mario Luigi" width="80" /><br/><sub><b>Mario Luigi</b></sub></td>
    <td align="center" width="16%"><img src="characters/Mario_Mario/shime1.png" alt="Mario Mario" width="80" /><br/><sub><b>Mario Mario</b></sub></td>
    <td align="center" width="16%"><img src="characters/Mario_Peach/shime1.png" alt="Mario Peach" width="80" /><br/><sub><b>Mario Peach</b></sub></td>
    <td align="center" width="16%"><img src="characters/Mario_Yoshi/shime1.png" alt="Mario Yoshi" width="80" /><br/><sub><b>Mario Yoshi</b></sub></td>
    <td align="center" width="16%"><img src="characters/Miku/shime1.png" alt="Miku" width="80" /><br/><sub><b>Miku</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Miraculous_Cat_Noir/shime1.png" alt="Miraculous Cat Noir" width="80" /><br/><sub><b>Miraculous Cat Noir</b></sub></td>
    <td align="center" width="16%"><img src="characters/Miraculous_Ladybug/shime1.png" alt="Miraculous Ladybug" width="80" /><br/><sub><b>Miraculous Ladybug</b></sub></td>
    <td align="center" width="16%"><img src="characters/My_Chemical_Romance_Bob_Bryar/shime1.png" alt="My Chemical Romance Bob Bryar" width="80" /><br/><sub><b>My Chemical Romance Bob Bryar</b></sub></td>
    <td align="center" width="16%"><img src="characters/My_Chemical_Romance_Frank_Iero/shime1.png" alt="My Chemical Romance Frank Iero" width="80" /><br/><sub><b>My Chemical Romance Frank Iero</b></sub></td>
    <td align="center" width="16%"><img src="characters/My_Chemical_Romance_Gerard_Way/shime1.png" alt="My Chemical Romance Gerard Way" width="80" /><br/><sub><b>My Chemical Romance Gerard Way</b></sub></td>
    <td align="center" width="16%"><img src="characters/My_Chemical_Romance_Mikey_Way/shime1.png" alt="My Chemical Romance Mikey Way" width="80" /><br/><sub><b>My Chemical Romance Mikey Way</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/My_Chemical_Romance_Ray_Toro/shime1.png" alt="My Chemical Romance Ray Toro" width="80" /><br/><sub><b>My Chemical Romance Ray Toro</b></sub></td>
    <td align="center" width="16%"><img src="characters/My_Hero_Academia_Katsuki_Bakugo_Kacchan/shime1.png" alt="My Hero Academia Katsuki Bakugo Kacchan" width="80" /><br/><sub><b>My Hero Academia Katsuki Bakugo Kacchan</b></sub></td>
    <td align="center" width="16%"><img src="characters/My_Hero_Academia_Keigo_Takami_Wing_Hero_Hawks/shime1.png" alt="My Hero Academia Keigo Takami Wing Hero Hawks" width="80" /><br/><sub><b>My Hero Academia Keigo Takami Wing Hero Hawks</b></sub></td>
    <td align="center" width="16%"><img src="characters/My_Hero_Academia_Ochako_Uraraka_Uravity/shime1.png" alt="My Hero Academia Ochako Uraraka Uravity" width="80" /><br/><sub><b>My Hero Academia Ochako Uraraka Uravity</b></sub></td>
    <td align="center" width="16%"><img src="characters/My_Hero_Academia_Shota_Aizawa_Eraser_Head/shime1.png" alt="My Hero Academia Shota Aizawa Eraser Head" width="80" /><br/><sub><b>My Hero Academia Shota Aizawa Eraser Head</b></sub></td>
    <td align="center" width="16%"><img src="characters/My_Hero_Academia_Tenko_Shimura_Tomura_Shigaraki/shime1.png" alt="My Hero Academia Tenko Shimura Tomura Shigaraki" width="80" /><br/><sub><b>My Hero Academia Tenko Shimura Tomura Shigaraki</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/My_Hero_Academia_Toshinori_Yagi_All_Might/shime1.png" alt="My Hero Academia Toshinori Yagi All Might" width="80" /><br/><sub><b>My Hero Academia Toshinori Yagi All Might</b></sub></td>
    <td align="center" width="16%"><img src="characters/Mystic_Messenger_707/shime1.png" alt="Mystic Messenger 707" width="80" /><br/><sub><b>Mystic Messenger 707</b></sub></td>
    <td align="center" width="16%"><img src="characters/Naruto_Deidara/shime1.png" alt="Naruto Deidara" width="80" /><br/><sub><b>Naruto Deidara</b></sub></td>
    <td align="center" width="16%"><img src="characters/Naruto_Gaara/shime1.png" alt="Naruto Gaara" width="80" /><br/><sub><b>Naruto Gaara</b></sub></td>
    <td align="center" width="16%"><img src="characters/Naruto_Hidan/shime1.png" alt="Naruto Hidan" width="80" /><br/><sub><b>Naruto Hidan</b></sub></td>
    <td align="center" width="16%"><img src="characters/Naruto_Hinata/shime1.png" alt="Naruto Hinata" width="80" /><br/><sub><b>Naruto Hinata</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Naruto_Kakashi/shime1.png" alt="Naruto Kakashi" width="80" /><br/><sub><b>Naruto Kakashi</b></sub></td>
    <td align="center" width="16%"><img src="characters/Naruto_Naruto_Uzumaki/shime1.png" alt="Naruto Naruto Uzumaki" width="80" /><br/><sub><b>Naruto Naruto Uzumaki</b></sub></td>
    <td align="center" width="16%"><img src="characters/Naruto_Neji/shime1.png" alt="Naruto Neji" width="80" /><br/><sub><b>Naruto Neji</b></sub></td>
    <td align="center" width="16%"><img src="characters/Naruto_Pein/shime1.png" alt="Naruto Pein" width="80" /><br/><sub><b>Naruto Pein</b></sub></td>
    <td align="center" width="16%"><img src="characters/Naruto_Sasori/shime1.png" alt="Naruto Sasori" width="80" /><br/><sub><b>Naruto Sasori</b></sub></td>
    <td align="center" width="16%"><img src="characters/Naruto_Sasuke/shime1.png" alt="Naruto Sasuke" width="80" /><br/><sub><b>Naruto Sasuke</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Night_In_The_Woods_Angus/shime1.png" alt="Night In The Woods Angus" width="80" /><br/><sub><b>Night In The Woods Angus</b></sub></td>
    <td align="center" width="16%"><img src="characters/Night_In_The_Woods_Bea/shime1.png" alt="Night In The Woods Bea" width="80" /><br/><sub><b>Night In The Woods Bea</b></sub></td>
    <td align="center" width="16%"><img src="characters/Night_In_The_Woods_Gregg/shime1.png" alt="Night In The Woods Gregg" width="80" /><br/><sub><b>Night In The Woods Gregg</b></sub></td>
    <td align="center" width="16%"><img src="characters/Night_In_The_Woods_Mae/shime1.png" alt="Night In The Woods Mae" width="80" /><br/><sub><b>Night In The Woods Mae</b></sub></td>
    <td align="center" width="16%"><img src="characters/One_Piece_Ace/shime1.png" alt="One Piece Ace" width="80" /><br/><sub><b>One Piece Ace</b></sub></td>
    <td align="center" width="16%"><img src="characters/One_Piece_Bepo/shime1.png" alt="One Piece Bepo" width="80" /><br/><sub><b>One Piece Bepo</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/One_Piece_Cass/shime1.png" alt="One Piece Cass" width="80" /><br/><sub><b>One Piece Cass</b></sub></td>
    <td align="center" width="16%"><img src="characters/One_Piece_Croc/shime1.png" alt="One Piece Croc" width="80" /><br/><sub><b>One Piece Croc</b></sub></td>
    <td align="center" width="16%"><img src="characters/One_Piece_Dofla/shime1.png" alt="One Piece Dofla" width="80" /><br/><sub><b>One Piece Dofla</b></sub></td>
    <td align="center" width="16%"><img src="characters/One_Piece_Kidd/shime1.png" alt="One Piece Kidd" width="80" /><br/><sub><b>One Piece Kidd</b></sub></td>
    <td align="center" width="16%"><img src="characters/One_Piece_Law/shime1.png" alt="One Piece Law" width="80" /><br/><sub><b>One Piece Law</b></sub></td>
    <td align="center" width="16%"><img src="characters/One_Piece_Lucci/shime1.png" alt="One Piece Lucci" width="80" /><br/><sub><b>One Piece Lucci</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/One_Piece_Luffy/shime1.png" alt="One Piece Luffy" width="80" /><br/><sub><b>One Piece Luffy</b></sub></td>
    <td align="center" width="16%"><img src="characters/One_Piece_Marco/shime1.png" alt="One Piece Marco" width="80" /><br/><sub><b>One Piece Marco</b></sub></td>
    <td align="center" width="16%"><img src="characters/One_Piece_Mihawk/shime1.png" alt="One Piece Mihawk" width="80" /><br/><sub><b>One Piece Mihawk</b></sub></td>
    <td align="center" width="16%"><img src="characters/One_Piece_Zoro/shime1.png" alt="One Piece Zoro" width="80" /><br/><sub><b>One Piece Zoro</b></sub></td>
    <td align="center" width="16%"><img src="characters/One_Punch_Man_Genos/shime1.png" alt="One Punch Man Genos" width="80" /><br/><sub><b>One Punch Man Genos</b></sub></td>
    <td align="center" width="16%"><img src="characters/One_Punch_Man_Saitama/shime1.png" alt="One Punch Man Saitama" width="80" /><br/><sub><b>One Punch Man Saitama</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/One_Punch_Man_Sonic/shime1.png" alt="One Punch Man Sonic" width="80" /><br/><sub><b>One Punch Man Sonic</b></sub></td>
    <td align="center" width="16%"><img src="characters/Osomatsu_San_Choromatsu_Matsuno/shime1.png" alt="Osomatsu San Choromatsu Matsuno" width="80" /><br/><sub><b>Osomatsu San Choromatsu Matsuno</b></sub></td>
    <td align="center" width="16%"><img src="characters/Osomatsu_San_Ichimatsu_Matsuno/shime1.png" alt="Osomatsu San Ichimatsu Matsuno" width="80" /><br/><sub><b>Osomatsu San Ichimatsu Matsuno</b></sub></td>
    <td align="center" width="16%"><img src="characters/Osomatsu_San_Jyuushimatsu_Matsuno/shime1.png" alt="Osomatsu San Jyuushimatsu Matsuno" width="80" /><br/><sub><b>Osomatsu San Jyuushimatsu Matsuno</b></sub></td>
    <td align="center" width="16%"><img src="characters/Osomatsu_San_Karamatsu_Matsuno/shime1.png" alt="Osomatsu San Karamatsu Matsuno" width="80" /><br/><sub><b>Osomatsu San Karamatsu Matsuno</b></sub></td>
    <td align="center" width="16%"><img src="characters/Osomatsu_San_Osomatsu_Matsuno/shime1.png" alt="Osomatsu San Osomatsu Matsuno" width="80" /><br/><sub><b>Osomatsu San Osomatsu Matsuno</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Osomatsu_San_Todomatsu_Matsuno/shime1.png" alt="Osomatsu San Todomatsu Matsuno" width="80" /><br/><sub><b>Osomatsu San Todomatsu Matsuno</b></sub></td>
    <td align="center" width="16%"><img src="characters/Persons_Daniel_Howell/shime1.png" alt="Persons Daniel Howell" width="80" /><br/><sub><b>Persons Daniel Howell</b></sub></td>
    <td align="center" width="16%"><img src="characters/Persons_Jacksepticeye/shime1.png" alt="Persons Jacksepticeye" width="80" /><br/><sub><b>Persons Jacksepticeye</b></sub></td>
    <td align="center" width="16%"><img src="characters/Persons_Link/shime1.png" alt="Persons Link" width="80" /><br/><sub><b>Persons Link</b></sub></td>
    <td align="center" width="16%"><img src="characters/Persons_Markiplier/shime1.png" alt="Persons Markiplier" width="80" /><br/><sub><b>Persons Markiplier</b></sub></td>
    <td align="center" width="16%"><img src="characters/Persons_Pew_Die_Pie/shime1.png" alt="Persons Pew Die Pie" width="80" /><br/><sub><b>Persons Pew Die Pie</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Persons_Phil_Lester/shime1.png" alt="Persons Phil Lester" width="80" /><br/><sub><b>Persons Phil Lester</b></sub></td>
    <td align="center" width="16%"><img src="characters/Persons_Rhett/shime1.png" alt="Persons Rhett" width="80" /><br/><sub><b>Persons Rhett</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Ampharos/shime1.png" alt="Pokemon Ampharos" width="80" /><br/><sub><b>Pokemon Ampharos</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Archen/shime1.png" alt="Pokemon Archen" width="80" /><br/><sub><b>Pokemon Archen</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Armaldo/shime1.png" alt="Pokemon Armaldo" width="80" /><br/><sub><b>Pokemon Armaldo</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Chandelure/shime1.png" alt="Pokemon Chandelure" width="80" /><br/><sub><b>Pokemon Chandelure</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Pokemon_Charmander/shime1.png" alt="Pokemon Charmander" width="80" /><br/><sub><b>Pokemon Charmander</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Clefable/shime1.png" alt="Pokemon Clefable" width="80" /><br/><sub><b>Pokemon Clefable</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Crobat/shime1.png" alt="Pokemon Crobat" width="80" /><br/><sub><b>Pokemon Crobat</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Cumceon/shime1.png" alt="Pokemon Cumceon" width="80" /><br/><sub><b>Pokemon Cumceon</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Dewott/shime1.png" alt="Pokemon Dewott" width="80" /><br/><sub><b>Pokemon Dewott</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Drifloon/shime1.png" alt="Pokemon Drifloon" width="80" /><br/><sub><b>Pokemon Drifloon</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Pokemon_Eevee/shime1.png" alt="Pokemon Eevee" width="80" /><br/><sub><b>Pokemon Eevee</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Feraligatr/shime1.png" alt="Pokemon Feraligatr" width="80" /><br/><sub><b>Pokemon Feraligatr</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Flygon/shime1.png" alt="Pokemon Flygon" width="80" /><br/><sub><b>Pokemon Flygon</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Gardevoir/shime1.png" alt="Pokemon Gardevoir" width="80" /><br/><sub><b>Pokemon Gardevoir</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Gastly/shime1.png" alt="Pokemon Gastly" width="80" /><br/><sub><b>Pokemon Gastly</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Jolteon/shime1.png" alt="Pokemon Jolteon" width="80" /><br/><sub><b>Pokemon Jolteon</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Pokemon_Kyurem/shime1.png" alt="Pokemon Kyurem" width="80" /><br/><sub><b>Pokemon Kyurem</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Larvitar/shime1.png" alt="Pokemon Larvitar" width="80" /><br/><sub><b>Pokemon Larvitar</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Litwick/shime1.png" alt="Pokemon Litwick" width="80" /><br/><sub><b>Pokemon Litwick</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Mew/shime1.png" alt="Pokemon Mew" width="80" /><br/><sub><b>Pokemon Mew</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Misdreavus/shime1.png" alt="Pokemon Misdreavus" width="80" /><br/><sub><b>Pokemon Misdreavus</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Mudkip/shime1.png" alt="Pokemon Mudkip" width="80" /><br/><sub><b>Pokemon Mudkip</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Pokemon_Only_Slowpoke/shime1.png" alt="Pokemon Only Slowpoke" width="80" /><br/><sub><b>Pokemon Only Slowpoke</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Oshawott/shime1.png" alt="Pokemon Oshawott" width="80" /><br/><sub><b>Pokemon Oshawott</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Pikachu/shime1.png" alt="Pokemon Pikachu" width="80" /><br/><sub><b>Pokemon Pikachu</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Purrloin/shime1.png" alt="Pokemon Purrloin" width="80" /><br/><sub><b>Pokemon Purrloin</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Raichu/shime1.png" alt="Pokemon Raichu" width="80" /><br/><sub><b>Pokemon Raichu</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Reshriram/shime1.png" alt="Pokemon Reshriram" width="80" /><br/><sub><b>Pokemon Reshriram</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Pokemon_Sewaddle/shime1.png" alt="Pokemon Sewaddle" width="80" /><br/><sub><b>Pokemon Sewaddle</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Shedinja/shime1.png" alt="Pokemon Shedinja" width="80" /><br/><sub><b>Pokemon Shedinja</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Snivy/shime1.png" alt="Pokemon Snivy" width="80" /><br/><sub><b>Pokemon Snivy</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Sparker/shime1.png" alt="Pokemon Sparker" width="80" /><br/><sub><b>Pokemon Sparker</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Squirtle/shime1.png" alt="Pokemon Squirtle" width="80" /><br/><sub><b>Pokemon Squirtle</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Suicune/shime1.png" alt="Pokemon Suicune" width="80" /><br/><sub><b>Pokemon Suicune</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Pokemon_Surfachu/shime1.png" alt="Pokemon Surfachu" width="80" /><br/><sub><b>Pokemon Surfachu</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Swablu/shime1.png" alt="Pokemon Swablu" width="80" /><br/><sub><b>Pokemon Swablu</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Tepig/shime1.png" alt="Pokemon Tepig" width="80" /><br/><sub><b>Pokemon Tepig</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Togekiss/shime1.png" alt="Pokemon Togekiss" width="80" /><br/><sub><b>Pokemon Togekiss</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Tyranitar/shime1.png" alt="Pokemon Tyranitar" width="80" /><br/><sub><b>Pokemon Tyranitar</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Umbreon/shime1.png" alt="Pokemon Umbreon" width="80" /><br/><sub><b>Pokemon Umbreon</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Pokemon_Umbreon_Shiny/shime1.png" alt="Pokemon Umbreon Shiny" width="80" /><br/><sub><b>Pokemon Umbreon Shiny</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Zangoose/shime1.png" alt="Pokemon Zangoose" width="80" /><br/><sub><b>Pokemon Zangoose</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Zorua/shime1.png" alt="Pokemon Zorua" width="80" /><br/><sub><b>Pokemon Zorua</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pokemon_Zweilous/shime1.png" alt="Pokemon Zweilous" width="80" /><br/><sub><b>Pokemon Zweilous</b></sub></td>
    <td align="center" width="16%"><img src="characters/Pusheen_Pusheen_The_Cat/shime1.png" alt="Pusheen Pusheen The Cat" width="80" /><br/><sub><b>Pusheen Pusheen The Cat</b></sub></td>
    <td align="center" width="16%"><img src="characters/Rick_And_Morty_Rick/shime1.png" alt="Rick And Morty Rick" width="80" /><br/><sub><b>Rick And Morty Rick</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Sonic_Sonic/shime1.png" alt="Sonic Sonic" width="80" /><br/><sub><b>Sonic Sonic</b></sub></td>
    <td align="center" width="16%"><img src="characters/Sonic_Tails/shime1.png" alt="Sonic Tails" width="80" /><br/><sub><b>Sonic Tails</b></sub></td>
    <td align="center" width="16%"><img src="characters/Sponge_Bob_Square_Pants_Sponge_Bob/shime1.png" alt="Sponge Bob Square Pants Sponge Bob" width="80" /><br/><sub><b>Sponge Bob Square Pants Sponge Bob</b></sub></td>
    <td align="center" width="16%"><img src="characters/Steven_Universe_Garnet/shime1.png" alt="Steven Universe Garnet" width="80" /><br/><sub><b>Steven Universe Garnet</b></sub></td>
    <td align="center" width="16%"><img src="characters/Steven_Universe_Lapis_Lazuli/shime1.png" alt="Steven Universe Lapis Lazuli" width="80" /><br/><sub><b>Steven Universe Lapis Lazuli</b></sub></td>
    <td align="center" width="16%"><img src="characters/Steven_Universe_Pearl/shime1.png" alt="Steven Universe Pearl" width="80" /><br/><sub><b>Steven Universe Pearl</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Steven_Universe_Peridot/shime1.png" alt="Steven Universe Peridot" width="80" /><br/><sub><b>Steven Universe Peridot</b></sub></td>
    <td align="center" width="16%"><img src="characters/Steven_Universe_Ruby/shime1.png" alt="Steven Universe Ruby" width="80" /><br/><sub><b>Steven Universe Ruby</b></sub></td>
    <td align="center" width="16%"><img src="characters/The_Avengers_Bruce_Banner/shime1.png" alt="The Avengers Bruce Banner" width="80" /><br/><sub><b>The Avengers Bruce Banner</b></sub></td>
    <td align="center" width="16%"><img src="characters/The_Avengers_Captain_America/shime1.png" alt="The Avengers Captain America" width="80" /><br/><sub><b>The Avengers Captain America</b></sub></td>
    <td align="center" width="16%"><img src="characters/The_Avengers_Hawkeye/shime1.png" alt="The Avengers Hawkeye" width="80" /><br/><sub><b>The Avengers Hawkeye</b></sub></td>
    <td align="center" width="16%"><img src="characters/The_Avengers_Loki/shime1.png" alt="The Avengers Loki" width="80" /><br/><sub><b>The Avengers Loki</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/The_Avengers_Loki_(helmet)/shime1.png" alt="The Avengers Loki (helmet)" width="80" /><br/><sub><b>The Avengers Loki (helmet)</b></sub></td>
    <td align="center" width="16%"><img src="characters/The_Avengers_Tony_Stark/shime1.png" alt="The Avengers Tony Stark" width="80" /><br/><sub><b>The Avengers Tony Stark</b></sub></td>
    <td align="center" width="16%"><img src="characters/The_Beatles_George_Harrison/shime1.png" alt="The Beatles George Harrison" width="80" /><br/><sub><b>The Beatles George Harrison</b></sub></td>
    <td align="center" width="16%"><img src="characters/The_Beatles_John_Lennon/shime1.png" alt="The Beatles John Lennon" width="80" /><br/><sub><b>The Beatles John Lennon</b></sub></td>
    <td align="center" width="16%"><img src="characters/The_Beatles_Paul_Mccartney/shime1.png" alt="The Beatles Paul Mccartney" width="80" /><br/><sub><b>The Beatles Paul Mccartney</b></sub></td>
    <td align="center" width="16%"><img src="characters/The_Beatles_Ringo_Starr/shime1.png" alt="The Beatles Ringo Starr" width="80" /><br/><sub><b>The Beatles Ringo Starr</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Tokyo_Ghoul_Shuu_Tsukiyama/shime1.png" alt="Tokyo Ghoul Shuu Tsukiyama" width="80" /><br/><sub><b>Tokyo Ghoul Shuu Tsukiyama</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Alphys/shime1.png" alt="Undertale Alphys" width="80" /><br/><sub><b>Undertale Alphys</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Asriel/shime1.png" alt="Undertale Asriel" width="80" /><br/><sub><b>Undertale Asriel</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Asylum_Sans/shime1.png" alt="Undertale Asylum Sans" width="80" /><br/><sub><b>Undertale Asylum Sans</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Birdtale_Sans/shime1.png" alt="Undertale Birdtale Sans" width="80" /><br/><sub><b>Undertale Birdtale Sans</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Blueberry/shime1.png" alt="Undertale Blueberry" width="80" /><br/><sub><b>Undertale Blueberry</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Undertale_Chara/shime1.png" alt="Undertale Chara" width="80" /><br/><sub><b>Undertale Chara</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Dreamtale_Sans/shime1.png" alt="Undertale Dreamtale Sans" width="80" /><br/><sub><b>Undertale Dreamtale Sans</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Dust_Sans/shime1.png" alt="Undertale Dust Sans" width="80" /><br/><sub><b>Undertale Dust Sans</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Dusty_Sansy/shime1.png" alt="Undertale Dusty Sansy" width="80" /><br/><sub><b>Undertale Dusty Sansy</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Error_Sans/shime1.png" alt="Undertale Error Sans" width="80" /><br/><sub><b>Undertale Error Sans</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Flower_Fell_Sans/shime1.png" alt="Undertale Flower Fell Sans" width="80" /><br/><sub><b>Undertale Flower Fell Sans</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Undertale_Flowey/shime1.png" alt="Undertale Flowey" width="80" /><br/><sub><b>Undertale Flowey</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Fresh_Sans/shime1.png" alt="Undertale Fresh Sans" width="80" /><br/><sub><b>Undertale Fresh Sans</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Frisk/shime1.png" alt="Undertale Frisk" width="80" /><br/><sub><b>Undertale Frisk</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Gaster_Sans/shime1.png" alt="Undertale Gaster Sans" width="80" /><br/><sub><b>Undertale Gaster Sans</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Horror_Sans/shime1.png" alt="Undertale Horror Sans" width="80" /><br/><sub><b>Undertale Horror Sans</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Ink_Sans/shime1.png" alt="Undertale Ink Sans" width="80" /><br/><sub><b>Undertale Ink Sans</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Undertale_Napstablook/shime1.png" alt="Undertale Napstablook" width="80" /><br/><sub><b>Undertale Napstablook</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Nightmare_Sans/shime1.png" alt="Undertale Nightmare Sans" width="80" /><br/><sub><b>Undertale Nightmare Sans</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Papyrus/shime1.png" alt="Undertale Papyrus" width="80" /><br/><sub><b>Undertale Papyrus</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Reaper_Sans/shime1.png" alt="Undertale Reaper Sans" width="80" /><br/><sub><b>Undertale Reaper Sans</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Sans/shime1.png" alt="Undertale Sans" width="80" /><br/><sub><b>Undertale Sans</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Soriel/shime1.png" alt="Undertale Soriel" width="80" /><br/><sub><b>Undertale Soriel</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Undertale_Underfell_Sans/shime1.png" alt="Undertale Underfell Sans" width="80" /><br/><sub><b>Undertale Underfell Sans</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Underswap_Sans/shime1.png" alt="Undertale Underswap Sans" width="80" /><br/><sub><b>Undertale Underswap Sans</b></sub></td>
    <td align="center" width="16%"><img src="characters/Undertale_Undyne/shime1.png" alt="Undertale Undyne" width="80" /><br/><sub><b>Undertale Undyne</b></sub></td>
    <td align="center" width="16%"><img src="characters/Vocaloid_Gakupo/shime1.png" alt="Vocaloid Gakupo" width="80" /><br/><sub><b>Vocaloid Gakupo</b></sub></td>
    <td align="center" width="16%"><img src="characters/Vocaloid_Hatsune_Miku/shime1.png" alt="Vocaloid Hatsune Miku" width="80" /><br/><sub><b>Vocaloid Hatsune Miku</b></sub></td>
    <td align="center" width="16%"><img src="characters/Vocaloid_Ia/shime1.png" alt="Vocaloid Ia" width="80" /><br/><sub><b>Vocaloid Ia</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Vocaloid_Kagamine_Len/shime1.png" alt="Vocaloid Kagamine Len" width="80" /><br/><sub><b>Vocaloid Kagamine Len</b></sub></td>
    <td align="center" width="16%"><img src="characters/Vocaloid_Kagamine_Rin/shime1.png" alt="Vocaloid Kagamine Rin" width="80" /><br/><sub><b>Vocaloid Kagamine Rin</b></sub></td>
    <td align="center" width="16%"><img src="characters/Vocaloid_Kaito/shime1.png" alt="Vocaloid Kaito" width="80" /><br/><sub><b>Vocaloid Kaito</b></sub></td>
    <td align="center" width="16%"><img src="characters/Vocaloid_Luka/shime1.png" alt="Vocaloid Luka" width="80" /><br/><sub><b>Vocaloid Luka</b></sub></td>
    <td align="center" width="16%"><img src="characters/Vocaloid_Mikuo/shime1.png" alt="Vocaloid Mikuo" width="80" /><br/><sub><b>Vocaloid Mikuo</b></sub></td>
    <td align="center" width="16%"><img src="characters/Vocaloid_Oliver/shime1.png" alt="Vocaloid Oliver" width="80" /><br/><sub><b>Vocaloid Oliver</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Voltron_Keith/shime1.png" alt="Voltron Keith" width="80" /><br/><sub><b>Voltron Keith</b></sub></td>
    <td align="center" width="16%"><img src="characters/Voltron_Pidge/shime1.png" alt="Voltron Pidge" width="80" /><br/><sub><b>Voltron Pidge</b></sub></td>
    <td align="center" width="16%"><img src="characters/X_Men_Deadpool/shime1.png" alt="X Men Deadpool" width="80" /><br/><sub><b>X Men Deadpool</b></sub></td>
    <td align="center" width="16%"><img src="characters/XiaoCatboy/shime1.png" alt="XiaoCatboy" width="80" /><br/><sub><b>XiaoCatboy</b></sub></td>
    <td align="center" width="16%"><img src="characters/Yu_Gi_Oh_Blue_Eyes/shime1.png" alt="Yu Gi Oh Blue Eyes" width="80" /><br/><sub><b>Yu Gi Oh Blue Eyes</b></sub></td>
    <td align="center" width="16%"><img src="characters/Yu_Gi_Oh_Dark_Magician/shime1.png" alt="Yu Gi Oh Dark Magician" width="80" /><br/><sub><b>Yu Gi Oh Dark Magician</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Yu_Gi_Oh_Kiribo/shime1.png" alt="Yu Gi Oh Kiribo" width="80" /><br/><sub><b>Yu Gi Oh Kiribo</b></sub></td>
    <td align="center" width="16%"><img src="characters/Yu_Gi_Oh_New_Bakura/shime1.png" alt="Yu Gi Oh New Bakura" width="80" /><br/><sub><b>Yu Gi Oh New Bakura</b></sub></td>
    <td align="center" width="16%"><img src="characters/Yu_Gi_Oh_New_Yugi/shime1.png" alt="Yu Gi Oh New Yugi" width="80" /><br/><sub><b>Yu Gi Oh New Yugi</b></sub></td>
    <td align="center" width="16%"><img src="characters/Yu_Gi_Oh_Old_Bakura/shime1.png" alt="Yu Gi Oh Old Bakura" width="80" /><br/><sub><b>Yu Gi Oh Old Bakura</b></sub></td>
    <td align="center" width="16%"><img src="characters/Yu_Gi_Oh_Rex_Raptor/shime1.png" alt="Yu Gi Oh Rex Raptor" width="80" /><br/><sub><b>Yu Gi Oh Rex Raptor</b></sub></td>
    <td align="center" width="16%"><img src="characters/Yu_Gi_Oh_Seto_Kaiba/shime1.png" alt="Yu Gi Oh Seto Kaiba" width="80" /><br/><sub><b>Yu Gi Oh Seto Kaiba</b></sub></td>
  </tr>
  <tr>
    <td align="center" width="16%"><img src="characters/Yu_Gi_Oh_Weevil_Underwood/shime1.png" alt="Yu Gi Oh Weevil Underwood" width="80" /><br/><sub><b>Yu Gi Oh Weevil Underwood</b></sub></td>
    <td align="center" width="16%"><img src="characters/Yu_Gi_Oh_Yugi/shime1.png" alt="Yu Gi Oh Yugi" width="80" /><br/><sub><b>Yu Gi Oh Yugi</b></sub></td>
    <td align="center" width="16%"><img src="characters/Yuri_On_Ice_Viktor/shime1.png" alt="Yuri On Ice Viktor" width="80" /><br/><sub><b>Yuri On Ice Viktor</b></sub></td>
    <td align="center" width="16%"></td>
    <td align="center" width="16%"></td>
    <td align="center" width="16%"></td>
  </tr>
</table>

---

## 📜 License & Credits

This project inherits the ZLIB/LIBPNG license of the original Shimeji project by Yuki Yamada of Group Finity.

- **Java Native Access (JNA)**: Licensed under LGPL.
- **Mozilla Rhino JS Engine**: Licensed under MPL.
