"""Course routes — welcome page, grammar, vocabulary, culture, settings"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from core.database import SessionLocal
from features.user.models import User
from features.grammar.models import Proficiency, Chapter, Exercise

router = APIRouter()


@router.get("/welcome", response_class=HTMLResponse)
async def welcome():
    return """
    <html>
    <head>
        <title>Welcome</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
        <style>
            body { margin: 0; height: 100vh; overflow: hidden; opacity: 0; transition: opacity 1s ease; }
            body.loaded { opacity: 1; }
            .bg-image {
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background: url('/textures/welcomepage.png') no-repeat center center;
                background-size: cover;
                z-index: -1;
                transform: scale(1);
                transition: transform 3s ease;
            }
            .bg-image.zoom { transform: scale(1.08); }
            .welcome-title {
                color: #E56AB3;
                font-family: 'Playfair Display', serif;
                font-size: 120px;
                text-align: center;
                margin-top: 20vh;
                letter-spacing: 2px;
                font-weight: 700;
                transition: transform 1s cubic-bezier(0.68,-0.55,0.27,1.55);
            }
            .slide-up { transform: translateY(-120vh); }
            .selection-table {
                display: flex;
                width: 100vw;
                height: 100vh;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                position: absolute;
                top: 0; left: 0;
                z-index: 10;
                opacity: 0;
                pointer-events: none;
                transition: opacity 1s ease;
                overflow: hidden;
            }
            .selection-table.visible {
                opacity: 1;
                pointer-events: all;
            }
            .selection-bg {
                position: absolute;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background: url('/textures/tablepage.png') no-repeat center center;
                background-size: cover;
                z-index: -1;
                transform: scale(1.15);
                transition: transform 3s ease;
            }
            .selection-bg.zoom-in { transform: scale(1); }
            .selection-title {
                font-family: 'Playfair Display', serif;
                font-size: 48px;
                color: #FCBCD7;
                margin-bottom: 16px;
                margin-top: 40px;
            }
            .selection-desc {
                font-family: 'Playfair Display', serif;
                font-size: 20px;
                color: #FCBCD7;
                margin-bottom: 32px;
            }
            .select-table {
                display: flex;
                gap: 40px;
                justify-content: center;
            }
            .select-item {
                background: transparent;
                border-radius: 18px;
                box-shadow: none;
                padding: 40px 60px;
                font-size: 32px;
                color: #FCBCD7;
                font-family: 'Playfair Display', serif;
                cursor: pointer;
                transition: box-shadow 0.3s ease, transform 0.4s ease, opacity 0.5s ease;
                border: none;
            }
            .select-item:hover {
                box-shadow: 0 0 25px 10px rgba(191, 80, 130, 0.5);
                transform: scale(1.06);
            }

            .selection-table.slide-away .selection-title,
            .selection-table.slide-away .selection-desc,
            .selection-table.slide-away .course-link {
                opacity: 0;
                transform: translateY(-40px);
                transition: opacity 0.4s ease, transform 0.5s ease;
            }
            .selection-table.slide-away .select-item {
                opacity: 0;
                transform: translateY(60px) scale(0.9);
            }
            .selection-table.slide-away .select-item:nth-child(1) { transition-delay: 0s; }
            .selection-table.slide-away .select-item:nth-child(2) { transition-delay: 0.08s; }
            .selection-table.slide-away .select-item:nth-child(3) { transition-delay: 0.16s; }

            .page-slide {
                position: fixed;
                top: 100%;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(180deg, #1a0a12 0%, #0a0a0a 100%);
                z-index: 200;
                transition: top 0.8s cubic-bezier(0.65, 0, 0.35, 1);
            }
            .page-slide.active {
                top: 0;
            }
            .page-slide-label {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-family: 'Playfair Display', serif;
                font-size: 52px;
                color: #FCBCD7;
                opacity: 0;
                transition: opacity 0.5s ease 0.5s;
                letter-spacing: 4px;
            }
            .page-slide.active .page-slide-label {
                opacity: 1;
            }
            .course-link {
                font-family: 'Playfair Display', serif;
                font-size: 16px;
                color: #FCBCD7;
                margin-top: 40px;
                text-decoration: none;
                cursor: pointer;
                transition: color 0.3s ease;
            }
            .course-link:hover {
                color: #fde0ed;
            }

            .black-overlay {
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background: #000;
                z-index: 100;
                opacity: 0;
                pointer-events: none;
                transition: opacity 1.2s ease;
            }
            .black-overlay.active {
                opacity: 1;
                pointer-events: all;
            }

            .course-menu {
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background: url('/textures/templepick.png') no-repeat center center;
                background-size: cover;
                z-index: 99;
                display: flex;
                align-items: center;
                justify-content: space-between;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.8s ease 0.3s;
            }
            .course-menu.visible {
                opacity: 1;
                pointer-events: all;
            }

            .ribbon-container {
                display: flex;
                flex-direction: column;
                gap: 40px;
                align-items: flex-end;
                margin-right: 0;
            }
            .ribbon-container.is-left {
                align-items: flex-start;
                margin-left: 0;
            }

            .ribbon-item {
                position: relative;
                width: 588px;
                height: 140px;
                cursor: pointer;
                transform: translateX(100%);
                transition: transform 0.9s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            }
            .ribbon-item.is-left {
                transform: translateX(-100%);
            }
            .ribbon-item.slide-in {
                transform: translateX(30px);
            }
            .ribbon-item.is-left.slide-in {
                transform: translateX(-30px);
            }
            .ribbon-item:hover {
                transform: translateX(10px) !important;
            }
            .ribbon-item.is-left:hover {
                transform: translateX(-10px) !important;
            }

            .ribbon-item img {
                width: 100%;
                height: 100%;
                object-fit: contain;
                object-position: right;
            }
            .ribbon-item.is-left img {
                object-position: left;
            }

            .ribbon-text {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-family: 'Playfair Display', serif;
                font-size: 30px;
                color: #12060e;
                text-shadow: none;
                letter-spacing: 3px;
                pointer-events: none;
                white-space: nowrap;
            }

            .ribbon-tooltip {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) translateY(20px);
                background: rgba(13, 6, 8, 0.95);
                border: 1px solid rgba(229, 106, 179, 0.4);
                color: #FCBCD7;
                font-family: 'Playfair Display', serif;
                font-size: 14px;
                letter-spacing: 1px;
                padding: 10px 18px;
                border-radius: 12px;
                white-space: nowrap;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.3s ease 0s, transform 0.3s ease 0s;
                box-shadow: 0 8px 32px rgba(191, 80, 130, 0.25);
                z-index: 10;
            }

            .ribbon-item:hover .ribbon-tooltip {
                opacity: 1;
                transform: translate(-50%, -50%) translateY(0);
                transition: opacity 0.4s ease 2s, transform 0.4s ease 2s;
            }

            .ribbon-item:nth-child(1) { transition-delay: 0.3s; }
            .ribbon-item:nth-child(2) { transition-delay: 0.5s; }
            .ribbon-item:nth-child(3) { transition-delay: 0.7s; }
            .ribbon-item:nth-child(4) { transition-delay: 0.9s; }
            .ribbon-container.is-left .ribbon-item:nth-child(1) { transition-delay: 1.1s; }

            .ribbon-container.fade-out .ribbon-item {
                opacity: 0;
                transform: translateX(100%) !important;
                transition: opacity 0.6s ease, transform 0.8s ease;
            }
            .ribbon-container.fade-out .ribbon-item.is-left {
                transform: translateX(-100%) !important;
            }
            .ribbon-container.fade-out .ribbon-item:nth-child(1) { transition-delay: 0s; }
            .ribbon-container.fade-out .ribbon-item:nth-child(2) { transition-delay: 0.1s; }
            .ribbon-container.fade-out .ribbon-item:nth-child(3) { transition-delay: 0.2s; }
            .ribbon-container.fade-out .ribbon-item:nth-child(4) { transition-delay: 0.3s; }
            .ribbon-container.is-left.fade-out .ribbon-item:nth-child(1) { transition-delay: 0.4s; }

            .fox-video-overlay {
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                z-index: 101;
                opacity: 0;
                pointer-events: none;
                transition: opacity 1s ease;
            }
            .fox-video-overlay.visible {
                opacity: 1;
                pointer-events: all;
            }
            .fox-video-overlay video {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }

        </style>
    </head>
    <body>
        <div class="bg-image" id="bgImage"></div>
        <div id="welcomeTitle" class="welcome-title">Welcome</div>

        <div class="black-overlay" id="blackOverlay"></div>

        <div class="course-menu" id="courseMenu">
            <div class="ribbon-container is-left" id="leftRibbonContainer">
                <div class="ribbon-item is-left" data-href="/writing-tables">
                    <img src="/textures/ribbontables.png" alt="ribbon">
                    <div class="ribbon-tooltip">Table Contents</div>
                </div>
                <div class="ribbon-item is-left" data-href="/writing-practice">
                    <img src="/textures/ribbonwritting.png" alt="ribbon">
                    <div class="ribbon-tooltip">Writing Practice</div>
                </div>
            </div>
            <div class="ribbon-container" id="ribbonContainer">
                <div class="ribbon-item" data-href="/course/grammar">
                    <img src="/textures/ribbon1.png" alt="ribbon">
                    <div class="ribbon-text">Grammar</div>
                </div>
                <div class="ribbon-item" data-href="/course/vocabulary">
                    <img src="/textures/ribbon2.png" alt="ribbon">
                    <div class="ribbon-text">Vocabulary</div>
                </div>
                <div class="ribbon-item" data-href="/course/culture">
                    <img src="/textures/ribbon3.png" alt="ribbon">
                    <div class="ribbon-text">Culture</div>
                </div>
                <div class="ribbon-item" data-href="/profile">
                    <img src="/textures/ribbon4.png" alt="ribbon">
                    <div class="ribbon-text">Profile</div>
                </div>
            </div>
        </div>

        <div class="fox-video-overlay" id="foxVideo">
            <video muted preload="auto" id="foxVid">
                <source src="/textures/fox%20running.mp4" type="video/mp4">
            </video>
        </div>

        <script>
            window.addEventListener('load', () => {
                document.body.classList.add('loaded');
                document.getElementById('bgImage').classList.add('zoom');

                const hash = window.location.hash;
                if (hash === '#selection') {
                    // instant — already on selection screen
                    document.getElementById('welcomeTitle').style.display = 'none';
                    const courseMenu = document.getElementById('courseMenu');
                    courseMenu.style.transition = 'none';
                    courseMenu.classList.add('visible');
                    document.querySelectorAll('.ribbon-item').forEach(item => {
                        item.style.transition = 'none';
                        item.classList.add('slide-in');
                    });
                    setTimeout(() => {
                        courseMenu.style.transition = '';
                        document.querySelectorAll('.ribbon-item').forEach(i => i.style.transition = '');
                    }, 50);
                } else {
                    // normal flow: Welcome title → course menu
                    setTimeout(() => {
                        document.getElementById('welcomeTitle').classList.add('slide-up');
                        setTimeout(() => {
                            window.history.replaceState(null, null, '#selection');
                            const courseMenu = document.getElementById('courseMenu');
                            courseMenu.classList.add('visible');
                            setTimeout(() => {
                                document.querySelectorAll('.ribbon-item').forEach(item => {
                                    item.classList.add('slide-in');
                                });
                            }, 300);
                        }, 700);
                    }, 2000);
                }
            });

            document.querySelectorAll('.ribbon-item').forEach(item => {
                item.addEventListener('click', function() {
                    const targetUrl = this.getAttribute('data-href');
                    const ribbonContainer = document.getElementById('ribbonContainer');
                    const leftRibbonContainer = document.getElementById('leftRibbonContainer');
                    const foxOverlay = document.getElementById('foxVideo');
                    const foxVid = document.getElementById('foxVid');
                    const overlay = document.getElementById('blackOverlay');
                    ribbonContainer.classList.add('fade-out');
                    if (leftRibbonContainer) leftRibbonContainer.classList.add('fade-out');
                    setTimeout(() => {
                        foxVid.currentTime = 0;
                        foxVid.play();
                        foxOverlay.classList.add('visible');
                    }, 800);
                    foxVid.addEventListener('ended', function() {
                        overlay.style.zIndex = '102';
                        overlay.classList.add('active');
                        setTimeout(() => { window.location.href = targetUrl; }, 1300);
                    });
                });
            });
        </script>
    </body>
    </html>
    """


# ─────────────────────────────────────────────────────────
#  WRITING TABLES — standalone picker
# ─────────────────────────────────────────────────────────

@router.get("/writing-tables", response_class=HTMLResponse)
async def writing_tables():
    """Standalone writing-system picker — reached from the welcome page 'あ' button."""
    return r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Writing Systems — Tenjin-Ya</title>
        <meta name="description" content="Choose a writing system to learn: Hiragana, Katakana, or Kanji.">
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

            body {
                font-family: 'Inter', sans-serif;
                height: 100vh;
                overflow: hidden;
                background: #0d0608;
                color: #FCBCD7;
                opacity: 0;
                transition: opacity 0.9s ease;
                user-select: none;
            }
            body.loaded { opacity: 1; }

            /* Background */
            .bg-img {
                position: fixed; inset: 0;
                background: url('/textures/island1 (1).png') no-repeat center center / cover;
                opacity: 0.22; z-index: 0; pointer-events: none;
            }
            .vignette {
                position: fixed; inset: 0;
                background: radial-gradient(ellipse at center, transparent 20%, #0d0608 88%);
                z-index: 1; pointer-events: none;
            }

            /* Back button */
            .back-btn {
                position: fixed; top: 32px; left: 36px; z-index: 50;
                width: 44px; height: 44px; border-radius: 50%;
                background: rgba(252,188,215,0.06);
                border: 1px solid rgba(252,188,215,0.15);
                display: flex; align-items: center; justify-content: center;
                cursor: pointer; transition: all 0.3s ease;
                color: #FCBCD7; text-decoration: none;
            }
            .back-btn svg { width: 24px; height: 24px; fill: currentColor; }
            .back-btn:hover {
                background: rgba(252,188,215,0.12);
                border-color: rgba(252,188,215,0.35);
                box-shadow: 0 0 16px rgba(191,80,130,0.3);
                transform: scale(1.08);
            }

            /* Centre content */
            .centre {
                position: relative; z-index: 2;
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                height: 100vh;
                text-align: center;
                gap: 0;
            }

            .eyebrow {
                font-size: 11px; font-weight: 500;
                letter-spacing: 3px; text-transform: uppercase;
                color: #E56AB3; margin-bottom: 18px;
                opacity: 0; transform: translateY(10px);
                animation: fadeUp 0.6s ease 0.3s forwards;
            }

            h1 {
                font-family: 'Playfair Display', serif;
                font-size: clamp(36px, 5vw, 60px);
                font-weight: 700;
                color: #FCBCD7;
                line-height: 1.15;
                margin-bottom: 14px;
                opacity: 0; transform: translateY(12px);
                animation: fadeUp 0.6s ease 0.5s forwards;
            }

            .subtitle {
                font-size: 16px; font-weight: 300;
                color: rgba(252,188,215,0.6);
                letter-spacing: 0.5px;
                margin-bottom: 64px;
                opacity: 0; transform: translateY(12px);
                animation: fadeUp 0.6s ease 0.65s forwards;
            }

            /* Cards row */
            .cards {
                display: flex; gap: 28px;
                opacity: 0; transform: translateY(16px);
                animation: fadeUp 0.6s ease 0.85s forwards;
            }

            .card {
                position: relative;
                width: 180px; height: 220px;
                border-radius: 20px;
                background: rgba(252,188,215,0.04);
                border: 1px solid rgba(252,188,215,0.12);
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                gap: 16px;
                cursor: pointer;
                text-decoration: none;
                transition: background 0.3s ease, border-color 0.3s ease,
                            box-shadow 0.3s ease, transform 0.3s ease;
                overflow: hidden;
            }
            .card::before {
                content: '';
                position: absolute; inset: 0;
                background: radial-gradient(circle at 50% 50%, rgba(229,106,179,0.12) 0%, transparent 70%);
                opacity: 0; transition: opacity 0.4s ease;
            }
            .card:hover { border-color: rgba(252,188,215,0.35); transform: translateY(-6px); }
            .card:hover::before { opacity: 1; }
            .card:hover { box-shadow: 0 12px 40px rgba(191,80,130,0.25); }

            .card-jp {
                font-family: 'Playfair Display', serif;
                font-size: 52px;
                color: #FCBCD7;
                line-height: 1;
                transition: transform 0.3s ease;
            }
            .card:hover .card-jp { transform: scale(1.1); }

            .card-label {
                font-family: 'Inter', sans-serif;
                font-size: 13px; font-weight: 500;
                letter-spacing: 2px; text-transform: uppercase;
                color: rgba(252,188,215,0.65);
            }

            @keyframes fadeUp {
                to { opacity: 1; transform: none; }
            }

            /* Page transition overlay */
            .page-fade {
                position: fixed; inset: 0;
                background: #0d0608;
                z-index: 200;
                opacity: 0; pointer-events: none;
                transition: opacity 0.6s ease;
            }
            .page-fade.active { opacity: 1; pointer-events: all; }
        </style>
    </head>
    <body>
        <div class="bg-img"></div>
        <div class="vignette"></div>
        <div class="page-fade" id="pageFade"></div>

        <!-- Back to Welcome -->
        <a class="back-btn" href="/welcome#selection" title="Back to Welcome">
            <svg viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
        </a>

        <div class="centre">
            <div class="eyebrow">Writing Systems</div>
            <h1>What do you want to learn?</h1>
            <p class="subtitle">Choose a writing system to explore its character table.</p>

            <div class="cards">
                <a class="card" href="/hiragana-table" id="cardHiragana">
                    <div class="card-jp">あ</div>
                    <div class="card-label">Hiragana</div>
                </a>
                <a class="card" href="/katakana-table" id="cardKatakana">
                    <div class="card-jp">ア</div>
                    <div class="card-label">Katakana</div>
                </a>
                <a class="card" href="/kanji-table" id="cardKanji">
                    <div class="card-jp">字</div>
                    <div class="card-label">Kanji</div>
                </a>
            </div>
        </div>

        <script>
            window.addEventListener('load', () => document.body.classList.add('loaded'));

            // Smooth transition out on card click
            document.querySelectorAll('.card').forEach(card => {
                card.addEventListener('click', function(e) {
                    e.preventDefault();
                    const href = this.getAttribute('href');
                    const fade = document.getElementById('pageFade');
                    fade.classList.add('active');
                    setTimeout(() => { window.location.href = href; }, 650);
                });
            });

            // Smooth transition out on back button
            document.querySelector('.back-btn').addEventListener('click', function(e) {
                e.preventDefault();
                const href = this.getAttribute('href');
                const fade = document.getElementById('pageFade');
                fade.classList.add('active');
                setTimeout(() => { window.location.href = href; }, 650);
            });
        </script>
    </body>
    </html>
    """

