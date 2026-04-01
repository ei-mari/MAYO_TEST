from __future__ import annotations

import csv
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path("/Users/eight/Documents/MAYO")
AUDIO_ROOT = ROOT / "audio" / "eijukugo_zukan"
IMAGE_ROOT = ROOT / "images" / "eijukugo_zukan"
DATA_ROOT = ROOT / "data" / "eijukugo_zukan" / "units"
PUBLIC_ROOT = ROOT / "apps" / "eijukugo_zukan" / "cloudflare_quiz" / "public"
PUBLIC_AUDIO_ROOT = PUBLIC_ROOT / "audio" / "eijukugo_zukan"
PUBLIC_DATA_ROOT = PUBLIC_ROOT / "data" / "eijukugo_zukan" / "units"
SOURCE_AUDIO_ROOT = ROOT / "AUDIO 01"

SOURCE_AUDIO = {
    "U04": SOURCE_AUDIO_ROOT / "004 04 down.mp3",
    "U05": SOURCE_AUDIO_ROOT / "005 05 over.mp3",
    "U06": SOURCE_AUDIO_ROOT / "006 06 out.mp3",
    "U07": SOURCE_AUDIO_ROOT / "007 07 in.mp3",
    "U08": SOURCE_AUDIO_ROOT / "008 08 at.mp3",
    "U09": SOURCE_AUDIO_ROOT / "009 09 on.mp3",
    "U10": SOURCE_AUDIO_ROOT / "010 10 to.mp3",
}

TARGET_WORD = {
    "U04": "down",
    "U05": "over",
    "U06": "out",
    "U07": "in",
    "U08": "at",
    "U09": "on",
    "U10": "to",
}

