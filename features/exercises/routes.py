from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from core.database import SessionLocal
from features.grammar.models import Exercise, Test
from features.exercises.templates.exercise_runner import render_exercise_runner
from features.exercises.renderer import RENDERERS
import json

router = APIRouter()

@router.get("/course/grammar/Chapter{chapter_id}/exercise/{exercise_id}", response_class=HTMLResponse)
async def exercise_page(chapter_id: int, exercise_id: int):
    db = SessionLocal()
    try:
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id, Exercise.chapter_id == chapter_id).first()
        if not exercise:
            raise HTTPException(status_code=404, detail="Exercise not found")
        
        tests = db.query(Test).filter(Test.exercise_id == exercise_id).order_by(Test.order_index).all()
        return render_exercise_runner(exercise, tests, chapter_id)
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
