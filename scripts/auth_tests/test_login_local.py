import hashlib
from core.database import SessionLocal
from features.user.models import User

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def test_login(email, password):
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == email).first()
    db.close()
    input_hash = hash_password(password)
    print(f"[DEBUG] Login for {email}: input_hash={input_hash}, db_hash={getattr(db_user, 'password', None)}")
    if not db_user or db_user.password != input_hash:
        print("Failed!")
    else:
        print("Success!")

test_login('mariatompea@gmail.com', 'password')
