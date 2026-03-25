from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.database import Base, engine
from core.routes import router
import os

# Import all models so their tables are created
from features.user.models import User, UserProfile, UserPhoto, StatusLearning, UserItem  # noqa
from features.customization.models import Achievement  # noqa
from features.grammar.models import Proficiency, Chapter, Exercise, Test  # noqa
from features.japanese.models import Hiragana, Katakana  # noqa

# Create tables
Base.metadata.create_all(bind=engine)

# Ensure upload directories exist
os.makedirs("customisableprofile/avatars", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

# Initialize FastAPI app
app = FastAPI()

# Mount static files
app.mount("/images", StaticFiles(directory="features/customization/static/images"), name="images")
app.mount("/audio", StaticFiles(directory="features/japanese/static/audio"), name="audio")
app.mount("/icons", StaticFiles(directory="features/customization/static/icons"), name="icons")
app.mount("/textures", StaticFiles(directory="features/customization/static/textures"), name="textures")
app.mount("/videos", StaticFiles(directory="features/customization/static/videos"), name="videos")
app.mount("/katakana_assets", StaticFiles(directory="features/japanese/static/katakana_assets"), name="katakana_assets")
app.mount("/customisableprofile", StaticFiles(directory="features/customization/static/customisableprofile"), name="customisableprofile")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routes
app.include_router(router)

# Documentation
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/hiragana-table
# http://127.0.0.1:8000/hiragana
