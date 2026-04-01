#!/usr/bin/env python3
import csv
import os
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CHAPTER = "AUDIO01-001"

ROWS = [
    {
        "chapter": CHAPTER,
        "index": 1,
        "english": "The hotel is five hundred meters away from the sea.",
        "japanese": "そのホテルは海から500メートル離れた所にある。",
        "ipa_us": "/ðə hoʊˈtɛl ɪz faɪv ˈhʌndrəd ˈmiːtərz əˈweɪ frəm ðə siː/",
    },
    {
        "chapter": CHAPTER,
        "index": 2,
        "english": "I'll be away for a week.",
        "japanese": "1週間留守にします。",
        "ipa_us": "/aɪl bi əˈweɪ fɔr ə wiːk/",
    },
    {
        "chapter": CHAPTER,
        "index": 3,
        "english": "The bird swam away when I got near.",
        "japanese": "私が近づくと鳥は泳いで去った。",
        "ipa_us": "/ðə bɝd swæm əˈweɪ wɛn aɪ ɡɑt nɪr/",
    },
    {
        "chapter": CHAPTER,
        "index": 4,
        "english": "He was crying away in his room.",
        "japanese": "彼は部屋で泣き続けていた。",
        "ipa_us": "/hi wəz ˈkraɪɪŋ əˈweɪ ɪn hɪz ruːm/",
    },
    {
        "chapter": CHAPTER,
        "index": 5,
        "english": "Go away.",
        "japanese": "立ち去れ。",
        "ipa_us": "/ɡoʊ əˈweɪ/",
    },
    {
        "chapter": CHAPTER,
        "index": 6,
        "english": "We'll go away for the weekend.",
        "japanese": "週末には出かけるつもりです。",
        "ipa_us": "/wil ɡoʊ əˈweɪ fɔr ðə ˈwiːkˌɛnd/",
    },
    {
        "chapter": CHAPTER,
        "index": 7,
        "english": "Drive away.",
        "japanese": "車で立ち去る。",
        "ipa_us": "/draɪv əˈweɪ/",
    },
    {
        "chapter": CHAPTER,
        "index": 8,
        "english": "I heard a car drive away.",
        "japanese": "車が立ち去る音が聞こえた。",
        "ipa_us": "/aɪ hɝd ə kɑr draɪv əˈweɪ/",
    },
    {
        "chapter": CHAPTER,
        "index": 9,
        "english": "Laugh away.",
        "japanese": "（心配などを）笑い飛ばす。",
        "ipa_us": "/læf əˈweɪ/",
    },
    {
        "chapter": CHAPTER,
        "index": 10,
        "english": "Laugh off.",
        "japanese": "（心配などを）笑って受け流す。",
        "ipa_us": "/læf ɔf/",
    },
    {
        "chapter": CHAPTER,
        "index": 11,
        "english": "He laughed away his worries.",
        "japanese": "彼は心配事を笑い飛ばした。",
        "ipa_us": "/hi læft əˈweɪ hɪz ˈwɝiz/",
    },
    {
        "chapter": CHAPTER,
        "index": 12,
        "english": "Melt away.",
        "japanese": "溶けてなくなる。",
        "ipa_us": "/mɛlt əˈweɪ/",
    },
    {
        "chapter": CHAPTER,
        "index": 13,
        "english": "The snowman melted away.",
        "japanese": "雪だるまが溶けてなくなった。",
        "ipa_us": "/ðə ˈsnoʊˌmæn ˈmɛltɪd əˈweɪ/",
    },
    {
        "chapter": CHAPTER,
        "index": 14,
        "english": "Die away.",
        "japanese": "（音・光などが）徐々に消える。",
        "ipa_us": "/daɪ əˈweɪ/",
    },
    {
        "chapter": CHAPTER,
        "index": 15,
        "english": "The noise of the car died away.",
        "japanese": "その車の騒音は徐々に消えていった。",
        "ipa_us": "/ðə nɔɪz əv ðə kɑr daɪd əˈweɪ/",
    },
    {
        "chapter": CHAPTER,
        "index": 16,
        "english": "Fade away.",
        "japanese": "（記憶・感情などが）徐々に消える。",
        "ipa_us": "/feɪd əˈweɪ/",
    },
    {
        "chapter": CHAPTER,
        "index": 17,
        "english": "This flower will soon fade away.",
        "japanese": "この花はすぐに枯れるだろう。",
        "ipa_us": "/ðɪs ˈflaʊər wɪl suːn feɪd əˈweɪ/",
    },
    {
        "chapter": CHAPTER,
        "index": 18,
        "english": "Boil away.",
        "japanese": "煮詰まって蒸発する。",
        "ipa_us": "/bɔɪl əˈweɪ/",
    },
    {
        "chapter": CHAPTER,
        "index": 19,
        "english": "The water in the kettle is boiling away.",
        "japanese": "やかんのお湯が蒸発しかけている。",
        "ipa_us": "/ðə ˈwɔtər ɪn ðə ˈkɛtəl ɪz ˈbɔɪlɪŋ əˈweɪ/",
    },
    {
        "chapter": CHAPTER,
        "index": 20,
        "english": "Work away.",
        "japanese": "せっせと働く。",
        "ipa_us": "/wɝk əˈweɪ/",
    },
    {
        "chapter": CHAPTER,
        "index": 21,
        "english": "He is working away in the fields.",
        "japanese": "彼は畑でせっせと働いている。",
        "ipa_us": "/hi ɪz ˈwɝkɪŋ əˈweɪ ɪn ðə fiːldz/",
    },
]

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "AUDIO01_001_away.csv"
QUESTION_DIR = BASE_DIR / "question_images"
ANSWER_DIR = BASE_DIR / "answer_images"


