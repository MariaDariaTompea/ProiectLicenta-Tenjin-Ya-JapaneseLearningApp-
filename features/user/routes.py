"""Authentication routes — login, register, root"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from core.database import SessionLocal
from features.user.models import User, UserProfile, StatusLearning
from features.user.templates.auth import get_login_page_html, get_register_page_html
import hashlib

router = APIRouter()


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
    response = RedirectResponse(url="/welcome", status_code=303)
    response.set_cookie(key="user_email", value=user.email, httponly=True)
    return response


@router.post("/register")
def register(user: UserRegister):
    db = SessionLocal()
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    print(f"[DEBUG] Register {user.email}: password={user.password}, hash={hashed_password}")
    new_user = User(
        email=user.email,
        name=user.name,
        password=hashed_password,
        nickname=user.name,
        current_level="N5"
    )
    db.add(new_user)
    db.flush()  # flush to get new_user.id

    # Create default profile (avatar, banner, no equipped achievements)
    new_profile = UserProfile(
        user_id=new_user.id,
        avatar_url="/customisableprofile/defaultsettings/profileicondefault.png",
        banner_url="/customisableprofile/defaultsettings/bannerdefault.png"
    )
    db.add(new_profile)

    # Create learning status
    new_status = StatusLearning(
        user_id=new_user.id,
        status_chapter_overall=1,
        status_chapter_grammar=1,
        status_exercise_grammar=1,
        status_chapter_vocabulary=1,
        status_exercise_vocabulary=1
    )
    db.add(new_status)
    db.commit()
    db.close()
    return {"message": "User registered successfully", "email": user.email}
