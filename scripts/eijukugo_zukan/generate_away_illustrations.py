#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw

OUT_DIR = Path('/Users/eight/Documents/MAYO/AUDIO 01/001_assets/question_images')
W, H = 768, 768

PINK_BG = '#f6efef'
CARD_BG = '#efefef'
BLACK = '#2b2b2b'
RED = '#ff5f76'
GRAY = '#b9bcc1'


def card_canvas():
    img = Image.new('RGB', (W, H), PINK_BG)
    d = ImageDraw.Draw(img)
    m = 26
    d.rounded_rectangle((m, m, W - m, H - m), radius=40, fill=CARD_BG)
    return img, d


def arrow_head(draw, p1, p2, color=RED, size=16):
    x1, y1 = p1
    x2, y2 = p2
    vx, vy = x2 - x1, y2 - y1
    ln = (vx * vx + vy * vy) ** 0.5 or 1
    ux, uy = vx / ln, vy / ln
    px, py = -uy, ux
    a = (x2, y2)
    b = (x2 - ux * size + px * (size * 0.65), y2 - uy * size + py * (size * 0.65))
    c = (x2 - ux * size - px * (size * 0.65), y2 - uy * size - py * (size * 0.65))
    draw.polygon([a, b, c], fill=color)


def away_path(draw, variant=0):
    if variant == 0:
        p0, p1 = (118, 575), (570, 280)
    elif variant == 1:
        p0, p1 = (162, 540), (610, 240)
    else:
        p0, p1 = (110, 540), (580, 300)

    draw.line((p0, p1), fill=BLACK, width=5)
    draw.line((p0[0] + 80, p0[1] - 30, p1[0] + 22, p1[1] - 8), fill=BLACK, width=5)

    r0 = (p0[0] + 110, p0[1] - 18)
    r1 = (p1[0] + 12, p1[1] + 10)
    draw.line((r0, r1), fill=RED, width=6)
    arrow_head(draw, r0, r1, color=RED, size=20)

    b0 = (p0[0] + 170, p0[1] - 62)
    b1 = (p1[0] - 34, p1[1] + 20)
    draw.line((b0, b1), fill=RED, width=10)
    arrow_head(draw, b0, b1, color=RED, size=22)


def draw_building(draw, x, y):
    draw.polygon([(x, y), (x + 72, y - 14), (x + 74, y + 112), (x + 2, y + 126)], outline=BLACK, width=5, fill='#fefefe')
    for r in range(4):
        for c in range(2):
            sx = x + 15 + c * 22
            sy = y + 15 + r * 25
            draw.rectangle((sx, sy, sx + 9, sy + 11), fill=BLACK)


def draw_waves(draw):
    curves = [
        (65, 540, 130, 565),
        (90, 590, 155, 612),
        (130, 620, 195, 640),
        (55, 575, 105, 598),
    ]
    for x0, y0, x1, y1 in curves:
        draw.arc((x0, y0, x1, y1), start=190, end=350, fill=BLACK, width=5)


def draw_person(draw, x, y):
    draw.ellipse((x, y, x + 56, y + 56), outline=BLACK, width=5, fill='#fafafa')
    draw.ellipse((x + 18, y + 56, x + 42, y + 96), outline='#d98f95', width=4, fill='#f6bcc3')
    draw.line((x + 42, y + 74, x + 70, y + 96), fill=BLACK, width=5)
    draw.line((x + 28, y + 92, x + 14, y + 120), fill=BLACK, width=5)
    draw.line((x + 52, y + 92, x + 68, y + 118), fill=BLACK, width=5)
    draw.rectangle((x - 18, y + 72, x + 2, y + 102), outline=BLACK, width=4, fill='#fefefe')


