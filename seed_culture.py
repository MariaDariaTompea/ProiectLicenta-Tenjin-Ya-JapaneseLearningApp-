from core.database import SessionLocal
from features.grammar.models import Proficiency, Chapter, Exercise
import os

def seed_culture():
    db = SessionLocal()
    try:
        # Get or create N5 proficiency for start
        prof = db.query(Proficiency).filter(Proficiency.level == "N5").first()
        if not prof:
            prof = Proficiency(level="N5", name="Beginner", order_index=1)
            db.add(prof)
            db.commit()
            db.refresh(prof)
        
        culture_chapters = [
            {
                "title": "Traditional Tea Ceremony",
                "description": "Learn about the ancient art of Chanoyu, the Japanese way of tea.",
                "category": "culture",
                "order_index": 1,
                "image_url": "/uploads/culture/tea_ceremony.png"
            },
            {
                "title": "History of the Samurai",
                "description": "Explore the code of Bushido and the life of Japan's legendary warriors.",
                "category": "culture",
                "order_index": 2,
                "image_url": "/uploads/culture/samurai_history.png"
            },
            {
                "title": "Kimono & Traditional Dress",
                "description": "Discover the intricate beauty of Japan's traditional garments.",
                "category": "culture",
                "order_index": 3,
                "image_url": "/uploads/culture/kimono_tradition.png"
            }
        ]
        
        for ch_data in culture_chapters:
            existing = db.query(Chapter).filter(Chapter.title == ch_data["title"]).first()
            if not existing:
                ch = Chapter(
                    proficiency_id=prof.id,
                    title=ch_data["title"],
                    description=ch_data["description"],
                    category=ch_data["category"],
                    order_index=ch_data["order_index"],
                    image_url=ch_data["image_url"]
                )
                db.add(ch)
                db.commit()
                db.refresh(ch)
                
                # Add a dummy exercise so it's "comprintable"
                ex = Exercise(
                    chapter_id=ch.id,
                    title=ch.title + " Reading",
                    description="Read through the material to complete this chapter.",
                    exercise_type="course",
                    order_index=1
                )
                db.add(ex)
                db.commit()
                print(f"Added Culture Chapter: {ch.title}")
            else:
                # Update image_url if exists
                existing.image_url = ch_data["image_url"]
                db.commit()
                print(f"Updated Culture Chapter image: {ch_data['title']}")
                
    finally:
        db.close()

if __name__ == "__main__":
    seed_culture()
