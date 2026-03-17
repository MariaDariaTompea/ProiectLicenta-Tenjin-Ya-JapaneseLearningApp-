from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from routes import router

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Mount static files
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/audio", StaticFiles(directory="audio"), name="audio")
app.mount("/icons", StaticFiles(directory="icons"), name="icons")
app.mount("/textures", StaticFiles(directory="textures"), name="textures")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")
app.mount("/katakana_assets", StaticFiles(directory="katakana_assets"), name="katakana_assets")
app.mount("/customisableprofile", StaticFiles(directory="customisableprofile"), name="customisableprofile")

# Include routes
app.include_router(router)

# Documentation
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/hiragana-table
# http://127.0.0.1:8000/hiragana
