from __future__ import annotations

import csv
import re
import shutil
import subprocess
from pathlib import Path

import eng_to_ipa as ipa


ROOT = Path("/Users/eight/Documents/MAYO")
DATA_ROOT = ROOT / "data" / "eijukugo_zukan" / "units"
PUBLIC_DATA_ROOT = (
    ROOT
    / "apps"
    / "eijukugo_zukan"
    / "cloudflare_quiz"
    / "public"
    / "data"
    / "eijukugo_zukan"
    / "units"
)
SOURCE_AUDIO_ROOT = ROOT / "AUDIO 01"
AUDIO_ROOT = ROOT / "audio" / "eijukugo_zukan"
PUBLIC_AUDIO_ROOT = (
    ROOT
    / "apps"
    / "eijukugo_zukan"
    / "cloudflare_quiz"
    / "public"
    / "audio"
    / "eijukugo_zukan"
)

SOURCE_AUDIO = {
    "U11": SOURCE_AUDIO_ROOT / "011 11 for.mp3",
    "U12": SOURCE_AUDIO_ROOT / "012 12 from.mp3",
    "U13": SOURCE_AUDIO_ROOT / "013 13 of.mp3",
    "U14": SOURCE_AUDIO_ROOT / "014 14 with.mp3",
    "U15": SOURCE_AUDIO_ROOT / "015 15 by - aside.mp3",
    "U16": SOURCE_AUDIO_ROOT / "016 16 into.mp3",
    "U17": SOURCE_AUDIO_ROOT / "017 17 after - along - across.mp3",
    "U18": SOURCE_AUDIO_ROOT / "018 18 out of - through.mp3",
    "U19": SOURCE_AUDIO_ROOT / "019 19 about - around.mp3",
    "U20": SOURCE_AUDIO_ROOT / "020 20 back - forward - ahead.mp3",
    "U21": SOURCE_AUDIO_ROOT / "021 21 together - apart.mp3",
}

