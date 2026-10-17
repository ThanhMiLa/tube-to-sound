#!/bin/bash
set -e

echo "🔨 Building TubeToSound.app..."
./.venv/bin/pyinstaller --noconfirm --noconsole --windowed --icon=AppIcon.icns \
  --name="TubeToSound" \
  --collect-all customtkinter \
  --collect-all yt_dlp \
  app.py

echo "📦 Updating /Applications/TubeToSound.app..."
rm -rf /Applications/TubeToSound.app
cp -r dist/TubeToSound.app /Applications/

echo "✅ All done! The updated TubeToSound.app is now ready in /Applications."
