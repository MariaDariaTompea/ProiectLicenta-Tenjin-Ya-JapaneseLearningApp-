from core.database import SessionLocal
from features.user.models import User

db = SessionLocal()
users = db.query(User).all()
print(f"Total users: {len(users)}")
for u in users:
    print(f"- {u.email} : {u.password}")
db.close()
