"""
Migration script — create chapters, exercises, tests tables.
Run once:  python migrations/migrate_exercises.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import engine, SessionLocal
from sqlalchemy import text

DDL = """
-- chapters
CREATE TABLE IF NOT EXISTS chapters (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR NOT NULL,
    description TEXT DEFAULT '',
    category    VARCHAR DEFAULT 'general',
    level       VARCHAR DEFAULT 'N5',
    order_index INTEGER DEFAULT 0,
    image_url   VARCHAR DEFAULT ''
);

-- exercises (belong to a chapter)
CREATE TABLE IF NOT EXISTS exercises (
    id            SERIAL PRIMARY KEY,
    chapter_id    INTEGER NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    title         VARCHAR NOT NULL,
    description   TEXT DEFAULT '',
    exercise_type VARCHAR DEFAULT 'quiz',
    order_index   INTEGER DEFAULT 0,
    points        INTEGER DEFAULT 10
);

-- tests (belong to an exercise)
CREATE TABLE IF NOT EXISTS tests (
    id             SERIAL PRIMARY KEY,
    exercise_id    INTEGER NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    question       TEXT NOT NULL,
    correct_answer VARCHAR NOT NULL,
    option_a       VARCHAR DEFAULT '',
    option_b       VARCHAR DEFAULT '',
    option_c       VARCHAR DEFAULT '',
    option_d       VARCHAR DEFAULT '',
    test_type      VARCHAR DEFAULT 'multiple_choice',
    image_url      VARCHAR DEFAULT '',
    audio_url      VARCHAR DEFAULT '',
    order_index    INTEGER DEFAULT 0,
    explanation    TEXT DEFAULT ''
);

-- indexes
CREATE INDEX IF NOT EXISTS ix_chapters_id       ON chapters(id);
CREATE INDEX IF NOT EXISTS ix_exercises_id      ON exercises(id);
CREATE INDEX IF NOT EXISTS ix_exercises_chapter ON exercises(chapter_id);
CREATE INDEX IF NOT EXISTS ix_tests_id          ON tests(id);
CREATE INDEX IF NOT EXISTS ix_tests_exercise    ON tests(exercise_id);
"""

def run():
    with engine.connect() as conn:
        for stmt in DDL.strip().split(";"):
            stmt = stmt.strip()
            if stmt and not stmt.startswith("--"):
                conn.execute(text(stmt))
        conn.commit()
    print("Migration complete — chapters, exercises, tests tables created.")

if __name__ == "__main__":
    run()
