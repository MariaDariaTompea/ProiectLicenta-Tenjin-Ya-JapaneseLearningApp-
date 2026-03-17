from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.database import Base, engine
from core.routes import router

# Create tables
Base.metadata.create_all(bind=engine)

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

# Include routes
app.include_router(router)

# Documentation
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/hiragana-table
# http://127.0.0.1:8000/hiragana
