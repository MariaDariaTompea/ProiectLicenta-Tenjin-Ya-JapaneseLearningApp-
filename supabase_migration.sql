-- ============================================================
--  MIGRATION: Restructure database for Tenjin-Ya app
--  This script updates the Supabase database to match the new schema
-- ============================================================

-- ────────────────────────────────────────────────────────────
--  1. CREATE NEW TABLES
-- ────────────────────────────────────────────────────────────

-- Proficiency levels (N5, N4, N3, N2, N1)
CREATE TABLE IF NOT EXISTS proficiencies (
    id SERIAL PRIMARY KEY,
    level VARCHAR NOT NULL UNIQUE,
    name VARCHAR NOT NULL DEFAULT '',
    description TEXT DEFAULT '',
    order_index INTEGER DEFAULT 0
);

-- User profiles (avatar, banner, equipped achievements)
CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    avatar_url VARCHAR DEFAULT '/customisableprofile/defaultsettings/profileicondefault.png',
    banner_url VARCHAR DEFAULT '/customisableprofile/defaultsettings/bannerdefault.png',
    equipped_achievement_1 INTEGER REFERENCES achievements(id),
    equipped_achievement_2 INTEGER REFERENCES achievements(id),
    equipped_achievement_3 INTEGER REFERENCES achievements(id)
);

-- User photos (uploaded images)
CREATE TABLE IF NOT EXISTS user_photos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    photo_url VARCHAR NOT NULL,
    photo_type VARCHAR NOT NULL DEFAULT 'avatar',
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- ────────────────────────────────────────────────────────────
--  2. MIGRATE DATA: Copy profile data from users to user_profiles
-- ────────────────────────────────────────────────────────────

-- Create a profile for each existing user (copy avatar, banner, achievements)
INSERT INTO user_profiles (user_id, avatar_url, banner_url, equipped_achievement_1, equipped_achievement_2, equipped_achievement_3)
SELECT 
    id,
    COALESCE(avatar_url, '/customisableprofile/defaultsettings/profileicondefault.png'),
    COALESCE(banner_url, '/customisableprofile/defaultsettings/bannerdefault.png'),
    equipped_achievement_1,
    equipped_achievement_2,
    equipped_achievement_3
FROM users
ON CONFLICT (user_id) DO NOTHING;

-- ────────────────────────────────────────────────────────────
--  3. ADD proficiency_id TO chapters
-- ────────────────────────────────────────────────────────────

-- Insert default proficiency levels
INSERT INTO proficiencies (level, name, description, order_index) VALUES
    ('N5', 'Beginner', 'JLPT N5 — Foundation', 1),
    ('N4', 'Elementary', 'JLPT N4 — Basic', 2),
    ('N3', 'Intermediate', 'JLPT N3 — Intermediate', 3),
    ('N2', 'Upper-Intermediate', 'JLPT N2 — Upper-Intermediate', 4),
    ('N1', 'Advanced', 'JLPT N1 — Advanced', 5)
ON CONFLICT (level) DO NOTHING;

-- Add proficiency_id column to chapters
ALTER TABLE chapters ADD COLUMN IF NOT EXISTS proficiency_id INTEGER REFERENCES proficiencies(id);

-- Migrate existing chapters: map their 'level' column to proficiency_id
UPDATE chapters SET proficiency_id = p.id
FROM proficiencies p
WHERE chapters.level = p.level AND chapters.proficiency_id IS NULL;

-- Set default proficiency (N5) for any remaining chapters without one
UPDATE chapters SET proficiency_id = (SELECT id FROM proficiencies WHERE level = 'N5' LIMIT 1)
WHERE proficiency_id IS NULL;

-- Make proficiency_id NOT NULL now that all rows have a value
ALTER TABLE chapters ALTER COLUMN proficiency_id SET NOT NULL;

-- ────────────────────────────────────────────────────────────
--  4. MODIFY tests TABLE: Replace option_a/b/c/d with options JSON
-- ────────────────────────────────────────────────────────────

-- Add new 'options' column
ALTER TABLE tests ADD COLUMN IF NOT EXISTS options TEXT DEFAULT '';

-- Add 'explanation' column if not exists
ALTER TABLE tests ADD COLUMN IF NOT EXISTS explanation TEXT DEFAULT '';

-- Migrate existing option data into JSON format
UPDATE tests SET options = 
    '["' || COALESCE(NULLIF(option_a, ''), '') || '","' || 
    COALESCE(NULLIF(option_b, ''), '') || '","' || 
    COALESCE(NULLIF(option_c, ''), '') || '","' || 
    COALESCE(NULLIF(option_d, ''), '') || '"]'
WHERE options = '' OR options IS NULL;

-- ────────────────────────────────────────────────────────────
--  5. CLEAN UP: Remove old columns from users
-- ────────────────────────────────────────────────────────────

-- Remove columns that moved to user_profiles
ALTER TABLE users DROP COLUMN IF EXISTS avatar_url;
ALTER TABLE users DROP COLUMN IF EXISTS banner_url;
ALTER TABLE users DROP COLUMN IF EXISTS equipped_achievement_1;
ALTER TABLE users DROP COLUMN IF EXISTS equipped_achievement_2;
ALTER TABLE users DROP COLUMN IF EXISTS equipped_achievement_3;

-- Remove old progress columns from users (they're in status_learning)
ALTER TABLE users DROP COLUMN IF EXISTS status_chapter;
ALTER TABLE users DROP COLUMN IF EXISTS status_exercise;

-- Remove old columns from chapters
ALTER TABLE chapters DROP COLUMN IF EXISTS level;
ALTER TABLE chapters DROP COLUMN IF EXISTS image_url;

-- Remove old option columns from tests (data is now in 'options')
ALTER TABLE tests DROP COLUMN IF EXISTS option_a;
ALTER TABLE tests DROP COLUMN IF EXISTS option_b;
ALTER TABLE tests DROP COLUMN IF EXISTS option_c;
ALTER TABLE tests DROP COLUMN IF EXISTS option_d;

-- ────────────────────────────────────────────────────────────
--  DONE! Your database is now restructured.
-- ────────────────────────────────────────────────────────────
