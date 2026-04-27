"""
Seed hiragana and katakana character data into the local database.
Run: .venv\\Scripts\\python.exe seed_kana.py
"""
from core.database import SessionLocal
from features.japanese.models import Hiragana, Katakana

# All basic hiragana characters (gojūon)
HIRAGANA_DATA = [
    # vowels
    ("あ", "a", "a.png"), ("い", "i", "i.png"), ("う", "u", "u.png"), ("え", "e", "e.png"), ("お", "o", "o.png"),
    # k-row
    ("か", "ka", "ka.png"), ("き", "ki", "ki.png"), ("く", "ku", "ku.png"), ("け", "ke", "ke.png"), ("こ", "ko", "ko.png"),
    # s-row
    ("さ", "sa", "sa.png"), ("し", "shi", "shi.png"), ("す", "su", "su.png"), ("せ", "se", "se.png"), ("そ", "so", "so.png"),
    # t-row
    ("た", "ta", "ta.png"), ("ち", "chi", "chi.png"), ("つ", "tsu", "tsu.png"), ("て", "te", "te.png"), ("と", "to", "to.png"),
    # n-row
    ("な", "na", "na.png"), ("に", "ni", "ni.png"), ("ぬ", "nu", "nu.png"), ("ね", "ne", "ne.png"), ("の", "no", "no.png"),
    # h-row
    ("は", "ha", "ha.png"), ("ひ", "hi", "hi.png"), ("ふ", "fu", "fu.png"), ("へ", "he", "he.png"), ("ほ", "ho", "ho.png"),
    # m-row
    ("ま", "ma", "ma.png"), ("み", "mi", "mi.png"), ("む", "mu", "mu.png"), ("め", "me", "me.png"), ("も", "mo", "mo.png"),
    # y-row
    ("や", "ya", "ya.png"), ("ゆ", "yu", "yu.png"), ("よ", "yo", "yo.png"),
    # r-row
    ("ら", "ra", "ra.png"), ("り", "ri", "ri.png"), ("る", "ru", "ru.png"), ("れ", "re", "re.png"), ("ろ", "ro", "ro.png"),
    # w-row + n
    ("わ", "wa", "wa.png"), ("ゐ", "wi", "wi.png"), ("ゑ", "we", "we.png"), ("を", "wo", "wo.png"), ("ん", "n", "n.png"),
]

# All basic katakana characters (gojūon)
KATAKANA_DATA = [
    # vowels
    ("ア", "a", "a.png"), ("イ", "i", "i.png"), ("ウ", "u", "u.png"), ("エ", "e", "e.png"), ("オ", "o", "o.png"),
    # k-row
    ("カ", "ka", "ka.png"), ("キ", "ki", "ki.png"), ("ク", "ku", "ku.png"), ("ケ", "ke", "ke.png"), ("コ", "ko", "ko.png"),
    # s-row
    ("サ", "sa", "sa.png"), ("シ", "shi", "shi.png"), ("ス", "su", "su.png"), ("セ", "se", "se.png"), ("ソ", "so", "so.png"),
    # t-row
    ("タ", "ta", "ta.png"), ("チ", "chi", "chi.png"), ("ツ", "tsu", "tsu.png"), ("テ", "te", "te.png"), ("ト", "to", "to.png"),
    # n-row
    ("ナ", "na", "na.png"), ("ニ", "ni", "ni.png"), ("ヌ", "nu", "nu.png"), ("ネ", "ne", "ne.png"), ("ノ", "no", "no.png"),
    # h-row
    ("ハ", "ha", "ha.png"), ("ヒ", "hi", "hi.png"), ("フ", "fu", "fu.png"), ("ヘ", "he", "he.png"), ("ホ", "ho", "ho.png"),
    # m-row
    ("マ", "ma", "ma.png"), ("ミ", "mi", "mi.png"), ("ム", "mu", "mu.png"), ("メ", "me", "me.png"), ("モ", "mo", "mo.png"),
    # y-row
    ("ヤ", "ya", "ya.png"), ("ユ", "yu", "yu.png"), ("ヨ", "yo", "yo.png"),
    # r-row
    ("ラ", "ra", "ra.png"), ("リ", "ri", "ri.png"), ("ル", "ru", "ru.png"), ("レ", "re", "re.png"), ("ロ", "ro", "ro.png"),
    # w-row + n
    ("ワ", "wa", "wa.png"), ("ヲ", "wo", "wo.png"), ("ン", "n", "n.png"),
]


def seed():
    db = SessionLocal()

    # Clear existing data
    db.query(Hiragana).delete()
    db.query(Katakana).delete()
    db.commit()

    # Seed hiragana
    for char, romaji, img in HIRAGANA_DATA:
        db.add(Hiragana(character=char, romaji=romaji, image_filename=img))

    # Seed katakana
    for char, romaji, img in KATAKANA_DATA:
        db.add(Katakana(character=char, romaji=romaji, image_filename=img))

    db.commit()

    h_count = db.query(Hiragana).count()
    k_count = db.query(Katakana).count()
    print(f"[OK] Seeded {h_count} hiragana characters")
    print(f"[OK] Seeded {k_count} katakana characters")

    db.close()


if __name__ == "__main__":
    seed()
