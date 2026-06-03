#!/usr/bin/env python3
"""
生成 Android 应用图标（各密度 PNG）
运行: python generate_icons.py
需要: Pillow (pip install Pillow)
"""
import os
from PIL import Image, ImageDraw, ImageFont

def draw_icon(size):
    """绘制一个带麦克风的渐变圆形图标"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 背景渐变（近似：顶色#667eea -> 底色#764ba2）
    for y in range(size):
        r = int(102 + (118 - 102) * y / size)
        g = int(126 + (75 - 126) * y / size)
        b = int(234 + (162 - 234) * y / size)
        draw.rectangle([(0, y), (size, y + 1)], fill=(r, g, b, 255))

    # 圆角蒙版
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    radius = int(size * 0.22)
    mask_draw.rounded_rectangle([(0, 0), (size - 1, size - 1)], radius=radius, fill=255)
    img.putalpha(mask)

    # 绘制白色麦克风图案
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    s = size / 108  # 缩放比

    # 麦克风主体（圆角矩形）
    mw = int(20 * s)
    mh = int(32 * s)
    mx = cx - mw // 2
    my = cy - int(22 * s)
    draw.rounded_rectangle(
        [(mx, my), (mx + mw, my + mh)],
        radius=int(10 * s),
        fill=(255, 255, 255, 230)
    )

    # 麦克风弧形支架
    arc_r = int(22 * s)
    arc_x = cx - arc_r
    arc_y = cy - int(2 * s)
    draw.arc(
        [(arc_x, arc_y), (arc_x + arc_r * 2, arc_y + arc_r * 2)],
        start=180, end=0,
        fill=(255, 255, 255, 200),
        width=int(3 * s)
    )

    # 麦克风竖杆
    stem_w = int(3 * s)
    stem_x = cx - stem_w // 2
    stem_top = cy + arc_r - int(2 * s)
    stem_bot = cy + int(26 * s)
    draw.rectangle(
        [(stem_x, stem_top), (stem_x + stem_w, stem_bot)],
        fill=(255, 255, 255, 200)
    )

    # 底部横杆
    bar_w = int(16 * s)
    bar_h = int(3 * s)
    draw.rectangle(
        [(cx - bar_w // 2, stem_bot), (cx + bar_w // 2, stem_bot + bar_h)],
        fill=(255, 255, 255, 200)
    )

    return img

# Android mipmap 尺寸规范
sizes = {
    'mipmap-mdpi':    48,
    'mipmap-hdpi':    72,
    'mipmap-xhdpi':   96,
    'mipmap-xxhdpi':  144,
    'mipmap-xxxhdpi': 192,
}

base = os.path.join(os.path.dirname(__file__), 'app', 'src', 'main', 'res')

for folder, size in sizes.items():
    out_dir = os.path.join(base, folder)
    os.makedirs(out_dir, exist_ok=True)

    icon = draw_icon(size)
    icon.save(os.path.join(out_dir, 'ic_launcher.png'))

    # round icon（圆形）
    round_icon = draw_icon(size)
    circle_mask = Image.new('L', (size, size), 0)
    cd = ImageDraw.Draw(circle_mask)
    cd.ellipse([(0, 0), (size - 1, size - 1)], fill=255)
    round_icon.putalpha(circle_mask)
    round_icon.save(os.path.join(out_dir, 'ic_launcher_round.png'))

    print(f"  ✓ {folder}: {size}x{size}")

print("\n✅ 图标生成完毕！")
