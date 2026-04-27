import sys
import os
sys.path.append('d:/JapaneseApp')
from core.database import SessionLocal
from features.user.models import User
from features.user.routes import hash_password

db = SessionLocal()
user = db.query(User).filter(User.email == "mariatompea@gmail.com").first()
if user:
    print(f"User found! Email: {user.email}")
    print(f"Password in DB: {user.password}")
    print(f"Expected Hash for 'passwrod': {hash_password('passwrod')}")
    print(f"Expected Hash for 'password': {hash_password('password')}")
else:
    print("User not found: mariatompea@gmail.com")
    all_users = db.query(User).all()
    print("All users:")
    for u in all_users:
        print(u.email)
