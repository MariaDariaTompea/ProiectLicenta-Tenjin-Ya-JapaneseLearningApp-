from fastapi import APIRouter, HTTPException, Request, Cookie, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from pydantic import BaseModel
from database import SessionLocal
from models import Hiragana, Katakana, User, Achievement, UserItem
from templates import get_hiragana_table_html, get_katakana_table_html, get_login_page_html, get_register_page_html, get_profile_page_html
import hashlib
import shutil
import os
from typing import Optional

router = APIRouter()

# Ensure user upload directories exist
os.makedirs("customisableprofile/avatars", exist_ok=True)
# Welcome page route
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

            /* Slide transition for writing system selection */
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

            /* Page slide overlay */
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

            /* Black fade overlay */
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

            /* Course menu screen */
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

            /* Ribbon fade out */
            .ribbon-container.fade-out .ribbon-item {
                opacity: 0;
                transform: translateX(100%) !important;
                transition: opacity 0.6s ease, transform 0.8s ease;
            }
            .ribbon-container.fade-out .ribbon-item:nth-child(1) { transition-delay: 0s; }
            .ribbon-container.fade-out .ribbon-item:nth-child(2) { transition-delay: 0.1s; }
            .ribbon-container.fade-out .ribbon-item:nth-child(3) { transition-delay: 0.2s; }
            .ribbon-container.fade-out .ribbon-item:nth-child(4) { transition-delay: 0.3s; }

            /* Fox video overlay */
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

        <!-- Black fade overlay -->
        <div class="black-overlay" id="blackOverlay"></div>

        <!-- Page slide transition -->
        <div class="page-slide" id="pageSlide">
            <div class="page-slide-label" id="pageSlideLabel"></div>
        </div>

        <!-- Course menu with ribbons -->
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

        <!-- Fox running video overlay -->
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
                    // Skip intro — show selection immediately
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

            // Writing system selection slide transition
            document.querySelectorAll('.select-item').forEach(item => {
                item.addEventListener('click', function() {
                    const targetUrl = this.getAttribute('data-href');
                    const label = this.getAttribute('data-label');
                    const selectionTable = document.getElementById('selectionTable');
                    const pageSlide = document.getElementById('pageSlide');
                    const pageSlideLabel = document.getElementById('pageSlideLabel');

                    // Set the label text
                    pageSlideLabel.textContent = label;

                    // Phase 1: Fade out other elements
                    selectionTable.classList.add('slide-away');

                    // Phase 2: Slide panel up from bottom
                    setTimeout(() => {
                        pageSlide.classList.add('active');
                    }, 400);

                    // Phase 3: Redirect after slide completes and label shows
                    setTimeout(() => {
                        window.location.href = targetUrl;
                    }, 1800);
                });
            });

            // Start the course transition
            document.getElementById('startCourseLink').addEventListener('click', function(e) {
                e.preventDefault();
                const overlay = document.getElementById('blackOverlay');
                const courseMenu = document.getElementById('courseMenu');

                // Phase 1: Black fade in
                overlay.classList.add('active');

                // Phase 2: After black screen, show course menu behind overlay
                setTimeout(() => {
                    courseMenu.classList.add('visible');
                }, 1200);

                // Phase 3: Fade out black overlay to reveal course menu
                setTimeout(() => {
                    overlay.classList.remove('active');
                }, 1600);

                // Phase 4: Slide in ribbons
                setTimeout(() => {
                    document.querySelectorAll('.ribbon-item').forEach(item => {
                        item.classList.add('slide-in');
                    });
                }, 1800);
            });

            // Ribbon click: fade ribbons, show fox video, then redirect
            document.querySelectorAll('.ribbon-item').forEach(item => {
                item.addEventListener('click', function() {
                    const targetUrl = this.getAttribute('data-href');
                    const ribbonContainer = document.getElementById('ribbonContainer');
                    const foxOverlay = document.getElementById('foxVideo');
                    const foxVid = document.getElementById('foxVid');
                    const overlay = document.getElementById('blackOverlay');

                    // Phase 1: Fade out ribbons
                    ribbonContainer.classList.add('fade-out');

                    // Phase 2: After ribbons fade, show fox video
                    setTimeout(() => {
                        foxVid.currentTime = 0;
                        foxVid.play();
                        foxOverlay.classList.add('visible');
                    }, 800);

                    // Phase 3: Wait for video to end, then blend to black and redirect
                    foxVid.addEventListener('ended', function() {
                        // Fade to black
                        overlay.style.zIndex = '102';
                        overlay.classList.add('active');

                        // Redirect after black fade completes
                        setTimeout(() => {
                            window.location.href = targetUrl;
                        }, 1300);
                    });
                });
            });
        </script>
    </body>
    </html>
    """

# Course section routes
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

# Katakana table route
@router.get("/katakana-table", response_class=HTMLResponse)
def get_katakana_table():
    try:
        db = SessionLocal()
        katakana_list = db.query(Katakana).all()
        db.close()
        return get_katakana_table_html(katakana_list)
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

# Kanji table route
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
# Pydantic models for request bodies
class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    name: str
    password: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.get("/")
def read_root():
    return {"message": "Japanese app backend is running!"}

@router.get("/login", response_class=HTMLResponse)
def login_page():
    return get_login_page_html()

@router.get("/register", response_class=HTMLResponse)
def register_page():
    return get_register_page_html()

@router.post("/login")
def login(user: UserLogin):
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user.email).first()
    db.close()
    input_hash = hash_password(user.password)
    print(f"[DEBUG] Login for {user.email}: input_hash={input_hash}, db_hash={getattr(db_user, 'password', None)}")
    if not db_user or db_user.password != input_hash:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    # Redirect to welcome page after successful login, set user cookie
    response = RedirectResponse(url="/welcome", status_code=303)
    response.set_cookie(key="user_email", value=user.email, httponly=True)
    return response

@router.post("/register")
def register(user: UserRegister):
    db = SessionLocal()
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    # Create new user
    hashed_password = hash_password(user.password)
    print(f"[DEBUG] Register {user.email}: password={user.password}, hash={hashed_password}")
    new_user = User(
        email=user.email,
        name=user.name,
        password=hashed_password,
        nickname=user.name,
        avatar_url="/customisableprofile/defaultsettings/profileicondefault.png",
        banner_url="/customisableprofile/defaultsettings/bannerdefault.png",
        current_level="N5"
    )
    db.add(new_user)
    db.commit()
    db.close()
    return {"message": "User registered successfully", "email": user.email}

# ── Profile screen ──
@router.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request, user_email: Optional[str] = Cookie(None)):
    if not user_email:
        return RedirectResponse(url="/login", status_code=303)
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        db.close()
        return RedirectResponse(url="/login", status_code=303)

    # Build achievements list for the 3 equipped slots
    default_ach = {"name": "Empty Slot", "description": "Equip an achievement you own",
                   "image_url": "/customisableprofile/defaultsettings/defaultgem.png", "earned": False}
    achievements = []
    for slot_col in [db_user.equipped_achievement_1, db_user.equipped_achievement_2, db_user.equipped_achievement_3]:
        if slot_col:
            ach = db.query(Achievement).filter(Achievement.id == slot_col).first()
            if ach:
                achievements.append({"name": ach.name, "description": ach.description,
                                     "image_url": ach.image_url, "earned": True})
            else:
                achievements.append(default_ach)
        else:
            achievements.append(default_ach)

    # Load owned items
    owned_banner_items = db.query(UserItem).filter(UserItem.user_id == db_user.id, UserItem.item_type == "banner").all()
    owned_banners = []
    for ui in owned_banner_items:
        # For banners, item_id stores banner path index or we store the URL directly
        owned_banners.append({"id": ui.item_id, "name": f"Banner #{ui.item_id}", "image_url": f"/customisableprofile/banners/{ui.item_id}.png"})

    owned_ach_items = db.query(UserItem).filter(UserItem.user_id == db_user.id, UserItem.item_type == "achievement").all()
    owned_achievements = []
    for ui in owned_ach_items:
        ach = db.query(Achievement).filter(Achievement.id == ui.item_id).first()
        if ach:
            owned_achievements.append({"id": ach.id, "name": ach.name, "image_url": ach.image_url})

    db.close()
    return get_profile_page_html(
        user_name=db_user.name,
        nickname=db_user.nickname or db_user.name,
        avatar_url=db_user.avatar_url or "/customisableprofile/defaultsettings/profileicondefault.png",
        banner_url=db_user.banner_url or "/customisableprofile/defaultsettings/bannerdefault.png",
        user_email=db_user.email,
        current_level=db_user.current_level or "N5",
        achievements=achievements,
        owned_banners=owned_banners,
        owned_achievements=owned_achievements
    )

@router.post("/profile/update-avatar")
async def update_avatar(avatar: UploadFile = File(...), user_email: Optional[str] = Cookie(None)):
    if not user_email:
        raise HTTPException(status_code=401, detail="Not logged in")
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    # Save the uploaded file
    ext = os.path.splitext(avatar.filename)[1] or ".png"
    safe_email = user_email.replace("@", "_at_").replace(".", "_")
    filename = f"{safe_email}_avatar{ext}"
    filepath = os.path.join("customisableprofile", "avatars", filename)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(avatar.file, f)

    avatar_url = f"/customisableprofile/avatars/{filename}"
    db_user.avatar_url = avatar_url
    db.commit()
    db.close()
    return JSONResponse({"avatar_url": avatar_url})

@router.post("/profile/update-banner")
async def update_banner(banner: UploadFile = File(...), user_email: Optional[str] = Cookie(None)):
    if not user_email:
        raise HTTPException(status_code=401, detail="Not logged in")
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    ext = os.path.splitext(banner.filename)[1] or ".png"
    safe_email = user_email.replace("@", "_at_").replace(".", "_")
    filename = f"{safe_email}_banner{ext}"
    filepath = os.path.join("customisableprofile", "avatars", filename)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(banner.file, f)

    banner_url = f"/customisableprofile/avatars/{filename}"
    db_user.banner_url = banner_url
    db.commit()
    db.close()
    return JSONResponse({"banner_url": banner_url})

class NicknameUpdate(BaseModel):
    nickname: str

@router.post("/profile/update-nickname")
async def update_nickname(body: NicknameUpdate, user_email: Optional[str] = Cookie(None)):
    if not user_email:
        raise HTTPException(status_code=401, detail="Not logged in")
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    db_user.nickname = body.nickname.strip()[:24]
    db.commit()
    db.close()
    return JSONResponse({"nickname": db_user.nickname})


class EquipBannerRequest(BaseModel):
    item_id: int

class EquipAchievementRequest(BaseModel):
    achievement_id: int
    slot: int  # 0, 1, or 2


@router.post("/profile/equip-banner")
async def equip_banner(body: EquipBannerRequest, user_email: Optional[str] = Cookie(None)):
    if not user_email:
        raise HTTPException(status_code=401, detail="Not logged in")
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    # Verify user owns this banner
    owns = db.query(UserItem).filter(
        UserItem.user_id == db_user.id,
        UserItem.item_id == body.item_id,
        UserItem.item_type == "banner"
    ).first()
    if not owns:
        db.close()
        raise HTTPException(status_code=403, detail="You don't own this banner")
    banner_url = f"/customisableprofile/banners/{body.item_id}.png"
    db_user.banner_url = banner_url
    db.commit()
    db.close()
    return JSONResponse({"banner_url": banner_url})


@router.post("/profile/equip-achievement")
async def equip_achievement(body: EquipAchievementRequest, user_email: Optional[str] = Cookie(None)):
    if not user_email:
        raise HTTPException(status_code=401, detail="Not logged in")
    if body.slot not in (0, 1, 2):
        raise HTTPException(status_code=400, detail="Slot must be 0, 1, or 2")
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    # Verify user owns this achievement
    owns = db.query(UserItem).filter(
        UserItem.user_id == db_user.id,
        UserItem.item_id == body.achievement_id,
        UserItem.item_type == "achievement"
    ).first()
    if not owns:
        db.close()
        raise HTTPException(status_code=403, detail="You don't own this achievement")
    # Equip to the right slot
    if body.slot == 0:
        db_user.equipped_achievement_1 = body.achievement_id
    elif body.slot == 1:
        db_user.equipped_achievement_2 = body.achievement_id
    else:
        db_user.equipped_achievement_3 = body.achievement_id
    db.commit()
    db.close()
    return JSONResponse({"equipped": True, "slot": body.slot})

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