def pick_font(size: int, mono: bool = False):
    font_candidates = []
    if mono:
        font_candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
                "/System/Library/Fonts/SFNSMono.ttf",
            ]
        )
    font_candidates.extend(
        [
            "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
            "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]
    )
    for fp in font_candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int):
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        cand = w if not cur else f"{cur} {w}"
        width = draw.textbbox((0, 0), cand, font=font)[2]
        if width <= max_width:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def write_csv(rows):
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["chapter", "index", "english", "japanese", "ipa_us", "question_image", "answer_image"],
        )
        writer.writeheader()
        for row in rows:
            q_name = f"Q{row['index']:02d}.png"
            a_name = f"A{row['index']:02d}.png"
            out = dict(row)
            out["question_image"] = str((QUESTION_DIR / q_name).relative_to(BASE_DIR))
            out["answer_image"] = str((ANSWER_DIR / a_name).relative_to(BASE_DIR))
            writer.writerow(out)


def make_question_image(row):
    img = Image.new("RGB", (1600, 900), "#fffafc")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1600, 90), fill="#ffe6ee")

    title_font = pick_font(42)
    chapter_font = pick_font(30)
    body_font = pick_font(74)

    draw.text((60, 26), f"{row['chapter']}  Q{row['index']:02d}", font=chapter_font, fill="#8b3a4a")
    draw.text((1280, 22), "Question", font=title_font, fill="#d64a6a")

    max_width = 1450
    lines = wrap_text(draw, row["english"], body_font, max_width=max_width)

    total_h = len(lines) * 95
    y = (900 - total_h) // 2
    for line in lines:
        w = draw.textbbox((0, 0), line, font=body_font)[2]
        x = (1600 - w) // 2
        draw.text((x, y), line, font=body_font, fill="#1d1d1f")
        y += 95

    draw.text((60, 840), "Think: meaning + pronunciation", font=pick_font(30), fill="#666")
    return img


def make_answer_image(row):
    img = Image.new("RGB", (1600, 900), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1600, 90), fill="#ecf8ff")

    chapter_font = pick_font(30)
    en_font = pick_font(56)
    jp_font = pick_font(52)
    ipa_font = pick_font(44, mono=True)

    draw.text((60, 26), f"{row['chapter']}  A{row['index']:02d}", font=chapter_font, fill="#2d5d75")
    draw.text((1360, 22), "Answer", font=pick_font(42), fill="#2f88b8")

    en_lines = wrap_text(draw, row["english"], en_font, max_width=1450)
    y = 150
    for line in en_lines:
        draw.text((70, y), line, font=en_font, fill="#111")
        y += 78

    y += 38
    draw.text((70, y), row["japanese"], font=jp_font, fill="#1a4d39")

    y += 130
    ipa_lines = textwrap.wrap(row["ipa_us"], width=70)
    draw.text((70, y - 55), "US IPA", font=pick_font(34), fill="#555")
    for line in ipa_lines:
        draw.text((70, y), line, font=ipa_font, fill="#3b3b3b")
        y += 62

    return img


def make_images(rows):
    QUESTION_DIR.mkdir(parents=True, exist_ok=True)
    ANSWER_DIR.mkdir(parents=True, exist_ok=True)

    for row in rows:
        q_name = QUESTION_DIR / f"Q{row['index']:02d}.png"
        a_name = ANSWER_DIR / f"A{row['index']:02d}.png"
        make_question_image(row).save(q_name)
        make_answer_image(row).save(a_name)


def write_readme(rows):
    readme = BASE_DIR / "README_001_dataset.txt"
    with readme.open("w", encoding="utf-8") as f:
        f.write("AUDIO 01 / 001 away dataset\n")
        f.write("\n")
        f.write(f"Rows: {len(rows)}\n")
        f.write(f"CSV : {CSV_PATH.name}\n")
        f.write(f"Question images: {QUESTION_DIR.name}/Qxx.png\n")
        f.write(f"Answer images  : {ANSWER_DIR.name}/Axx.png\n")


def main():
    write_csv(ROWS)
    make_images(ROWS)
    write_readme(ROWS)
    print(f"Created: {CSV_PATH}")
    print(f"Created: {QUESTION_DIR} ({len(ROWS)} files)")
    print(f"Created: {ANSWER_DIR} ({len(ROWS)} files)")


if __name__ == "__main__":
    main()
