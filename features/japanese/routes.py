"""Japanese writing system routes — hiragana, katakana, kanji tables"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from core.database import SessionLocal
from features.japanese.models import Hiragana, Katakana
from features.japanese.templates.hiragana import get_hiragana_table_html
from features.japanese.templates.katakana import get_katakana_table_html

router = APIRouter()


@router.get("/hiragana")
def get_all_hiragana():
    db = SessionLocal()
    hiragana = db.query(Hiragana).all()
    db.close()
    return hiragana


@router.get("/hiragana-table", response_class=HTMLResponse)
def get_hiragana_table():
    try:
        db = SessionLocal()
        hiragana_list = db.query(Hiragana).all()
        db.close()
        return get_hiragana_table_html(hiragana_list)
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"


@router.get("/katakana-table", response_class=HTMLResponse)
def get_katakana_table():
    try:
        db = SessionLocal()
        katakana_list = db.query(Katakana).all()
        db.close()
        return get_katakana_table_html(katakana_list)
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"


@router.get("/kanji-table", response_class=HTMLResponse)
async def kanji_table():
    return """
    <html>
    <head>
        <title>Kanji Characters</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #fff; }
            h1 { font-family: 'Playfair Display', serif; font-size: 48px; color: #FCBCD7; font-weight: 700; letter-spacing: 2px; }
        </style>
    </head>
    <body>
        <h1>Kanji Characters</h1>
        <p>Coming soon...</p>
    </body>
    </html>
    """
