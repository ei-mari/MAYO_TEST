#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageOps

BASE = Path('/Users/eight/Documents/MAYO/AUDIO 01/001_assets')
INCOMING = BASE / 'incoming_q1_q4'
OUT = BASE / 'question_images'

# expected names in incoming_q1_q4
CANDIDATES = {
    1: ['Q1.png', 'q1.png', 'Q01.png', 'q01.png', '1.png'],
    2: ['Q2.png', 'q2.png', 'Q02.png', 'q02.png', '2.png'],
    3: ['Q3.png', 'q3.png', 'Q03.png', 'q03.png', '3.png'],
    4: ['Q4.png', 'q4.png', 'Q04.png', 'q04.png', '4.png'],
}


def find_src(idx: int):
    for name in CANDIDATES[idx]:
        p = INCOMING / name
        if p.exists():
            return p
    return None


def fit_square(src: Path, dst: Path, size=768):
    img = Image.open(src).convert('RGB')
    canvas = Image.new('RGB', (size, size), '#f6efef')

    # fit inside with a bit of margin
    target = size - 24
    fitted = ImageOps.contain(img, (target, target), Image.Resampling.LANCZOS)
    x = (size - fitted.width) // 2
    y = (size - fitted.height) // 2
    canvas.paste(fitted, (x, y))
    canvas.save(dst)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    missing = []
    applied = []

    for idx in range(1, 5):
        src = find_src(idx)
        if not src:
            missing.append(idx)
            continue
        dst = OUT / f'Q{idx:02d}.png'
        fit_square(src, dst)
        applied.append((idx, src.name, dst.name))

    if applied:
        print('Applied:')
        for idx, s, d in applied:
            print(f'  Q{idx}: {s} -> {d}')

    if missing:
        print('Missing image for:', ', '.join(f'Q{m}' for m in missing))
        raise SystemExit(1)

    print('Done: Q01-Q04 updated.')


if __name__ == '__main__':
    main()
