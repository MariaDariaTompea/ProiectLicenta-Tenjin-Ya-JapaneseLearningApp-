import hashlib
from core.database import SessionLocal, Base, engine
from features.user.models import User, UserProfile, StatusLearning, UserItem
from features.customization.models import Achievement
from features.grammar.models import Proficiency, Chapter, Exercise
from datetime import datetime

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def rebuild():
    db = SessionLocal()
    email = "mariatompea@gmail.com"
    
    # 1. Delete user if exists
    user = db.query(User).filter(User.email == email).first()
    if user:
        print(f"Deleting user {email} and their data...")
        # Delete profile
        db.query(UserProfile).filter(UserProfile.user_id == user.id).delete()
        # Delete status
        db.query(StatusLearning).filter(StatusLearning.user_id == user.id).delete()
        # Delete items
        db.query(UserItem).filter(UserItem.user_id == user.id).delete()
        # Delete user
        db.delete(user)
        db.commit()

    # 2. Add proficiency levels if empty
    existing_prof = db.query(Proficiency).all()
    if not existing_prof:
        print("Adding default proficiency levels...")
        profs = [
            Proficiency(level="N5", name="Beginner", description="JLPT N5 — Foundation", order_index=1),
            Proficiency(level="N4", name="Elementary", description="JLPT N4 — Basic", order_index=2),
            Proficiency(level="N3", name="Intermediate", description="JLPT N3 — Intermediate", order_index=3),
            Proficiency(level="N2", name="Upper-Intermediate", description="JLPT N2 — Upper-Intermediate", order_index=4),
            Proficiency(level="N1", name="Advanced", description="JLPT N1 — Advanced", order_index=5),
        ]
        db.add_all(profs)
        db.commit()

    # 3. Add some achievements to the DB if it's empty
    existing_achievements = db.query(Achievement).all()
    if not existing_achievements:
        print("Adding default achievements to the database...")
        ach1 = Achievement(name="First Steps", description="Completed your first lesson", category="general")
        ach2 = Achievement(name="Hiragana Master", description="Learned all Hiragana", category="hiragana")
        ach3 = Achievement(name="Streak 7", description="7-day login streak", category="general")
        db.add_all([ach1, ach2, ach3])
        db.commit()
        existing_achievements = [ach1, ach2, ach3]

    # 4. Create the user again
    print(f"Creating user {email}...")
    new_user = User(
        email=email,
        name="Maria Tompea",
        password=hash_password("password"),
        nickname="Maria",
        current_level="N5"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 5. Create UserProfile (default avatar/banner, no equipped achievements)
    new_profile = UserProfile(
        user_id=new_user.id,
        avatar_url="/customisableprofile/defaultsettings/profileicondefault.png",
        banner_url="/customisableprofile/defaultsettings/bannerdefault.png"
    )
    db.add(new_profile)
    db.commit()

    # 6. Create StatusLearning
    new_status = StatusLearning(user_id=new_user.id)
    db.add(new_status)
    db.commit()

    # 7. Add items to user
    print(f"Adding items to {email}...")
    for ach in existing_achievements:
        user_item = UserItem(
            user_id=new_user.id,
            item_id=ach.id,
            item_type="achievement",
            acquired_at=datetime.utcnow()
        )
        db.add(user_item)
    
    # Add a banner item
    banner_item = UserItem(
        user_id=new_user.id,
        item_id=1,
        item_type="banner",
        acquired_at=datetime.utcnow()
    )
    db.add(banner_item)
    db.commit()

    # 8. Equip one achievement
    new_profile.equipped_achievement_1 = existing_achievements[0].id
    db.commit()

    print("Rebuild complete!")
    db.close()

if __name__ == "__main__":
    rebuild()
