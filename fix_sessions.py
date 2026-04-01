from core.database import SessionLocal
from features.user.models import User, StatusLearning
from features.grammar.models import Chapter, Exercise

def fix():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == 1).first()
        status = db.query(StatusLearning).filter(StatusLearning.user_id == 1).first()
        
        # Grammar
        ch_g1 = db.query(Chapter).filter(Chapter.category == 'grammar').order_by(Chapter.order_index).first()
        ex_g1 = db.query(Exercise).filter(Exercise.chapter_id == ch_g1.id).order_by(Exercise.order_index).first() if ch_g1 else None
        
        # Vocabulary
        ch_v1 = db.query(Chapter).filter(Chapter.category == 'vocabulary').order_by(Chapter.order_index).first()
        ex_v1 = db.query(Exercise).filter(Exercise.chapter_id == ch_v1.id).order_by(Exercise.order_index).first() if ch_v1 else None
        
        if status:
            if ch_g1: 
                status.status_chapter_grammar = ch_g1.id
                status.status_exercise_grammar = ex_g1.id if ex_g1 else ch_g1.id
            if ch_v1:
                status.status_chapter_vocabulary = ch_v1.id
                status.status_exercise_vocabulary = ex_v1.id if ex_v1 else ch_v1.id
            db.commit()
            print(f"Fixed: G({status.status_chapter_grammar}, {status.status_exercise_grammar}) V({status.status_chapter_vocabulary}, {status.status_exercise_vocabulary})")
    finally:
        db.close()

if __name__ == "__main__":
    fix()
