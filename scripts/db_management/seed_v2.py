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

        # ---------------------------------------------------------------------
        # 2. SEED GRAMMAR (Chapter 1)
        # ---------------------------------------------------------------------
        ch_g1 = db.query(Chapter).filter(Chapter.title == "Introduction to Japanese Grammar", Chapter.category == "grammar").first()
        if not ch_g1:
            ch_g1 = Chapter(
                proficiency_id=n5.id,
                title="Introduction to Japanese Grammar",
                description="Learn the basics of Japanese sentence structure, particles, and telling time.",
                category="grammar",
                order_index=1
            )
            db.add(ch_g1)
            db.flush()

        # Grammar Exercises Data (minimal version of what's in seed_exercises.py)
        grammar_exercises = [
            {"title": "Particle Wa (は)", "desc": "How Japanese marks topics"},
            {"title": "Desu Verb (です)", "desc": "The polite copula"},
            {"title": "Hour in Japanese (〜時)", "desc": "Telling time"},
            {"title": "Prices in Japanese", "desc": "Numbers and currency"},
            {"title": "Evaluation Chapters 1-4", "desc": "Progress check"},
            {"title": "Describing clothes", "desc": "Adjectives and verbs"},
            {"title": "Basic adjectives List", "desc": "Common descriptors"},
            {"title": "Basic adjective list (part 2)", "desc": "More descriptors"},
            {"title": "Basic japanese verbs", "desc": "Action words"},
            {"title": "Particle Mo", "desc": "The particle for 'also'"},
            {"title": "\"And\" / \"Or\"", "desc": "Connecting nouns"},
            {"title": "Describe distance", "desc": "Kono, Sono, Ano, Dono"},
            {"title": "Verb Conjugation", "desc": "Polite form basis"},
            {"title": "Present Tense", "desc": "Habitual actions"},
            {"title": "Verb Particles, Word Order", "desc": "Sentence structure"},
            {"title": "General Examination 1-14", "desc": "Comprehensive check"},
            {"title": "Past Tense of Desu", "desc": "Was / Were"},
            {"title": "Past tense of verbs", "desc": "Completed actions"},
            {"title": "Past tense of verbs (part 2)", "desc": "More practice"},
            {"title": "Practice verbs", "desc": "Drills"},
            {"title": "Final examination chapter 1", "desc": "Mastery proof"},
        ]

        for i, ex_data in enumerate(grammar_exercises):
            ex = db.query(Exercise).filter(Exercise.chapter_id == ch_g1.id, Exercise.order_index == i+1).first()
            if not ex:
                ex = Exercise(
                    chapter_id=ch_g1.id,
                    title=ex_data["title"],
                    description=ex_data["desc"],
                    theory_content=f"<h3>{ex_data['title']}</h3><p>{ex_data['desc']}</p>",
                    exercise_type="quiz",
                    order_index=i+1,
                    points=10
                )
                db.add(ex)
                db.flush()
            
            # Simple test for each grammar exercise if none exist
            if not db.query(Test).filter(Test.exercise_id == ex.id).first():
                test = Test(
                    exercise_id=ex.id,
                    question=f"Is {ex_data['title']} important?",
                    correct_answer="True",
                    options=json.dumps(["True", "False"]),
                    test_type="true_false",
                    order_index=1
                )
                db.add(test)

        # ---------------------------------------------------------------------
        # 3. SEED VOCABULARY (Chapters 5, 6, 7...)
        # ---------------------------------------------------------------------
        vocab_chapters = [
            {
                "title": "Writing Systems & Greetings",
                "desc": "Foundational scripts and first words.",
                "order_index": 1,
                "exercises": [
                    {"title": "Writing Systems Overview", "desc": "Hiragana, Katakana, Kanji"},
                    {"title": "Essential Greetings", "desc": "Ohayou, Konnichiwa, Oyasumi"},
                    {"title": "Self-Introduction", "desc": "Hajimemashite, Yoroshiku"},
                ]
            },
            {
                "title": "Numbers & Daily Life",
                "desc": "Count things and talk about your day.",
                "order_index": 2,
                "exercises": [
                    {"title": "Numbers 1-1000", "desc": "Counting in Japanese"},
                    {"title": "Family Members", "desc": "Kazoku terms"},
                    {"title": "Time & Days of Week", "desc": "Schedule vocabulary"},
                ]
            },
            {
                "title": "Town & Travel",
                "desc": "Navigate the city and Japanese transport.",
                "order_index": 3,
                "exercises": [
                    {"title": "Places in Town", "desc": "Ginkou, Konbini, Eruption?"},
                    {"title": "Transportation", "desc": "Densha, Basu, Takushi-"},
                    {"title": "Giving Directions", "desc": "Migi, Hidari, Massugu"},
                ]
            }
        ]

        for v_ch_data in vocab_chapters:
            ch = db.query(Chapter).filter(Chapter.title == v_ch_data["title"], Chapter.category == "vocabulary").first()
            if not ch:
                ch = Chapter(
                    proficiency_id=n5.id,
                    title=v_ch_data["title"],
                    description=v_ch_data["desc"],
                    category="vocabulary",
                    order_index=v_ch_data["order_index"]
                )
                db.add(ch)
                db.flush()
            
            for i, ex_v_data in enumerate(v_ch_data["exercises"]):
                ex = db.query(Exercise).filter(Exercise.chapter_id == ch.id, Exercise.order_index == i+1).first()
                if not ex:
                    ex = Exercise(
                        chapter_id=ch.id,
                        title=ex_v_data["title"],
                        description=ex_v_data["desc"],
                        theory_content=f"<h3>{ex_v_data['title']}</h3><p>{ex_v_data['desc']}</p>",
                        exercise_type="vocabulary",
                        order_index=i+1,
                        points=10
                    )
                    db.add(ex)
                    db.flush()
                
                # Simple test for each vocabulary exercise if none exist
                if not db.query(Test).filter(Test.exercise_id == ex.id).first():
                    test = Test(
                        exercise_id=ex.id,
                        question=f"How do you say '{ex_v_data['title']}'?",
                        correct_answer="Answer",
                        options=json.dumps(["Answer", "Distractor"]),
                        test_type="multiple_choice",
                        order_index=1
                    )
                    db.add(test)

        db.commit()
        print("Success: Grammar and Vocabulary seeded without touching Culture.")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
