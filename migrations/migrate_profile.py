"""One-time migration script to add profile columns to users table"""
from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users'"))
    cols = [row[0] for row in result]
    print("Existing columns:", cols)
    
    if "nickname" not in cols:
        conn.execute(text("ALTER TABLE users ADD COLUMN nickname VARCHAR DEFAULT ''"))
        print("Added nickname column")
    
    if "avatar_url" not in cols:
        conn.execute(text("ALTER TABLE users ADD COLUMN avatar_url VARCHAR DEFAULT '/customisableprofile/defaultsettings/profileicondefault.png'"))
        print("Added avatar_url column")
    
    if "banner_url" not in cols:
        conn.execute(text("ALTER TABLE users ADD COLUMN banner_url VARCHAR DEFAULT '/customisableprofile/defaultsettings/bannerdefault.png'"))
        print("Added banner_url column")

    if "current_level" not in cols:
        conn.execute(text("ALTER TABLE users ADD COLUMN current_level VARCHAR DEFAULT 'N5'"))
        print("Added current_level column")
    
    # Update existing users that have NULL or old default values
    conn.execute(text("UPDATE users SET nickname = name WHERE nickname IS NULL OR nickname = ''"))
    conn.execute(text("UPDATE users SET avatar_url = '/customisableprofile/defaultsettings/profileicondefault.png' WHERE avatar_url IS NULL OR avatar_url = '/customisableprofile/defaultsettings/bannerdefault.png'"))
    conn.execute(text("UPDATE users SET banner_url = '/customisableprofile/defaultsettings/bannerdefault.png' WHERE banner_url IS NULL"))
    conn.execute(text("UPDATE users SET current_level = 'N5' WHERE current_level IS NULL"))
    
    conn.commit()
    print("Migration complete")
