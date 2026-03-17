"""
Routes package — all FastAPI routers combined.
Import from here: `from routes import router`
"""

from fastapi import APIRouter
from routes.auth_routes import router as auth_router
from routes.profile_routes import router as profile_router
from routes.course_routes import router as course_router
from routes.japanese_routes import router as japanese_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(course_router)
router.include_router(japanese_router)
