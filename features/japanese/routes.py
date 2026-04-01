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
            body { font-family: Arial, sans-serif; margin: 20px; background-image: url('/textures/vignettepinkflower.png'); background-size: cover; background-position: center; background-attachment: fixed; }
            h1 { font-family: 'Playfair Display', serif; font-size: 48px; color: #FCBCD7; font-weight: 700; letter-spacing: 2px; margin-left:160px; margin-top: 20px; }
            p { font-family: 'Playfair Display', serif; font-size: 18px; color: #FCBCD7; margin-left:160px; }
            
            /* Back button */
            .back-btn {
                position: fixed;
                top: 30px;
                left: 30px;
                z-index: 500;
                background: rgba(239, 135, 190, 0.15);
                border: 2px solid #EF87BE;
                color: #FCBCD7;
                font-family: 'Playfair Display', serif;
                font-size: 18px;
                padding: 10px 24px;
                border-radius: 30px;
                cursor: pointer;
                transition: background 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
                letter-spacing: 1px;
                text-decoration: none;
                display: inline-block;
            }
            .back-btn:hover {
                background: rgba(239, 135, 190, 0.35);
                transform: scale(1.05);
                box-shadow: 0 0 15px rgba(239, 135, 190, 0.4);
            }
        </style>
    </head>
    <body>
        <a href="/writing-tables" class="back-btn">&#8592; Back</a>
        <h1>Kanji Characters</h1>
        <p>Coming soon...</p>
    </body>
    </html>
    """
