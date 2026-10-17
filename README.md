# 🎵 Tube to Sound - YouTube to MP3 Converter

Ứng dụng Desktop đa nền tảng (macOS & Windows) chuyển đổi link YouTube sang file âm thanh `.mp3` chất lượng cao, nhanh chóng và mượt mà.

---

## ✨ Tính năng nổi bật

- ⚡ **Tải siêu tốc:** Áp dụng kỹ thuật tải đa luồng song song (8 fragments đồng thời) và tối ưu hóa toàn bộ nhân CPU khi mã hóa bằng FFmpeg.
- 🎚️ **Tùy chọn chất lượng:** Hỗ trợ xuất MP3 từ 128 kbps đến **320 kbps (Cực nét)**.
- 🏷️ **Tự động gắn thẻ Metadata:** Tự động điền thông tin tên bài hát, nghệ sĩ vào file MP3.
- 🖥️ **Giao diện hiện đại:** Tự động thích ứng giao diện Sáng / Tối (Light / Dark mode) của hệ điều hành macOS và Windows.
- 📂 **Tải & Mở trực tiếp:** Tự động lưu vào thư mục Downloads của máy tính và có nút mở nhanh thư mục.

---

## 📥 Tải về ứng dụng (Không cần cài đặt code)

Vào trang **[Releases](https://github.com/ThanhMiLa/tube-to-sound/releases)** để tải bản cài đặt mới nhất:

- 🍏 **Dành cho macOS:** Tải file `TubeToSound-macOS.dmg`, mở lên và kéo vào thư mục `Applications`.
- 🪟 **Dành cho Windows:** Tải file `TubeToSound-Windows.exe` về nhấp đúp là sử dụng được ngay (đã tích hợp sẵn FFmpeg).

---

## 🛠️ Dành cho lập trình viên (Chạy từ mã nguồn)

### 1. Yêu cầu hệ thống:
- Python 3.12+
- FFmpeg

### 2. Cài đặt môi trường:
```bash
# Clone dự án
git clone https://github.com/ThanhMiLa/tube-to-sound.git
cd tube-to-sound

# Tạo môi trường ảo & cài thư viện
python -m venv .venv
source .venv/bin/activate  # Trên Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Chạy ứng dụng:
```bash
python app.py
```

### 4. Đóng gói ứng dụng:
```bash
# Tạo icon
python create_icon.py

# Đóng gói ra ứng dụng máy tính
pyinstaller --noconsole --windowed --name="TubeToSound" --collect-all customtkinter --collect-all yt_dlp app.py
```
