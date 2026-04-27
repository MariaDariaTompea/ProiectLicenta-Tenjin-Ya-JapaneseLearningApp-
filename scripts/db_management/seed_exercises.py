import json
from core.database import SessionLocal, Base, engine
from features.grammar.models import Proficiency, Chapter, Exercise, Test

def seed():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Get or Create Proficiency (N5)
        n5 = db.query(Proficiency).filter(Proficiency.level == "N5").first()
        if not n5:
            n5 = Proficiency(level="N5", name="Beginner", description="JLPT N5 — Foundation", order_index=1)
            db.add(n5)
            db.flush()

        # 2. Create Chapter 1
        ch1 = db.query(Chapter).filter(Chapter.title == "Introduction to Japanese Grammar").first()
        if not ch1:
            ch1 = Chapter(
                proficiency_id=n5.id,
                title="Introduction to Japanese Grammar",
                description="Learn the basics of Japanese sentence structure, particles, and telling time.",
                category="grammar",
                order_index=1
            )
            db.add(ch1)
            db.flush()

        # 3. Create Exercises & Tests
        theory_1 = """
        <h3>Particle は (wa)</h3>
        <p>In Japanese, the particle <strong>は</strong> is used to mark the topic of a sentence. Even though it is written with the hiragana character 'ha', it is pronounced 'wa' when used as a particle.</p>
        <p><strong>Pattern:</strong> [Topic] は [Description] です。</p>
        <ul>
            <li><strong>ねこ は かわいい です。</strong> (The cat is cute.)</li>
            <li><strong>すし は おいしい です。</strong> (Sushi is tasty.)</li>
            <li><strong>わたし は がくせい です。</strong> (I am a student.)</li>
        </ul>
        <p>Use it to tell the listener what you are talking about before you describe it!</p>
        """

        theory_2 = """
        <h3>The Copula です (desu)</h3>
        <p><strong>です</strong> (pronounced "dess") is the polite Japanese copula. It represents the verb "to be" (is, am, are) and makes a sentence polite.</p>
        <p><strong>Pattern:</strong> X は Y です。 (As for X, it is Y.)</p>
        <ul>
            <li><strong>これ は ほん です。</strong> (This is a book.)</li>
            <li><strong>わたし は がくせい です。</strong> (I am a student.)</li>
        </ul>
        <p>The negative polite form is <strong>じゃないです</strong> (janai desu).</p>
        """

        theory_3 = """
        <h3>Hour in Japanese (〜時)</h3>
        <p>To tell the time in hours, you attach the counter <strong>時 (じ, ji)</strong> to the number.</p>
        <p><strong>Pattern:</strong> [Number] じ</p>
        <ul>
            <li><strong>1時</strong> = いちじ (ichiji)</li>
            <li><strong>3時</strong> = さんじ (sanji)</li>
            <li><strong>4時</strong> = よじ (yoji) — *Irregular! Not yonji.</li>
            <li><strong>9時</strong> = くじ (kuji) — *Irregular! Not kyuuji.</li>
        </ul>
        <p>To say "What time is it now?", you ask: <strong>いま なんじ です か。</strong></p>
        """

        detailed_tests_1 = [
            {"type": "multiple_choice", "q": "What does the particle は (wa) do in a sentence?", "a": "Marks the topic of the sentence", "opts": ["Marks the object", "Marks the topic of the sentence", "Shows possession", "Indicates action"]},
            {"type": "multiple_choice", "q": "りんご は ______ です", "a": "たべもの", "opts": ["どうぶつ", "たべもの", "なまえ", "のみもの"]},
            {"type": "fill_blank", "q": "ねこ ___ かわいい です (The cat is cute)", "a": "は", "opts": {"sentence": "ねこ ___ かわいい です", "choices": ["は", "が", "を", "に"]}},
            {"type": "fill_blank", "q": "さくら ___ がくせい です (Sakura is a student)", "a": "は", "opts": {"sentence": "さくら ___ がくせい です", "choices": ["は", "を", "が", "も"]}},
            {"type": "sentence_builder", "q": "Build: 'The cat is cute'", "a": "ねこ は かわいい です", "opts": {"words": ["ねこ", "は", "かわいい", "です"], "distractors": ["が", "を"]}},
            {"type": "sentence_builder", "q": "Build: 'Sushi is tasty'", "a": "すし は おいしい です", "opts": {"words": ["すし", "は", "おいしい", "です"], "distractors": ["も", "が"]}},
            {"type": "matching", "q": "Match the subject to its category", "a": "pair match", "opts": {"pairs": [["いぬ", "どうぶつ"], ["ぱん", "たべもの"], ["ゆき", "なまえ"], ["さかな", "どうぶつ"]]}},
            {"type": "matching", "q": "Match the Japanese sentence to its meaning", "a": "pair match", "opts": {"pairs": [["ねこ は かわいい です", "The cat is cute"], ["すし は おいしい です", "Sushi is tasty"], ["たろう は がくせい です", "Tarou is a student"]]}},
            {"type": "true_false", "q": "は is always pronounced 'ha' in Japanese", "a": "False", "opts": ["True", "False"]},
            {"type": "true_false", "q": "さかな は どうぶつ です (Fish is an animal) — Is this correct?", "a": "True", "opts": ["True", "False"]},
            {"type": "true_false", "q": "ぱん は どうぶつ です (Bread is an animal) — Is this correct?", "a": "False", "opts": ["True", "False"]},
            {"type": "text_input", "q": "Write in hiragana: 'The dog is big'", "a": "いぬ は おおきい です", "opts": {"hint": "inu wa ookii desu"}},
            {"type": "text_input", "q": "Write in hiragana: 'Hana is a student'", "a": "はな は がくせい です", "opts": {"hint": "hana wa gakusei desu"}},
            {"type": "multiple_choice", "q": "Which sentence correctly uses は?", "a": "ねこ は かわいい です", "opts": ["ねこ を かわいい です", "ねこ は かわいい です", "ねこ に かわいい です", "ねこ で かわいい です"]},
            {"type": "multiple_choice", "q": "In the sentence けん は にほんじん です, what is the topic?", "a": "けん", "opts": ["にほんじん", "けん", "です", "は"]},
        ]

        detailed_tests_2 = [
            {"type": "multiple_choice", "q": "What is the purpose of です (desu)?", "a": "It is the polite copula ('to be')", "opts": ["It marks the subject", "It is the polite copula ('to be')", "It shows past tense", "It negates the sentence"]},
            {"type": "multiple_choice", "q": "What is the negative form of です?", "a": "じゃないです", "opts": ["ではます", "じゃないです", "ですない", "ません"]},
            {"type": "multiple_choice", "q": "Which is the correct polite sentence for 'I am a student'?", "a": "わたし は がくせい です", "opts": ["わたし は がくせい だ", "わたし は がくせい です", "わたし が がくせい です", "わたし は がくせい ます"]},
            {"type": "fill_blank", "q": "これ は ぱん ___。(This is bread)", "a": "です", "opts": {"sentence": "これ は ぱん ___。", "choices": ["です", "ます", "だ", "ある"]}},
            {"type": "fill_blank", "q": "りんご は たべもの ___。(An apple is food)", "a": "です", "opts": {"sentence": "りんご は たべもの ___。", "choices": ["です", "ます", "だった", "じゃない"]}},
            {"type": "fill_blank", "q": "ねこ は どうぶつ ___。(A cat is an animal)", "a": "です", "opts": {"sentence": "ねこ は どうぶつ ___。", "choices": ["です", "ます", "ある", "いる"]}},
            {"type": "sentence_builder", "q": "Build: 'This is water'", "a": "これ は みず です", "opts": {"words": ["これ", "は", "みず", "です"], "distractors": ["あれ", "ます"]}},
            {"type": "sentence_builder", "q": "Build: 'An egg is food'", "a": "たまご は たべもの です", "opts": {"words": ["たまご", "は", "たべもの", "です"], "distractors": ["どうぶつ", "が"]}},
            {"type": "matching", "q": "Match Japanese to English", "a": "pair match", "opts": {"pairs": [["がくせい です", "is a student"], ["せんせい です", "is a teacher"], ["にほんじん です", "is Japanese"], ["ともだち です", "is a friend"]]}},
            {"type": "matching", "q": "Match the sentence to its meaning", "a": "pair match", "opts": {"pairs": [["これ は りんご です", "This is an apple"], ["これ は みず です", "This is water"], ["これ は たまご です", "This is an egg"]]}},
            {"type": "true_false", "q": "です can be used with adjectives in polite speech", "a": "True", "opts": ["True", "False"]},
            {"type": "true_false", "q": "です and だ mean the same thing but です is more polite", "a": "True", "opts": ["True", "False"]},
            {"type": "true_false", "q": "You can say ねこ は かわいい ます (The cat is cute)", "a": "False", "opts": ["True", "False"]},
            {"type": "text_input", "q": "Write in hiragana: 'This is a dog'", "a": "これ は いぬ です", "opts": {"hint": "kore wa inu desu"}},
            {"type": "text_input", "q": "Write in hiragana: 'Sakura is a friend'", "a": "さくら は ともだち です", "opts": {"hint": "sakura wa tomodachi desu"}},
        ]

        detailed_tests_3 = [
            {"type": "multiple_choice", "q": "How do you say '3 o'clock' in Japanese?", "a": "さんじ", "opts": ["さんじ", "さんぷん", "さんがつ", "みっか"]},
            {"type": "multiple_choice", "q": "What is the counter for hours in Japanese?", "a": "じ (時)", "opts": ["じ (時)", "ふん (分)", "びょう (秒)", "ねん (年)"]},
            {"type": "multiple_choice", "q": "How do you say 'what time is it?' in Japanese?", "a": "いま なんじ です か", "opts": ["いま なんにち です か", "いま なんじ です か", "いま なんがつ です か", "いま どこ です か"]},
            {"type": "fill_blank", "q": "いま ___ なんじ です か。(What time is it now?)", "a": "は", "opts": {"sentence": "いま ___ なんじ です か。", "choices": ["は", "が", "を", "に"]}},
            {"type": "fill_blank", "q": "ごぜん く ___ です。(It is 9 AM)", "a": "じ", "opts": {"sentence": "ごぜん く ___ です。", "choices": ["じ", "ふん", "がつ", "にち"]}},
            {"type": "fill_blank", "q": "いま さん ___ です。(It is 3 o'clock now)", "a": "じ", "opts": {"sentence": "いま さん ___ です。", "choices": ["じ", "ふん", "にち", "ねん"]}},
            {"type": "sentence_builder", "q": "Build: 'It is 7 o'clock now'", "a": "いま しちじ です", "opts": {"words": ["いま", "しちじ", "です"], "distractors": ["ごぜん", "ごご", "なんじ"]}},
            {"type": "sentence_builder", "q": "Build: 'It is 2 PM'", "a": "ごご にじ です", "opts": {"words": ["ごご", "にじ", "です"], "distractors": ["ごぜん", "いま", "か"]}},
            {"type": "matching", "q": "Match the times", "a": "pair match", "opts": {"pairs": [["いちじ", "1 o'clock"], ["ごじ", "5 o'clock"], ["じゅうじ", "10 o'clock"], ["しちじ", "7 o'clock"]]}},
            {"type": "matching", "q": "Match the time expressions", "a": "pair match", "opts": {"pairs": [["ごぜん", "AM / morning"], ["ごご", "PM / afternoon"], ["いま", "now"], ["なんじ", "what time"]]}},
            {"type": "true_false", "q": "4 o'clock is よんじ in Japanese", "a": "False", "opts": ["True", "False"]},
            {"type": "true_false", "q": "ごぜん means 'morning / AM' in Japanese", "a": "True", "opts": ["True", "False"]},
            {"type": "true_false", "q": "9 o'clock is きゅうじ in Japanese", "a": "False", "opts": ["True", "False"]},
            {"type": "text_input", "q": "Type '9 o'clock' in hiragana", "a": "くじ", "opts": {"hint": "ku + ji"}},
            {"type": "text_input", "q": "Type '4 o'clock' in hiragana", "a": "よじ", "opts": {"hint": "yo + ji (irregular!)"}},
        ]

        exercises_data = []
        for i in range(1, 22):
            if i == 1:
                exercises_data.append({
                    "title": "Particle Wa (は)",
                    "desc": "How Japanese marks topics",
                    "theory": theory_1,
                    "tests": detailed_tests_1
                })
            elif i == 2:
                exercises_data.append({
                    "title": "Desu Verb (です)",
                    "desc": "The polite copula",
                    "theory": theory_2,
                    "tests": detailed_tests_2
                })
            elif i == 3:
                exercises_data.append({
                    "title": "Hour in Japanese (〜時)",
                    "desc": "Telling time",
                    "theory": theory_3,
                    "tests": detailed_tests_3
                })
            else:
                exercises_data.append({
                    "title": f"Grammar Exercise {i}",
                    "desc": f"Placeholder for Exercise {i} content",
                    "theory": f"<p>This is the theory placeholder for Exercise {i}.</p>",
                    "tests": [
                        {"type": "true_false", "q": f"Placeholder Question {j+1}", "a": "True", "opts": ["True", "False"]} for j in range(15)
                    ]
                })

        for i, ex_data in enumerate(exercises_data):
            ex = db.query(Exercise).filter(Exercise.chapter_id == ch1.id, Exercise.order_index == i+1).first()
            if not ex:
                ex = Exercise(
                    chapter_id=ch1.id,
                    title=ex_data["title"],
                    description=ex_data["desc"],
                    theory_content=ex_data["theory"],
                    exercise_type="quiz",
                    order_index=i+1,
                    points=10
                )
                db.add(ex)
                db.flush()
            else:
                ex.title = ex_data["title"]
                ex.description = ex_data["desc"]
                ex.theory_content = ex_data["theory"]
                db.flush()
            
            # Add tests for this exercise
            db.query(Test).filter(Test.exercise_id == ex.id).delete()
            
            for j, t_data in enumerate(ex_data["tests"]):
                test = Test(
                    exercise_id=ex.id,
                    question=t_data["q"],
                    correct_answer=t_data["a"],
                    options=json.dumps(t_data["opts"]),
                    test_type=t_data["type"],
                    order_index=j+1
                )
                db.add(test)
        
        db.commit()
        print(f"Database seeded successfully with {len(exercises_data)} exercises!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