CURATED: dict[str, list[dict[str, object]]] = {
    "U11": [
        {"english": "I bought a present for him.", "japanese": "私は彼にプレゼントを買った。", "phrasal": "for", "chunk": 3},
        {"english": "This is for you.", "japanese": "これはあなたへのプレゼントです。", "phrasal": "for", "chunk": 4},
        {"english": "I bought this watch for 1000 dollars.", "japanese": "私はこの腕時計を1000ドルで買った。", "phrasal": "for", "chunk": 5},
        {"english": "Thank you for the present.", "japanese": "プレゼントをありがとうございます。", "phrasal": "for", "chunk": 6},
        {"english": "This country is heading for recession.", "japanese": "この国は不況に向かっている。", "phrasal": "for", "chunk": 8},
        {"english": "That company is searching for a new CEO.", "japanese": "その会社は新しいCEOを探している。", "phrasal": "for", "chunk": 16},
        {"english": "This train is bound for Osaka.", "japanese": "この列車は大阪行きです。", "phrasal": "for", "chunk": 10},
        {"english": "The baby is crying for milk.", "japanese": "赤ちゃんは泣いてミルクを求めている。", "phrasal": "for", "chunk": 18},
        {"english": "I voted for that law.", "japanese": "私はその法律に賛成票を投じた。", "phrasal": "for", "chunk": 12},
        {"english": "I asked for her advice.", "japanese": "彼女の助言を求めた。", "phrasal": "for", "chunk": 21},
        {"english": "I'm dying for a beer.", "japanese": "私はビールが飲みたくてたまらない。", "phrasal": "for", "chunk": 14},
        {"english": "We hoped for a successful result.", "japanese": "私たちは首尾よい結果を願った。", "phrasal": "for", "chunk": 23},
        {"english": "We wish for world peace.", "japanese": "私たちは世界平和を願っている。", "phrasal": "for", "chunk": 25},
        {"english": "He spilled his drink while reaching for the salt.", "japanese": "彼は塩に手を伸ばしている時に飲み物をこぼした。", "phrasal": "for", "chunk": 33},
        {"english": "They longed for his safe return.", "japanese": "彼らは彼が無事に戻って来ることを切望した。", "phrasal": "for", "chunk": 27},
        {"english": "Could you exchange these pants for bigger ones?", "japanese": "このズボンをもっと大きいのと交換してくれますか。", "phrasal": "for", "chunk": 35},
        {"english": "I waited for him to come.", "japanese": "彼が来るのを待った。", "phrasal": "for", "chunk": 29},
        {"english": "You can substitute margarine for butter.", "japanese": "バターの代わりにマーガリンが使えます。", "phrasal": "for", "chunk": 37},
        {"english": "Many people applied for the job.", "japanese": "その仕事に多くの人が応募した。", "phrasal": "for", "chunk": 31},
        {"english": "How much did you pay for the car?", "japanese": "その車にいくら払いましたか。", "phrasal": "for", "chunk": 39},
    ],
    "U12": [
        {"english": "He took the knife from the robber.", "japanese": "彼は強盗からナイフを取った。", "phrasal": "from", "chunk": 3},
        {"english": "She makes jam from apricots.", "japanese": "彼女はアンズでジャムを作る。", "phrasal": "from", "chunk": 4},
        {"english": "The cat shivers from cold.", "japanese": "ネコは寒さで震えている。", "phrasal": "from", "chunk": 5},
        {"english": "The accident kept me from coming in time.", "japanese": "その事故で私は間に合わなかった。", "phrasal": "from", "chunk": 6},
        {"english": "The twins are so alike I can't tell one from the other.", "japanese": "その双子はそっくりで区別がつかない。", "phrasal": "from", "chunk": 8},
        {"english": "The accident resulted from the driver's carelessness.", "japanese": "その事故はドライバーの不注意の結果起こった。", "phrasal": "from", "chunk": 16},
        {"english": "My car differs from yours in color.", "japanese": "私の車はあなたの車とは色が違う。", "phrasal": "from", "chunk": 10},
        {"english": "Please refrain from smoking.", "japanese": "たばこはご遠慮ください。", "phrasal": "from", "chunk": 18},
        {"english": "Many children die from starvation.", "japanese": "多くの子どもたちは飢えによって亡くなる。", "phrasal": "from", "chunk": 12},
        {"english": "The typhoon prevented the train from arriving on time.", "japanese": "台風のために列車は時間通り到着できなかった。", "phrasal": "from", "chunk": 21},
        {"english": "He's suffering from depression.", "japanese": "彼はうつ病に苦しんでいる。", "phrasal": "from", "chunk": 14},
        {"english": "The law prohibits minors from drinking.", "japanese": "法律で未成年の飲酒を禁止している。", "phrasal": "from", "chunk": 25},
    ],
    "U13": [
        {"english": "This beer is free of charge.", "japanese": "このビールは無料です。", "phrasal": "of", "chunk": 3},
        {"english": "They came to the same conclusion independent of each other.", "japanese": "彼らはお互いに影響を受けることなく同じ結論に達した。", "phrasal": "of", "chunk": 4},
        {"english": "This desk is made of wood.", "japanese": "この机は木でできている。", "phrasal": "of", "chunk": 5},
        {"english": "I always think of you.", "japanese": "私はいつもあなたのことを思っています。", "phrasal": "of", "chunk": 6},
        {"english": "The thief robbed me of my bag.", "japanese": "泥棒は私のバッグを奪った。", "phrasal": "of", "chunk": 8},
        {"english": "America consists of 50 states.", "japanese": "アメリカは50州から成り立つ。", "phrasal": "of", "chunk": 16},
        {"english": "They cleared the roads of snow.", "japanese": "彼らは道路の除雪をした。", "phrasal": "of", "chunk": 10},
        {"english": "Speak of the devil, and he'll soon appear.", "japanese": "噂をすれば影が差す。", "phrasal": "of", "span": (18, 19)},
        {"english": "The doctor cured me of the disease.", "japanese": "医者は私の病気を治してくれた。", "phrasal": "of", "chunk": 12},
        {"english": "I heard nothing of him after that.", "japanese": "その後、彼の噂を聞かなかった。", "phrasal": "of", "chunk": 21},
        {"english": "You should dispose of these books.", "japanese": "これらの本を処分したほうがいいですよ。", "phrasal": "of", "chunk": 14},
        {"english": "He's always complaining of something.", "japanese": "彼はいつも何かに不平を言っている。", "phrasal": "of", "chunk": 23},
    ],
    "U14": [
        {"english": "Do you want some sugar with your coffee?", "japanese": "コーヒーに砂糖を入れますか。", "phrasal": "with", "chunk": 3},
        {"english": "The robber threatened the clerk with a gun.", "japanese": "強盗は銃で店員を脅した。", "phrasal": "with", "chunk": 4},
        {"english": "I agree with you.", "japanese": "私はあなたに賛成です。", "phrasal": "with", "chunk": 5},
        {"english": "He's always quarreling with his wife.", "japanese": "彼はいつも妻と口論ばかりしている。", "phrasal": "with", "chunk": 6},
        {"english": "The glass is filled with wine.", "japanese": "グラスはワインで満たされている。", "phrasal": "with", "chunk": 8},
        {"english": "The room is furnished with a bed and a sofa.", "japanese": "その部屋はベッドとソファが備え付けられている。", "phrasal": "with", "chunk": 16},
        {"english": "The mountain is covered with snow.", "japanese": "山は雪で覆われている。", "phrasal": "with", "chunk": 10},
        {"english": "He was presented with an award.", "japanese": "彼は賞を贈呈された。", "phrasal": "with", "chunk": 18},
        {"english": "The bus is crowded with passengers.", "japanese": "バスは乗客で混み合っている。", "phrasal": "with", "chunk": 12},
        {"english": "He's a difficult person to deal with.", "japanese": "彼は扱いにくい人だ。", "phrasal": "with", "chunk": 20},
        {"english": "They were equipped with weapons.", "japanese": "彼らは武器を装備していた。", "phrasal": "with", "chunk": 14},
        {"english": "Cows provide us with milk.", "japanese": "牛は私たちに牛乳を供給する。", "phrasal": "with", "chunk": 22},
        {"english": "He planted the garden with tulips.", "japanese": "彼は庭にチューリップを植えた。", "phrasal": "with", "chunk": 24},
        {"english": "The company is faced with a difficult situation.", "japanese": "その会社は難しい状況に直面している。", "phrasal": "with", "chunk": 32},
        {"english": "They replaced coal with oil.", "japanese": "彼らは石炭を石油に替えた。", "phrasal": "with", "chunk": 26},
        {"english": "I compared my answer with his.", "japanese": "私の答えを彼の答えと比べた。", "phrasal": "with", "chunk": 34},
        {"english": "Oil does not mix with water.", "japanese": "油は水と混ざらない。", "phrasal": "with", "chunk": 28},
        {"english": "Japan competed for a gold medal with America.", "japanese": "日本は金メダルをかけてアメリカと競った。", "phrasal": "with", "chunk": 36},
        {"english": "I correspond with a friend in India.", "japanese": "私はインドの友達と文通している。", "phrasal": "with", "chunk": 30},
        {"english": "The police officer struggled with a robber.", "japanese": "警察官は強盗と格闘した。", "phrasal": "with", "chunk": 38},
    ],
    "U15": [
        {"english": "The orchestra was conducted by Ozawa Seiji.", "japanese": "そのオーケストラは小澤征爾によって指揮された。", "phrasal": "by", "chunk": 4},
        {"english": "How do you go to work? I go to work by train.", "japanese": "「通勤方法は何ですか」「電車で通勤します」", "phrasal": "by", "span": (5, 6)},
        {"english": "I seldom watch TV, aside from news.", "japanese": "ニュースは別として、テレビをめったに見ません。", "phrasal": "aside", "span": (7, 8)},
        {"english": "Will you move that box aside?", "japanese": "その箱を脇へどけてくれますか。", "phrasal": "aside", "chunk": 9},
        {"english": "I saw children running by.", "japanese": "子どもたちが走って通り過ぎるのが見えた。", "phrasal": "by", "chunk": 11},
        {"english": "He stepped aside for me to pass.", "japanese": "私が通れるように彼はわきに寄った。", "phrasal": "aside", "chunk": 20},
        {"english": "Come by on your way home.", "japanese": "家に帰る途中に立ち寄ってください。", "phrasal": "by", "chunk": 13},
        {"english": "He laid aside his glasses.", "japanese": "彼はメガネをわきに置いた。", "phrasal": "aside", "chunk": 22},
        {"english": "Can I stop by at that convenience store?", "japanese": "あのコンビニにちょっと寄ってもいい？", "phrasal": "by", "chunk": 15},
        {"english": "You should lay aside this money for the future.", "japanese": "将来のためにこのお金を取っておいたほうがいいでしょう。", "phrasal": "aside", "chunk": 24},
        {"english": "I'll set this money aside for the future.", "japanese": "将来のためにこのお金を取っておきます。", "phrasal": "aside", "chunk": 18},
        {"english": "He elbowed people aside.", "japanese": "彼は人々を肘で押しのけた。", "phrasal": "aside", "chunk": 27},
    ],
    "U16": [
        {"english": "The car crashed into the wall.", "japanese": "車は壁に衝突した。", "phrasal": "into", "chunk": 3},
        {"english": "I'm into jazz.", "japanese": "ジャズにはまっています。", "phrasal": "into", "chunk": 4},
        {"english": "I don't have time to go into detail.", "japanese": "詳しく説明している時間はない。", "phrasal": "into", "chunk": 5},
        {"english": "The plate broke into pieces.", "japanese": "皿は粉々に割れた。", "phrasal": "into", "chunk": 6},
        {"english": "I bumped into my ex-girlfriend yesterday.", "japanese": "昨日、元カノに偶然会った。", "phrasal": "into", "chunk": 8},
        {"english": "Can you translate this sentence into Chinese?", "japanese": "この文を中国語に翻訳できますか。", "phrasal": "into", "chunk": 17},
        {"english": "I'll change into a suit.", "japanese": "スーツに着替えます。", "phrasal": "into", "chunk": 10},
        {"english": "The class burst into laughter at the teacher's joke.", "japanese": "クラスのみんなが先生の冗談に突然笑い出した。", "phrasal": "into", "chunk": 19},
        {"english": "The ice melted into water.", "japanese": "氷は溶けて水になった。", "phrasal": "into", "chunk": 12},
        {"english": "His business grew into a big company.", "japanese": "彼の会社は大企業に成長した。", "phrasal": "into", "chunk": 21},
        {"english": "Mother divided the cake into five.", "japanese": "母はケーキを5個に分けた。", "phrasal": "into", "chunk": 14},
        {"english": "I talked him into giving up smoking.", "japanese": "彼を説得して禁煙させた。", "phrasal": "into", "chunk": 25},
    ],
    "U17": [
        {"english": "He paints pictures after Monet.", "japanese": "彼はモネ風の絵を描く。", "phrasal": "after", "chunk": 5},
        {"english": "They continued the work day after day.", "japanese": "彼らは来る日も来る日も仕事を続けた。", "phrasal": "after", "chunk": 6},
        {"english": "Add milk along with butter to the soup.", "japanese": "バターと一緒にミルクをスープに加えます。", "phrasal": "along", "chunk": 7},
        {"english": "His house is across the street from the library.", "japanese": "彼の家は図書館の向かいにある。", "phrasal": "across", "chunk": 8},
        {"english": "The police officer chased after the pickpocket.", "japanese": "警察官はそのスリを追いかけた。", "phrasal": "after", "chunk": 10},
        {"english": "You'll make it up as you go along.", "japanese": "やっていくうちに遅れを取り戻せるよ。", "phrasal": "along", "chunk": 19},
        {"english": "He continued to seek after the truth.", "japanese": "彼は真実を追い求め続けた。", "phrasal": "after", "chunk": 12},
        {"english": "I can't go along with your proposal.", "japanese": "あなたの提案には賛成できません。", "phrasal": "along", "chunk": 21},
        {"english": "My father named me after a famous actor.", "japanese": "父は有名な俳優にちなんで私に名前をつけた。", "phrasal": "after", "chunk": 15},
        {"english": "I'll come along, too.", "japanese": "私も一緒に行きます。", "phrasal": "along", "chunk": 23},
        {"english": "Go along this street.", "japanese": "この道を進んでください。", "phrasal": "along", "chunk": 17},
        {"english": "I ran across him at the airport.", "japanese": "空港で偶然彼に会った。", "phrasal": "across", "chunk": 25},
    ],
    "U18": [
        {"english": "Take your hands out of your pockets.", "japanese": "ポケットから手を出しなさい。", "phrasal": "out of", "chunk": 4},
        {"english": "We are out of danger.", "japanese": "危険な状態から脱している。", "phrasal": "out of", "chunk": 5},
        {"english": "This train goes through to Ginza.", "japanese": "この列車は銀座まで乗り換えなしで行きます。", "phrasal": "through", "chunk": 6},
        {"english": "This shop is open Monday through Saturday.", "japanese": "この店は月曜日から土曜日までやっています。", "phrasal": "through", "chunk": 7},
        {"english": "He cheated me out of my money.", "japanese": "彼は私からお金をだまし取った。", "phrasal": "out of", "chunk": 9},
        {"english": "Have you read the report through?", "japanese": "報告書を全部読みましたか。", "phrasal": "through", "chunk": 20},
        {"english": "I talked him out of marrying her.", "japanese": "私は彼を説得して彼女との結婚を思いとどまらせた。", "phrasal": "out of", "chunk": 13},
        {"english": "I couldn't see through his lies.", "japanese": "彼の嘘を見抜けなかった。", "phrasal": "through", "chunk": 22},
        {"english": "The ship went out of sight.", "japanese": "その船は見えなくなった。", "phrasal": "out of", "chunk": 15},
        {"english": "I want to see this job through.", "japanese": "私はこの仕事を最後までやり通したい。", "phrasal": "through", "chunk": 25},
        {"english": "Stay out of my business.", "japanese": "私のことに関わらないで。", "phrasal": "out of", "chunk": 17},
        {"english": "The Thames flows through London.", "japanese": "テムズ川はロンドンを貫流している。", "phrasal": "through", "chunk": 27},
    ],
    "U19": [
        {"english": "He writes many books about cats.", "japanese": "彼はネコに関する本をたくさん書いています。", "phrasal": "about", "chunk": 4},
        {"english": "That rock is about to fall.", "japanese": "その岩は今にも落ちそうだ。", "phrasal": "about", "chunk": 5},
        {"english": "I want to travel around the world.", "japanese": "世界一周旅行をしたい。", "phrasal": "around", "chunk": 6},
        {"english": "Turn around the corner.", "japanese": "その角を曲がってください。", "phrasal": "around", "chunk": 7},
        {"english": "What are you talking about?", "japanese": "何について話しているのですか。", "phrasal": "about", "chunk": 9},
        {"english": "I went around to his office.", "japanese": "彼のオフィスに立ち寄った。", "phrasal": "around", "chunk": 17},
        {"english": "What are you thinking about?", "japanese": "何のことを考えているの？", "phrasal": "about", "chunk": 11},
        {"english": "I hung around the bookshop.", "japanese": "書店をぶらぶらした。", "phrasal": "around", "chunk": 19},
        {"english": "He spoke about Japan's economy.", "japanese": "彼は日本の経済について話をした。", "phrasal": "about", "chunk": 13},
        {"english": "I'll shop around this afternoon.", "japanese": "今日の午後はぶらぶら見て回ります。", "phrasal": "around", "chunk": 21},
        {"english": "That cat comes around when it's hungry.", "japanese": "そのネコはお腹がへるとやって来る。", "phrasal": "around", "chunk": 15},
        {"english": "The kids are running around in the park.", "japanese": "子どもたちは公園で遊びまわっている。", "phrasal": "around", "chunk": 23},
    ],
    "U20": [
        {"english": "He looked back at me.", "japanese": "彼は振り返って私を見た。", "phrasal": "back", "chunk": 5},
        {"english": "Don't look back. Just keep moving forward.", "japanese": "過去は振り向くな、前進あるのみ。", "phrasal": "back", "span": (6, 7)},
        {"english": "I look forward to the next game.", "japanese": "次の試合を楽しみにしている。", "phrasal": "forward", "chunk": 8},
        {"english": "The Giants are ahead in the third inning.", "japanese": "ジャイアンツは3回でリードしている。", "phrasal": "ahead", "chunk": 9},
        {"english": "I'll call you back later.", "japanese": "あとでかけ直します。", "phrasal": "back", "chunk": 12},
        {"english": "I put my watch forward 5 seconds.", "japanese": "時計を5秒早めた。", "phrasal": "forward", "chunk": 21},
        {"english": "Please step back.", "japanese": "後ろへ下がってください。", "phrasal": "back", "chunk": 14},
        {"english": "Go ahead.", "japanese": "どうぞ先に。", "phrasal": "ahead", "span": (22, 22)},
        {"english": "He stepped forward to receive the prize.", "japanese": "彼は賞を受けるために前に出た。", "phrasal": "forward", "chunk": 16},
        {"english": "Can I use the restroom? Yes, go ahead.", "japanese": "「トイレを借りてもいいですか」「ええ、どうぞ」", "phrasal": "ahead", "span": (25, 27)},
        {"english": "Don't put yourself forward.", "japanese": "でしゃばるな。", "phrasal": "forward", "chunk": 18},
        {"english": "The festival will go ahead as planned.", "japanese": "お祭りは予定通り行われる。", "phrasal": "ahead", "chunk": 29},
    ],
    "U21": [
        {"english": "I work together with Alice.", "japanese": "私はアリスと一緒に働いている。", "phrasal": "together", "chunk": 4},
        {"english": "Let's sing a song together.", "japanese": "みんなで一緒に歌を歌いましょう。", "phrasal": "together", "chunk": 5},
        {"english": "I live apart from my parents.", "japanese": "私は両親とは別々に暮らしている。", "phrasal": "apart", "chunk": 6},
        {"english": "My brother and I are five years apart.", "japanese": "兄と私は5歳離れている。", "phrasal": "apart", "chunk": 7},
        {"english": "Let's get together tonight.", "japanese": "今夜集まろう。", "phrasal": "together", "chunk": 9},
        {"english": "The country is going to fall apart.", "japanese": "その国は崩壊するだろう。", "phrasal": "apart", "chunk": 17},
        {"english": "We lived together before we got married.", "japanese": "私たちは結婚する前から同棲していた。", "phrasal": "together", "chunk": 11},
        {"english": "He can take the radio apart.", "japanese": "彼はそのラジオを分解できる。", "phrasal": "apart", "chunk": 19},
        {"english": "This tie and this suit go together.", "japanese": "このネクタイとこのスーツは合っている。", "phrasal": "together", "chunk": 13},
        {"english": "He took apart his opponent.", "japanese": "彼は敵に楽勝した。", "phrasal": "apart", "chunk": 21},
        {"english": "Those two countries came together on this issue.", "japanese": "両国はこの問題に関して1つにまとまった。", "phrasal": "together", "chunk": 15},
        {"english": "Can you tell those twin sisters apart?", "japanese": "あの双子の姉妹を見分けられますか。", "phrasal": "apart", "chunk": 24},
    ],
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def normalize_english(text: str) -> str:
    text = " ".join((text or "").split())
    if not text:
        return text
    if text[-1] not in ".!?":
        text += "."
    return text


def cloze_sentence(sentence: str, target: str) -> str:
    return re.sub(rf"\b{re.escape(target)}\b", "[BLANK]", sentence, count=1, flags=re.IGNORECASE)


def ipa_input_text(text: str) -> str:
    replacements = {
        r"\bA\b": "ay",
        r"\bB\b": "bee",
        r"\bCEO\b": "C E O",
        r"\b5\b": "five",
        r"\b1000\b": "one thousand",
    }
    result = text
    for pattern, replacement in replacements.items():
        result = re.sub(pattern, replacement, result)
    return result


def to_ipa(text: str) -> str:
    phonemes = ipa.convert(ipa_input_text(text)).strip()
    phonemes = phonemes.replace("ˈjuˈɛs", "ʌs")
    phonemes = phonemes.replace("juˈɛs", "ʌs")
    return f"/{phonemes}/" if phonemes else ""


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


def manifest_map(unit: str) -> dict[int, dict[str, str]]:
    return {
        int(row["chunk_index"]): row
        for row in read_tsv(DATA_ROOT / unit / "audio_manifest.tsv")
    }


def span_times(audio_rows: dict[int, dict[str, str]], entry: dict[str, object]) -> tuple[float, float]:
    if "span" in entry:
        start_chunk, end_chunk = entry["span"]  # type: ignore[misc]
        return float(audio_rows[start_chunk]["start"]), float(audio_rows[end_chunk]["end"])
    chunk = int(entry["chunk"])  # type: ignore[arg-type]
    return float(audio_rows[chunk]["start"]), float(audio_rows[chunk]["end"])


def build_unit(unit: str) -> None:
    entries = CURATED[unit]
    image_rows = read_tsv(DATA_ROOT / unit / "image_manifest.tsv")
    audio_rows = manifest_map(unit)
    source_audio = SOURCE_AUDIO[unit]
    audio_dir = AUDIO_ROOT / unit
    public_audio_dir = PUBLIC_AUDIO_ROOT / unit
    audio_dir.mkdir(parents=True, exist_ok=True)
    public_audio_dir.mkdir(parents=True, exist_ok=True)

    if len(entries) > len(image_rows):
        raise ValueError(f"{unit}: {len(entries)} entries but only {len(image_rows)} images")
    image_rows = image_rows[: len(entries)]

    rows: list[dict[str, str]] = []
    for idx, entry in enumerate(entries, start=1):
        english = normalize_english(str(entry["english"]))
        japanese = str(entry["japanese"])
        phrasal = str(entry["phrasal"])
        accepted = str(entry.get("accepted", phrasal))
        image_file = f"/images/eijukugo_zukan/{unit}/Q{idx:02d}.png"
        audio_file = f"/audio/eijukugo_zukan/{unit}/S{idx:02d}.mp3"
        start, end = span_times(audio_rows, entry)
        dest = audio_dir / f"S{idx:02d}.mp3"
        cut_clip(source_audio, start, end, dest)
        shutil.copy2(dest, public_audio_dir / dest.name)

        rows.append(
            {
                "chapter": unit,
                "qno": str(idx),
                "english": english,
                "japanese": japanese,
                "ipa_us": to_ipa(english),
                "question_image": image_file,
                "audio_file": audio_file,
                "phrasal": phrasal,
                "accepted": accepted,
                "cloze": cloze_sentence(english, phrasal),
            }
        )

    header = [
        "chapter",
        "qno",
        "english",
        "japanese",
        "ipa_us",
        "question_image",
        "audio_file",
        "phrasal",
        "accepted",
        "cloze",
    ]
    for out_root in (DATA_ROOT, PUBLIC_DATA_ROOT):
        out_dir = out_root / unit
        out_dir.mkdir(parents=True, exist_ok=True)
        with (out_dir / "dataset.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(rows)
    print(f"{unit}: {len(rows)} rows")


def main() -> None:
    for unit in CURATED:
        build_unit(unit)


if __name__ == "__main__":
    main()
