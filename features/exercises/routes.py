from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from core.database import SessionLocal
from features.grammar.models import Exercise, Test, Chapter
from features.exercises.templates.exercise_runner import render_exercise_runner
from features.exercises.renderer import RENDERERS
from features.user.models import User, UserExerciseScore, StatusLearning
from pydantic import BaseModel
import json

router = APIRouter()

class ExerciseCompletion(BaseModel):
    exercise_id: int
    stars: int


def _check_exercise_unlocked(db, exercise, chapter, request):
    """Check if user has ≥2 stars on the previous exercise. First exercise is always unlocked."""
    # Find all exercises in this chapter, ordered
    all_exercises = (
        db.query(Exercise)
        .filter(Exercise.chapter_id == chapter.id)
        .order_by(Exercise.order_index)
        .all()
    )

    # If this is the first exercise in the chapter, always unlocked
    if len(all_exercises) == 0 or all_exercises[0].id == exercise.id:
        return True

    # Find the previous exercise
    prev_exercise = None
    for ex in all_exercises:
        if ex.id == exercise.id:
            break
        prev_exercise = ex

    if prev_exercise is None:
        return True  # No previous exercise found, allow

    # Check user's score on the previous exercise
    email = request.cookies.get("user_email")
    if not email:
        return False  # Not logged in, can't verify

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False

    score = db.query(UserExerciseScore).filter(
        UserExerciseScore.user_id == user.id,
        UserExerciseScore.exercise_id == prev_exercise.id
    ).first()

    if not score or score.stars < 2:
        return False

    return True


@router.get("/course/grammar/Chapter{chapter_id}/exercise/{exercise_id}", response_class=HTMLResponse)
async def exercise_page(request: Request, chapter_id: int, exercise_id: int):
    db = SessionLocal()
    try:
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id, Exercise.chapter_id == chapter_id).first()
        if not exercise:
            raise HTTPException(status_code=404, detail="Exercise not found")

        chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
        category = chapter.category if chapter else "grammar"

        # Check progression: require ≥2 stars on previous exercise
        if not _check_exercise_unlocked(db, exercise, chapter, request):
            # Redirect back to the course page with a message
            return HTMLResponse(f"""
            <!DOCTYPE html><html><head>
            <meta charset="UTF-8"><title>Exercise Locked</title>
            <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {{ font-family: 'Inter', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; background: #0d0608; color: #FCBCD7; gap: 24px; text-align: center; }}
                h1 {{ font-family: 'Playfair Display', serif; font-size: 48px; color: #E56AB3; }}
                p {{ font-size: 16px; opacity: 0.7; max-width: 400px; line-height: 1.6; }}
                .lock-icon {{ font-size: 72px; margin-bottom: 10px; }}
                a {{ color: #E56AB3; text-decoration: none; font-size: 14px; letter-spacing: 1px; border: 1px solid rgba(229,106,179,0.3); padding: 12px 30px; border-radius: 30px; transition: all 0.3s; }}
                a:hover {{ background: rgba(229,106,179,0.1); }}
            </style>
            </head><body>
            <div class="lock-icon">🔒</div>
            <h1>Exercise Locked</h1>
            <p>You need at least 2 foxheads (stars) on the previous exercise to unlock this one.</p>
            <a href="/course/{category}">← Back to {category.title()}</a>
            </body></html>
            """)

        tests = db.query(Test).filter(Test.exercise_id == exercise_id).order_by(Test.order_index).all()
        return render_exercise_runner(exercise, tests, chapter_id, category=category)
    finally:
        db.close()


