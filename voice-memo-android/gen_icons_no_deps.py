#!/usr/bin/env python3
"""
生成 Android 应用图标（不依赖第三方库，使用纯 Python struct 生成 PNG）
"""
import os
import struct
import zlib
import math

def create_png(width, height, pixels):
    """pixels: list of (r,g,b,a) tuples, row by row"""
    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr = chunk(b'IHDR', ihdr_data)

    raw_rows = []
    for y in range(height):
        row = b'\x00'  # filter type = None
        for x in range(width):
            r, g, b, a = pixels[y * width + x]
            row += struct.pack('BBBB', r, g, b, a)
        raw_rows.append(row)

    raw = zlib.compress(b''.join(raw_rows), 9)
    idat = chunk(b'IDAT', raw)
    iend = chunk(b'IEND', b'')
    return sig + ihdr + idat + iend


def lerp(a, b, t):
    return int(a + (b - a) * t)


def draw_icon(size):
    pixels = []
    cx, cy = size / 2, size / 2
    radius = size / 2  # 圆形

    # 渐变色：左上 #667eea -> 右下 #764ba2
    start_rgb = (102, 126, 234)
    end_rgb   = (118, 75, 162)

    for y in range(size):
        for x in range(size):
            # 计算是否在圆内
            dx, dy = x - cx + 0.5, y - cy + 0.5
            dist = math.sqrt(dx*dx + dy*dy)

            if dist > radius - 0.5:
                pixels.append((0, 0, 0, 0))
                continue

            t = (x + y) / (2 * size)
            r = lerp(start_rgb[0], end_rgb[0], t)
            g = lerp(start_rgb[1], end_rgb[1], t)
            b = lerp(start_rgb[2], end_rgb[2], t)

            # 轻微抗锯齿
            if dist > radius - 1.5:
                alpha = int(255 * (radius - 0.5 - dist))
                alpha = max(0, min(255, alpha))
            else:
                alpha = 255

            # 绘制麦克风（白色）
            s = size / 96
            mic_x = cx - 8 * s
            mic_y = cy - 18 * s
            mic_w = 16 * s
            mic_h = 24 * s

            # 麦克风主体矩形（圆角近似）
            in_mic_body = (mic_x <= x <= mic_x + mic_w and
                           mic_y <= y <= mic_y + mic_h)

            # 麦克风弧形（半圆）
            arc_r = 18 * s
            arc_cx, arc_cy = cx, cy + 2 * s
            arc_dist = math.sqrt((x - arc_cx)**2 + (y - arc_cy)**2)
            in_arc_outer = arc_dist <= arc_r + 1.5 * s
            in_arc_inner = arc_dist <= arc_r - 1.5 * s
            in_arc = (in_arc_outer and not in_arc_inner and y <= arc_cy)

            # 竖杆
            stem_x1, stem_x2 = cx - 1.5 * s, cx + 1.5 * s
            stem_y1, stem_y2 = arc_cy, cy + 22 * s
            in_stem = (stem_x1 <= x <= stem_x2 and stem_y1 <= y <= stem_y2)

            # 横杆
            bar_x1, bar_x2 = cx - 10 * s, cx + 10 * s
            bar_y1, bar_y2 = cy + 21 * s, cy + 24 * s
            in_bar = (bar_x1 <= x <= bar_x2 and bar_y1 <= y <= bar_y2)

            if in_mic_body or in_arc or in_stem or in_bar:
                pixels.append((255, 255, 255, alpha))
            else:
                pixels.append((r, g, b, alpha))

    return pixels


sizes = {
    'mipmap-mdpi':    48,
    'mipmap-hdpi':    72,
    'mipmap-xhdpi':   96,
    'mipmap-xxhdpi':  144,
    'mipmap-xxxhdpi': 192,
}

script_dir = os.path.dirname(os.path.abspath(__file__))
base = os.path.join(script_dir, 'app', 'src', 'main', 'res')

for folder, size in sizes.items():
    out_dir = os.path.join(base, folder)
    os.makedirs(out_dir, exist_ok=True)

    print(f"  生成 {folder} ({size}x{size})...", end='', flush=True)
    pixels = draw_icon(size)
    png_data = create_png(size, size, pixels)

    with open(os.path.join(out_dir, 'ic_launcher.png'), 'wb') as f:
        f.write(png_data)
    with open(os.path.join(out_dir, 'ic_launcher_round.png'), 'wb') as f:
        f.write(png_data)
    print(" ✓")

print("\n✅ 所有图标生成完毕！")
