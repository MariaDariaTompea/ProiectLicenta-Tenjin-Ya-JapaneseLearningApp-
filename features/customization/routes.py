"""Profile routes — profile page, avatar/banner/nickname updates, equip items"""

from fastapi import APIRouter, HTTPException, Request, Cookie, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from pydantic import BaseModel
from core.database import SessionLocal
from features.user.models import User, UserItem
from features.customization.models import Achievement
from features.customization.templates.profile import get_profile_page_html
from features.customization.templates.achievements import get_achievements_page_html
import shutil
import os
import hashlib
from typing import Optional

router = APIRouter()

os.makedirs("customisableprofile/avatars", exist_ok=True)


# ── Profile page ──
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
        owned_banners.append({"id": ui.item_id, "name": f"Banner #{ui.item_id}", "image_url": f"/customisableprofile/banners/{ui.item_id}.png"})

    owned_ach_items = db.query(UserItem).filter(UserItem.user_id == db_user.id, UserItem.item_type == "achievement").all()
    owned_achievements = []
    for ui in owned_ach_items:
        ach = db.query(Achievement).filter(Achievement.id == ui.item_id).first()
        if ach:
            owned_achievements.append({"id": ach.id, "name": ach.name, "description": ach.description, "image_url": ach.image_url})

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


# ── Achievements page ──
@router.get("/achievements", response_class=HTMLResponse)
def achievements_page(request: Request, user_email: Optional[str] = Cookie(None)):
    if not user_email:
        return RedirectResponse(url="/login", status_code=303)
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        db.close()
        return RedirectResponse(url="/login", status_code=303)

    # Gather all achievements the user owns
    owned_items = db.query(UserItem).filter(
        UserItem.user_id == db_user.id,
        UserItem.item_type == "achievement"
    ).order_by(UserItem.acquired_at.asc()).all()
    achievements = []
    for ui in owned_items:
        ach = db.query(Achievement).filter(Achievement.id == ui.item_id).first()
        if ach:
            date_str = ui.acquired_at.strftime("%B %d, %Y") if ui.acquired_at else ""
            achievements.append({
                "name": ach.name,
                "description": ach.description,
                "image_url": ach.image_url,
                "date": date_str
            })
    db.close()
    return get_achievements_page_html(achievements=achievements)


# ── Avatar upload ──
@router.post("/profile/update-avatar")
async def update_avatar(avatar: UploadFile = File(...), user_email: Optional[str] = Cookie(None)):
    if not user_email:
        raise HTTPException(status_code=401, detail="Not logged in")
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

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


# ── Banner upload ──
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


# ── Nickname update ──
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


# ── Equip banner from inventory ──
class EquipBannerRequest(BaseModel):
    item_id: int

@router.post("/profile/equip-banner")
async def equip_banner(body: EquipBannerRequest, user_email: Optional[str] = Cookie(None)):
    if not user_email:
        raise HTTPException(status_code=401, detail="Not logged in")
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
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


# ── Equip achievement to slot ──
class EquipAchievementRequest(BaseModel):
    achievement_id: int
    slot: int

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
    owns = db.query(UserItem).filter(
        UserItem.user_id == db_user.id,
        UserItem.item_id == body.achievement_id,
        UserItem.item_type == "achievement"
    ).first()
    if not owns:
        db.close()
        raise HTTPException(status_code=403, detail="You don't own this achievement")
    if body.slot == 0:
        db_user.equipped_achievement_1 = body.achievement_id
    elif body.slot == 1:
        db_user.equipped_achievement_2 = body.achievement_id
    else:
        db_user.equipped_achievement_3 = body.achievement_id
    db.commit()
    db.close()
    return JSONResponse({"equipped": True, "slot": body.slot})


# ── Change Password ──
class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/profile/change-password")
async def change_password(body: ChangePasswordRequest, user_email: Optional[str] = Cookie(None)):
    if not user_email:
        raise HTTPException(status_code=401, detail="Not logged in")
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.password != hash_password(body.current_password):
        db.close()
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    db_user.password = hash_password(body.new_password)
    db.commit()
    db.close()
    return JSONResponse({"success": True})


# ── Change Email ──
class ChangeEmailRequest(BaseModel):
    current_email: str
    new_email: str

@router.post("/profile/change-email")
async def change_email(body: ChangeEmailRequest, user_email: Optional[str] = Cookie(None)):
    if not user_email:
        raise HTTPException(status_code=401, detail="Not logged in")
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.email != body.current_email:
        db.close()
        raise HTTPException(status_code=400, detail="Current email is incorrect")
    existing = db.query(User).filter(User.email == body.new_email).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="This email is already in use")
    db_user.email = body.new_email
    db.commit()
    db.close()
    response = JSONResponse({"success": True})
    response.set_cookie(key="user_email", value=body.new_email, path="/")
    return response
