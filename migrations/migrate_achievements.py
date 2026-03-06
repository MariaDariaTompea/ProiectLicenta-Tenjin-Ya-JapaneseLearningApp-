"""Migration: Create achievements table, user_items table, 
   add equipped_achievement columns to users, and seed default achievements."""

from database import engine, SessionLocal
from sqlalchemy import text

def run_migration():
    with engine.connect() as conn:
        # 1) Create achievements table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS achievements (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                description VARCHAR NOT NULL,
                image_url VARCHAR NOT NULL DEFAULT '/customisableprofile/defaultsettings/defaultgem.png',
                category VARCHAR DEFAULT 'general'
            );
        """))

        # 2) Create user_items table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS user_items (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                item_id INTEGER NOT NULL,
                item_type VARCHAR NOT NULL,
                acquired_at TIMESTAMP DEFAULT NOW()
            );
        """))

        # 3) Add equipped achievement columns to users (if not exist)
        for col in ['equipped_achievement_1', 'equipped_achievement_2', 'equipped_achievement_3']:
            try:
                conn.execute(text(f"""
                    ALTER TABLE users ADD COLUMN {col} INTEGER REFERENCES achievements(id);
                """))
                print(f"  Added column {col}")
            except Exception as e:
                if 'already exists' in str(e).lower() or 'duplicate' in str(e).lower():
                    print(f"  Column {col} already exists, skipping")
                else:
                    print(f"  Warning for {col}: {e}")

        conn.commit()
        print("Tables created successfully.")

        # 4) Seed 3 default gem achievements (if table is empty)
        result = conn.execute(text("SELECT COUNT(*) FROM achievements"))
        count = result.scalar()
        if count == 0:
            conn.execute(text("""
                INSERT INTO achievements (name, description, image_url, category) VALUES
                ('Default Gem 1', 'Equip an achievement you own', '/customisableprofile/defaultsettings/defaultgem.png', 'general'),
                ('Default Gem 2', 'Equip an achievement you own', '/customisableprofile/defaultsettings/defaultgem.png', 'general'),
                ('Default Gem 3', 'Equip an achievement you own', '/customisableprofile/defaultsettings/defaultgem.png', 'general');
            """))
            conn.commit()
            print("Seeded 3 default achievements.")
        else:
            print(f"Achievements table already has {count} rows, skipping seed.")

    print("Migration complete!")

if __name__ == "__main__":
    run_migration()