def draw_desk_chair(draw, x, y):
    draw.rectangle((x, y, x + 110, y + 22), outline=BLACK, width=5, fill='#fefefe')
    draw.line((x + 18, y + 22, x + 18, y + 62), fill=BLACK, width=5)
    draw.line((x + 90, y + 22, x + 90, y + 62), fill=BLACK, width=5)
    draw.ellipse((x - 66, y - 22, x - 22, y + 22), outline=BLACK, width=5, fill='#fafafa')
    draw.line((x - 44, y + 20, x - 44, y + 58), fill=BLACK, width=5)
    draw.ellipse((x - 56, y + 52, x - 30, y + 74), outline=BLACK, width=4)


def draw_bird(draw, x, y):
    draw.ellipse((x, y, x + 90, y + 62), outline=BLACK, width=5, fill='#f5b7bf')
    draw.ellipse((x + 52, y - 20, x + 86, y + 20), outline=BLACK, width=5, fill='#f5b7bf')
    draw.polygon([(x + 84, y - 2), (x + 104, y + 4), (x + 84, y + 12)], fill=BLACK)
    draw.arc((x + 10, y + 45, x + 70, y + 78), start=180, end=330, fill=BLACK, width=4)
    for i in range(4):
        ox = x - 12 - i * 14
        oy = y + 20 + i * 6
        draw.ellipse((ox, oy, ox + 4, oy + 4), fill=BLACK)


def draw_fade(draw):
    draw.line((96, 450, 450, 372), fill=RED, width=13)
    arrow_head(draw, (330, 398), (450, 372), color=RED, size=22)
    draw.line((100, 428, 360, 380), fill=BLACK, width=5)
    draw.line((90, 525, 600, 370), fill=BLACK, width=5)
    draw.line((120, 592, 640, 398), fill=BLACK, width=5)
    draw.line((460, 528, 610, 402), fill=BLACK, width=5)
    draw.ellipse((146, 356, 236, 446), outline=GRAY, width=5)
    draw.ellipse((265, 342, 335, 412), outline=GRAY, width=5)
    draw.ellipse((372, 330, 412, 370), outline=BLACK, width=5)
    draw.line((110, 398, 364, 354), fill=BLACK, width=5)


def draw_car(draw, x, y):
    draw.rounded_rectangle((x, y + 20, x + 120, y + 70), radius=16, outline=BLACK, width=5, fill='#fce2d2')
    draw.polygon([(x + 20, y + 20), (x + 44, y - 10), (x + 88, y - 10), (x + 108, y + 20)], outline=BLACK, width=5, fill='#fce2d2')
    draw.ellipse((x + 18, y + 58, x + 50, y + 90), outline=BLACK, width=5, fill='#fff')
    draw.ellipse((x + 78, y + 58, x + 110, y + 90), outline=BLACK, width=5, fill='#fff')


def draw_smile(draw, x, y):
    draw.ellipse((x, y, x + 82, y + 82), outline=BLACK, width=5, fill='#ffe2df')
    draw.ellipse((x + 20, y + 26, x + 28, y + 34), fill=BLACK)
    draw.ellipse((x + 52, y + 26, x + 60, y + 34), fill=BLACK)
    draw.arc((x + 18, y + 30, x + 64, y + 62), start=18, end=162, fill=BLACK, width=4)


def draw_snowman(draw, x, y):
    draw.ellipse((x, y + 38, x + 86, y + 130), outline=BLACK, width=5, fill='#fff')
    draw.ellipse((x + 40, y, x + 110, y + 70), outline=BLACK, width=5, fill='#fff')
    draw.line((x + 76, y + 12, x + 94, y + 34), fill=RED, width=6)
    draw.line((x + 96, y + 10, x + 112, y + 30), fill=RED, width=6)


def draw_flower(draw, x, y):
    draw.line((x + 42, y + 45, x + 42, y + 130), fill=BLACK, width=5)
    draw.ellipse((x + 18, y + 84, x + 40, y + 104), outline=BLACK, width=4)
    draw.ellipse((x + 44, y + 72, x + 68, y + 96), outline=BLACK, width=4)
    for dx, dy in [(0, 0), (18, -12), (34, 0), (18, 14), (8, 18)]:
        draw.ellipse((x + dx, y + dy, x + dx + 24, y + dy + 24), outline=BLACK, width=4, fill='#ffdce1')
    draw.ellipse((x + 18, y + 8, x + 34, y + 24), fill='#ffc462')