UNITS = {
    "U04": [
        {"chunk": 3, "english": "Put your hand down.", "japanese": "手を降ろしなさい。"},
        {"chunk": 4, "english": "The train slowed down.", "japanese": "列車は速度を落とした。"},
        {"chunk": 5, "english": "This scrap metal will be melted down and used again.", "japanese": "この鉄くずは溶かして再利用されるでしょう。"},
        {"chunk": 6, "english": "He settled down on the sofa.", "japanese": "彼はソファにゆったりと座った。"},
        {"chunk": 8, "english": "The building suddenly fell down.", "japanese": "その建物は突然崩れ落ちた。"},
        {"chunk": 10, "english": "Write down your name and address.", "japanese": "名前と住所を書き留めなさい。"},
        {"chunk": 12, "english": "I want to lie down on the sofa.", "japanese": "ソファに横になりたい。"},
        {"chunk": 14, "english": "The soldiers laid down their weapons.", "japanese": "兵士たちは武器を置いた。"},
        {"chunk": 16, "english": "I hope things will calm down.", "japanese": "事態が落ち着くといいのですが。"},
        {"chunk": 18, "english": "My house was burned down.", "japanese": "私の家は焼け落ちた。"},
        {"chunk": 21, "english": "They decided to shut down the branch.", "japanese": "彼らはその支店を閉鎖することにした。"},
        {"chunk": 23, "english": "The wind died down.", "japanese": "風は次第に弱まった。"},
    ],
    "U05": [
        {"chunk": 3, "english": "He flew over to America.", "japanese": "彼はアメリカへ飛んで行った。"},
        {"chunk": 4, "english": "School is over.", "japanese": "学校は終わりだ。"},
        {"chunk": 5, "english": "Can I start over from the beginning?", "japanese": "最初からやり直してもいいですか。"},
        {"chunk": 6, "english": "Let's discuss this matter over lunch.", "japanese": "昼食をとりながらこの件を話し合いましょう。"},
        {"chunk": 8, "english": "I stopped over at Hong Kong.", "japanese": "私は香港に途中立ち寄った。"},
        {"chunk": 10, "english": "Let's cross over that bridge.", "japanese": "あの橋を渡ろう。"},
        {"chunk": 12, "english": "He leaned over and picked up a wallet.", "japanese": "彼は身をかがめて財布を拾った。"},
        {"chunk": 14, "english": "The soup is boiling over.", "japanese": "スープが吹きこぼれている。"},
        {"chunk": 16, "english": "The car rolled over in the street.", "japanese": "その車は通りで横転した。"},
        {"chunk": 18, "english": "Let's talk it over later.", "japanese": "それはあとでよく話し合おう。"},
        {"chunk": 20, "english": "I think you should think it over.", "japanese": "それをよく考えたほうがいいと思う。"},
        {"chunk": 22, "english": "Don't cry over spilt milk.", "japanese": "終わったことを嘆くな。"},
    ],
    "U06": [
        {"chunk": 3, "english": "Let's go out for a drink.", "japanese": "飲みに出かけよう。"},
        {"chunk": 5, "english": "Stars are out.", "japanese": "星が出ている。"},
        {"chunk": 6, "english": "The electricity is out again.", "japanese": "また停電している。"},
        {"chunk": 7, "english": "Hear me out.", "japanese": "最後まで話を聞いて。"},
        {"chunk": 9, "english": "How about eating out tonight?", "japanese": "今夜は外食しませんか。"},
        {"chunk": 11, "english": "He pointed out some mistakes in my English.", "japanese": "彼は私の英語の間違いをいくつか指摘した。"},
        {"chunk": 13, "english": "I found out he was lying.", "japanese": "彼がうそをついていたことが分かった。"},
        {"chunk": 16, "english": "I asked her out for a date.", "japanese": "私は彼女をデートに誘った。"},
        {"chunk": 18, "english": "He usually stretches out on the sofa after dinner.", "japanese": "彼はたいてい夕食後ソファで足を伸ばしてくつろぐ。"},
        {"chunk": 20, "english": "We must reach out to homeless people.", "japanese": "私たちはホームレスの人たちに手を差し伸べなければならない。"},
        {"chunk": 22, "english": "I have to hang out the laundry.", "japanese": "洗濯物を干さなければならない。"},
        {"chunk": 24, "english": "He laid out a large map on the desk.", "japanese": "彼は机の上に大きな地図を広げた。"},
        {"chunk": 26, "english": "They laid out a fortune on the wedding.", "japanese": "彼らは結婚式に大金をつぎ込んだ。"},
        {"chunk": 29, "english": "You can count me out this time.", "japanese": "今回は私を当てにしないで。"},
        {"chunk": 31, "english": "He spoke out against the decision.", "japanese": "彼はその決定に反対して声を上げた。"},
        {"chunk": 34, "english": "Don't stick your head out of the window.", "japanese": "窓の外に頭を出さないで。"},
        {"chunk": 36, "english": "That bird species died out a century ago.", "japanese": "その鳥の種は1世紀前に絶滅した。"},
        {"chunk": 38, "english": "Cross out the wrong words.", "japanese": "間違った語句を線で消しなさい。"},
        {"chunk": 40, "english": "Those shoes wear out easily.", "japanese": "あの靴はすぐすり減る。"},
        {"chunk": 42, "english": "Could you fill out this form?", "japanese": "この用紙に記入していただけますか。"},
    ],
    "U07": [
        {"chunk": 3, "english": "The train arrived in Asakusa.", "japanese": "電車は浅草に着いた。"},
        {"chunk": 4, "english": "Asakusa lies in the east of Tokyo.", "japanese": "浅草は東京の東部にある。"},
        {"chunk": 5, "english": "I'm in the construction business.", "japanese": "私は建設業をしています。"},
        {"chunk": 6, "english": "My boss will be in at noon.", "japanese": "上司は正午に出社します。"},
        {"chunk": 8, "english": "He took part in the speech contest.", "japanese": "彼はスピーチコンテストに参加した。"},
        {"chunk": 10, "english": "I'd like to check in this baggage.", "japanese": "この荷物を預けたいのですが。"},
        {"chunk": 12, "english": "He was involved in an accident.", "japanese": "彼は事故に巻き込まれた。"},
        {"chunk": 15, "english": "Help me in.", "japanese": "中に入るのを手伝って。"},
        {"chunk": 17, "english": "Fill in your name and address here.", "japanese": "ここに名前と住所を記入してください。"},
        {"chunk": 19, "english": "I usually stay in on Saturday nights.", "japanese": "私は土曜の夜はたいてい家にいる。"},
        {"chunk": 21, "english": "She is dressed in white today.", "japanese": "彼女は今日は白い服を着ている。"},
        {"chunk": 23, "english": "Do you believe in God?", "japanese": "あなたは神を信じますか。"},
    ],
    "U08": [
        {"chunk": 3, "english": "Our train arrived at Tokyo Station.", "japanese": "私たちの列車は東京駅に着いた。"},
        {"chunk": 4, "english": "The President arrived at Tokyo.", "japanese": "大統領は東京に到着した。"},
        {"chunk": 5, "english": "He threw a ball at me.", "japanese": "彼は私にボールを投げた。"},
        {"chunk": 6, "english": "My husband is still at work.", "japanese": "夫はまだ仕事中です。"},
        {"chunk": 8, "english": "I called at his office yesterday.", "japanese": "私は昨日彼の事務所に立ち寄った。"},
        {"chunk": 10, "english": "She's smiling at me.", "japanese": "彼女は私にほほえみかけている。"},
        {"chunk": 12, "english": "Don't laugh at me.", "japanese": "私を笑わないで。"},
        {"chunk": 14, "english": "He glanced at his watch.", "japanese": "彼はちらっと腕時計を見た。"},
        {"chunk": 16, "english": "Why are you staring at me?", "japanese": "どうして私をじっと見ているの。"},
        {"chunk": 18, "english": "She gazed at the diamond ring.", "japanese": "彼女はそのダイヤの指輪を見つめた。"},
        {"chunk": 20, "english": "Don't get angry at me.", "japanese": "私に腹を立てないで。"},
        {"chunk": 22, "english": "You don't have to shout at me.", "japanese": "私に怒鳴る必要はない。"},
        {"chunk": 24, "english": "He was surprised at the news.", "japanese": "彼はその知らせに驚いた。"},
        {"chunk": 26, "english": "The dog is sniffing at my bag.", "japanese": "犬が私のカバンのにおいをくんくんかいでいる。"},
        {"chunk": 27, "english": "Point A at B.", "japanese": "AをBに向けなさい。"},
        {"chunk": 28, "english": "Don't point your finger at me.", "japanese": "私に指をささないで。"},
        {"chunk": 30, "english": "He aimed a gun at the target.", "japanese": "彼は銃で的を狙った。"},
        {"chunk": 32, "english": "The hunter shot at a bird.", "japanese": "猟師は鳥を狙い撃ちした。"},
        {"chunk": 34, "english": "Can you make a guess at my age?", "japanese": "私の年齢を推測できますか。"},
        {"chunk": 36, "english": "He caught at the ball.", "japanese": "彼はボールに飛びつこうとした。"},
        {"chunk": 38, "english": "What are you driving at?", "japanese": "何を言いたいの？"},
    ],
    "U09": [
        {"chunk": 3, "english": "I want to stand on my own feet.", "japanese": "独り立ちがしたい。"},
        {"chunk": 4, "english": "Success depends on your effort.", "japanese": "成功は君の努力次第だ。"},
        {"chunk": 5, "english": "Concentrate on your work.", "japanese": "仕事に集中しなさい。"},
        {"chunk": 6, "english": "It is raining on and on.", "japanese": "雨がどんどん降り続いている。"},
        {"chunk": 8, "english": "I called on him yesterday.", "japanese": "昨日、彼を訪ねた。"},
        {"chunk": 11, "english": "Can I try it on?", "japanese": "試着してもいいですか。"},
        {"chunk": 13, "english": "You can rely on me.", "japanese": "私を当てにしてもいい。"},
        {"chunk": 15, "english": "Cows feed on grass.", "japanese": "牛は草を常食とする。"},
        {"chunk": 17, "english": "He lives on a small income.", "japanese": "彼は低収入で生活している。"},
        {"chunk": 19, "english": "It is based on a true story.", "japanese": "それは実話に基づいている。"},
        {"chunk": 21, "english": "Hang on to the rope.", "japanese": "ロープにしっかりつかまりなさい。"},
        {"chunk": 23, "english": "It's raining off and on.", "japanese": "雨が降ったりやんだりしている。"},
    ],
    "U10": [
        {"chunk": 3, "english": "The city lies to the north of Tokyo.", "japanese": "その都市は東京の北方にある。"},
        {"chunk": 4, "english": "He goes to work by car.", "japanese": "彼は車で会社に行く。"},
        {"chunk": 5, "english": "He grew up to be a doctor.", "japanese": "彼は成長して医者になった。"},
        {"chunk": 6, "english": "The Giants defeated the Dragons, 10 to 1.", "japanese": "ジャイアンツはドラゴンズに10対1で勝った。"},
        {"chunk": 8, "english": "Listen to me.", "japanese": "私の言うことに耳を傾けなさい。"},
        {"chunk": 10, "english": "All roads lead to Rome.", "japanese": "全ての道はローマに通じる。"},
        {"chunk": 12, "english": "His debts amounted to one million dollars.", "japanese": "彼の借金は百万ドルに達した。"},
        {"chunk": 14, "english": "I agree to your proposal.", "japanese": "あなたの提案に賛成です。"},
        {"chunk": 16, "english": "I belong to the tennis club.", "japanese": "私はテニスクラブに所属している。"},
        {"chunk": 18, "english": "Stick to your decision.", "japanese": "自分で決めたことを最後まで貫きなさい。"},
        {"chunk": 20, "english": "They objected to the construction of a new airport.", "japanese": "彼らは新空港の建設に反対した。"},
        {"chunk": 22, "english": "I prefer baseball to soccer.", "japanese": "私はサッカーより野球が好きだ。"},
    ],
}


