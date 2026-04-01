import re
import shutil
import subprocess
from pathlib import Path

import whisper


BASE_DIR = Path("/Users/eight/Documents/MAYO")
SRC_DIR = BASE_DIR / "AUDIO 01"
AUDIO_DIR = BASE_DIR / "audio" / "eijukugo_zukan"
PUBLIC_AUDIO_DIR = BASE_DIR / "apps" / "eijukugo_zukan" / "cloudflare_quiz" / "public" / "audio" / "eijukugo_zukan"
DATA_DIR = BASE_DIR / "data" / "eijukugo_zukan" / "units"
PUBLIC_DATA_DIR = BASE_DIR / "apps" / "eijukugo_zukan" / "cloudflare_quiz" / "public" / "data" / "eijukugo_zukan" / "units"

TRACKS = [
    ("U04", "004 04 down.mp3"),
    ("U05", "005 05 over.mp3"),
    ("U06", "006 06 out.mp3"),
    ("U07", "007 07 in.mp3"),
    ("U08", "008 08 at.mp3"),
    ("U09", "009 09 on.mp3"),
    ("U10", "010 10 to.mp3"),
    ("U11", "011 11 for.mp3"),
    ("U12", "012 12 from.mp3"),
    ("U13", "013 13 of.mp3"),
    ("U14", "014 14 with.mp3"),
    ("U15", "015 15 by - aside.mp3"),
    ("U16", "016 16 into.mp3"),
    ("U17", "017 17 after - along - across.mp3"),
    ("U18", "018 18 out of - through.mp3"),
    ("U19", "019 19 about - around.mp3"),
    ("U20", "020 20 back - forward - ahead.mp3"),
    ("U21", "021 21 together - apart.mp3"),
]

CLIP_OVERRIDES = {
    ("U02", 2): {"start_pad": 0.28, "end_pad": 0.45},
    ("U02", 3): {"start_pad": 0.26, "end_pad": 0.44},
    ("U02", 4): {"start_pad": 0.28, "end_pad": 0.42},
    ("U02", 5): {"start_pad": 0.26, "end_pad": 0.44},
    ("U02", 6): {"start_pad": 0.30, "end_pad": 0.46},
    ("U02", 8): {"start_pad": 0.30, "end_pad": 0.48},
    ("U02", 9): {"start_pad": 0.28, "end_pad": 0.46},
    ("U02", 11): {"start_pad": 0.30, "end_pad": 0.48},
    ("U02", 12): {"start_pad": 0.30, "end_pad": 0.52},
}

INTRO_WORDS = {"chapter", "unit"}
PRONOUNS_AND_HELPERS = {
    "i", "i'll", "i'd", "i'm", "you", "your", "yours", "he", "she", "it", "we", "they",
    "me", "him", "her", "us", "them", "my", "our", "their", "this", "that", "these", "those",
    "the", "a", "an", "can", "could", "what", "when", "where", "why", "how", "let's", "lets",
    "don't", "dont", "do", "does", "did", "will", "would", "should", "must", "please",
}


def run(cmd):
    return subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def speech_intervals(src: Path):
    res = run([
        "ffmpeg",
        "-hide_banner",
        "-nostats",
        "-i",
        str(src),
        "-af",
        "silencedetect=noise=-30dB:d=0.25",
        "-f",
        "null",
        "-",
    ])
    starts = [float(m.group(1)) for m in re.finditer(r"silence_start: ([0-9.]+)", res.stderr)]
    ends = [float(m.group(1)) for m in re.finditer(r"silence_end: ([0-9.]+)", res.stderr)]
    intervals = []
    for idx, end in enumerate(ends):
        if idx + 1 >= len(starts):
            break
        nxt = starts[idx + 1]
        if nxt > end:
            intervals.append((end, nxt))
    return intervals


def transcribe_chunk(model, src: Path, start: float, end: float, tmp_wav: Path):
    run([
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{start:.3f}",
        "-to",
        f"{end:.3f}",
        "-i",
        str(src),
        "-ac",
        "1",
        "-ar",
        "16000",
        str(tmp_wav),
    ])
    return model.transcribe(str(tmp_wav), language="en", fp16=False, verbose=False)["text"].strip()


def word_tokens(text: str):
    return re.findall(r"[A-Za-z']+", text)


def is_sentence(text: str, duration: float):
    tokens = word_tokens(text)
    lowered = [token.lower() for token in tokens]
    if not tokens:
        return False
    if any(token in INTRO_WORDS for token in lowered):
        return False
    if len(tokens) == 1:
        return False
    if len(tokens) == 2 and duration <= 1.25:
        return False
    if len(tokens) >= 4:
        return True
    if any(token in PRONOUNS_AND_HELPERS for token in lowered):
        return True
    if "?" in text:
        return True
    if duration >= 1.35:
        return True
    return False


def cut_mp3(src: Path, start: float, end: float, out_path: Path):
    run([
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        f"{start:.3f}",
        "-to",
        f"{end:.3f}",
        "-i",
        str(src),
        "-vn",
        "-acodec",
        "libmp3lame",
        "-q:a",
        "4",
        str(out_path),
    ])


def process_track(model, unit: str, filename: str):
    src = SRC_DIR / filename
    out_dir = AUDIO_DIR / unit
    public_out_dir = PUBLIC_AUDIO_DIR / unit
    data_dir = DATA_DIR / unit
    public_data_dir = PUBLIC_DATA_DIR / unit
    out_dir.mkdir(parents=True, exist_ok=True)
    public_out_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    public_data_dir.mkdir(parents=True, exist_ok=True)

    intervals = speech_intervals(src)
    manifest_rows = []
    sentence_count = 0

    for idx, (start, end) in enumerate(intervals, 1):
        tmp_wav = Path(f"/tmp/{unit}_{idx:02d}.wav")
        text = transcribe_chunk(model, src, start, end, tmp_wav)
        duration = end - start
        keep = is_sentence(text, duration)
        clip_name = ""

        if keep:
          sentence_count += 1
          clip_name = f"S{sentence_count:02d}.mp3"
          pads = CLIP_OVERRIDES.get((unit, sentence_count), {})
          clip_start = max(0, start - pads.get("start_pad", 0.20))
          clip_end = end + pads.get("end_pad", 0.24)
          out_path = out_dir / clip_name
          cut_mp3(src, clip_start, clip_end, out_path)
          shutil.copy2(out_path, public_out_dir / clip_name)

        manifest_rows.append(
            {
                "chunk_index": idx,
                "start": f"{start:.3f}",
                "end": f"{end:.3f}",
                "duration": f"{duration:.3f}",
                "type": "sentence" if keep else "skip",
                "clip": clip_name,
                "text": text,
            }
        )

    header = "chunk_index\tstart\tend\tduration\ttype\tclip\ttext\n"
    body = "".join(
        f"{row['chunk_index']}\t{row['start']}\t{row['end']}\t{row['duration']}\t{row['type']}\t{row['clip']}\t{row['text']}\n"
        for row in manifest_rows
    )
    for path in (data_dir / "audio_manifest.tsv", public_data_dir / "audio_manifest.tsv"):
        path.write_text(header + body, encoding="utf-8")

    return sentence_count


def main():
    model = whisper.load_model("tiny")
    for unit, filename in TRACKS:
        count = process_track(model, unit, filename)
        print(f"{unit}\t{filename}\t{count}")


if __name__ == "__main__":
    main()