# ─────────────────────────────────────────────────────────
#  WRITING PRACTICE
# ─────────────────────────────────────────────────────────

@router.get("/writing-practice", response_class=HTMLResponse)
async def writing_practice():
    """Writing practice menu with system selection and amount slider."""
    return r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Writing Practice — Tenjin-Ya</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: 'Inter', sans-serif; height: 100vh; overflow: hidden; background: #0d0608; color: #FCBCD7; opacity: 0; transition: opacity 0.9s ease; user-select: none; }
            body.loaded { opacity: 1; }
            .bg-img { position: fixed; inset: 0; background: url('/textures/island1 (1).png') no-repeat center center / cover; opacity: 0.22; z-index: 0; pointer-events: none; }
            .vignette { position: fixed; inset: 0; background: radial-gradient(ellipse at center, transparent 20%, #0d0608 88%); z-index: 1; pointer-events: none; }
            .back-btn { position: fixed; top: 32px; left: 36px; z-index: 50; width: 44px; height: 44px; border-radius: 50%; background: rgba(252,188,215,0.06); border: 1px solid rgba(252,188,215,0.15); display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.3s ease; color: #FCBCD7; text-decoration: none; }
            .back-btn svg { width: 24px; height: 24px; fill: currentColor; }
            .back-btn:hover { background: rgba(252,188,215,0.12); border-color: rgba(252,188,215,0.35); box-shadow: 0 0 16px rgba(191,80,130,0.3); transform: scale(1.08); }
            .centre { position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; text-align: center; gap: 0; }
            .eyebrow { font-size: 11px; font-weight: 500; letter-spacing: 3px; text-transform: uppercase; color: #E56AB3; margin-bottom: 18px; opacity: 0; transform: translateY(10px); animation: fadeUp 0.6s ease 0.3s forwards; }
            h1 { font-family: 'Playfair Display', serif; font-size: clamp(36px, 5vw, 60px); font-weight: 700; color: #FCBCD7; line-height: 1.15; margin-bottom: 14px; opacity: 0; transform: translateY(12px); animation: fadeUp 0.6s ease 0.5s forwards; }
            .subtitle { font-size: 16px; font-weight: 300; color: rgba(252,188,215,0.6); letter-spacing: 0.5px; margin-bottom: 64px; opacity: 0; transform: translateY(12px); animation: fadeUp 0.6s ease 0.65s forwards; }
            .cards { display: flex; gap: 28px; opacity: 0; transform: translateY(16px); animation: fadeUp 0.6s ease 0.85s forwards; }
            .card { position: relative; width: 180px; height: 220px; border-radius: 20px; background: rgba(252,188,215,0.04); border: 1px solid rgba(252,188,215,0.12); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; cursor: pointer; text-decoration: none; transition: background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease; overflow: hidden; }
            .card::before { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 50% 50%, rgba(229,106,179,0.12) 0%, transparent 70%); opacity: 0; transition: opacity 0.4s ease; }
            .card:hover { border-color: rgba(252,188,215,0.35); transform: translateY(-6px); }
            .card:hover::before { opacity: 1; }
            .card:hover { box-shadow: 0 12px 40px rgba(191,80,130,0.25); }
            .card-jp { font-family: 'Playfair Display', serif; font-size: 52px; color: #FCBCD7; line-height: 1; transition: transform 0.3s ease; }
            .card:hover .card-jp { transform: scale(1.1); }
            .card-label { font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 500; letter-spacing: 2px; text-transform: uppercase; color: rgba(252,188,215,0.65); pointer-events: none; }
            @keyframes fadeUp { to { opacity: 1; transform: none; } }
            
            /* Popup styles */
            .popup-overlay { position: fixed; inset: 0; background: rgba(13,6,8,0.8); backdrop-filter: blur(8px); z-index: 100; display: flex; align-items: center; justify-content: center; opacity: 0; pointer-events: none; transition: opacity 0.4s ease; }
            .popup-overlay.active { opacity: 1; pointer-events: all; }
            .popup-box { background: rgba(20, 10, 15, 0.95); border: 1px solid rgba(252,188,215,0.2); border-radius: 24px; padding: 40px; width: 400px; max-width: 90%; box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 20px rgba(229,106,179,0.1); transform: translateY(20px); transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1); text-align: center; }
            .popup-overlay.active .popup-box { transform: translateY(0); }
            .popup-box h2 { font-family: 'Playfair Display', serif; font-size: 28px; color: #FCBCD7; margin-bottom: 12px; }
            .popup-box p { color: rgba(252,188,215,0.7); font-size: 15px; margin-bottom: 30px; }
            .slider-container { display: flex; align-items: center; gap: 16px; margin-bottom: 30px; }
            .slider-container span { font-family: 'Inter', sans-serif; font-size: 16px; font-weight: 600; color: #E56AB3; width: 30px; text-align: center; }
            input[type=range] { flex: 1; -webkit-appearance: none; background: transparent; }
            input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; height: 20px; width: 20px; border-radius: 50%; background: #E56AB3; cursor: pointer; margin-top: -8px; box-shadow: 0 0 10px rgba(229,106,179,0.5); }
            input[type=range]::-webkit-slider-runnable-track { width: 100%; height: 4px; cursor: pointer; background: rgba(252,188,215,0.2); border-radius: 2px; }
            .btn-group { display: flex; gap: 16px; }
            .btn { flex: 1; padding: 12px; border-radius: 12px; font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 1px; }
            .btn-cancel { background: transparent; border: 1px solid rgba(252,188,215,0.3); color: #FCBCD7; }
            .btn-cancel:hover { background: rgba(252,188,215,0.1); }
            .btn-start { background: linear-gradient(135deg, #E56AB3 0%, #BF5082 100%); border: none; color: #fff; }
            .btn-start:hover { box-shadow: 0 0 20px rgba(191,80,130,0.4); transform: translateY(-2px); }
        </style>
    </head>
    <body>
        <div class="bg-img"></div>
        <div class="vignette"></div>
        <a class="back-btn" href="/welcome#selection" title="Back to Welcome">
            <svg viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
        </a>

        <div class="centre">
            <div class="eyebrow">Writing Practice</div>
            <h1>What do you want to practice?</h1>
            <p class="subtitle">Select a writing system to start your drawing session.</p>

            <div class="cards">
                <div class="card" data-system="hiragana" data-max="46">
                    <div class="card-jp">あ</div>
                    <div class="card-label">Hiragana</div>
                </div>
                <div class="card" data-system="katakana" data-max="46">
                    <div class="card-jp">ア</div>
                    <div class="card-label">Katakana</div>
                </div>
                <div class="card" data-system="kanji" data-max="30">
                    <div class="card-jp">字</div>
                    <div class="card-label">Kanji</div>
                </div>
            </div>
        </div>

        <div class="popup-overlay" id="popupOverlay">
            <div class="popup-box">
                <h2 id="popupTitle">Practice</h2>
                <p>How many characters do you want to practice?</p>
                <div class="slider-container">
                    <span id="sliderCur">1</span>
                    <input type="range" id="popupSlider" min="1" max="46" value="7">
                    <span id="sliderMaxTxt">46</span>
                </div>
                <div class="btn-group">
                    <button class="btn btn-cancel" id="btnCancel">Cancel</button>
                    <button class="btn btn-start" id="btnStart">Start</button>
                </div>
            </div>
        </div>

        <script>
            window.addEventListener('load', () => document.body.classList.add('loaded'));

            const overlay = document.getElementById('popupOverlay');
            const slider = document.getElementById('popupSlider');
            const curTxt = document.getElementById('sliderCur');
            const maxTxt = document.getElementById('sliderMaxTxt');
            const title = document.getElementById('popupTitle');
            let selectedSystem = '';

            document.querySelectorAll('.card').forEach(card => {
                card.addEventListener('click', () => {
                    selectedSystem = card.getAttribute('data-system');
                    const max = parseInt(card.getAttribute('data-max'));
                    title.innerText = 'Practice ' + selectedSystem.charAt(0).toUpperCase() + selectedSystem.slice(1);
                    slider.max = max;
                    slider.value = Math.min(7, max);
                    curTxt.innerText = slider.value;
                    maxTxt.innerText = max;
                    overlay.classList.add('active');
                });
            });

            slider.addEventListener('input', () => {
                curTxt.innerText = slider.value;
            });

            document.getElementById('btnCancel').addEventListener('click', () => {
                overlay.classList.remove('active');
            });

            document.getElementById('btnStart').addEventListener('click', () => {
                window.location.href = `/writing-exercise?system=${selectedSystem}&count=${slider.value}`;
            });
            
            document.querySelector('.back-btn').addEventListener('click', function(e) {
                e.preventDefault();
                const href = this.getAttribute('href');
                document.body.style.opacity = '0';
                setTimeout(() => { window.location.href = href; }, 650);
            });
        </script>
    </body>
    </html>
    """

@router.get("/writing-exercise", response_class=HTMLResponse)
async def writing_exercise(system: str = "hiragana", count: int = 1):
    """The canvas exercise loop."""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Practice {{system.capitalize()}} — Tenjin-Ya</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ font-family: 'Inter', sans-serif; height: 100vh; background: #0d0608; color: #FCBCD7; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden; }}
            .bg-img {{ position: fixed; inset: 0; background: url('/textures/tablepage.png') no-repeat center center / cover; opacity: 0.15; z-index: 0; pointer-events: none; }}
            .container {{ position: relative; z-index: 10; display: flex; flex-direction: column; align-items: center; gap: 24px; width: 100%; max-width: 800px; }}
            h1 {{ font-family: 'Playfair Display', serif; font-size: 42px; color: #FCBCD7; text-transform: capitalize; margin-bottom: 8px; }}
            .eyebrow {{ font-size: 16px; font-weight: 500; letter-spacing: 2px; color: #E56AB3; text-transform: uppercase; margin-bottom: -16px; }}
            .board-container {{ background: rgba(252,188,215,0.05); border: 1px solid rgba(252,188,215,0.15); border-radius: 24px; padding: 40px; box-shadow: 0 0 40px rgba(191,80,130,0.15); display: flex; flex-direction: column; align-items: center; gap: 24px; position:relative; overflow:hidden; }}
            canvas {{ background: #fff; border-radius: 12px; cursor: crosshair; box-shadow: inset 0 0 20px rgba(0,0,0,0.1); touch-action: none; }}
            .controls {{ display: flex; gap: 16px; width: 100%; }}
            button {{ flex: 1; padding: 14px; border-radius: 12px; border: 1px solid rgba(252,188,215,0.25); background: rgba(252,188,215,0.06); color: #FCBCD7; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 1px; }}
            button:hover {{ background: rgba(252,188,215,0.15); border-color: rgba(252,188,215,0.45); transform: translateY(-2px); }}
            button.primary {{ background: linear-gradient(135deg, #E56AB3 0%, #BF5082 100%); color: #fff; border: none; }}
            button.primary:hover {{ box-shadow: 0 0 20px rgba(191,80,130,0.4); }}
            .result-panel {{ margin-top: 20px; font-size: 18px; color: #E56AB3; font-weight: 500; min-height: 27px; transition: opacity 0.3s ease; text-align: center; }}
            .back-link {{ position: fixed; top: 32px; left: 36px; color: #FCBCD7; text-decoration: none; font-size: 14px; display: flex; align-items: center; gap: 8px; opacity: 0.7; transition: opacity 0.3s ease; z-index:50; }}
            .back-link:hover {{ opacity: 1; }}
            .progress-bar {{ position: absolute; top: 0; left: 0; height: 4px; background: #E56AB3; width: 0%; transition: width 0.3s ease; }}
            .completion-overlay {{ position: absolute; inset: 0; background: rgba(13,6,8,0.9); z-index: 20; display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0; pointer-events: none; transition: opacity 0.5s ease; border-radius: 24px; }}
            .completion-overlay.active {{ opacity: 1; pointer-events: all; }}
            .completion-overlay h2 {{ font-family: 'Playfair Display', serif; font-size: 32px; margin-bottom: 24px; color: #FCBCD7; }}
        </style>
    </head>
    <body>
        <div class="bg-img"></div>
        <a href="/writing-practice" class="back-link">
            ← Back to Menu
        </a>

        <div class="container">
            <div class="eyebrow" id="progressText">Exercise 1 of {{count}}</div>
            <h1>Practice {{system}}</h1>
            <p style="opacity: 0.6" id="promptText">Draw the character below</p>
            
            <div class="board-container">
                <div class="progress-bar" id="progressBar"></div>
                <canvas id="paintCanvas" width="400" height="400"></canvas>
                <div class="controls">
                    <button onclick="clearCanvas()">Clear Board</button>
                    <button class="primary" onclick="recognize()">Recognize</button>
                </div>
                
                <div class="completion-overlay" id="completionOverlay">
                    <h2>Session Complete!</h2>
                    <button class="primary" style="max-width: 200px" onclick="window.location.href='/writing-practice'">Finish</button>
                </div>
            </div>
            
            <div class="result-panel" id="resultText"></div>
        </div>

        <script>
            const canvas = document.getElementById('paintCanvas');
            const ctx = canvas.getContext('2d');
            let drawing = false;
            
            const totalCount = {count};
            let currentCount = 1;

            canvas.addEventListener('mousedown', (e) => {{ 
                drawing = true; 
                ctx.beginPath();
                ctx.moveTo(e.offsetX, e.offsetY);
            }});
            window.addEventListener('mouseup', () => {{ drawing = false; }});
            canvas.addEventListener('mousemove', (e) => {{
                if (!drawing) return;
                ctx.lineWidth = 14;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                ctx.strokeStyle = '#2d2d2d';
                ctx.lineTo(e.offsetX, e.offsetY);
                ctx.stroke();
            }});

            canvas.addEventListener('touchstart', (e) => {{
                const touch = e.touches[0];
                const rect = canvas.getBoundingClientRect();
                drawing = true;
                ctx.beginPath();
                ctx.moveTo(touch.clientX - rect.left, touch.clientY - rect.top);
                e.preventDefault();
            }}, {{ passive: false }});
            canvas.addEventListener('touchmove', (e) => {{
                if (!drawing) return;
                const touch = e.touches[0];
                const rect = canvas.getBoundingClientRect();
                ctx.lineWidth = 14;
                ctx.lineCap = 'round';
                ctx.strokeStyle = '#2d2d2d';
                ctx.lineTo(touch.clientX - rect.left, touch.clientY - rect.top);
                ctx.stroke();
                e.preventDefault();
            }}, {{ passive: false }});

            function clearCanvas() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                document.getElementById('resultText').innerText = "";
            }}
            
            function updateProgress() {{
                document.getElementById('progressText').innerText = `Exercise ${{currentCount}} of ${{totalCount}}`;
                const pct = ((currentCount - 1) / totalCount) * 100;
                document.getElementById('progressBar').style.width = pct + '%';
            }}

            async function recognize() {{
                const resText = document.getElementById('resultText');
                resText.innerText = "Analyzing Strokes...";
                
                setTimeout(() => {{
                    resText.innerText = "AI Recognition placeholder: Looks good! Continuing...";
                    setTimeout(nextExercise, 1500);
                }}, 800);
            }}
            
            function nextExercise() {{
                if (currentCount >= totalCount) {{
                    document.getElementById('progressBar').style.width = '100%';
                    document.getElementById('completionOverlay').classList.add('active');
                }} else {{
                    currentCount++;
                    updateProgress();
                    clearCanvas();
                    document.getElementById('resultText').innerText = "";
                }}
            }}
            
            updateProgress();
        </script>
    </body>
    </html>
    """

# ─────────────────────────────────────────────────────────
#  GRAMMAR API ENDPOINTS
# ─────────────────────────────────────────────────────────


@router.get("/api/grammar/user-status")
async def grammar_user_status(request: Request):
    """Return the current user's grammar status."""
    email = request.cookies.get("user_email")
    if not email:
        return JSONResponse({"status_chapter": 1, "status_exercise": 1})
    db = SessionLocal()
    try:
        from features.user.models import User, StatusLearning
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return JSONResponse({"status_chapter": 1, "status_exercise": 1})
        status = db.query(StatusLearning).filter(StatusLearning.user_id == user.id).first()
        if not status:
            return JSONResponse({"status_chapter": 1, "status_exercise": 1})
        return JSONResponse({
            "status_chapter":  status.status_chapter_grammar  or 1,
            "status_exercise": status.status_exercise_grammar or 1,
        })
    finally:
        db.close()


@router.get("/api/grammar/chapter/{chapter_id}")
async def grammar_chapter(chapter_id: int):
    """Return chapter info + its exercises."""
    db = SessionLocal()
    try:
        chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        # Get proficiency level
        prof = db.query(Proficiency).filter(Proficiency.id == chapter.proficiency_id).first()
        level = prof.level if prof else "N5"
        exercises = (
            db.query(Exercise)
            .filter(Exercise.chapter_id == chapter_id)
            .order_by(Exercise.order_index)
            .all()
        )
        return JSONResponse({
            "chapter": {
                "id":          chapter.id,
                "title":       chapter.title,
                "description": chapter.description or "",
                "level":       level,
            },
            "exercises": [
                {
                    "id":          e.id,
                    "chapter_id":  e.chapter_id,
                    "title":       e.title,
                    "description": e.description or "",
                    "order_index": e.order_index,
                }
                for e in exercises
            ],
        })
    finally:
        db.close()


@router.get("/api/grammar/exercise/{exercise_id}")
async def grammar_exercise_chapter(exercise_id: int):
    """Return the chapter_id for a given exercise (used client-side after hold)."""
    db = SessionLocal()
    try:
        ex = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not ex:
            raise HTTPException(status_code=404, detail="Exercise not found")
        return JSONResponse({"chapter_id": ex.chapter_id, "exercise_id": ex.id})
    finally:
        db.close()


@router.get("/api/grammar/exercises")
async def grammar_all_exercises(request: Request):
    """Return all grammar exercises ordered by chapter order_index then exercise order_index with star info."""
    email = request.cookies.get("user_email")
    db = SessionLocal()
    try:
        from features.user.models import User, UserExerciseScore
        user = None
        if email:
            user = db.query(User).filter(User.email == email).first()
            
        exercises = (
            db.query(Exercise, Chapter, Proficiency)
            .join(Chapter, Exercise.chapter_id == Chapter.id)
            .join(Proficiency, Chapter.proficiency_id == Proficiency.id)
            .filter(Chapter.category == "grammar")
            .order_by(Chapter.order_index, Exercise.order_index)
            .all()
        )
        
        # Get stars for the current user
        scores_map = {}
        if user:
            scores = db.query(UserExerciseScore).filter(UserExerciseScore.user_id == user.id).all()
            scores_map = {s.exercise_id: s.stars for s in scores}
            
        return JSONResponse([
            {
                "id":          ex.id,
                "chapter_id":  ex.chapter_id,
                "title":       ex.title,
                "description": ex.description or "",
                "level":       prof.level if prof else "N5",
                "order_index": ex.order_index,
                "chapter_index": ch.order_index,
                "stars":       scores_map.get(ex.id, 0)
            }
            for ex, ch, prof in exercises
        ])
    finally:
        db.close()


# ─────────────────────────────────────────────────────────
#  GRAMMAR PAGE
# ─────────────────────────────────────────────────────────

@router.get("/course/grammar", response_class=HTMLResponse)
async def course_grammar():
    return r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Grammar — Tenjin-Ya</title>
        <meta name="description" content="Japanese grammar level progression — explore chapters and exercises.">
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            /* ── Reset ── */
            *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

            body {
                font-family: 'Inter', sans-serif;
                height: 100vh;
                overflow: hidden;
                background: #0d0608;
                color: #FCBCD7;
                opacity: 0;
                transition: opacity 0.9s ease;
                user-select: none;
            }
            body.loaded { opacity: 1; }

            /* ── Background ── */
            .bg-layer {
                position: fixed; inset: 0;
                background: url('/textures/tablepage.png') no-repeat center center / cover;
                opacity: 0.18; z-index: 0; pointer-events: none;
            }
            .vignette {
                position: fixed; inset: 0;
                background: radial-gradient(ellipse at center, transparent 30%, #0d0608 90%);
                z-index: 1; pointer-events: none;
            }

            /* ── Split layout ── */
            .layout {
                position: relative; z-index: 2;
                display: flex; width: 100vw; height: 100vh;
            }

            /* ═══════════════════════════════════════════
               LEFT PANEL — 33%  — Info panel
            ═══════════════════════════════════════════ */
            .panel-left {
                width: 33.333%; height: 100%; flex-shrink: 0;
                display: flex; flex-direction: column;
                padding: 48px 32px 48px 36px;
                border-right: 1px solid rgba(252,188,215,0.06);
                position: relative;
                overflow: hidden;
            }

            /* decorative top fade */
            .panel-left::before {
                content: ''; position: absolute;
                top: 0; left: 0; right: 0; height: 120px;
                background: linear-gradient(to bottom, rgba(13,6,8,0.8), transparent);
                pointer-events: none; z-index: 1;
            }

            .left-inner {
                display: flex; flex-direction: column; height: 100%;
                opacity: 0;
                transform: translateY(12px);
                transition: opacity 0.45s ease, transform 0.45s ease;
            }
            .left-inner.visible {
                opacity: 1; transform: none;
            }

            .info-eyebrow {
                font-family: 'Inter', sans-serif;
                font-size: 10px; font-weight: 500;
                letter-spacing: 3px; text-transform: uppercase;
                color: #E56AB3; margin-bottom: 12px;
            }
            .info-title {
                font-family: 'Playfair Display', serif;
                font-size: 28px; font-weight: 700;
                color: #FCBCD7; line-height: 1.25;
                margin-bottom: 14px;
            }
            .info-desc {
                font-family: 'Inter', sans-serif;
                font-size: 13px; font-weight: 300;
                color: rgba(252,188,215,0.58); line-height: 1.7;
                margin-bottom: 28px;
            }

            .exercises-label {
                font-family: 'Inter', sans-serif;
                font-size: 10px; font-weight: 500;
                letter-spacing: 2.5px; text-transform: uppercase;
                color: rgba(252,188,215,0.35); margin-bottom: 12px;
            }
            .exercises-list {
                list-style: none;
                display: flex; flex-direction: column; gap: 8px;
                overflow-y: auto; flex: 1;
                padding-right: 4px;
                scrollbar-width: thin;
                scrollbar-color: rgba(229,106,179,0.25) transparent;
            }
            .exercises-list::-webkit-scrollbar { width: 3px; }
            .exercises-list::-webkit-scrollbar-thumb { background: rgba(229,106,179,0.25); border-radius: 2px; }

            .ex-item {
                display: flex; align-items: flex-start; gap: 12px;
                padding: 10px 14px;
                border-radius: 10px;
                background: rgba(252,188,215,0.04);
                border: 1px solid rgba(252,188,215,0.07);
                transition: background 0.2s ease, border-color 0.2s ease;
                cursor: pointer;
            }
            .ex-item:hover {
                background: rgba(252,188,215,0.09);
                border-color: rgba(252,188,215,0.18);
            }
            .ex-item.current {
                background: rgba(229,106,179,0.12);
                border-color: rgba(229,106,179,0.35);
            }
            .ex-num {
                font-family: 'Playfair Display', serif;
                font-size: 14px; font-weight: 700;
                color: #E56AB3; flex-shrink: 0;
                min-width: 22px;
            }
            .ex-text { display: flex; flex-direction: column; gap: 2px; }
            .ex-title {
                font-family: 'Inter', sans-serif;
                font-size: 13px; font-weight: 500;
                color: #FCBCD7;
            }
            .ex-desc {
                font-family: 'Inter', sans-serif;
                font-size: 11px; font-weight: 300;
                color: rgba(252,188,215,0.45); line-height: 1.5;
            }
            .ex-item.locked {
                opacity: 0.35;
                cursor: not-allowed;
                position: relative;
            }
            .ex-item.locked:hover {
                background: rgba(252,188,215,0.04);
                border-color: rgba(252,188,215,0.07);
            }
            .ex-lock-icon {
                font-size: 14px;
                flex-shrink: 0;
                margin-left: auto;
                opacity: 0.6;
            }
            .ex-stars {
                display: flex; gap: 2px; margin-top: 2px;
            }
            .ex-stars img {
                width: 14px; height: 14px;
            }

            /* empty state */
            .left-empty {
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                height: 100%; gap: 14px; opacity: 0.35;
                text-align: center;
            }
            .left-empty-icon { font-size: 36px; }
            .left-empty-text {
                font-family: 'Inter', sans-serif;
                font-size: 13px; font-weight: 300;
                color: rgba(252,188,215,0.6); line-height: 1.6;
            }

            /* ═══════════════════════════════════════════
               RIGHT PANEL — 66%  — Axis + nodes
            ═══════════════════════════════════════════ */
            .panel-right {
                width: 66.666%; height: 100%; flex-shrink: 0;
                position: relative; display: flex;
                align-items: center; overflow: hidden;
            }

            /* ── Header ── */
            .page-header {
                position: absolute; top: 36px; left: 32px; z-index: 10;
                opacity: 0; transform: translateY(10px);
                transition: opacity 0.7s ease 0.15s, transform 0.7s ease 0.15s;
            }
            body.loaded .page-header { opacity: 1; transform: none; }
            .page-header h1 {
                font-family: 'Playfair Display', serif;
                font-size: 42px; font-weight: 700;
                color: #FCBCD7; letter-spacing: 2px; line-height: 1;
            }
            .page-header .subtitle {
                font-size: 13px; font-weight: 300;
                color: rgba(252,188,215,0.5);
                margin-top: 6px; letter-spacing: 3px; text-transform: uppercase;
            }

            /* ── Back button ── */
            .back-btn {
                position: absolute; top: 32px; right: 36px; z-index: 50;
                width: 44px; height: 44px; border-radius: 50%;
                background: rgba(252,188,215,0.06);
                border: 1px solid rgba(252,188,215,0.15);
                display: flex; align-items: center; justify-content: center;
                cursor: pointer; transition: all 0.3s ease;
                opacity: 0; transform: translateY(10px);
                color: #FCBCD7; text-decoration: none;
            }
            body.loaded .back-btn { opacity: 1; transform: none; transition: opacity 0.7s ease 0.25s, transform 0.7s ease 0.25s, all 0.3s; }
            .back-btn svg { width: 24px; height: 24px; fill: currentColor; }
            .back-btn:hover {
                background: rgba(252,188,215,0.12);
                border-color: rgba(252,188,215,0.35);
                transform: scale(1.08) !important;
                box-shadow: 0 0 16px rgba(191,80,130,0.3);
            }

            /* ── Axis ── */
            .axis-track {
                position: absolute; top: 50%; left: 0; width: 100%;
                height: 0; pointer-events: none; z-index: 3;
            }
            .axis-line {
                position: absolute; top: 0; left: 0; width: 100%; height: 1px;
                background: linear-gradient(
                    90deg,
                    transparent 0%,
                    rgba(252,188,215,0.06) 5%,
                    rgba(252,188,215,0.28) 25%,
                    rgba(252,188,215,0.28) 75%,
                    rgba(252,188,215,0.06) 95%,
                    transparent 100%
                );
                transform: translateY(-50%);
            }

            /* ── Nodes belt ── */
            .nodes-belt {
                position: absolute; top: 50%; left: 0;
                display: flex; align-items: center; flex-wrap: nowrap;
                cursor: grab; will-change: transform; z-index: 4;
            }
            .nodes-belt.dragging { cursor: grabbing; }

            /* ── Node wrapper ── */
            .node-wrapper {
                flex-shrink: 0;
                display: flex; flex-direction: column; align-items: center;
                width: 110px; position: relative;
            }

            /* ── Circle node ── */
            .node {
                position: relative;
                width: 58px; height: 58px; border-radius: 50%;
                background: radial-gradient(circle at 35% 30%,
                    rgba(252,188,215,0.14), rgba(191,80,130,0.06));
                border: 1.5px solid rgba(252,188,215,0.20);
                cursor: pointer;
                display: flex; align-items: center; justify-content: center;
                transition:
                    transform 0.22s cubic-bezier(0.34,1.56,0.64,1),
                    border-color 0.2s ease,
                    box-shadow 0.2s ease,
                    background 0.2s ease;
                -webkit-tap-highlight-color: transparent;
            }
            .node:hover:not(.holding) {
                transform: scale(1.10);
                border-color: rgba(252,188,215,0.46);
                box-shadow: 0 0 18px rgba(252,188,215,0.14);
            }
            /* active = current progress node */
            .node.active {
                width: 76px; height: 76px;
                background: radial-gradient(circle at 35% 30%,
                    rgba(252,188,215,0.28), rgba(191,80,130,0.18));
                border: 2px solid rgba(252,188,215,0.70);
                box-shadow:
                    0 0 24px rgba(252,188,215,0.24),
                    0 0 60px rgba(191,80,130,0.14),
                    inset 0 0 12px rgba(252,188,215,0.06);
            }
            .node.active:hover:not(.holding) { transform: scale(1.08); }
            /* previewed = held/highlighted by user */
            .node.previewed {
                transform: scale(1.16) !important;
                border-color: rgba(229,106,179,0.85) !important;
                background: radial-gradient(circle at 35% 30%,
                    rgba(229,106,179,0.28), rgba(191,80,130,0.20)) !important;
                box-shadow:
                    0 0 28px rgba(229,106,179,0.36),
                    0 0 72px rgba(191,80,130,0.22) !important;
                transition:
                    transform 0.15s cubic-bezier(0.34,1.56,0.64,1),
                    border-color 0.15s ease,
                    box-shadow 0.15s ease,
                    background 0.15s ease !important;
            }

            /* ── Node number ── */
            .node-number {
                font-family: 'Playfair Display', serif;
                font-size: 16px; font-weight: 700;
                color: rgba(252,188,215,0.65);
                pointer-events: none; line-height: 1;
                position: relative; z-index: 1;
            }
            .node.active .node-number { font-size: 20px; color: #FCBCD7; }
            .node.previewed .node-number { color: #FCBCD7; }
            .node.locked {
                opacity: 0.3;
                cursor: not-allowed;
            }
            .node.locked:hover:not(.holding) {
                transform: none;
                border-color: rgba(252,188,215,0.20);
                box-shadow: none;
            }

            /* ── Node label (below) ── */
            .node-label {
                margin-top: 10px;
                font-size: 9px; font-weight: 300;
                color: rgba(252,188,215,0.30);
                letter-spacing: 1.5px; text-transform: uppercase;
                white-space: nowrap; pointer-events: none;
                transition: color 0.2s;
            }
            .node-wrapper.active-node .node-label,
            .node-wrapper.preview-node .node-label {
                color: rgba(252,188,215,0.65);
            }

            /* ── Connector ── */
            .node-connector {
                width: 46px; height: 1px;
                background: rgba(252,188,215,0.09);
                flex-shrink: 0; align-self: center;
                pointer-events: none;
            }

            /* ── Progress bar ── */
            .progress-bar-wrap {
                position: absolute; bottom: 38px;
                left: 32px; right: 36px;
                display: flex; align-items: center; gap: 14px;
                z-index: 10;
                opacity: 0; transform: translateY(10px);
                transition: opacity 0.7s ease 0.45s, transform 0.7s ease 0.45s;
            }
            body.loaded .progress-bar-wrap { opacity: 1; transform: none; }
            .progress-bar-track {
                flex: 1; height: 2px;
                background: rgba(252,188,215,0.07); border-radius: 2px; overflow: hidden;
            }
            .progress-bar-fill {
                height: 100%;
                background: linear-gradient(90deg, #E56AB3, #FCBCD7);
                border-radius: 2px; transition: width 0.5s ease;
            }
            .progress-label {
                font-size: 11px; font-weight: 300;
                color: rgba(252,188,215,0.38);
                letter-spacing: 1.5px; white-space: nowrap;
            }

            /* ── Loading spinner (left panel while fetching) ── */
            @keyframes spin { to { transform: rotate(360deg); } }
            .spinner {
                width: 20px; height: 20px;
                border: 2px solid rgba(252,188,215,0.15);
                border-top-color: #E56AB3;
                border-radius: 50%;
                animation: spin 0.8s linear infinite;
                margin: auto;
            }
        </style>
    </head>
    <body>

        <div class="bg-layer" aria-hidden="true"></div>
        <div class="vignette" aria-hidden="true"></div>

        <div class="layout">

            <!-- ═══════════════════════════════════════
                 LEFT PANEL — 33%  — Info
            ═══════════════════════════════════════ -->
            <aside class="panel-left" id="panelLeft">
                <!-- populated by JS -->
                <div class="left-empty" id="leftEmpty">
                    <div class="left-empty-icon">☁️</div>
                    <div class="left-empty-text">Hover over a level node<br>to preview its content</div>
                </div>
                <div class="left-inner" id="leftInner" style="display:none">
                    <div class="info-eyebrow" id="infoEyebrow">Chapter</div>
                    <div class="info-title"  id="infoTitle"></div>
                    <div class="info-desc"   id="infoDesc"></div>
                    <div class="exercises-label">Exercises</div>
                    <ul class="exercises-list" id="exercisesList"></ul>
                </div>
            </aside>

            <!-- ═══════════════════════════════════════
                 RIGHT PANEL — 66%  — Axis
            ═══════════════════════════════════════ -->
            <main class="panel-right" id="panelRight">

                <div class="page-header">
                    <h1>Grammar</h1>
                    <p class="subtitle">Level progression</p>
                </div>

                <a class="back-btn" href="/welcome#selection" title="Back to Menu"><svg viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg></a>

                <div class="axis-track" id="axisTrack" aria-hidden="true">
                    <div class="axis-line"></div>
                </div>

                <div class="nodes-belt" id="nodesBelt"
                     role="list" aria-label="Grammar exercises"></div>

                <div class="progress-bar-wrap">
                    <span class="progress-label" id="progressLabel">—</span>
                    <div class="progress-bar-track">
                        <div class="progress-bar-fill" id="progressFill" style="width:0%"></div>
                    </div>
                    <span class="progress-label" id="levelLabel">N5</span>
                </div>

            </main>
        </div>

        <script>
        (function () {
            'use strict';

            /* ═══════════════════════════════════════════════════════
               CONSTANTS
            ═══════════════════════════════════════════════════════ */
            const NODE_WRAP_W  = 110;  // .node-wrapper width  (px, matches CSS)
            const CONNECTOR_W  = 46;   // .node-connector width (px, matches CSS)

            /* ═══════════════════════════════════════════════════════
               STATE
            ═══════════════════════════════════════════════════════ */
            let EXERCISES      = [];   // loaded from /api/grammar/exercises
            let CURRENT_EX_ID  = 1;   // user's current exercise id
            let CURRENT_CH_ID  = 1;   // user's current chapter id

            // belt / drag
            let beltX       = 0;
            let isDragging  = false;
            let dragStartX  = 0;
            let dragStartBX = 0;
            let lastPtrX    = 0;
            let lastPtrT    = 0;
            let velocity    = 0;
            let momentumRAF = null;

            // hold / interaction
            let pointerDownTime = 0;
            let previewedNodeEl = null;   // currently .previewed node

            // left panel cache  { chapterId → {chapter, exercises} }
            const panelCache = {};

            /* ═══════════════════════════════════════════════════════
               DOM REFS
            ═══════════════════════════════════════════════════════ */
            const belt        = document.getElementById('nodesBelt');
            const rightPanel  = document.getElementById('panelRight');
            const leftEmpty   = document.getElementById('leftEmpty');
            const leftInner   = document.getElementById('leftInner');
            const infoEyebrow = document.getElementById('infoEyebrow');
            const infoTitle   = document.getElementById('infoTitle');
            const infoDesc    = document.getElementById('infoDesc');
            const exList      = document.getElementById('exercisesList');
            const progFill    = document.getElementById('progressFill');
            const progLabel   = document.getElementById('progressLabel');
            const levelLabel  = document.getElementById('levelLabel');

            /* ═══════════════════════════════════════════════════════
               BELT HELPERS
            ═══════════════════════════════════════════════════════ */
            function copyWidth() {
                return EXERCISES.length * (NODE_WRAP_W + CONNECTOR_W);
            }

            function setBeltX(x, smooth) {
                beltX = x;
                belt.style.transition = smooth
                    ? 'transform 0.5s cubic-bezier(0.25,0.46,0.45,0.94)'
                    : 'none';
                belt.style.transform = `translateX(${x}px) translateY(-50%)`;
            }

            function cyclicCorrect() {
                const cw = copyWidth();
                if (beltX > 0)          setBeltX(beltX - cw,  false);
                else if (beltX < -(cw * 2)) setBeltX(beltX + cw, false);
            }

            function startGlide() {
                cancelAnimationFrame(momentumRAF);
                function step() {
                    velocity *= 0.91;
                    if (Math.abs(velocity) < 0.35) { cyclicCorrect(); return; }
                    setBeltX(beltX + velocity, false);
                    cyclicCorrect();
                    momentumRAF = requestAnimationFrame(step);
                }
                momentumRAF = requestAnimationFrame(step);
            }

            /* ═══════════════════════════════════════════════════════
               SCROLL TO ACTIVE NODE
            ═══════════════════════════════════════════════════════ */
            function scrollToActive() {
                const centreX = rightPanel.offsetWidth / 2;
                const wrappers = belt.querySelectorAll('.node-wrapper');
                let target = null; let count = 0;
                for (const w of wrappers) {
                    if (parseInt(w.dataset.id) === CURRENT_EX_ID) {
                        count++;
                        if (count === 2) { target = w; break; } // middle copy
                    }
                }
                if (!target) target = belt.querySelector('.active-node') || belt.querySelector('.node-wrapper');
                if (!target) return;

                const pRect = rightPanel.getBoundingClientRect();
                const wRect = target.getBoundingClientRect();
                const wCentre = wRect.left - pRect.left + wRect.width / 2;
                setBeltX(beltX + (centreX - wCentre), false);
                cyclicCorrect();
            }

            /* ═══════════════════════════════════════════════════════
               LEFT PANEL RENDERING
            ═══════════════════════════════════════════════════════ */
            function buildFallbackChapter(chapterId) {
                // Build chapter info from the EXERCISES array when the API has no DB chapter
                const chExs = EXERCISES.filter(e => e.chapter_id === chapterId);
                const first = chExs[0] || {};
                return {
                    chapter: {
                        id: chapterId,
                        title: `Chapter ${first.chapter_index || chapterId}`,
                        description: '',
                        level: first.level || 'N5',
                    },
                    exercises: chExs.map(e => ({
                        id: e.id,
                        title: e.title,
                        description: e.description || '',
                        order_index: e.order_index,
                        chapter_index: e.chapter_index || chapterId,
                    }))
                };
            }

            async function showPanel(chapterId, currentExId) {
                // Show spinner while loading
                if (!panelCache[chapterId]) {
                    leftEmpty.style.display = 'none';
                    leftInner.style.display = 'none';
                    leftInner.innerHTML = '<div class="spinner" style="margin-top:40px"></div>';
                    leftInner.style.display = 'flex';
                    leftInner.style.justifyContent = 'center';

                    try {
                        const res = await fetch(`/api/grammar/chapter/${chapterId}`);
                        if (!res.ok) throw new Error('not found');
                        panelCache[chapterId] = await res.json();
                    } catch {
                        // Fallback: build panel data from loaded EXERCISES array
                        panelCache[chapterId] = buildFallbackChapter(chapterId);
                    }
                }

                const data = panelCache[chapterId];
                const ch   = data.chapter;
                const exs  = data.exercises;

                // Rebuild inner HTML properly
                leftInner.innerHTML = '';
                leftInner.style.display = 'flex';
                leftInner.style.justifyContent = '';

                // eyebrow
                const eyebrow = document.createElement('div');
                eyebrow.className = 'info-eyebrow';
                eyebrow.textContent = ch.level ? `Chapter · ${ch.level}` : 'Chapter';
                leftInner.appendChild(eyebrow);

                // title
                const title = document.createElement('div');
                title.className = 'info-title';
                title.textContent = ch.title;
                leftInner.appendChild(title);

                // description
                if (ch.description) {
                    const desc = document.createElement('div');
                    desc.className = 'info-desc';
                    desc.textContent = ch.description;
                    leftInner.appendChild(desc);
                }

                // exercises label
                const exLabel = document.createElement('div');
                exLabel.className = 'exercises-label';
                exLabel.textContent = `Exercises · ${exs.length}`;
                leftInner.appendChild(exLabel);

                // exercises list
                if (exs.length === 0) {
                    const empty = document.createElement('div');
                    empty.className = 'left-empty-text';
                    empty.style.opacity = '0.45';
                    empty.style.marginTop = '12px';
                    empty.textContent = 'No exercises yet for this chapter.';
                    leftInner.appendChild(empty);
                } else {
                    const ul = document.createElement('ul');
                    ul.className = 'exercises-list';
                    exs.forEach((ex, idx) => {
                        // Check if this exercise is locked
                        // Find this exercise in EXERCISES array to get its stars
                        const exData = EXERCISES.find(e => e.id === ex.id);
                        const prevExData = idx > 0 ? EXERCISES.find(e => e.id === exs[idx - 1].id) : null;
                        const isLocked = idx > 0 && prevExData && (prevExData.stars || 0) < 2;

                        const li = document.createElement('li');
                        li.className = 'ex-item' + (ex.id === currentExId ? ' current' : '') + (isLocked ? ' locked' : '');
                        li.setAttribute('role', 'button');
                        li.setAttribute('tabindex', isLocked ? '-1' : '0');
                        
                        // Stars display
                        const stars = exData ? (exData.stars || 0) : 0;
                        let starsHtml = '';
                        if (stars > 0) {
                            starsHtml = '<span class="ex-stars">';
                            for (let s = 1; s <= 3; s++) {
                                starsHtml += s <= stars 
                                    ? '<img src="/icons/foxheadlighton.png" alt="★">' 
                                    : '<img src="/icons/foxheadlightoff.png" alt="☆">';
                            }
                            starsHtml += '</span>';
                        }

                        li.innerHTML = `
                            <span class="ex-num">${idx + 1}</span>
                            <span class="ex-text">
                                <span class="ex-title">${ex.title}</span>
                                ${ex.description ? `<span class="ex-desc">${ex.description}</span>` : ''}
                                ${starsHtml}
                            </span>
                            ${isLocked ? '<span class="ex-lock-icon">🔒</span>' : ''}`;
                        if (!isLocked) {
                            li.addEventListener('click', () => {
                                window.location.href = `/course/grammar/Chapter${ex.chapter_id || 1}/exercise/${ex.id || (idx + 1)}`;
                            });
                            li.addEventListener('keydown', e => {
                                if (e.key === 'Enter' || e.key === ' ')
                                    window.location.href = `/course/grammar/Chapter${ex.chapter_id || 1}/exercise/${ex.id || (idx + 1)}`;
                            });
                        }
                        ul.appendChild(li);
                    });
                    leftInner.appendChild(ul);
                }

                leftEmpty.style.display = 'none';

                // fade in
                leftInner.style.opacity = '0';
                leftInner.style.transform = 'translateY(10px)';
                requestAnimationFrame(() => {
                    leftInner.style.transition = 'opacity 0.35s ease, transform 0.35s ease';
                    leftInner.style.opacity = '1';
                    leftInner.style.transform = 'none';
                });
            }

            /* ═══════════════════════════════════════════════════════
               BUILD BELT FROM EXERCISES ARRAY
            ═══════════════════════════════════════════════════════ */
            function buildBelt() {
                belt.innerHTML = '';
                const repeated = [...EXERCISES, ...EXERCISES, ...EXERCISES];
                repeated.forEach((ex, i) => {
                    const N = EXERCISES.length;
                    const inMiddle = i >= N && i < N * 2;
                    const isActive = ex.id === CURRENT_EX_ID && inMiddle;

                    if (i > 0) {
                        const conn = document.createElement('div');
                        conn.className = 'node-connector';
                        conn.setAttribute('aria-hidden', 'true');
                        belt.appendChild(conn);
                    }

                    const wrapper = document.createElement('div');
                    wrapper.className = 'node-wrapper' + (isActive ? ' active-node' : '');
                    wrapper.dataset.id        = ex.id;
                    wrapper.dataset.chapterId = ex.chapter_id;
                    wrapper.setAttribute('role', 'listitem');

                    // Check if locked
                    const exIdx = EXERCISES.findIndex(e => e.id === ex.id);
                    const isLocked = exIdx > 0 && (EXERCISES[exIdx - 1].stars || 0) < 2;

                    const node = document.createElement('div');
                    node.className = 'node' + (isActive ? ' active' : '') + (isLocked ? ' locked' : '');
                    if (isActive) node.id = 'active-node';
                    node.setAttribute('aria-label', `${ex.title} — ${ex.level}`);
                    node.setAttribute('tabindex', isLocked ? '-1' : '0');
                    node.setAttribute('role', 'button');

                    const num = document.createElement('span');
                    num.className = 'node-number';
                    num.textContent = i % EXERCISES.length + 1; // 1-based visual number
                    node.appendChild(num);

                    const label = document.createElement('div');
                    label.className = 'node-label';
                    label.setAttribute('aria-hidden', 'true');
                    label.textContent = ex.title.length > 12
                        ? ex.title.slice(0, 11) + '…'
                        : ex.title;

                    wrapper.appendChild(node);
                    wrapper.appendChild(label);

                    attachNodeEvents(node, ex);
                    belt.appendChild(wrapper);
                });
            }

            /* ═══════════════════════════════════════════════════════
               NODE  EVENTS  (hover = preview panel, click = navigate)
            ═══════════════════════════════════════════════════════ */
            function clearPreview() {
                if (previewedNodeEl) {
                    previewedNodeEl.classList.remove('previewed');
                    const pw = previewedNodeEl.closest('.node-wrapper');
                    if (pw) pw.classList.remove('preview-node');
                    previewedNodeEl = null;
                }
            }

            function setPreview(nodeEl, ex) {
                if (previewedNodeEl === nodeEl) return; // already previewing this node
                clearPreview();
                previewedNodeEl = nodeEl;
                nodeEl.classList.add('previewed');
                const pw = nodeEl.closest('.node-wrapper');
                if (pw) pw.classList.add('preview-node');
                // update panel with the chapter this exercise belongs to
                showPanel(ex.chapter_id, ex.id);
            }

            function attachNodeEvents(nodeEl, ex) {
                let localDownTime = 0;

                // Check if this exercise is locked
                function isExLocked() {
                    const exIdx = EXERCISES.findIndex(e => e.id === ex.id);
                    if (exIdx <= 0) return false; // First exercise or not found
                    const prevEx = EXERCISES[exIdx - 1];
                    return (prevEx.stars || 0) < 2;
                }

                // ── HOVER: update left panel on mouseenter ──
                nodeEl.addEventListener('mouseenter', () => {
                    setPreview(nodeEl, ex);
                });

                // ── CLICK: navigate to the exercise ──
                function onDown(e) {
                    e.stopPropagation(); // don't start belt-drag from node
                    localDownTime = performance.now();
                    pointerDownTime = localDownTime;
                }

                function onUp() {
                    if (isDragging) return; // drag happened — ignore
                    const elapsed = performance.now() - localDownTime;
                    if (elapsed < 400) {
                        if (isExLocked()) return; // Don't navigate to locked exercise
                        window.location.href = `/course/grammar/Chapter${ex.chapter_id || 1}/exercise/${ex.id || 1}`;
                    }
                }

                nodeEl.addEventListener('mousedown',  onDown);
                nodeEl.addEventListener('mouseup',    onUp);

                nodeEl.addEventListener('touchstart', e => {
                    e.stopPropagation();
                    localDownTime = performance.now();
                    setPreview(nodeEl, ex);
                }, { passive: true });

                nodeEl.addEventListener('touchend', () => {
                    if (isDragging) return;
                    const elapsed = performance.now() - localDownTime;
                    if (elapsed < 400) {
                        if (isExLocked()) return;
                        window.location.href = `/course/grammar/Chapter${ex.chapter_id || 1}/exercise/${ex.id || 1}`;
                    }
                });

                nodeEl.addEventListener('keydown', e => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        if (isExLocked()) return;
                        window.location.href = `/course/grammar/Chapter${ex.chapter_id || 1}/exercise/${ex.id || 1}`;
                    }
                });
            }

            /* ═══════════════════════════════════════════════════════
               DRAG / SCROLL
            ═══════════════════════════════════════════════════════ */
            function setupDrag() {
                let startBX = 0;

                belt.addEventListener('mousedown', e => {
                    cancelAnimationFrame(momentumRAF);
                    isDragging  = false;
                    dragStartX  = e.clientX;
                    startBX     = beltX;
                    lastPtrX    = e.clientX;
                    lastPtrT    = performance.now();
                    velocity    = 0;
                    belt.style.transition = 'none';
                    belt.classList.add('dragging');

                    function onMove(ev) {
                        const dx = ev.clientX - dragStartX;
                        if (!isDragging && Math.abs(dx) > 5) isDragging = true;
                        if (!isDragging) return;
                        const now = performance.now();
                        velocity = (ev.clientX - lastPtrX) / Math.max(now - lastPtrT, 1) * 16;
                        lastPtrX = ev.clientX; lastPtrT = now;
                        setBeltX(startBX + dx, false);
                        cyclicCorrect();
                    }

                    function onUp() {
                        window.removeEventListener('mousemove', onMove);
                        window.removeEventListener('mouseup', onUp);
                        belt.classList.remove('dragging');
                        startGlide();
                        setTimeout(() => { isDragging = false; }, 60);
                    }

                    window.addEventListener('mousemove', onMove);
                    window.addEventListener('mouseup', onUp);
                });

                // Touch
                let tStartX = 0, tStartBX = 0;
                belt.addEventListener('touchstart', e => {
                    cancelAnimationFrame(momentumRAF);
                    tStartX  = e.touches[0].clientX;
                    tStartBX = beltX;
                    lastPtrX = tStartX; lastPtrT = performance.now();
                    velocity = 0; isDragging = false;
                    belt.style.transition = 'none';
                }, { passive: true });

                belt.addEventListener('touchmove', e => {
                    const dx = e.touches[0].clientX - tStartX;
                    if (!isDragging && Math.abs(dx) > 5) isDragging = true;
                    if (!isDragging) return;
                    const now = performance.now();
                    velocity = (e.touches[0].clientX - lastPtrX) / Math.max(now - lastPtrT, 1) * 16;
                    lastPtrX = e.touches[0].clientX; lastPtrT = now;
                    setBeltX(tStartBX + dx, false);
                    cyclicCorrect();
                }, { passive: true });

                belt.addEventListener('touchend', () => {
                    startGlide();
                    setTimeout(() => { isDragging = false; }, 60);
                });

                // Wheel
                rightPanel.addEventListener('wheel', e => {
                    e.preventDefault();
                    cancelAnimationFrame(momentumRAF);
                    const delta = e.deltaX !== 0 ? e.deltaX : e.deltaY;
                    setBeltX(beltX - delta * 0.9, false);
                    cyclicCorrect();
                }, { passive: false });
            }

            /* ═══════════════════════════════════════════════════════
               PROGRESS BAR
            ═══════════════════════════════════════════════════════ */
            function updateProgress() {
                const total = EXERCISES.length;
                if (!total) return;
                const idx = EXERCISES.findIndex(e => e.id === CURRENT_EX_ID);
                const done = Math.max(0, idx);
                progFill.style.width  = Math.round((done / total) * 100) + '%';
                progLabel.textContent = `${done} / ${total}`;
                const ex = EXERCISES.find(e => e.id === CURRENT_EX_ID);
                levelLabel.textContent = ex ? ex.level : 'N5';
            }

            /* ═══════════════════════════════════════════════════════
               INIT  — fetch exercises + user status, then build UI
            ═══════════════════════════════════════════════════════ */
            async function init() {
                try {
                    // Fetch in parallel
                    const [exRes, userRes] = await Promise.all([
                        fetch('/api/grammar/exercises'),
                        fetch('/api/grammar/user-status'),
                    ]);

                    EXERCISES = await exRes.json();
                    const userStatus = await userRes.json();
                    CURRENT_EX_ID = userStatus.status_exercise || 1;
                    CURRENT_CH_ID = userStatus.status_chapter  || 1;

                    // Fallback: if no DB exercises yet, use a placeholder list
                    if (!EXERCISES || EXERCISES.length === 0) {
                        EXERCISES = [
                            {id:1,chapter_id:1,title:'Particle Wa',level:'N5',description:'Learn about how japanese highlights subjects', chapter_index: 1, order_index: 1},
                            {id:2,chapter_id:1,title:'Desu verb',level:'N5',description:'', chapter_index: 1, order_index: 2},
                            {id:3,chapter_id:1,title:'Hour in japanese',level:'N5',description:'', chapter_index: 1, order_index: 3},
                            {id:4,chapter_id:1,title:'Prices in japanese',level:'N5',description:'', chapter_index: 1, order_index: 4},
                            {id:5,chapter_id:1,title:'evaluation capters 1-4',level:'N5',description:'', chapter_index: 1, order_index: 5},
                            {id:6,chapter_id:1,title:'Describing clothes',level:'N5',description:'', chapter_index: 1, order_index: 6},
                            {id:7,chapter_id:1,title:'Basic adjectives List',level:'N5',description:'', chapter_index: 1, order_index: 7},
                            {id:8,chapter_id:1,title:'Basic adjective list (part2)',level:'N5',description:'', chapter_index: 1, order_index: 8},
                            {id:9,chapter_id:1,title:'Basic japanese verbs',level:'N5',description:'', chapter_index: 1, order_index: 9},
                            {id:10,chapter_id:1,title:'Particle Mo',level:'N5',description:'', chapter_index: 1, order_index: 10},
                            {id:11,chapter_id:1,title:'"And" / "Or"',level:'N5',description:'', chapter_index: 1, order_index: 11},
                            {id:12,chapter_id:1,title:'Describe distance',level:'N5',description:'Use of kono, ano etc.', chapter_index: 1, order_index: 12},
                            {id:13,chapter_id:1,title:'Verb Conjugation',level:'N5',description:'', chapter_index: 1, order_index: 13},
                            {id:14,chapter_id:1,title:'Present Tense',level:'N5',description:'', chapter_index: 1, order_index: 14},
                            {id:15,chapter_id:1,title:'Verb Particles, Word Order',level:'N5',description:'', chapter_index: 1, order_index: 15},
                            {id:16,chapter_id:1,title:'Genneral Examination 1-14',level:'N5',description:'', chapter_index: 1, order_index: 16},
                            {id:17,chapter_id:1,title:'Past Tense of Desu',level:'N5',description:'', chapter_index: 1, order_index: 17},
                            {id:18,chapter_id:1,title:'Past tense of verbs',level:'N5',description:'', chapter_index: 1, order_index: 18},
                            {id:19,chapter_id:1,title:'Past tense of verbs (part 2)',level:'N5',description:'', chapter_index: 1, order_index: 19},
                            {id:20,chapter_id:1,title:'Practice verbs',level:'N5',description:'', chapter_index: 1, order_index: 20},
                            {id:21,chapter_id:1,title:'Final examination chapter 1',level:'N5',description:'', chapter_index: 1, order_index: 21},
                        ];
                    }

                    buildBelt();
                    setupDrag();
                    updateProgress();

                    // Scroll to active then show body
                    requestAnimationFrame(() => {
                        requestAnimationFrame(() => {
                            scrollToActive();
                            document.body.classList.add('loaded');
                            // Load left panel with current chapter
                            showPanel(CURRENT_CH_ID, CURRENT_EX_ID);
                        });
                    });

                } catch (err) {
                    console.error('Grammar init error:', err);
                    document.body.classList.add('loaded');
                }
            }

            // Clear preview on background click
            document.addEventListener('mousedown', e => {
                if (!e.target.closest('.node') && !e.target.closest('.panel-left')) {
                    clearPreview();
                }
            });

            init();

        })();
        </script>
    </body>
    </html>
    """
@router.get("/course/vocabulary", response_class=HTMLResponse)
async def course_vocabulary():
    return r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vocabulary — Tenjin-Ya</title>
        <meta name="description" content="Japanese vocabulary level progression — explore chapters and exercises.">
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            /* ── Reset ── */
            *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

            body {
                font-family: 'Inter', sans-serif;
                height: 100vh;
                overflow: hidden;
                background: #0d0608;
                color: #FCBCD7;
                opacity: 0;
                transition: opacity 0.9s ease;
                user-select: none;
            }
            body.loaded { opacity: 1; }

            /* ── Background ── */
            .bg-layer {
                position: fixed; inset: 0;
                background: url('/textures/tablepage.png') no-repeat center center / cover;
                opacity: 0.18; z-index: 0; pointer-events: none;
            }
            .vignette {
                position: fixed; inset: 0;
                background: radial-gradient(ellipse at center, transparent 30%, #0d0608 90%);
                z-index: 1; pointer-events: none;
            }

            /* ── Split layout ── */
            .layout {
                position: relative; z-index: 2;
                display: flex; width: 100vw; height: 100vh;
            }

            /* ═══════════════════════════════════════════
               LEFT PANEL — 33%  — Info panel
            ═══════════════════════════════════════════ */
            .panel-left {
                width: 33.333%; height: 100%; flex-shrink: 0;
                display: flex; flex-direction: column;
                padding: 48px 32px 48px 36px;
                border-right: 1px solid rgba(252,188,215,0.06);
                position: relative;
                overflow: hidden;
            }

            /* decorative top fade */
            .panel-left::before {
                content: ''; position: absolute;
                top: 0; left: 0; right: 0; height: 120px;
                background: linear-gradient(to bottom, rgba(13,6,8,0.8), transparent);
                pointer-events: none; z-index: 1;
            }

            .left-inner {
                display: flex; flex-direction: column; height: 100%;
                opacity: 0;
                transform: translateY(12px);
                transition: opacity 0.45s ease, transform 0.45s ease;
            }
            .left-inner.visible {
                opacity: 1; transform: none;
            }

            .info-eyebrow {
                font-family: 'Inter', sans-serif;
                font-size: 10px; font-weight: 500;
                letter-spacing: 3px; text-transform: uppercase;
                color: #E56AB3; margin-bottom: 12px;
            }
            .info-title {
                font-family: 'Playfair Display', serif;
                font-size: 28px; font-weight: 700;
                color: #FCBCD7; line-height: 1.25;
                margin-bottom: 14px;
            }
            .info-desc {
                font-family: 'Inter', sans-serif;
                font-size: 13px; font-weight: 300;
                color: rgba(252,188,215,0.58); line-height: 1.7;
                margin-bottom: 28px;
            }

            .exercises-label {
                font-family: 'Inter', sans-serif;
                font-size: 10px; font-weight: 500;
                letter-spacing: 2.5px; text-transform: uppercase;
                color: rgba(252,188,215,0.35); margin-bottom: 12px;
            }
            .exercises-list {
                list-style: none;
                display: flex; flex-direction: column; gap: 8px;
                overflow-y: auto; flex: 1;
                padding-right: 4px;
                scrollbar-width: thin;
                scrollbar-color: rgba(229,106,179,0.25) transparent;
            }
            .exercises-list::-webkit-scrollbar { width: 3px; }
            .exercises-list::-webkit-scrollbar-thumb { background: rgba(229,106,179,0.25); border-radius: 2px; }

            .ex-item {
                display: flex; align-items: flex-start; gap: 12px;
                padding: 10px 14px;
                border-radius: 10px;
                background: rgba(252,188,215,0.04);
                border: 1px solid rgba(252,188,215,0.07);
                transition: background 0.2s ease, border-color 0.2s ease;
                cursor: pointer;
            }
            .ex-item:hover {
                background: rgba(252,188,215,0.09);
                border-color: rgba(252,188,215,0.18);
            }
            .ex-item.current {
                background: rgba(229,106,179,0.12);
                border-color: rgba(229,106,179,0.35);
            }
            .ex-num {
                font-family: 'Playfair Display', serif;
                font-size: 14px; font-weight: 700;
                color: #E56AB3; flex-shrink: 0;
                min-width: 22px;
            }
            .ex-text { display: flex; flex-direction: column; gap: 2px; }
            .ex-title {
                font-family: 'Inter', sans-serif;
                font-size: 13px; font-weight: 500;
                color: #FCBCD7;
            }
            .ex-desc {
                font-family: 'Inter', sans-serif;
                font-size: 11px; font-weight: 300;
                color: rgba(252,188,215,0.45); line-height: 1.5;
            }
            .ex-item.locked {
                opacity: 0.35;
                cursor: not-allowed;
                position: relative;
            }
            .ex-item.locked:hover {
                background: rgba(252,188,215,0.04);
                border-color: rgba(252,188,215,0.07);
            }
            .ex-lock-icon {
                font-size: 14px;
                flex-shrink: 0;
                margin-left: auto;
                opacity: 0.6;
            }
            .ex-stars {
                display: flex; gap: 2px; margin-top: 2px;
            }
            .ex-stars img {
                width: 14px; height: 14px;
            }

            /* empty state */
            .left-empty {
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                height: 100%; gap: 14px; opacity: 0.35;
                text-align: center;
            }
            .left-empty-icon { font-size: 36px; }
            .left-empty-text {
                font-family: 'Inter', sans-serif;
                font-size: 13px; font-weight: 300;
                color: rgba(252,188,215,0.6); line-height: 1.6;
            }

            /* ═══════════════════════════════════════════
               RIGHT PANEL — 66%  — Axis + nodes
            ═══════════════════════════════════════════ */
            .panel-right {
                width: 66.666%; height: 100%; flex-shrink: 0;
                position: relative; display: flex;
                align-items: center; overflow: hidden;
            }

            /* ── Header ── */
            .page-header {
                position: absolute; top: 36px; left: 32px; z-index: 10;
                opacity: 0; transform: translateY(10px);
                transition: opacity 0.7s ease 0.15s, transform 0.7s ease 0.15s;
            }
            body.loaded .page-header { opacity: 1; transform: none; }
            .page-header h1 {
                font-family: 'Playfair Display', serif;
                font-size: 42px; font-weight: 700;
                color: #FCBCD7; letter-spacing: 2px; line-height: 1;
            }
            .page-header .subtitle {
                font-size: 13px; font-weight: 300;
                color: rgba(252,188,215,0.5);
                margin-top: 6px; letter-spacing: 3px; text-transform: uppercase;
            }

            /* ── Back button ── */
            .back-btn {
                position: absolute; top: 32px; right: 36px; z-index: 50;
                width: 44px; height: 44px; border-radius: 50%;
                background: rgba(252,188,215,0.06);
                border: 1px solid rgba(252,188,215,0.15);
                display: flex; align-items: center; justify-content: center;
                cursor: pointer; transition: all 0.3s ease;
                opacity: 0; transform: translateY(10px);
                color: #FCBCD7; text-decoration: none;
            }
            body.loaded .back-btn { opacity: 1; transform: none; transition: opacity 0.7s ease 0.25s, transform 0.7s ease 0.25s, all 0.3s; }
            .back-btn svg { width: 24px; height: 24px; fill: currentColor; }
            .back-btn:hover {
                background: rgba(252,188,215,0.12);
                border-color: rgba(252,188,215,0.35);
                transform: scale(1.08) !important;
                box-shadow: 0 0 16px rgba(191,80,130,0.3);
            }

            /* ── Axis ── */
            .axis-track {
                position: absolute; top: 50%; left: 0; width: 100%;
                height: 0; pointer-events: none; z-index: 3;
            }
            .axis-line {
                position: absolute; top: 0; left: 0; width: 100%; height: 1px;
                background: linear-gradient(
                    90deg,
                    transparent 0%,
                    rgba(252,188,215,0.06) 5%,
                    rgba(252,188,215,0.28) 25%,
                    rgba(252,188,215,0.28) 75%,
                    rgba(252,188,215,0.06) 95%,
                    transparent 100%
                );
                transform: translateY(-50%);
            }

            /* ── Nodes belt ── */
            .nodes-belt {
                position: absolute; top: 50%; left: 0;
                display: flex; align-items: center; flex-wrap: nowrap;
                cursor: grab; will-change: transform; z-index: 4;
            }
            .nodes-belt.dragging { cursor: grabbing; }

            /* ── Node wrapper ── */
            .node-wrapper {
                flex-shrink: 0;
                display: flex; flex-direction: column; align-items: center;
                width: 110px; position: relative;
            }

            /* ── Circle node ── */
            .node {
                position: relative;
                width: 58px; height: 58px; border-radius: 50%;
                background: radial-gradient(circle at 35% 30%,
                    rgba(252,188,215,0.14), rgba(191,80,130,0.06));
                border: 1.5px solid rgba(252,188,215,0.20);
                cursor: pointer;
                display: flex; align-items: center; justify-content: center;
                transition:
                    transform 0.22s cubic-bezier(0.34,1.56,0.64,1),
                    border-color 0.2s ease,
                    box-shadow 0.2s ease,
                    background 0.2s ease;
                -webkit-tap-highlight-color: transparent;
            }
            .node:hover:not(.holding) {
                transform: scale(1.10);
                border-color: rgba(252,188,215,0.46);
                box-shadow: 0 0 18px rgba(252,188,215,0.14);
            }
            /* active = current progress node */
            .node.active {
                width: 76px; height: 76px;
                background: radial-gradient(circle at 35% 30%,
                    rgba(252,188,215,0.28), rgba(191,80,130,0.18));
                border: 2px solid rgba(252,188,215,0.70);
                box-shadow:
                    0 0 24px rgba(252,188,215,0.24),
                    0 0 60px rgba(191,80,130,0.14),
                    inset 0 0 12px rgba(252,188,215,0.06);
            }
            .node.active:hover:not(.holding) { transform: scale(1.08); }
            /* previewed = held/highlighted by user */
            .node.previewed {
                transform: scale(1.16) !important;
                border-color: rgba(229,106,179,0.85) !important;
                background: radial-gradient(circle at 35% 30%,
                    rgba(229,106,179,0.28), rgba(191,80,130,0.20)) !important;
                box-shadow:
                    0 0 28px rgba(229,106,179,0.36),
                    0 0 72px rgba(191,80,130,0.22) !important;
                transition:
                    transform 0.15s cubic-bezier(0.34,1.56,0.64,1),
                    border-color 0.15s ease,
                    box-shadow 0.15s ease,
                    background 0.15s ease !important;
            }

            /* ── Node number ── */
            .node-number {
                font-family: 'Playfair Display', serif;
                font-size: 16px; font-weight: 700;
                color: rgba(252,188,215,0.65);
                pointer-events: none; line-height: 1;
                position: relative; z-index: 1;
            }
            .node.active .node-number { font-size: 20px; color: #FCBCD7; }
            .node.previewed .node-number { color: #FCBCD7; }
            .node.locked {
                opacity: 0.3;
                cursor: not-allowed;
            }
            .node.locked:hover:not(.holding) {
                transform: none;
                border-color: rgba(252,188,215,0.20);
                box-shadow: none;
            }

            /* ── Node label (below) ── */
            .node-label {
                margin-top: 10px;
                font-size: 9px; font-weight: 300;
                color: rgba(252,188,215,0.30);
                letter-spacing: 1.5px; text-transform: uppercase;
                white-space: nowrap; pointer-events: none;
                transition: color 0.2s;
            }
            .node-wrapper.active-node .node-label,
            .node-wrapper.preview-node .node-label {
                color: rgba(252,188,215,0.65);
            }

            /* ── Connector ── */
            .node-connector {
                width: 46px; height: 1px;
                background: rgba(252,188,215,0.09);
                flex-shrink: 0; align-self: center;
                pointer-events: none;
            }

            /* ── Progress bar ── */
            .progress-bar-wrap {
                position: absolute; bottom: 38px;
                left: 32px; right: 36px;
                display: flex; align-items: center; gap: 14px;
                z-index: 10;
                opacity: 0; transform: translateY(10px);
                transition: opacity 0.7s ease 0.45s, transform 0.7s ease 0.45s;
            }
            body.loaded .progress-bar-wrap { opacity: 1; transform: none; }
            .progress-bar-track {
                flex: 1; height: 2px;
                background: rgba(252,188,215,0.07); border-radius: 2px; overflow: hidden;
            }
            .progress-bar-fill {
                height: 100%;
                background: linear-gradient(90deg, #E56AB3, #FCBCD7);
                border-radius: 2px; transition: width 0.5s ease;
            }
            .progress-label {
                font-size: 11px; font-weight: 300;
                color: rgba(252,188,215,0.38);
                letter-spacing: 1.5px; white-space: nowrap;
            }

            /* ── Loading spinner (left panel while fetching) ── */
            @keyframes spin { to { transform: rotate(360deg); } }
            .spinner {
                width: 20px; height: 20px;
                border: 2px solid rgba(252,188,215,0.15);
                border-top-color: #E56AB3;
                border-radius: 50%;
                animation: spin 0.8s linear infinite;
                margin: auto;
            }
        </style>
    </head>
    <body>

        <div class="bg-layer" aria-hidden="true"></div>
        <div class="vignette" aria-hidden="true"></div>

        <div class="layout">

            <!-- ═══════════════════════════════════════
                 LEFT PANEL — 33%  — Info
            ═══════════════════════════════════════ -->
            <aside class="panel-left" id="panelLeft">
                <!-- populated by JS -->
                <div class="left-empty" id="leftEmpty">
                    <div class="left-empty-icon">☁️</div>
                    <div class="left-empty-text">Hover over a level node<br>to preview its content</div>
                </div>
                <div class="left-inner" id="leftInner" style="display:none">
                    <div class="info-eyebrow" id="infoEyebrow">Chapter</div>
                    <div class="info-title"  id="infoTitle"></div>
                    <div class="info-desc"   id="infoDesc"></div>
                    <div class="exercises-label">Exercises</div>
                    <ul class="exercises-list" id="exercisesList"></ul>
                </div>
            </aside>

            <!-- ═══════════════════════════════════════
                 RIGHT PANEL — 66%  — Axis
            ═══════════════════════════════════════ -->
            <main class="panel-right" id="panelRight">

                <div class="page-header">
                    <h1>Vocabulary</h1>
                    <p class="subtitle">Level progression</p>
                </div>

                <a class="back-btn" href="/welcome#selection" title="Back to Menu"><svg viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg></a>

                <div class="axis-track" id="axisTrack" aria-hidden="true">
                    <div class="axis-line"></div>
                </div>

                <div class="nodes-belt" id="nodesBelt"
                     role="list" aria-label="Vocabulary exercises"></div>

                <div class="progress-bar-wrap">
                    <span class="progress-label" id="progressLabel">—</span>
                    <div class="progress-bar-track">
                        <div class="progress-bar-fill" id="progressFill" style="width:0%"></div>
                    </div>
                    <span class="progress-label" id="levelLabel">N5</span>
                </div>

            </main>
        </div>

        <script>
        (function () {
            'use strict';

            /* ═══════════════════════════════════════════════════════
               CONSTANTS
            ═══════════════════════════════════════════════════════ */
            const NODE_WRAP_W  = 110;  // .node-wrapper width  (px, matches CSS)
            const CONNECTOR_W  = 46;   // .node-connector width (px, matches CSS)

            /* ═══════════════════════════════════════════════════════
               STATE
            ═══════════════════════════════════════════════════════ */
            let EXERCISES      = [];   // loaded from /api/vocabulary/exercises
            let CURRENT_EX_ID  = 1;   // user's current exercise id
            let CURRENT_CH_ID  = 1;   // user's current chapter id

            // belt / drag
            let beltX       = 0;
            let isDragging  = false;
            let dragStartX  = 0;
            let dragStartBX = 0;
            let lastPtrX    = 0;
            let lastPtrT    = 0;
            let velocity    = 0;
            let momentumRAF = null;

            // hold / interaction
            let pointerDownTime = 0;
            let previewedNodeEl = null;   // currently .previewed node

            // left panel cache  { chapterId → {chapter, exercises} }
            const panelCache = {};

            /* ═══════════════════════════════════════════════════════
               DOM REFS
            ═══════════════════════════════════════════════════════ */
            const belt        = document.getElementById('nodesBelt');
            const rightPanel  = document.getElementById('panelRight');
            const leftEmpty   = document.getElementById('leftEmpty');
            const leftInner   = document.getElementById('leftInner');
            const infoEyebrow = document.getElementById('infoEyebrow');
            const infoTitle   = document.getElementById('infoTitle');
            const infoDesc    = document.getElementById('infoDesc');
            const exList      = document.getElementById('exercisesList');
            const progFill    = document.getElementById('progressFill');
            const progLabel   = document.getElementById('progressLabel');
            const levelLabel  = document.getElementById('levelLabel');

            /* ═══════════════════════════════════════════════════════
               BELT HELPERS
            ═══════════════════════════════════════════════════════ */
            function copyWidth() {
                return EXERCISES.length * (NODE_WRAP_W + CONNECTOR_W);
            }

            function setBeltX(x, smooth) {
                beltX = x;
                belt.style.transition = smooth
                    ? 'transform 0.5s cubic-bezier(0.25,0.46,0.45,0.94)'
                    : 'none';
                belt.style.transform = `translateX(${x}px) translateY(-50%)`;
            }

            function cyclicCorrect() {
                const cw = copyWidth();
                if (beltX > 0)          setBeltX(beltX - cw,  false);
                else if (beltX < -(cw * 2)) setBeltX(beltX + cw, false);
            }

            function startGlide() {
                cancelAnimationFrame(momentumRAF);
                function step() {
                    velocity *= 0.91;
                    if (Math.abs(velocity) < 0.35) { cyclicCorrect(); return; }
                    setBeltX(beltX + velocity, false);
                    cyclicCorrect();
                    momentumRAF = requestAnimationFrame(step);
                }
                momentumRAF = requestAnimationFrame(step);
            }

            /* ═══════════════════════════════════════════════════════
               SCROLL TO ACTIVE NODE
            ═══════════════════════════════════════════════════════ */
            function scrollToActive() {
                const centreX = rightPanel.offsetWidth / 2;
                const wrappers = belt.querySelectorAll('.node-wrapper');
                let target = null; let count = 0;
                for (const w of wrappers) {
                    if (parseInt(w.dataset.id) === CURRENT_EX_ID) {
                        count++;
                        if (count === 2) { target = w; break; } // middle copy
                    }
                }
                if (!target) target = belt.querySelector('.active-node') || belt.querySelector('.node-wrapper');
                if (!target) return;

                const pRect = rightPanel.getBoundingClientRect();
                const wRect = target.getBoundingClientRect();
                const wCentre = wRect.left - pRect.left + wRect.width / 2;
                setBeltX(beltX + (centreX - wCentre), false);
                cyclicCorrect();
            }

            /* ═══════════════════════════════════════════════════════
               LEFT PANEL RENDERING
            ═══════════════════════════════════════════════════════ */
            function buildFallbackChapter(chapterId) {
                // Build chapter info from the EXERCISES array when the API has no DB chapter
                const chExs = EXERCISES.filter(e => e.chapter_id === chapterId);
                const first = chExs[0] || {};
                return {
                    chapter: {
                        id: chapterId,
                        title: `Chapter ${first.chapter_index || chapterId}`,
                        description: '',
                        level: first.level || 'N5',
                    },
                    exercises: chExs.map(e => ({
                        id: e.id,
                        title: e.title,
                        description: e.description || '',
                        order_index: e.order_index,
                        chapter_index: e.chapter_index || chapterId,
                    }))
                };
            }

            async function showPanel(chapterId, currentExId) {
                // Show spinner while loading
                if (!panelCache[chapterId]) {
                    leftEmpty.style.display = 'none';
                    leftInner.style.display = 'none';
                    leftInner.innerHTML = '<div class="spinner" style="margin-top:40px"></div>';
                    leftInner.style.display = 'flex';
                    leftInner.style.justifyContent = 'center';

                    try {
                        const res = await fetch(`/api/vocabulary/chapter/${chapterId}`);
                        if (!res.ok) throw new Error('not found');
                        panelCache[chapterId] = await res.json();
                    } catch {
                        // Fallback: build panel data from loaded EXERCISES array
                        panelCache[chapterId] = buildFallbackChapter(chapterId);
                    }
                }

                const data = panelCache[chapterId];
                const ch   = data.chapter;
                const exs  = data.exercises;

                // Rebuild inner HTML properly
                leftInner.innerHTML = '';
                leftInner.style.display = 'flex';
                leftInner.style.justifyContent = '';

                // eyebrow
                const eyebrow = document.createElement('div');
                eyebrow.className = 'info-eyebrow';
                eyebrow.textContent = ch.level ? `Chapter · ${ch.level}` : 'Chapter';
                leftInner.appendChild(eyebrow);

                // title
                const title = document.createElement('div');
                title.className = 'info-title';
                title.textContent = ch.title;
                leftInner.appendChild(title);

                // description
                if (ch.description) {
                    const desc = document.createElement('div');
                    desc.className = 'info-desc';
                    desc.textContent = ch.description;
                    leftInner.appendChild(desc);
                }

                // exercises label
                const exLabel = document.createElement('div');
                exLabel.className = 'exercises-label';
                exLabel.textContent = `Exercises · ${exs.length}`;
                leftInner.appendChild(exLabel);

                // exercises list
                if (exs.length === 0) {
                    const empty = document.createElement('div');
                    empty.className = 'left-empty-text';
                    empty.style.opacity = '0.45';
                    empty.style.marginTop = '12px';
                    empty.textContent = 'No exercises yet for this chapter.';
                    leftInner.appendChild(empty);
                } else {
                    const ul = document.createElement('ul');
                    ul.className = 'exercises-list';
                    exs.forEach((ex, idx) => {
                        // Check if this exercise is locked
                        const exData = EXERCISES.find(e => e.id === ex.id);
                        const prevExData = idx > 0 ? EXERCISES.find(e => e.id === exs[idx - 1].id) : null;
                        const isLocked = idx > 0 && prevExData && (prevExData.stars || 0) < 2;

                        const li = document.createElement('li');
                        li.className = 'ex-item' + (ex.id === currentExId ? ' current' : '') + (isLocked ? ' locked' : '');
                        li.setAttribute('role', 'button');
                        li.setAttribute('tabindex', isLocked ? '-1' : '0');
                        
                        // Stars display
                        const stars = exData ? (exData.stars || 0) : 0;
                        let starsHtml = '';
                        if (stars > 0) {
                            starsHtml = '<span class="ex-stars">';
                            for (let s = 1; s <= 3; s++) {
                                starsHtml += s <= stars 
                                    ? '<img src="/icons/foxheadlighton.png" alt="★">' 
                                    : '<img src="/icons/foxheadlightoff.png" alt="☆">';
                            }
                            starsHtml += '</span>';
                        }

                        li.innerHTML = `
                            <span class="ex-num">${idx + 1}</span>
                            <span class="ex-text">
                                <span class="ex-title">${ex.title}</span>
                                ${ex.description ? `<span class="ex-desc">${ex.description}</span>` : ''}
                                ${starsHtml}
                            </span>
                            ${isLocked ? '<span class="ex-lock-icon">🔒</span>' : ''}`;
                        if (!isLocked) {
                            li.addEventListener('click', () => {
                                window.location.href = `/course/vocabulary/Chapter${ex.chapter_id || chapterId}/exercise/${ex.id}`;
                            });
                            li.addEventListener('keydown', e => {
                                if (e.key === 'Enter' || e.key === ' ')
                                    window.location.href = `/course/vocabulary/Chapter${ex.chapter_id || chapterId}/exercise/${ex.id}`;
                            });
                        }
                        ul.appendChild(li);
                    });
                    leftInner.appendChild(ul);
                }

                leftEmpty.style.display = 'none';

                // fade in
                leftInner.style.opacity = '0';
                leftInner.style.transform = 'translateY(10px)';
                requestAnimationFrame(() => {
                    leftInner.style.transition = 'opacity 0.35s ease, transform 0.35s ease';
                    leftInner.style.opacity = '1';
                    leftInner.style.transform = 'none';
                });
            }

            /* ═══════════════════════════════════════════════════════
               BUILD BELT FROM EXERCISES ARRAY
            ═══════════════════════════════════════════════════════ */
            function buildBelt() {
                belt.innerHTML = '';
                const repeated = [...EXERCISES, ...EXERCISES, ...EXERCISES];
                repeated.forEach((ex, i) => {
                    const N = EXERCISES.length;
                    const inMiddle = i >= N && i < N * 2;
                    const isActive = ex.id === CURRENT_EX_ID && inMiddle;

                    if (i > 0) {
                        const conn = document.createElement('div');
                        conn.className = 'node-connector';
                        conn.setAttribute('aria-hidden', 'true');
                        belt.appendChild(conn);
                    }

                    const wrapper = document.createElement('div');
                    wrapper.className = 'node-wrapper' + (isActive ? ' active-node' : '');
                    wrapper.dataset.id        = ex.id;
                    wrapper.dataset.chapterId = ex.chapter_id;
                    wrapper.setAttribute('role', 'listitem');

                    // Check if locked
                    const exIdx = EXERCISES.findIndex(e => e.id === ex.id);
                    const isLocked = exIdx > 0 && (EXERCISES[exIdx - 1].stars || 0) < 2;

                    const node = document.createElement('div');
                    node.className = 'node' + (isActive ? ' active' : '') + (isLocked ? ' locked' : '');
                    if (isActive) node.id = 'active-node';
                    node.setAttribute('aria-label', `${ex.title} — ${ex.level}`);
                    node.setAttribute('tabindex', isLocked ? '-1' : '0');
                    node.setAttribute('role', 'button');

                    const num = document.createElement('span');
                    num.className = 'node-number';
                    num.textContent = i % EXERCISES.length + 1; // 1-based visual number
                    node.appendChild(num);

                    const label = document.createElement('div');
                    label.className = 'node-label';
                    label.setAttribute('aria-hidden', 'true');
                    label.textContent = ex.title.length > 12
                        ? ex.title.slice(0, 11) + '…'
                        : ex.title;

                    wrapper.appendChild(node);
                    wrapper.appendChild(label);

                    attachNodeEvents(node, ex);
                    belt.appendChild(wrapper);
                });
            }

            /* ═══════════════════════════════════════════════════════
               NODE  EVENTS  (hover = preview panel, click = navigate)
            ═══════════════════════════════════════════════════════ */
            function clearPreview() {
                if (previewedNodeEl) {
                    previewedNodeEl.classList.remove('previewed');
                    const pw = previewedNodeEl.closest('.node-wrapper');
                    if (pw) pw.classList.remove('preview-node');
                    previewedNodeEl = null;
                }
            }

            function setPreview(nodeEl, ex) {
                if (previewedNodeEl === nodeEl) return; // already previewing this node
                clearPreview();
                previewedNodeEl = nodeEl;
                nodeEl.classList.add('previewed');
                const pw = nodeEl.closest('.node-wrapper');
                if (pw) pw.classList.add('preview-node');
                // update panel with the chapter this exercise belongs to
                showPanel(ex.chapter_id, ex.id);
            }

            function attachNodeEvents(nodeEl, ex) {
                let localDownTime = 0;

                // Check if this exercise is locked
                function isExLocked() {
                    const exIdx = EXERCISES.findIndex(e => e.id === ex.id);
                    if (exIdx <= 0) return false; // First exercise or not found
                    const prevEx = EXERCISES[exIdx - 1];
                    return (prevEx.stars || 0) < 2;
                }

                // ── HOVER: update left panel on mouseenter ──
                nodeEl.addEventListener('mouseenter', () => {
                    setPreview(nodeEl, ex);
                });

                // ── CLICK: navigate to the exercise ──
                function onDown(e) {
                    e.stopPropagation(); // don't start belt-drag from node
                    localDownTime = performance.now();
                    pointerDownTime = localDownTime;
                }

                function onUp() {
                    if (isDragging) return; // drag happened — ignore
                    const elapsed = performance.now() - localDownTime;
                    if (elapsed < 400) {
                        if (isExLocked()) return; // Don't navigate to locked exercise
                        window.location.href = `/course/vocabulary/Chapter${ex.chapter_id || 1}/exercise/${ex.id || 1}`;
                    }
                }

                nodeEl.addEventListener('mousedown',  onDown);
                nodeEl.addEventListener('mouseup',    onUp);

                nodeEl.addEventListener('touchstart', e => {
                    e.stopPropagation();
                    localDownTime = performance.now();
                    setPreview(nodeEl, ex);
                }, { passive: true });

                nodeEl.addEventListener('touchend', () => {
                    if (isDragging) return;
                    const elapsed = performance.now() - localDownTime;
                    if (elapsed < 400) {
                        if (isExLocked()) return;
                        window.location.href = `/course/vocabulary/Chapter${ex.chapter_id || 1}/exercise/${ex.id || 1}`;
                    }
                });

                nodeEl.addEventListener('keydown', e => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        if (isExLocked()) return;
                        window.location.href = `/course/vocabulary/Chapter${ex.chapter_id || 1}/exercise/${ex.id || 1}`;
                    }
                });
            }

            /* ═══════════════════════════════════════════════════════
               DRAG / SCROLL
            ═══════════════════════════════════════════════════════ */
            function setupDrag() {
                let startBX = 0;

                belt.addEventListener('mousedown', e => {
                    cancelAnimationFrame(momentumRAF);
                    isDragging  = false;
                    dragStartX  = e.clientX;
                    startBX     = beltX;
                    lastPtrX    = e.clientX;
                    lastPtrT    = performance.now();
                    velocity    = 0;
                    belt.style.transition = 'none';
                    belt.classList.add('dragging');

                    function onMove(ev) {
                        const dx = ev.clientX - dragStartX;
                        if (!isDragging && Math.abs(dx) > 5) isDragging = true;
                        if (!isDragging) return;
                        const now = performance.now();
                        velocity = (ev.clientX - lastPtrX) / Math.max(now - lastPtrT, 1) * 16;
                        lastPtrX = ev.clientX; lastPtrT = now;
                        setBeltX(startBX + dx, false);
                        cyclicCorrect();
                    }

                    function onUp() {
                        window.removeEventListener('mousemove', onMove);
                        window.removeEventListener('mouseup', onUp);
                        belt.classList.remove('dragging');
                        startGlide();
                        setTimeout(() => { isDragging = false; }, 60);
                    }

                    window.addEventListener('mousemove', onMove);
                    window.addEventListener('mouseup', onUp);
                });

                // Touch
                let tStartX = 0, tStartBX = 0;
                belt.addEventListener('touchstart', e => {
                    cancelAnimationFrame(momentumRAF);
                    tStartX  = e.touches[0].clientX;
                    tStartBX = beltX;
                    lastPtrX = tStartX; lastPtrT = performance.now();
                    velocity = 0; isDragging = false;
                    belt.style.transition = 'none';
                }, { passive: true });

                belt.addEventListener('touchmove', e => {
                    const dx = e.touches[0].clientX - tStartX;
                    if (!isDragging && Math.abs(dx) > 5) isDragging = true;
                    if (!isDragging) return;
                    const now = performance.now();
                    velocity = (e.touches[0].clientX - lastPtrX) / Math.max(now - lastPtrT, 1) * 16;
                    lastPtrX = e.touches[0].clientX; lastPtrT = now;
                    setBeltX(tStartBX + dx, false);
                    cyclicCorrect();
                }, { passive: true });

                belt.addEventListener('touchend', () => {
                    startGlide();
                    setTimeout(() => { isDragging = false; }, 60);
                });

                // Wheel
                rightPanel.addEventListener('wheel', e => {
                    e.preventDefault();
                    cancelAnimationFrame(momentumRAF);
                    const delta = e.deltaX !== 0 ? e.deltaX : e.deltaY;
                    setBeltX(beltX - delta * 0.9, false);
                    cyclicCorrect();
                }, { passive: false });
            }

            /* ═══════════════════════════════════════════════════════
               PROGRESS BAR
            ═══════════════════════════════════════════════════════ */
            function updateProgress() {
                const total = EXERCISES.length;
                if (!total) return;
                const idx = EXERCISES.findIndex(e => e.id === CURRENT_EX_ID);
                const done = Math.max(0, idx);
                progFill.style.width  = Math.round((done / total) * 100) + '%';
                progLabel.textContent = `${done} / ${total}`;
                const ex = EXERCISES.find(e => e.id === CURRENT_EX_ID);
                levelLabel.textContent = ex ? ex.level : 'N5';
            }

            /* ═══════════════════════════════════════════════════════
               INIT  — fetch exercises + user status, then build UI
            ═══════════════════════════════════════════════════════ */
            async function init() {
                try {
                    // Fetch in parallel
                    const [exRes, userRes] = await Promise.all([
                        fetch('/api/vocabulary/exercises'),
                        fetch('/api/vocabulary/user-status'),
                    ]);

                    EXERCISES = await exRes.json();
                    const userStatus = await userRes.json();
                    CURRENT_EX_ID = userStatus.status_exercise || 1;
                    CURRENT_CH_ID = userStatus.status_chapter  || 1;

                    // Fallback: if no DB exercises yet, use a placeholder list
                    if (!EXERCISES || EXERCISES.length === 0) {
                        EXERCISES = [
                            {id:1,chapter_id:1,title:'Learn about writing systems',level:'N5',description:'Hiragana, Katakana, and Kanji tables.', chapter_index: 1, order_index: 1},
                            {id:2,chapter_id:1,title:'Practice Hiragana',level:'N5',description:'Draw and recognize Hiragana characters.', chapter_index: 1, order_index: 2},
                            {id:3,chapter_id:1,title:'Numbers 1-100',level:'N5',description:'Cardinal numbers in Japanese.', chapter_index: 1, order_index: 3},
                            {id:4,chapter_id:2,title:'Family Members',level:'N5',description:'Terms for relatives.', chapter_index: 2, order_index: 1},
                            {id:5,chapter_id:2,title:'Colors & Shapes',level:'N5',description:'Visual descriptors.', chapter_index: 2, order_index: 2},
                            {id:6,chapter_id:2,title:'Time & Days',level:'N5',description:'Temporal vocabulary.', chapter_index: 2, order_index: 3},
                            {id:7,chapter_id:3,title:'Food & Drinks',level:'N4',description:'Restaurant and kitchen terms.', chapter_index: 3, order_index: 1},
                            {id:8,chapter_id:3,title:'Body Parts',level:'N4',description:'Anatomy and health.', chapter_index: 3, order_index: 2},
                            {id:9,chapter_id:4,title:'Emotions',level:'N4',description:'Feelings and states of mind.', chapter_index: 4, order_index: 1},
                            {id:10,chapter_id:5,title:'Travel & Directions',level:'N3',description:'Map and station phrases.', chapter_index: 5, order_index: 1},
                        ];
                    }

                    buildBelt();
                    setupDrag();
                    updateProgress();

                    // Scroll to active then show body
                    // Use the chapter_id from the first vocabulary exercise in EXERCISES
                    // (do NOT use user status_chapter which is a grammar chapter ID)
                    const initialChapterId = EXERCISES.length > 0 ? EXERCISES[0].chapter_id : null;
                    const initialExId      = EXERCISES.length > 0 ? EXERCISES[0].id : null;

                    requestAnimationFrame(() => {
                        requestAnimationFrame(() => {
                            scrollToActive();
                            document.body.classList.add('loaded');
                            // Load left panel with first vocabulary chapter
                            if (initialChapterId) showPanel(initialChapterId, initialExId);
                        });
                    });

                } catch (err) {
                    console.error('Vocabulary init error:', err);
                    document.body.classList.add('loaded');
                }
            }

            // Clear preview on background click
            document.addEventListener('mousedown', e => {
                if (!e.target.closest('.node') && !e.target.closest('.panel-left')) {
                    clearPreview();
                }
            });

            init();

        })();
        </script>
    </body>
    </html>
    """




@router.get("/course/vocabulary/Chapter{chapter_index}/exercise{exercise_index}", response_class=HTMLResponse)
async def vocabulary_exercise_page(chapter_index: int, exercise_index: int):
    """Exercise page for vocabulary. The first exercise of the first vocab chapter = writing system picker."""
    is_writing_systems = (chapter_index == 1 and exercise_index == 1)

    if is_writing_systems:
        return r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Writing Systems — Tenjin-Ya</title>
        <meta name="description" content="Choose a writing system to learn: Hiragana, Katakana, or Kanji.">
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

            body {
                font-family: 'Inter', sans-serif;
                height: 100vh;
                overflow: hidden;
                background: #0d0608;
                color: #FCBCD7;
                opacity: 0;
                transition: opacity 0.9s ease;
                user-select: none;
            }
            body.loaded { opacity: 1; }

            /* Background */
            .bg-img {
                position: fixed; inset: 0;
                background: url('/textures/island1 (1).png') no-repeat center center / cover;
                opacity: 0.22; z-index: 0; pointer-events: none;
            }
            .vignette {
                position: fixed; inset: 0;
                background: radial-gradient(ellipse at center, transparent 20%, #0d0608 88%);
                z-index: 1; pointer-events: none;
            }

            /* Back button */
            .back-btn {
                position: fixed; top: 32px; left: 36px; z-index: 50;
                width: 44px; height: 44px; border-radius: 50%;
                background: rgba(252,188,215,0.06);
                border: 1px solid rgba(252,188,215,0.15);
                display: flex; align-items: center; justify-content: center;
                cursor: pointer; transition: all 0.3s ease;
                color: #FCBCD7; text-decoration: none;
            }
            .back-btn svg { width: 24px; height: 24px; fill: currentColor; }
            .back-btn:hover {
                background: rgba(252,188,215,0.12);
                border-color: rgba(252,188,215,0.35);
                box-shadow: 0 0 16px rgba(191,80,130,0.3);
                transform: scale(1.08);
            }

            /* Centre content */
            .centre {
                position: relative; z-index: 2;
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                height: 100vh;
                text-align: center;
                gap: 0;
            }

            .eyebrow {
                font-size: 11px; font-weight: 500;
                letter-spacing: 3px; text-transform: uppercase;
                color: #E56AB3; margin-bottom: 18px;
                opacity: 0; transform: translateY(10px);
                animation: fadeUp 0.6s ease 0.3s forwards;
            }

            h1 {
                font-family: 'Playfair Display', serif;
                font-size: clamp(36px, 5vw, 60px);
                font-weight: 700;
                color: #FCBCD7;
                line-height: 1.15;
                margin-bottom: 14px;
                opacity: 0; transform: translateY(12px);
                animation: fadeUp 0.6s ease 0.5s forwards;
            }

            .subtitle {
                font-size: 16px; font-weight: 300;
                color: rgba(252,188,215,0.6);
                letter-spacing: 0.5px;
                margin-bottom: 64px;
                opacity: 0; transform: translateY(12px);
                animation: fadeUp 0.6s ease 0.65s forwards;
            }

            /* Cards row */
            .cards {
                display: flex; gap: 28px;
                opacity: 0; transform: translateY(16px);
                animation: fadeUp 0.6s ease 0.85s forwards;
            }

            .card {
                position: relative;
                width: 180px; height: 220px;
                border-radius: 20px;
                background: rgba(252,188,215,0.04);
                border: 1px solid rgba(252,188,215,0.12);
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                gap: 16px;
                cursor: pointer;
                text-decoration: none;
                transition: background 0.3s ease, border-color 0.3s ease,
                            box-shadow 0.3s ease, transform 0.3s ease;
                overflow: hidden;
            }
            .card::before {
                content: '';
                position: absolute; inset: 0;
                background: radial-gradient(circle at 50% 50%, rgba(229,106,179,0.12) 0%, transparent 70%);
                opacity: 0; transition: opacity 0.4s ease;
            }
            .card:hover { border-color: rgba(252,188,215,0.35); transform: translateY(-6px); }
            .card:hover::before { opacity: 1; }
            .card:hover { box-shadow: 0 12px 40px rgba(191,80,130,0.25); }

            .card-jp {
                font-family: 'Playfair Display', serif;
                font-size: 52px;
                color: #FCBCD7;
                line-height: 1;
                transition: transform 0.3s ease;
            }
            .card:hover .card-jp { transform: scale(1.1); }

            .card-label {
                font-family: 'Inter', sans-serif;
                font-size: 13px; font-weight: 500;
                letter-spacing: 2px; text-transform: uppercase;
                color: rgba(252,188,215,0.65);
            }

            @keyframes fadeUp {
                to { opacity: 1; transform: none; }
            }

            /* Page transition overlay */
            .page-fade {
                position: fixed; inset: 0;
                background: #0d0608;
                z-index: 200;
                opacity: 0; pointer-events: none;
                transition: opacity 0.6s ease;
            }
            .page-fade.active { opacity: 1; pointer-events: all; }
        </style>
    </head>
    <body>
        <div class="bg-img"></div>
        <div class="vignette"></div>
        <div class="page-fade" id="pageFade"></div>

        <!-- Back to Vocabulary -->
        <a class="back-btn" href="/course/vocabulary" title="Back to Vocabulary">
            <svg viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
        </a>

        <div class="centre">
            <div class="eyebrow">Vocabulary · Chapter 1 · Exercise 1</div>
            <h1>What do you want to learn?</h1>
            <p class="subtitle">Choose a writing system to begin your journey.</p>

            <div class="cards">
                <a class="card" href="/hiragana-table" id="cardHiragana">
                    <div class="card-jp">あ</div>
                    <div class="card-label">Hiragana</div>
                </a>
                <a class="card" href="/katakana-table" id="cardKatakana">
                    <div class="card-jp">ア</div>
                    <div class="card-label">Katakana</div>
                </a>
                <a class="card" href="/kanji-table" id="cardKanji">
                    <div class="card-jp">字</div>
                    <div class="card-label">Kanji</div>
                </a>
            </div>
        </div>

        <script>
            window.addEventListener('load', () => document.body.classList.add('loaded'));

            // Smooth transition out on card click
            document.querySelectorAll('.card').forEach(card => {
                card.addEventListener('click', function(e) {
                    e.preventDefault();
                    const href = this.getAttribute('href');
                    const fade = document.getElementById('pageFade');
                    fade.classList.add('active');
                    setTimeout(() => { window.location.href = href; }, 650);
                });
            });

            // Smooth transition out on back button
            document.querySelector('.back-btn').addEventListener('click', function(e) {
                e.preventDefault();
                const href = this.getAttribute('href');
                const fade = document.getElementById('pageFade');
                fade.classList.add('active');
                setTimeout(() => { window.location.href = href; }, 650);
            });
        </script>
    </body>
    </html>
    """
    # Generic placeholder for other exercises
    is_practice_hiragana = (chapter_index == 1 and exercise_index == 2)

    if is_practice_hiragana:
        return r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Practice Hiragana — Tenjin-Ya</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

            body {
                font-family: 'Inter', sans-serif;
                height: 100vh;
                background: #0d0608;
                color: #FCBCD7;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                overflow: hidden;
            }

            .bg-img {
                position: fixed; inset: 0;
                background: url('/textures/tablepage.png') no-repeat center center / cover;
                opacity: 0.15; z-index: 0; pointer-events: none;
            }

            .container {
                position: relative; z-index: 10;
                display: flex; flex-direction: column; align-items: center;
                gap: 32px; width: 100%; max-width: 800px;
            }

            h1 {
                font-family: 'Playfair Display', serif;
                font-size: 42px; color: #FCBCD7;
            }

            .board-container {
                background: rgba(252,188,215,0.05);
                border: 1px solid rgba(252,188,215,0.15);
                border-radius: 24px;
                padding: 40px;
                box-shadow: 0 0 40px rgba(191,80,130,0.15);
                display: flex; flex-direction: column; align-items: center; gap: 24px;
            }

            canvas {
                background: #fff;
                border-radius: 12px;
                cursor: crosshair;
                box-shadow: inset 0 0 20px rgba(0,0,0,0.1);
            }

            .controls {
                display: flex; gap: 16px; width: 100%;
            }

            button {
                flex: 1; padding: 14px; border-radius: 12px;
                border: 1px solid rgba(252,188,215,0.25);
                background: rgba(252,188,215,0.06);
                color: #FCBCD7; font-size: 14px; font-weight: 600;
                cursor: pointer; transition: all 0.3s ease;
                text-transform: uppercase; letter-spacing: 1px;
            }
            button:hover {
                background: rgba(252,188,215,0.15);
                border-color: rgba(252,188,215,0.45);
                transform: translateY(-2px);
            }
            button.primary {
                background: linear-gradient(135deg, #E56AB3 0%, #BF5082 100%);
                color: #fff; border: none;
            }
            button.primary:hover {
                box-shadow: 0 0 20px rgba(191,80,130,0.4);
            }

            .result-panel {
                margin-top: 20px; font-size: 18px; color: #E56AB3;
                font-weight: 500; min-height: 27px;
            }

            .back-link {
                position: fixed; top: 32px; left: 36px;
                color: #FCBCD7; text-decoration: none;
                font-size: 14px; display: flex; align-items: center; gap: 8px;
                opacity: 0.7; transition: opacity 0.3s ease;
            }
            .back-link:hover { opacity: 1; }
        </style>
    </head>
    <body>
        <div class="bg-img"></div>
        <a href="/course/vocabulary" class="back-link">← Back to Vocabulary</a>

        <div class="container">
            <h1>Practice Hiragana</h1>
            <p style="opacity: 0.6">Draw the character on the canvas below</p>
            
            <div class="board-container">
                <canvas id="paintCanvas" width="400" height="400"></canvas>
                <div class="controls">
                    <button onclick="clearCanvas()">Clear Board</button>
                    <button class="primary" onclick="recognize()">Recognize Drawing</button>
                </div>
            </div>
            
            <div class="result-panel" id="resultText"></div>
        </div>

        <script>
            const canvas = document.getElementById('paintCanvas');
            const ctx = canvas.getContext('2d');
            let drawing = false;

            // Simple drawing logic
            canvas.addEventListener('mousedown', (e) => { 
                drawing = true; 
                ctx.beginPath();
                ctx.moveTo(e.offsetX, e.offsetY);
            });
            window.addEventListener('mouseup', () => { drawing = false; });
            canvas.addEventListener('mousemove', (e) => {
                if (!drawing) return;
                ctx.lineWidth = 14;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                ctx.strokeStyle = '#2d2d2d';
                ctx.lineTo(e.offsetX, e.offsetY);
                ctx.stroke();
            });

            // Touch support
            canvas.addEventListener('touchstart', (e) => {
                const touch = e.touches[0];
                const rect = canvas.getBoundingClientRect();
                drawing = true;
                ctx.beginPath();
                ctx.moveTo(touch.clientX - rect.left, touch.clientY - rect.top);
                e.preventDefault();
            }, { passive: false });
            canvas.addEventListener('touchmove', (e) => {
                if (!drawing) return;
                const touch = e.touches[0];
                const rect = canvas.getBoundingClientRect();
                ctx.lineWidth = 14;
                ctx.lineCap = 'round';
                ctx.strokeStyle = '#2d2d2d';
                ctx.lineTo(touch.clientX - rect.left, touch.clientY - rect.top);
                ctx.stroke();
                e.preventDefault();
            }, { passive: false });

            function clearCanvas() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                document.getElementById('resultText').innerText = "";
            }

            async function recognize() {
                const resText = document.getElementById('resultText');
                resText.innerText = "Analyzing Strokes...";
                
                // For now, this is a placeholder. 
                // In the future, you'll send the image to your AI endpoint!
                setTimeout(() => {
                    resText.innerText = "AI Recognition Placeholder: Looks like 'あ'";
                }, 1000);
            }
        </script>
    </body>
    </html>
    """

    return HTMLResponse(f"""
    <!DOCTYPE html><html lang="en"><head>
    <meta charset="UTF-8"><title>Vocabulary Chapter {chapter_index} - Exercise {exercise_index}</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>body{{font-family:'Playfair Display',serif;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;margin:0;background:#0d0608;color:#FCBCD7;gap:24px;opacity:0;transition:opacity 0.8s ease;}}body.loaded{{opacity:1;}}a{{color:#E56AB3;text-decoration:none;font-size:14px;letter-spacing:1px;}}</style>
    </head><body>
    <h1 style="font-size:48px">Exercise {exercise_index}</h1>
    <p style="font-size:18px;opacity:.6">Vocabulary exercise content coming soon.</p>
    <a href="/course/vocabulary">← Back to Vocabulary</a>
    <script>window.addEventListener('load',()=>document.body.classList.add('loaded'));</script>
    </body></html>
    """)




@router.get("/settings", response_class=HTMLResponse)
async def settings_page():
    return """
    <html>
    <head>
        <title>Settings</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Playfair Display', serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: url('/textures/templeprofile.png') no-repeat center center; background-size: cover; color: #FCBCD7; opacity: 0; transition: opacity 1s ease; }
            body.loaded { opacity: 1; }
            h1 { font-size: 48px; }
        </style>
    </head>
    <body>
        <h1>Settings</h1>
        <script>window.addEventListener('load', () => document.body.classList.add('loaded'));</script>
    </body>
    </html>
    """


# ─────────────────────────────────────────────────────────
#  VOCABULARY API ENDPOINTS
# ─────────────────────────────────────────────────────────

@router.get("/api/vocabulary/user-status")
async def vocabulary_user_status(request: Request):
    """Return the current user's vocabulary status."""
    email = request.cookies.get("user_email")
    if not email:
        return JSONResponse({"status_chapter": 1, "status_exercise": 1})
    db = SessionLocal()
    try:
        from features.user.models import User, StatusLearning
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return JSONResponse({"status_chapter": 1, "status_exercise": 1})

        status = db.query(StatusLearning).filter(StatusLearning.user_id == user.id).first()
        if not status:
            return JSONResponse({"status_chapter": 1, "status_exercise": 1})

        return JSONResponse({
            "status_chapter":  status.status_chapter_vocabulary,
            "status_exercise": status.status_exercise_vocabulary,
        })
    finally:
        db.close()

@router.get("/api/vocabulary/chapter/{chapter_id}")
async def vocabulary_chapter(chapter_id: int):
    """Return vocabulary chapter info + its exercises (filtered to vocabulary category only)."""
    db = SessionLocal()
    try:
        chapter = (
            db.query(Chapter)
            .filter(Chapter.id == chapter_id, Chapter.category == "vocabulary")
            .first()
        )
        if not chapter:
            raise HTTPException(status_code=404, detail="Vocabulary chapter not found")
        # Get proficiency level
        prof = db.query(Proficiency).filter(Proficiency.id == chapter.proficiency_id).first()
        level = prof.level if prof else "N5"
        exercises = (
            db.query(Exercise)
            .filter(Exercise.chapter_id == chapter_id)
            .order_by(Exercise.order_index)
            .all()
        )
        return JSONResponse({
            "chapter": {
                "id":          chapter.id,
                "title":       chapter.title,
                "description": chapter.description or "",
                "level":       level,
            },
            "exercises": [
                {
                    "id":          e.id,
                    "chapter_id":  e.chapter_id,
                    "title":       e.title,
                    "description": e.description or "",
                    "order_index": e.order_index,
                }
                for e in exercises
            ],
        })
    finally:
        db.close()

@router.get("/api/vocabulary/exercise/{exercise_id}")
async def vocabulary_exercise_chapter(exercise_id: int):
    return await grammar_exercise_chapter(exercise_id)

@router.get("/api/vocabulary/exercises")
async def vocabulary_all_exercises(request: Request):
    email = request.cookies.get("user_email")
    db = SessionLocal()
    try:
        from features.user.models import User, UserExerciseScore
        user = None
        if email:
            user = db.query(User).filter(User.email == email).first()
            
        exercises = (
            db.query(Exercise, Chapter, Proficiency)
            .join(Chapter, Exercise.chapter_id == Chapter.id)
            .join(Proficiency, Chapter.proficiency_id == Proficiency.id)
            .filter(Chapter.category == "vocabulary")
            .order_by(Chapter.order_index, Exercise.order_index)
            .all()
        )
        
        # Get stars for the current user
        scores_map = {}
        if user:
            scores = db.query(UserExerciseScore).filter(UserExerciseScore.user_id == user.id).all()
            scores_map = {s.exercise_id: s.stars for s in scores}
            
        return JSONResponse([
            {
                "id":          ex.id,
                "chapter_id":  ex.chapter_id,
                "title":       ex.title,
                "description": ex.description or "",
                "level":       prof.level if prof else "N5",
                "order_index": ex.order_index,
                "chapter_index": ch.order_index,
                "stars":       scores_map.get(ex.id, 0)
            }
            for ex, ch, prof in exercises
        ])
    finally:
        db.close()


# ─────────────────────────────────────────────────────────
#  CULTURE API ENDPOINTS
# ─────────────────────────────────────────────────────────

@router.get("/api/culture/user-status")
async def culture_user_status(request: Request):
    """Return the current user's culture status."""
    email = request.cookies.get("user_email")
    if not email:
        return JSONResponse({"status_chapter": 1})
    db = SessionLocal()
    try:
        from features.user.models import User, StatusLearning
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return JSONResponse({"status_chapter": 1})

        status = db.query(StatusLearning).filter(StatusLearning.user_id == user.id).first()
        if not status:
            return JSONResponse({"status_chapter": 1})

        return JSONResponse({"status_chapter":  status.status_chapter_culture or 1})
    finally:
        db.close()


@router.get("/api/culture/chapters")
async def culture_chapters_api():
    """Return all culture chapters."""
    db = SessionLocal()
    try:
        chapters = (
            db.query(Chapter)
            .filter(Chapter.category == "culture")
            .order_by(Chapter.order_index)
            .all()
        )
        return JSONResponse([
            {
                "id":          ch.id,
                "title":       ch.title,
                "description": ch.description or "",
                "order_index": ch.order_index,
                "image_url":   ch.image_url,
                "pdf_url":     ch.pdf_url,
            }
            for ch in chapters
        ])
    finally:
        db.close()


@router.post("/api/culture/complete/{chapter_id}")
async def culture_complete_chapter(chapter_id: int, request: Request):
    """Mark a culture chapter as completed and unlock the next one."""
    email = request.cookies.get("user_email")
    if not email:
        raise HTTPException(status_code=401, detail="Not logged in")
    
    db = SessionLocal()
    try:
        from features.user.models import User, StatusLearning
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        status = db.query(StatusLearning).filter(StatusLearning.user_id == user.id).first()
        if not status:
            raise HTTPException(status_code=404, detail="Status not found")
        
        chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        
        # If user just completed the current chapter, increment the status
        if status.status_chapter_culture <= chapter.order_index:
            status.status_chapter_culture = chapter.order_index + 1
            db.commit()
            
        return JSONResponse({"success": True, "new_status": status.status_chapter_culture})
    finally:
        db.close()


# ─────────────────────────────────────────────────────────
#  CULTURE PAGE
# ─────────────────────────────────────────────────────────

@router.get("/course/culture", response_class=HTMLResponse)
async def course_culture():
    return r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Japanese Culture — Tenjin-Ya</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            /* ── Reset & Foundations ── */
            *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: 'Inter', sans-serif;
                background: #0a0a0b;
                color: #FCBCD7;
                height: 100vh;
                overflow: hidden;
                display: flex;
            }

            /* ── Layout ── */
            .main-area {
                width: 70%;
                height: 100%;
                position: relative;
                display: flex;
                flex-direction: column;
                padding: 60px 80px;
                border-right: 1px solid rgba(252, 188, 215, 0.08);
                overflow: hidden;
                background: linear-gradient(135deg, #0a0a0b 0%, #1a0f14 100%);
            }
            .image-panel {
                width: 30%;
                height: 100%;
                background: #050505;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                overflow: hidden;
            }
            
            /* Background decoration */
            .main-area::before {
                content: "";
                position: absolute;
                top: -100px; right: -100px;
                width: 400px; height: 400px;
                background: radial-gradient(circle, rgba(229, 106, 179, 0.05) 0%, transparent 70%);
                z-index: 0;
            }

            /* ── Header ── */
            .header {
                margin-bottom: 50px;
                position: relative;
                z-index: 10;
            }
            .header h1 {
                font-family: 'Playfair Display', serif;
                font-size: 48px;
                letter-spacing: -1px;
                color: #FCBCD7;
                margin-bottom: 8px;
            }
            .header p {
                font-size: 14px;
                color: rgba(252, 188, 215, 0.5);
                text-transform: uppercase;
                letter-spacing: 3px;
            }

            /* ── Scrollable List ── */
            .chapter-list {
                flex: 1;
                overflow-y: auto;
                padding-right: 20px;
                scrollbar-width: thin;
                scrollbar-color: rgba(229, 106, 179, 0.3) transparent;
                position: relative;
            }
            .chapter-list::-webkit-scrollbar { width: 4px; }
            .chapter-list::-webkit-scrollbar-thumb { background: rgba(229, 106, 179, 0.3); border-radius: 10px; }

            /* Vertical Axis Line */
            .chapter-list::before {
                content: "";
                position: absolute;
                top: 40px; left: 30px;
                width: 1px; height: calc(100% - 80px);
                background: linear-gradient(to bottom, 
                    transparent 0%, 
                    rgba(229, 106, 179, 0.3) 10%, 
                    rgba(229, 106, 179, 0.3) 90%, 
                    transparent 100%);
                z-index: 1;
                pointer-events: none;
            }

            .chapter-row {
                display: flex;
                align-items: center;
                margin-bottom: 24px;
                position: relative;
                z-index: 2;
            }

            /* Dot Styles */
            .dot-area {
                width: 60px;
                flex-shrink: 0;
                display: flex;
                justify-content: center;
                z-index: 10;
            }
            .dot {
                width: 12px; height: 12px;
                border-radius: 50%;
                background: #1a1a1d;
                border: 2px solid rgba(229, 106, 179, 0.4);
                transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
                box-shadow: 0 0 0 rgba(229, 106, 179, 0);
            }
            .dot.completed {
                background: #E56AB3;
                border-color: #E56AB3;
                box-shadow: 0 0 15px rgba(229, 106, 179, 0.6);
            }
            .dot.active {
                background: #FCBCD7;
                border-color: #FCBCD7;
                transform: scale(1.4);
                box-shadow: 0 0 20px rgba(252, 188, 215, 0.4);
            }

            /* Card Styles */
            .chapter-card {
                flex: 1;
                background: rgba(252, 188, 215, 0.03);
                border: 1px solid rgba(252, 188, 215, 0.08);
                border-radius: 16px;
                padding: 24px 32px;
                cursor: pointer;
                transition: all 0.3s ease;
                position: relative;
                user-select: none;
                backdrop-filter: blur(4px);
            }
            .chapter-card:hover {
                background: rgba(252, 188, 215, 0.06);
                border-color: rgba(252, 188, 215, 0.2);
                transform: translateX(8px);
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .chapter-card.locked {
                opacity: 0.3;
                cursor: not-allowed;
                pointer-events: none;
            }
            .chapter-card h3 {
                font-family: 'Playfair Display', serif;
                font-size: 22px;
                margin-bottom: 6px;
                color: #FCBCD7;
                transition: color 0.3s;
            }
            .chapter-card p {
                font-size: 13px;
                color: rgba(252, 188, 215, 0.5);
                font-weight: 300;
                line-height: 1.5;
            }
            .chapter-card.completed h3 {
                color: #E56AB3;
            }

            /* Badge */
            .status-badge {
                position: absolute;
                top: 24px; right: 32px;
                font-size: 10px;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                color: #E56AB3;
                background: rgba(229, 106, 179, 0.1);
                padding: 4px 10px;
                border-radius: 20px;
                opacity: 0;
                transition: opacity 0.3s;
                font-weight: 600;
            }
            .chapter-card.completed .status-badge {
                opacity: 1;
            }

            /* ── Image Panel ── */
            #repImage {
                width: 100%; height: 100%;
                object-fit: cover;
                opacity: 0;
                transition: opacity 1.2s ease, transform 2s cubic-bezier(0.16, 1, 0.3, 1);
                transform: scale(1.15);
            }
            #repImage.visible {
                opacity: 0.6;
                transform: scale(1);
            }
            .panel-overlay {
                position: absolute;
                inset: 0;
                background: radial-gradient(circle at center, transparent 0%, #050505 90%);
                z-index: 2;
                pointer-events: none;
            }
            .image-placeholder {
                position: absolute;
                z-index: 3;
                color: rgba(252, 188, 215, 0.2);
                font-family: 'Playfair Display', serif;
                font-size: 20px;
                text-align: center;
                letter-spacing: 2px;
                max-width: 200px;
            }

            /* ── Controls ── */
            .back-btn {
                position: absolute;
                top: 40px; right: 40px;
                width: 54px; height: 54px;
                border-radius: 50%;
                background: rgba(252, 188, 215, 0.05);
                border: 1px solid rgba(252, 188, 215, 0.15);
                display: flex; align-items: center; justify-content: center;
                cursor: pointer; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                z-index: 100;
                color: #FCBCD7;
                text-decoration: none;
            }
            .back-btn:hover {
                background: rgba(252, 188, 215, 0.1);
                border-color: rgba(252, 188, 215, 0.4);
                transform: scale(1.1) rotate(-8deg);
                box-shadow: 0 0 20px rgba(229, 106, 179, 0.2);
            }
            
            .hint-toast {
                position: fixed;
                bottom: 30px; left: calc(35% - 100px);
                background: rgba(10, 10, 11, 0.8);
                backdrop-filter: blur(8px);
                color: rgba(252, 188, 215, 0.6);
                padding: 12px 24px;
                border-radius: 30px;
                font-size: 12px;
                border: 1px solid rgba(252, 188, 215, 0.1);
                z-index: 1000;
                pointer-events: none;
                animation: fadeIn 1s ease-out;
            }
            @keyframes fadeIn { from { opacity: 0; transform: translate(-50%, 20px); } to { opacity: 1; transform: translate(-50%, 0); } }

            /* ── Reading Overlay ── */
            .reading-overlay {
                position: fixed; inset: 0;
                background: #0d0608;
                z-index: 2000;
                display: flex; flex-direction: column;
                opacity: 0; pointer-events: none;
                transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
                transform: translateY(20px);
            }
            .reading-overlay.active { 
                opacity: 1; pointer-events: all;
                transform: translateY(0);
            }
            .reading-header {
                height: 100px; padding: 0 60px;
                display: flex; align-items: center; justify-content: space-between;
                border-bottom: 1px solid rgba(252, 188, 215, 0.08);
                background: #0d0608;
            }
            .reading-title-wrap {
                display: flex; flex-direction: column;
            }
            .reading-eyebrow {
                font-size: 10px; color: #E56AB3;
                text-transform: uppercase; letter-spacing: 3px;
                margin-bottom: 4px;
            }
            .reading-header h2 { font-family: 'Playfair Display', serif; font-size: 24px; color: #FCBCD7; }
            .close-reading {
                background: rgba(252, 188, 215, 0.05); border: 1px solid rgba(252, 188, 215, 0.1); 
                color: rgba(252, 188, 215, 0.6); padding: 10px 20px; border-radius: 30px;
                cursor: pointer; font-size: 12px; text-transform: uppercase; letter-spacing: 2px;
                transition: all 0.3s;
                display: flex; align-items: center; gap: 8px;
            }
            .close-reading:hover { 
                color: #FCBCD7; background: rgba(252, 188, 215, 0.1); 
                border-color: rgba(252, 188, 215, 0.3);
            }
            .pdf-container { 
                flex: 1; background: #1a1a1d; position: relative; 
                margin: 20px 40px; border-radius: 12px; overflow: hidden;
                box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            }
            #pdfFrame { width: 100%; height: 100%; border: none; }
            
            .pdf-loading {
                position: absolute; inset: 0;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                background: #1a1a1d; z-index: 10; gap: 20px;
            }
            .spinner {
                width: 40px; height: 40px;
                border: 3px solid rgba(229, 106, 179, 0.1);
                border-top-color: #E56AB3;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            @keyframes spin { to { transform: rotate(360deg); } }
            .pdf-loading p { color: rgba(252, 188, 215, 0.4); font-size: 14px; letter-spacing: 1px; }

            .reading-footer {
                height: 100px; display: flex; align-items: center; justify-content: center;
                border-top: 1px solid rgba(252, 188, 215, 0.08); background: #0d0608;
            }
            .complete-reading-btn {
                background: linear-gradient(90deg, #E56AB3, #BF5082);
                color: #0d0608; border: none;
                padding: 16px 40px; border-radius: 40px; font-weight: 700;
                cursor: pointer; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
                font-family: 'Inter', sans-serif;
                letter-spacing: 1px; text-transform: uppercase; font-size: 13px;
            }
            .complete-reading-btn:hover { 
                transform: scale(1.05) translateY(-5px); 
                box-shadow: 0 10px 30px rgba(229, 106, 179, 0.4); 
            }

        </style>
    </head>
    <body onload="init()">
        <a href="/welcome#selection" class="back-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        </a>

        <div class="main-area">
            <div class="header">
                <h1>Cultural Readings</h1>
                <p>Wisdom and traditions from the Land of the Rising Sun</p>
            </div>

            <div class="chapter-list" id="chapterList">
                <!-- Content generated by JS -->
            </div>
            
            <div class="hint-toast">Hold on a scroll of knowledge to reveal its essence</div>
        </div>

        <div class="image-panel">
            <div class="panel-overlay"></div>
            <div class="image-placeholder" id="placeholder">The essence is yet to be revealed</div>
            <img id="repImage" src="" alt="Cultural Illustration">
        </div>

        <!-- Reading Overlay -->
        <div class="reading-overlay" id="readingOverlay">
            <div class="reading-header">
                <div class="reading-title-wrap">
                    <span class="reading-eyebrow">Scroll of Knowledge</span>
                    <h2 id="readingTitle">Title</h2>
                </div>
                <button class="close-reading" onclick="closeReading()">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                    Close
                </button>
            </div>
            <div class="pdf-container">
                <div id="pdfLoading" class="pdf-loading">
                    <div class="spinner"></div>
                    <p>Unrolling the scroll...</p>
                </div>
                <iframe id="pdfFrame" src="" onload="document.getElementById('pdfLoading').style.display='none'"></iframe>
            </div>
            <div class="reading-footer">
                <button class="complete-reading-btn" id="completeBtn" onclick="onCompleteClick()">
                    I have absorbed this knowledge
                </button>
            </div>
        </div>

        <script>
            let chapters = [];
            let userStatus = 1;
            let currentOpenChapterId = null;

            async function init() {
                await fetchStatus();
                await fetchChapters();
                render();
            }

            async function fetchStatus() {
                try {
                    const res = await fetch('/api/culture/user-status');
                    const data = await res.json();
                    userStatus = data.status_chapter || 1;
                } catch (err) { console.error("Error fetching status:", err); }
            }

            async function fetchChapters() {
                try {
                    const res = await fetch('/api/culture/chapters');
                    chapters = await res.json();
                } catch (err) { console.error("Error fetching chapters:", err); }
            }

            function render() {
                const listEl = document.getElementById('chapterList');
                listEl.innerHTML = '';

                chapters.forEach((ch) => {
                    const isLocked = ch.order_index > userStatus;
                    const isCompleted = ch.order_index < userStatus;
                    const isActive = ch.order_index === userStatus;

                    const row = document.createElement('div');
                    row.className = 'chapter-row';

                    const dotArea = document.createElement('div');
                    dotArea.className = 'dot-area';
                    dotArea.innerHTML = `<div class="dot ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}"></div>`;

                    const card = document.createElement('div');
                    card.className = `chapter-card ${isLocked ? 'locked' : ''} ${isCompleted ? 'completed' : ''}`;
                    card.innerHTML = `
                        <div class="status-badge">Unlocked</div>
                        <h3>${ch.title}</h3>
                        <p>${ch.description}</p>
                    `;

                    // Interaction Logic: Long Press (Hold)
                    let pressTimer;
                    const startPress = () => {
                        if (isLocked) return;
                        pressTimer = setTimeout(() => showImage(ch.image_url), 400);
                    };
                    const endPress = () => clearTimeout(pressTimer);

                    card.addEventListener('mousedown', startPress);
                    card.addEventListener('touchstart', startPress);
                    card.addEventListener('mouseup', endPress);
                    card.addEventListener('mouseleave', endPress);
                    card.addEventListener('touchend', endPress);

                    // Click to open reading view
                    card.addEventListener('click', () => {
                        if (!isLocked) {
                            openReading(ch);
                        }
                    });

                    row.appendChild(dotArea);
                    row.appendChild(card);
                    listEl.appendChild(row);
                });
            }

            function openReading(ch) {
                currentOpenChapterId = ch.id;
                document.getElementById('readingTitle').innerText = ch.title;
                const pdfFrame = document.getElementById('pdfFrame');
                const pdfLoading = document.getElementById('pdfLoading');
                
                // Show loading screen
                pdfLoading.style.display = 'flex';
                
                // Construct the path
                const url = ch.pdf_url.startsWith('http') ? ch.pdf_url : `/uploads/${ch.pdf_url}`;
                pdfFrame.src = url;
                
                document.getElementById('readingOverlay').classList.add('active');
            }

            function closeReading() {
                document.getElementById('readingOverlay').classList.remove('active');
                document.getElementById('pdfFrame').src = '';
                currentOpenChapterId = null;
            }

            async function onCompleteClick() {
                if (currentOpenChapterId) {
                    await markAsComplete(currentOpenChapterId);
                    closeReading();
                }
            }

            function showImage(url) {
                const img = document.getElementById('repImage');
                const placeholder = document.getElementById('placeholder');
                
                if (placeholder) placeholder.style.opacity = '0';
                img.classList.remove('visible');
                
                setTimeout(() => {
                    img.src = url;
                    img.onload = () => img.classList.add('visible');
                }, 100);
            }

            async function markAsComplete(id) {
                try {
                    const res = await fetch(`/api/culture/complete/${id}`, { method: 'POST' });
                    if (res.ok) {
                        await fetchStatus();
                        render();
                    }
                } catch (err) { console.error("Error completing chapter:", err); }
            }
        </script>
    </body>
    </html>
    """

