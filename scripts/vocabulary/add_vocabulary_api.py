import re
from core.database import SessionLocal
from features.grammar.models import Chapter, Exercise
from fastapi.responses import JSONResponse
from fastapi import Request

api_endpoints = '''
@router.get("/api/vocabulary/user-status")
async def vocabulary_user_status(request: Request):
    return await grammar_user_status(request)

@router.get("/api/vocabulary/chapter/{chapter_id}")
async def vocabulary_chapter(chapter_id: int):
    return await grammar_chapter(chapter_id)

@router.get("/api/vocabulary/exercise/{exercise_id}")
async def vocabulary_exercise_chapter(exercise_id: int):
    return await grammar_exercise_chapter(exercise_id)

@router.get("/api/vocabulary/exercises")
async def vocabulary_all_exercises():
    db = SessionLocal()
    try:
        exercises = (
            db.query(Exercise, Chapter)
            .join(Chapter, Exercise.chapter_id == Chapter.id)
            .filter(Chapter.category == "vocabulary")
            .order_by(Chapter.order_index, Exercise.order_index)
            .all()
        )
        return JSONResponse([
            {
                "id":          ex.id,
                "chapter_id":  ex.chapter_id,
                "title":       ex.title,
                "description": ex.description or "",
                "level":       ch.level or "N5",
                "order_index": ex.order_index,
            }
            for ex, ch in exercises
        ])
    finally:
        db.close()
'''

with open('d:/JapaneseApp/features/grammar/routes.py', 'r', encoding='utf-8') as f:
    text = f.read()

if 'def vocabulary_user_status' not in text:
    with open('d:/JapaneseApp/features/grammar/routes.py', 'a', encoding='utf-8') as f:
        f.write('\n\n# ─────────────────────────────────────────────────────────\n#  VOCABULARY API ENDPOINTS\n# ─────────────────────────────────────────────────────────\n')
        f.write(api_endpoints)
    print('Vocabulary API added')
