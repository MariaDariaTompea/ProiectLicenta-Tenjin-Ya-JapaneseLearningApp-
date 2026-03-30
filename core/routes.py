from fastapi import APIRouter

from features.user.routes import router as auth_router
from features.customization.routes import router as profile_router
from features.grammar.routes import router as course_router
from features.japanese.routes import router as japanese_router
from features.exercises.routes import router as exercises_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(course_router)
router.include_router(japanese_router)
router.include_router(exercises_router)
