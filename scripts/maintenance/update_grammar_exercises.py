from core.database import SessionLocal
from features.grammar.models import Exercise

exercise_updates = [
    (1, "Particle Wa", "Learn about how Japanese highlights subjects"),
    (2, "Desu verb", ""),
    (3, "Hour in Japanese", ""),
    (4, "Prices in Japanese", ""),
    (5, "Evaluation Chapters 1-4", ""),
    (6, "Describing Clothes", ""),
    (7, "Basic Adjectives List", ""),
    (8, "Basic Adjectives List (Part 2)", ""),
    (9, "Basic Japanese Verbs", ""),
    (10, "Particle Mo", ""),
    (11, "And / Or", ""),
    (12, "Describe Distance", "Use of kono, ano, etc."),
    (13, "Verb Conjugation", ""),
    (14, "Present Tense", ""),
    (15, "Verb Particles, Word Order", ""),
    (16, "General Examination 1-14", ""),
    (17, "Past Tense of Desu", ""),
    (18, "Past Tense of Verbs", ""),
    (19, "Past Tense of Verbs (Part 2)", ""),
    (20, "Practice Verbs", ""),
    (21, "Final Examination Chapter 1", "")
]

def update_exercises():
    db = SessionLocal()
    for ex_id, title, desc in exercise_updates:
        ex = db.query(Exercise).filter(Exercise.id == ex_id).first()
        if ex:
            ex.title = title
            ex.description = desc
    db.commit()
    db.close()
    print("Exercises updated.")

if __name__ == "__main__":
    update_exercises()