@router.get("/course/vocabulary/Chapter{chapter_id}/exercise/{exercise_id}", response_class=HTMLResponse)
async def vocabulary_exercise_page_runner(request: Request, chapter_id: int, exercise_id: int):
    """Vocabulary exercise runner — uses the same exercise runner as grammar."""
    db = SessionLocal()
    try:
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id, Exercise.chapter_id == chapter_id).first()
        if not exercise:
            raise HTTPException(status_code=404, detail="Exercise not found")

        chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()

        # Check progression
        if not _check_exercise_unlocked(db, exercise, chapter, request):
            return HTMLResponse(f"""
            <!DOCTYPE html><html><head>
            <meta charset="UTF-8"><title>Exercise Locked</title>
            <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {{ font-family: 'Inter', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; background: #0d0608; color: #FCBCD7; gap: 24px; text-align: center; }}
                h1 {{ font-family: 'Playfair Display', serif; font-size: 48px; color: #E56AB3; }}
                p {{ font-size: 16px; opacity: 0.7; max-width: 400px; line-height: 1.6; }}
                .lock-icon {{ font-size: 72px; margin-bottom: 10px; }}
                a {{ color: #E56AB3; text-decoration: none; font-size: 14px; letter-spacing: 1px; border: 1px solid rgba(229,106,179,0.3); padding: 12px 30px; border-radius: 30px; transition: all 0.3s; }}
                a:hover {{ background: rgba(229,106,179,0.1); }}
            </style>
            </head><body>
            <div class="lock-icon">🔒</div>
            <h1>Exercise Locked</h1>
            <p>You need at least 2 foxheads (stars) on the previous exercise to unlock this one.</p>
            <a href="/course/vocabulary">← Back to Vocabulary</a>
            </body></html>
            """)

        tests = db.query(Test).filter(Test.exercise_id == exercise_id).order_by(Test.order_index).all()
        return render_exercise_runner(exercise, tests, chapter_id, category="vocabulary")
    finally:
        db.close()

@router.get("/api/exercise/render-test/{test_id}")
async def render_test_api(test_id: int):
    db = SessionLocal()
    try:
        test = db.query(Test).filter(Test.id == test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail="Test not found")
        
        renderer = RENDERERS.get(test.test_type, RENDERERS["multiple_choice"])
        html = renderer(test)
        
        return JSONResponse({"html": html})
    finally:
        db.close()

@router.post("/api/exercise/complete")
async def complete_exercise(request: Request, completion: ExerciseCompletion):
    email = request.cookies.get("user_email")
    if not email:
        raise HTTPException(status_code=401, detail="Not logged in")
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Save or update score
        score = db.query(UserExerciseScore).filter(
            UserExerciseScore.user_id == user.id,
            UserExerciseScore.exercise_id == completion.exercise_id
        ).first()
        
        if not score:
            score = UserExerciseScore(
                user_id=user.id,
                exercise_id=completion.exercise_id,
                stars=completion.stars,
                completed=True
            )
            db.add(score)
        else:
            # Update only if better stars
            if completion.stars > score.stars:
                score.stars = completion.stars
            score.completed = True
        
        # Update overall status if this was the "current" exercise
        exercise = db.query(Exercise).filter(Exercise.id == completion.exercise_id).first()
        if exercise:
            chapter = db.query(Chapter).filter(Chapter.id == exercise.chapter_id).first()
            status = db.query(StatusLearning).filter(StatusLearning.user_id == user.id).first()
            if status and chapter:
                if chapter.category == "grammar":
                    # Only advance if we finished the current or higher
                    if exercise.id >= (status.status_exercise_grammar or 0):
                        # Find next exercise
                        next_ex = db.query(Exercise).filter(
                            Exercise.chapter_id == chapter.id,
                            Exercise.order_index > exercise.order_index
                        ).order_by(Exercise.order_index).first()
                        
                        if next_ex:
                            status.status_exercise_grammar = next_ex.id
                        else:
                            # Chapter complete, find next chapter
                            next_ch = db.query(Chapter).filter(
                                Chapter.category == "grammar",
                                Chapter.order_index > chapter.order_index
                            ).order_by(Chapter.order_index).first()
                            if next_ch:
                                status.status_chapter_grammar = next_ch.id
                                first_ex = db.query(Exercise).filter(Exercise.chapter_id == next_ch.id).order_by(Exercise.order_index).first()
                                if first_ex:
                                    status.status_exercise_grammar = first_ex.id
                
                elif chapter.category == "vocabulary":
                    if exercise.id >= (status.status_exercise_vocabulary or 0):
                        next_ex = db.query(Exercise).filter(
                            Exercise.chapter_id == chapter.id,
                            Exercise.order_index > exercise.order_index
                        ).order_by(Exercise.order_index).first()
                        if next_ex:
                            status.status_exercise_vocabulary = next_ex.id
        
        db.commit()
        return {"status": "success", "stars": completion.stars}
    finally:
        db.close()