def draw_kettle(draw, x, y):
    draw.arc((x, y + 12, x + 120, y + 110), start=180, end=0, fill=BLACK, width=5)
    draw.line((x + 8, y + 62, x + 114, y + 62), fill=BLACK, width=5)
    draw.arc((x + 84, y + 38, x + 130, y + 84), start=240, end=80, fill=BLACK, width=5)
    draw.arc((x + 36, y - 8, x + 72, y + 20), start=0, end=180, fill=BLACK, width=5)
    draw.arc((x - 20, y + 34, x + 30, y + 78), start=270, end=70, fill=BLACK, width=5)
    for i in range(4):
        sx = x + 24 + i * 24
        draw.arc((sx, y - 40, sx + 20, y - 10), start=150, end=360, fill=BLACK, width=3)


def draw_worker(draw, x, y):
    draw_person(draw, x, y)
    draw.line((x + 82, y + 102, x + 138, y + 70), fill=BLACK, width=5)
    draw.line((x + 138, y + 70, x + 156, y + 88), fill=BLACK, width=5)


def draw_scene(draw, idx):
    if idx == 1:
        away_path(draw, 0)
        draw_waves(draw)
        draw_building(draw, 520, 150)
    elif idx == 2:
        away_path(draw, 1)
        draw_desk_chair(draw, 136, 492)
        draw_person(draw, 560, 150)
    elif idx == 3:
        away_path(draw, 0)
        draw.arc((80, 520, 260, 700), start=200, end=330, fill=BLACK, width=5)
        draw_bird(draw, 535, 210)
    elif idx == 4:
        draw_fade(draw)
    elif idx in (5, 6):
        away_path(draw, 2)
        draw_person(draw, 560, 150)
        if idx == 6:
            draw.rectangle((150, 500, 235, 570), outline=BLACK, width=5, fill='#fff')
            draw.line((150, 528, 235, 528), fill=BLACK, width=4)
    elif idx in (7, 8):
        away_path(draw, 1)
        draw_car(draw, 540, 160)
        if idx == 8:
            draw.arc((120, 500, 220, 600), start=290, end=60, fill=BLACK, width=5)
            draw.arc((106, 484, 234, 616), start=300, end=50, fill=BLACK, width=3)
    elif idx in (9, 10, 11):
        away_path(draw, 0)
        draw_smile(draw, 110, 210)
        if idx == 11:
            draw.arc((470, 160, 620, 290), start=200, end=340, fill=GRAY, width=4)
            draw.arc((500, 180, 680, 340), start=190, end=320, fill=GRAY, width=4)
    elif idx in (12, 13):
        away_path(draw, 0)
        draw_snowman(draw, 120, 420)
    elif idx in (14, 15):
        away_path(draw, 2)
        draw.line((560, 150, 610, 120), fill=RED, width=6)
        draw.line((590, 170, 640, 146), fill=RED, width=6)
        draw.line((610, 205, 650, 204), fill=RED, width=6)
        if idx == 15:
            draw_car(draw, 130, 430)
    elif idx in (16, 17):
        away_path(draw, 1)
        draw_flower(draw, 112, 220)
        draw_flower(draw, 228, 252)
        draw_flower(draw, 334, 276)
    elif idx in (18, 19):
        away_path(draw, 1)
        draw_kettle(draw, 108, 394)
    else:
        away_path(draw, 1)
        draw_worker(draw, 90, 432)
        if idx == 21:
            draw_worker(draw, 250, 390)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for idx in range(1, 22):
        img, draw = card_canvas()
        draw_scene(draw, idx)
        img.save(OUT_DIR / f'Q{idx:02d}.png')
    print(f'created {21} files in {OUT_DIR}')


if __name__ == '__main__':
    main()
