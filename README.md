# Tube to Sound

## Overview

Tube to Sound is a lightweight desktop application that converts YouTube videos into high-quality MP3 files directly on your computer—fast, private, and with no ads.

### Features

- **Fast & Multi-threaded**: Downloads audio in parallel streams for maximum speed.
- **High Audio Quality**: Supports MP3 conversion from 128 kbps up to 320 kbps.
- **No Duration Limits**: Seamlessly converts long videos, podcasts, and audiobooks.
- **Automatic Metadata**: Automatically tags track titles and artist information.
- **Cross-Platform**: Clean, native interface for both macOS and Windows (Dark & Light mode).

---

## Download

Pre-compiled standalone packages are available on the [Releases](https://github.com/ThanhMiLa/tube-to-sound/releases) page.

| Platform | File | Details |
| :--- | :--- | :--- |
| **macOS** | `TubeToSound-macOS.dmg` | Drag and drop into Applications |
| **Windows** | `TubeToSound-Windows.exe` | Standalone executable (FFmpeg included) |

---

## Installation

### macOS

1. Download `TubeToSound-macOS.dmg` from the latest release.
2. Open the downloaded `.dmg` file and drag `TubeToSound` into your `/Applications` folder.
3. Open the app from Launchpad or Spotlight (`Cmd + Space`).

> **First launch note:** If prompted by macOS Gatekeeper, go to **System Settings > Privacy & Security** and click **Open Anyway**.

### Windows

1. Download `TubeToSound-Windows.exe` from the latest release.
2. Double-click the file to run. No setup or extra tools required.

---

## Running from Source

### Prerequisites

- Python 3.12+
- FFmpeg installed

### Setup & Run

```bash
# Clone the repository
git clone https://github.com/ThanhMiLa/tube-to-sound.git
cd tube-to-sound

# Create virtual environment & install dependencies
python -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run application
python app.py
```
