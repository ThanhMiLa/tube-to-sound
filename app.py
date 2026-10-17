import os
import sys
import shutil
import threading
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Đảm bảo đường dẫn brew và system có trong PATH trên macOS / Linux
if sys.platform == "darwin":
    for path in ["/opt/homebrew/bin", "/usr/local/bin"]:
        if path not in os.environ.get("PATH", ""):
            os.environ["PATH"] = f"{path}:{os.environ.get('PATH', '')}"

import yt_dlp

# Cấu hình giao diện macOS & Windows
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def get_ffmpeg_dir():
    """Tự động tìm kiếm thư mục chứa ffmpeg trên cả macOS và Windows."""
    # Nếu chạy từ bản đóng gói PyInstaller
    if getattr(sys, 'frozen', False):
        bundle_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        binary_name = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"
        local_ffmpeg = os.path.join(bundle_dir, binary_name)
        if os.path.exists(local_ffmpeg):
            return bundle_dir

    # Tìm trong PATH
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return os.path.dirname(system_ffmpeg)

    # Đường dẫn brew mặc định trên Mac
    if sys.platform == "darwin":
        for p in ["/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"]:
            if os.path.exists(p):
                return os.path.dirname(p)

    return None


class TubeToSoundApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tube to Sound - YouTube to MP3")
        self.geometry("620x470")
        self.resizable(False, False)

        # Thư mục lưu mặc định: Downloads của máy
        self.download_folder = os.path.expanduser("~/Downloads")
        self.is_downloading = False

        self._build_ui()

    def _build_ui(self):
        # 1. Header
        self.title_label = ctk.CTkLabel(
            self,
            text="🎵 Tube to Sound",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Tải siêu tốc & chuyển đổi YouTube sang MP3 chất lượng cao",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 18))

        # 2. Khung nhập liệu chính
        self.main_frame = ctk.CTkFrame(self, corner_radius=12)
        self.main_frame.pack(padx=25, pady=5, fill="x")

        # URL Input
        self.url_label = ctk.CTkLabel(
            self.main_frame,
            text="Đường link YouTube:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.url_label.pack(anchor="w", padx=15, pady=(15, 5))

        self.url_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Dán link YouTube vào đây (https://www.youtube.com/watch?v=...)",
            height=38,
            font=ctk.CTkFont(size=13)
        )
        self.url_entry.pack(fill="x", padx=15, pady=(0, 15))

        # Cài đặt chất lượng & Thư mục lưu
        self.settings_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.settings_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Chất lượng
        self.quality_label = ctk.CTkLabel(self.settings_frame, text="Chất lượng âm thanh:")
        self.quality_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.quality_menu = ctk.CTkOptionMenu(
            self.settings_frame,
            values=["320 kbps (Cao nhất)", "256 kbps", "192 kbps (Tiêu chuẩn)", "128 kbps"],
            width=175
        )
        self.quality_menu.set("320 kbps (Cao nhất)")
        self.quality_menu.grid(row=0, column=1, sticky="w")

        # Thư mục lưu
        self.folder_label = ctk.CTkLabel(self.settings_frame, text="Lưu tại:")
        self.folder_label.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))

        folder_name = os.path.basename(self.download_folder) or self.download_folder
        self.folder_btn = ctk.CTkButton(
            self.settings_frame,
            text=f"📁 {folder_name}",
            fg_color=("gray75", "gray25"),
            text_color=("black", "white"),
            command=self._choose_folder,
            width=175
        )
        self.folder_btn.grid(row=1, column=1, sticky="w", pady=(10, 0))

        # 3. Thanh tiến trình & Trạng thái
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(padx=25, pady=(15, 8), fill="x")
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(
            self,
            text="Sẵn sàng tải...",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.pack(pady=(0, 10))

        # 4. Nút bấm hành động
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.pack(pady=10)

        self.download_btn = ctk.CTkButton(
            self.actions_frame,
            text="⚡ Bắt đầu tải MP3",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=42,
            width=180,
            command=self._start_download_thread
        )
        self.download_btn.pack(side="left", padx=10)

        self.open_folder_btn = ctk.CTkButton(
            self.actions_frame,
            text="Mở thư mục lưu",
            font=ctk.CTkFont(size=13),
            height=42,
            width=140,
            fg_color="transparent",
            border_width=1,
            command=self._open_downloads_folder
        )
        self.open_folder_btn.pack(side="left", padx=5)

    def _choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_folder, title="Chọn thư mục lưu file MP3")
        if folder:
            self.download_folder = folder
            self.folder_btn.configure(text=f"📁 {os.path.basename(folder) or folder}")

    def _open_downloads_folder(self):
        """Mở thư mục lưu hỗ trợ cả macOS, Windows và Linux"""
        if not os.path.exists(self.download_folder):
            return
        if sys.platform == "darwin":
            subprocess.run(["open", self.download_folder])
        elif sys.platform == "win32":
            os.startfile(self.download_folder)
        else:
            subprocess.run(["xdg-open", self.download_folder])

    def _update_status(self, text, progress=None, color=None):
        self.status_label.configure(text=text)
        if color:
            self.status_label.configure(text_color=color)
        else:
            self.status_label.configure(text_color="gray")
        if progress is not None:
            self.progress_bar.set(progress)

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                percent = downloaded / total
                speed = d.get('_speed_str', '')
                eta = d.get('_eta_str', '')
                self.after(0, self._update_status, f"Đang tải: {percent*100:.1f}% ({speed} - Còn: {eta})", percent)
            else:
                self.after(0, self._update_status, "Đang tải dữ liệu đa luồng...", 0.6)
        elif d['status'] == 'finished':
            self.after(0, self._update_status, "⚡ Đang tăng tốc chuyển đổi sang MP3...", 0.92)

    def _start_download_thread(self):
        if self.is_downloading:
            return

        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Thiếu link", "Vui lòng dán link YouTube cần tải!")
            return

        self.is_downloading = True
        self.download_btn.configure(state="disabled", text="Đang xử lý...")
        self.progress_bar.set(0)
        self._update_status("Đang kết nối...", 0.1)

        thread = threading.Thread(target=self._run_download, args=(url,), daemon=True)
        thread.start()

    def _run_download(self, url):
        quality_str = self.quality_menu.get().split()[0]  # ví dụ '320', '256', '192', '128'

        # CẤU HÌNH TỐI ƯU TỐC ĐỘ TỐI ĐA (TẢI ĐA LUỒNG & FFMPEG ĐA NHÂN)
        ydl_opts = {
            # 1. Chỉ chọn luồng audio trực tiếp chất lượng tốt nhất (m4a/opus)
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
            # 2. BẬT TẢI ĐA LUỒNG SONG SONG: Tải 8 phân đoạn cùng một lúc
            'concurrent_fragment_downloads': 8,
            # 3. Tăng bộ đệm buffer giúp stream nhanh hơn
            'buffersize': 1024 * 256,
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            # 4. Cấu hình FFmpeg: Dùng full số nhân CPU máy tính (-threads 0)
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality_str,
                },
                {
                    'key': 'FFmpegMetadata',
                    'add_metadata': True,
                }
            ],
            'postprocessor_args': {
                'ffmpeg': ['-threads', '0']
            },
            'progress_hooks': [self._progress_hook],
        }

        # Tìm thư mục ffmpeg
        ffmpeg_dir = get_ffmpeg_dir()
        if ffmpeg_dir:
            ydl_opts['ffmpeg_location'] = ffmpeg_dir

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Audio')

            self.after(0, self._on_success, title)
        except Exception as e:
            self.after(0, self._on_error, str(e))

    def _on_success(self, title):
        self.is_downloading = False
        self.download_btn.configure(state="normal", text="⚡ Bắt đầu tải MP3")
        self._update_status(f"✅ Hoàn tất: {title[:40]}...", 1.0, color="#2ecc71")
        self.url_entry.delete(0, "end")
        messagebox.showinfo("Thành công", f"Đã chuyển đổi và lưu file MP3 thành công vào:\n{self.download_folder}")

    def _on_error(self, err_msg):
        self.is_downloading = False
        self.download_btn.configure(state="normal", text="⚡ Bắt đầu tải MP3")
        self._update_status("❌ Có lỗi xảy ra", 0, color="#e74c3c")
        messagebox.showerror("Lỗi", f"Không thể tải video:\n{err_msg[:200]}")


if __name__ == "__main__":
    app = TubeToSoundApp()
    app.mainloop()