def read_manifest(unit: str) -> dict[int, dict[str, str]]:
    path = DATA_ROOT / unit / "audio_manifest.tsv"
    rows: dict[int, dict[str, str]] = {}
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rows[int(row["chunk_index"])] = row
    return rows


def cloze_sentence(sentence: str, target: str) -> str:
    pattern = re.compile(rf"\b{re.escape(target)}\b", re.IGNORECASE)
    return pattern.sub("[BLANK]", sentence, count=1)


def cut_clip(source: Path, start: float, end: float, dest: Path) -> None:
    padded_start = max(0.0, start - 0.12)
    padded_end = end + 0.22
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-ss",
            f"{padded_start:.3f}",
            "-to",
            f"{padded_end:.3f}",
            "-i",
            str(source),
            "-vn",
            "-acodec",
            "libmp3lame",
            "-q:a",
            "2",
            str(dest),
        ],
        check=True,
    )


def build_unit(unit: str, entries: list[dict[str, str]]) -> None:
    source_audio = SOURCE_AUDIO[unit]
    target = TARGET_WORD[unit]
    manifest = read_manifest(unit)

    audio_dir = AUDIO_ROOT / unit
    public_audio_dir = PUBLIC_AUDIO_ROOT / unit
    data_dir = DATA_ROOT / unit
    public_data_dir = PUBLIC_DATA_ROOT / unit

    audio_dir.mkdir(parents=True, exist_ok=True)
    public_audio_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    public_data_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for idx, entry in enumerate(entries, start=1):
        qno = str(idx)
        qfile = f"Q{idx:02d}.png"
        sfile = f"S{idx:02d}.mp3"
        chunk = manifest[entry["chunk"]]
        start = float(chunk["start"])
        end = float(chunk["end"])

        dest = audio_dir / sfile
        cut_clip(source_audio, start, end, dest)
        shutil.copy2(dest, public_audio_dir / sfile)

        sentence = entry["english"]
        rows.append(
            {
                "chapter": unit,
                "qno": qno,
                "english": sentence,
                "japanese": entry["japanese"],
                "ipa_us": "",
                "question_image": f"/images/eijukugo_zukan/{unit}/{qfile}",
                "audio_file": f"/audio/eijukugo_zukan/{unit}/{sfile}",
                "phrasal": target,
                "accepted": target,
                "cloze": cloze_sentence(sentence, target),
            }
        )

    header = ["chapter", "qno", "english", "japanese", "ipa_us", "question_image", "audio_file", "phrasal", "accepted", "cloze"]
    for out_dir in (data_dir, public_data_dir):
        with (out_dir / "dataset.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(rows)


def main() -> None:
    for unit, entries in UNITS.items():
        build_unit(unit, entries)
        print(unit, len(entries))


if __name__ == "__main__":
    main()
