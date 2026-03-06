"""Course routes — welcome page, grammar, vocabulary, culture, settings"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

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
                justify-content: flex-end;
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

            .ribbon-item {
                position: relative;
                width: 588px;
                height: 140px;
                cursor: pointer;
                transform: translateX(100%);
                transition: transform 0.9s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            }
            .ribbon-item.slide-in {
                transform: translateX(30px);
            }
            .ribbon-item:hover {
                transform: translateX(10px) !important;
            }

            .ribbon-item img {
                width: 100%;
                height: 100%;
                object-fit: contain;
                object-position: right;
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

            .ribbon-item:nth-child(1) { transition-delay: 0.3s; }
            .ribbon-item:nth-child(2) { transition-delay: 0.5s; }
            .ribbon-item:nth-child(3) { transition-delay: 0.7s; }
            .ribbon-item:nth-child(4) { transition-delay: 0.9s; }

            .ribbon-container.fade-out .ribbon-item {
                opacity: 0;
                transform: translateX(100%) !important;
                transition: opacity 0.6s ease, transform 0.8s ease;
            }
            .ribbon-container.fade-out .ribbon-item:nth-child(1) { transition-delay: 0s; }
            .ribbon-container.fade-out .ribbon-item:nth-child(2) { transition-delay: 0.1s; }
            .ribbon-container.fade-out .ribbon-item:nth-child(3) { transition-delay: 0.2s; }
            .ribbon-container.fade-out .ribbon-item:nth-child(4) { transition-delay: 0.3s; }

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
        <div id="selectionTable" class="selection-table">
            <div class="selection-bg" id="selectionBg"></div>
            <div class="selection-title">What do you want to learn?</div>
            <div class="selection-desc">Choose a writing system to begin your journey.</div>
            <div class="select-table">
                <div class="select-item" data-href="/hiragana-table" data-label="Hiragana">Hiragana</div>
                <div class="select-item" data-href="/katakana-table" data-label="Katakana">Katakana</div>
                <div class="select-item" data-href="/kanji-table" data-label="Kanji">Kanji</div>
            </div>
            <a class="course-link" href="#" id="startCourseLink">You already know these? Start the Japanese basic course!</a>
        </div>

        <div class="black-overlay" id="blackOverlay"></div>

        <div class="page-slide" id="pageSlide">
            <div class="page-slide-label" id="pageSlideLabel"></div>
        </div>

        <div class="course-menu" id="courseMenu">
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
                const skipIntro = window.location.hash === '#selection';

                if (skipIntro) {
                    document.getElementById('bgImage').classList.add('zoom');
                    document.getElementById('welcomeTitle').style.display = 'none';
                    const selectionTable = document.getElementById('selectionTable');
                    selectionTable.classList.add('visible');
                    selectionTable.style.transition = 'none';
                    selectionTable.style.opacity = '1';
                    document.getElementById('selectionBg').classList.add('zoom-in');
                } else {
                    setTimeout(() => {
                        document.getElementById('bgImage').classList.add('zoom');
                    }, 100);
                }
            });

            if (window.location.hash !== '#selection') {
                setTimeout(() => {
                    document.getElementById('welcomeTitle').classList.add('slide-up');
                    setTimeout(() => {
                        document.getElementById('selectionTable').classList.add('visible');
                        setTimeout(() => {
                            document.getElementById('selectionBg').classList.add('zoom-in');
                        }, 100);
                    }, 700);
                }, 2500);
            }

            document.querySelectorAll('.select-item').forEach(item => {
                item.addEventListener('click', function() {
                    const targetUrl = this.getAttribute('data-href');
                    const label = this.getAttribute('data-label');
                    const selectionTable = document.getElementById('selectionTable');
                    const pageSlide = document.getElementById('pageSlide');
                    const pageSlideLabel = document.getElementById('pageSlideLabel');
                    pageSlideLabel.textContent = label;
                    selectionTable.classList.add('slide-away');
                    setTimeout(() => { pageSlide.classList.add('active'); }, 400);
                    setTimeout(() => { window.location.href = targetUrl; }, 1800);
                });
            });

            document.getElementById('startCourseLink').addEventListener('click', function(e) {
                e.preventDefault();
                const overlay = document.getElementById('blackOverlay');
                const courseMenu = document.getElementById('courseMenu');
                overlay.classList.add('active');
                setTimeout(() => { courseMenu.classList.add('visible'); }, 1200);
                setTimeout(() => { overlay.classList.remove('active'); }, 1600);
                setTimeout(() => {
                    document.querySelectorAll('.ribbon-item').forEach(item => {
                        item.classList.add('slide-in');
                    });
                }, 1800);
            });

            document.querySelectorAll('.ribbon-item').forEach(item => {
                item.addEventListener('click', function() {
                    const targetUrl = this.getAttribute('data-href');
                    const ribbonContainer = document.getElementById('ribbonContainer');
                    const foxOverlay = document.getElementById('foxVideo');
                    const foxVid = document.getElementById('foxVid');
                    const overlay = document.getElementById('blackOverlay');
                    ribbonContainer.classList.add('fade-out');
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


@router.get("/course/grammar", response_class=HTMLResponse)
async def course_grammar():
    return """
    <html>
    <head>
        <title>Grammar</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Playfair Display', serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #111; color: #FCBCD7; opacity: 0; transition: opacity 1s ease; }
            body.loaded { opacity: 1; }
            h1 { font-size: 48px; }
        </style>
    </head>
    <body>
        <h1>Grammar</h1>
        <script>window.addEventListener('load', () => document.body.classList.add('loaded'));</script>
    </body>
    </html>
    """


@router.get("/course/vocabulary", response_class=HTMLResponse)
async def course_vocabulary():
    return """
    <html>
    <head>
        <title>Vocabulary</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Playfair Display', serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #111; color: #FCBCD7; opacity: 0; transition: opacity 1s ease; }
            body.loaded { opacity: 1; }
            h1 { font-size: 48px; }
        </style>
    </head>
    <body>
        <h1>Vocabulary</h1>
        <script>window.addEventListener('load', () => document.body.classList.add('loaded'));</script>
    </body>
    </html>
    """


@router.get("/course/culture", response_class=HTMLResponse)
async def course_culture():
    return """
    <html>
    <head>
        <title>Culture</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Playfair Display', serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #111; color: #FCBCD7; opacity: 0; transition: opacity 1s ease; }
            body.loaded { opacity: 1; }
            h1 { font-size: 48px; }
        </style>
    </head>
    <body>
        <h1>Culture</h1>
        <script>window.addEventListener('load', () => document.body.classList.add('loaded'));</script>
    </body>
    </html>
    """


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
