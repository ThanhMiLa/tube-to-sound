# Tube to Sound

Tube to Sound is a high-performance cross-platform desktop application designed to convert YouTube videos into high-quality MP3 audio files on macOS and Windows.

---

## Overview

The application provides a standalone, private, and ad-free alternative to web-based YouTube converters. It downloads audio streams directly and transcodes them locally using FFmpeg, eliminating queue wait times, audio compression degradation, and duration restrictions.

### Key Capabilities

- **Accelerated Download Pipeline**: Employs parallel multi-fragment stream retrieval to maximize network throughput and bypass bandwidth throttling.
- **Hardware-Optimized Audio Transcoding**: Leverages multi-threaded FFmpeg encoding across all available CPU cores for fast conversion of long videos and podcasts.
- **Selectable Bitrates**: Supports audio quality options from 128 kbps up to 320 kbps (CBR/VBR).
- **Automated Metadata Tagging**: Extracts and embeds track title and artist tags directly into the generated MP3 container.
- **Native OS Interface**: Built with an adaptive user interface conforming to system light and dark themes on both macOS and Windows.
- **No Length Limitations**: Converts videos of any length, including multi-hour lectures, audiobooks, and live recordings, without timeouts.

---

## Download

Pre-compiled standalone packages for each operating system are available on the [Releases](https://github.com/ThanhMiLa/tube-to-sound/releases) page.

| Platform | Package Format | Details |
| :--- | :--- | :--- |
| **macOS** | `.dmg` installer | Compatible with Apple Silicon and Intel Macs |
| **Windows** | `.exe` executable | Standalone binary with FFmpeg bundled |

---

## Installation

### macOS

1. Download `TubeToSound-macOS.dmg` from the latest release.
2. Open the downloaded `.dmg` file.
3. Drag the `TubeToSound` application into your `/Applications` directory.
4. Launch the application from Launchpad, Spotlight (`Cmd + Space`), or the Dock.

> **Note on macOS Security:** Because this application is compiled locally without an Apple Developer ID signature, macOS Gatekeeper may display a security notice on first launch. To permit execution, open **System Settings > Privacy & Security** and select **Open Anyway**.

### Windows

1. Download `TubeToSound-Windows.exe` from the latest release.
2. Double-click the `.exe` file to launch the application directly.
3. No separate installation of Python or FFmpeg is required; all dependencies are statically bundled within the binary.

---

## Running from Source

If you prefer running or building the project from source code:

### Prerequisites

- Python 3.12 or higher
- FFmpeg installed and available in the system `PATH`

### Setup

```bash
# Clone the repository
git clone https://github.com/ThanhMiLa/tube-to-sound.git
cd tube-to-sound

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
# .venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

### Build Binaries

```bash
# Generate application icon
python create_icon.py

# Package application with PyInstaller
pyinstaller --noconsole --windowed --name="TubeToSound" --collect-all customtkinter --collect-all yt_dlp app.py
```
