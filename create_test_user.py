import hashlib
from core.database import SessionLocal, Base, engine
from features.user.models import User, UserProfile, StatusLearning, UserItem
from features.customization.models import Achievement
from features.grammar.models import Proficiency
from features.japanese.models import Hiragana, Katakana

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    email = "mariatompea@gmail.com"
    password = "password"

    # Ensure proficiencies exist
    if not db.query(Proficiency).first():
        profs = [
            Proficiency(level="N5", name="Beginner", description="JLPT N5 — Foundation", order_index=1),
            Proficiency(level="N4", name="Elementary", description="JLPT N4 — Basic", order_index=2),
            Proficiency(level="N3", name="Intermediate", description="JLPT N3 — Intermediate", order_index=3),
            Proficiency(level="N2", name="Upper-Intermediate", description="JLPT N2 — Upper-Intermediate", order_index=4),
            Proficiency(level="N1", name="Advanced", description="JLPT N1 — Advanced", order_index=5),
        ]
        db.add_all(profs)
        db.commit()

    user = db.query(User).filter(User.email == email).first()
    if not user:
        new_user = User(
            email=email,
            name="Maria Tompea",
            password=hash_password(password),
            nickname="Maria",
            current_level="N5"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Create profile
        new_profile = UserProfile(user_id=new_user.id)
        db.add(new_profile)

        # Create status
        new_status = StatusLearning(user_id=new_user.id)
        db.add(new_status)
        db.commit()
        print(f"Created user {email}")
    else:
        print(f"User {email} already exists.")
    db.close()

if __name__ == "__main__":
    create_user()
