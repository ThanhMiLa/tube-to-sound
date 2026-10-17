import os
import sys
import subprocess
from PIL import Image, ImageDraw

def generate_base_icon(size=1024):
    base_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base_img)

    # 1. Nền bo góc đỏ hồng YouTube Music
    padding = 60
    corner_radius = 210
    draw.rounded_rectangle(
        [padding, padding, size - padding, size - padding],
        radius=corner_radius,
        fill=(255, 30, 86, 255)
    )

    # 2. Biểu tượng nốt nhạc trắng
    # Cột 1
    draw.rounded_rectangle([390, 360, 430, 680], radius=15, fill=(255, 255, 255, 255))
    # Bầu nốt 1
    draw.ellipse([310, 630, 440, 730], fill=(255, 255, 255, 255))
    # Cột 2
    draw.rounded_rectangle([590, 310, 630, 630], radius=15, fill=(255, 255, 255, 255))
    # Bầu nốt 2
    draw.ellipse([510, 580, 640, 680], fill=(255, 255, 255, 255))
    # Thanh nối
    draw.polygon(
        [(390, 360), (630, 310), (630, 380), (390, 430)],
        fill=(255, 255, 255, 255)
    )
    return base_img


def create_mac_icns(base_img, output_icns="AppIcon.icns"):
    iconset_dir = "AppIcon.iconset"
    os.makedirs(iconset_dir, exist_ok=True)
    sizes = [
        (16, "icon_16x16.png"),
        (32, "icon_16x16@2x.png"),
        (32, "icon_32x32.png"),
        (64, "icon_32x32@2x.png"),
        (128, "icon_128x128.png"),
        (256, "icon_128x128@2x.png"),
        (256, "icon_256x256.png"),
        (512, "icon_256x256@2x.png"),
        (512, "icon_512x512.png"),
        (1024, "icon_512x512@2x.png"),
    ]
    for s, name in sizes:
        resized = base_img.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(os.path.join(iconset_dir, name))

    if sys.platform == "darwin":
        subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", output_icns], check=True)
        # Dọn dẹp
        for f in os.listdir(iconset_dir):
            os.remove(os.path.join(iconset_dir, f))
        os.rmdir(iconset_dir)
        print(f"✅ Đã tạo icon macOS: {output_icns}")


def create_windows_ico(base_img, output_ico="AppIcon.ico"):
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    base_img.save(output_ico, format="ICO", sizes=ico_sizes)
    print(f"✅ Đã tạo icon Windows: {output_ico}")


if __name__ == "__main__":
    img = generate_base_icon()
    create_windows_ico(img)
    if sys.platform == "darwin":
        create_mac_icns(img)
