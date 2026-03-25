# Tenjin'ya (天神屋) — Innovative Japanese Language Learning

Tenjin'ya is an advanced language learning application initially designed for learning Japanese, with a high potential to be expanded to more languages. Unlike common platforms, Tenjin'ya provides a comprehensive and immersive path to fluency by focusing on the foundational elements of the language—starting with its unique writing systems—and integrating deep cultural context. We bridge the gap between mechanical memorization and true linguistic comprehension.

---

## 🎨 Concept & Philosophy

Through testing, analysis of existing apps, and research into platforms such as **Duolingo**, **HelloTalk**, and **Shinobi**, three main limitations were identified that Tenjin'ya improves upon:

### 1. Writing System Mastery (Hiragana, Katakana, Kanji)
The core reason Japanese was chosen as our starting language is because it contains non-Latin writing systems that require comprehension before grammar or vocabulary. Most popular apps skip this arduous task, jumping directly into words written in Latin transliterations (Romaji) or dialysis without a proper base. 
**Our Solution:** Tenjin'ya adds a vital piece missing from generic apps. We provide basic courses to visualize and practice the characters of **Hiragana**, **Katakana**, and **Kanji**. We include recognition tests to confirm a learner’s understanding before they move to advanced grammar.

### 2. Achievement-Based Motivation vs. Toxic Competition
Many apps create a competitive environment where users eventually focus more on gathering points or "streaks" than actually learning. This often leads to users exploiting the system for rewards, reducing the platform's educational value.
**Our Solution:** Tenjin'ya introduces a different motivational mechanism based on **individual achievements**. Instead of competing directly against others through rankings or leaderboards, users unlock missions and improve skills in different chapters. We keep competition healthy; users can visualize others' achievements, but the focus remains on personal goals rather than direct comparison.

### 3. Cultural Context & Interactive Learning
Modern language apps often lack a correlation to culture, neglecting the social context of speech. In Japanese, certain expressions must be adapted based on social context, age, or hierarchy.
**Our Solution:** Tenjin'ya implements an **interactive cultural learning module**. This help learners understand the society in which the language is used, ensuring they communicate appropriately and with nuance.

---

## 🏗️ Technical Architecture

Tenjin'ya aims not only to explore existing app abilities but to bring innovation through a well-crafted aesthetic and modern tech stack.

### **The Backend: FastAPI & Uvicorn**
The `main.py` file represents the application's entry point, initializing and configuring the **FastAPI** server. 
- **FastAPI:** A modern, high-performance web framework using Python type hints for automatic validation and interactive API documentation (accessible at `/docs`).
- **ASGI Standard:** FastAPI is based on the Asynchronous Server Gateway Interface, designed to handle multiple requests simultaneously for high efficiency.
- **Uvicorn:** A lightweight, high-performance ASGI server that executes the app on `127.0.0.1:8000`.
- **Static Resources:** Images, audio, icons, textures, and videos are served via the `StaticFiles` module, mounted to specific paths (e.g., `/audio`, `/images`) for accessibility by the frontend.

### **Database Strategy: Supabase & PostgreSQL**
Our core data infrastructure utilizes the **Supabase** platform to host a **PostgreSQL** database. 
- **PostgreSQL:** An industry-standard Relational Database Management System (RDBMS) supporting SQL, concurrency control, and diverse data types.
- **Cloud Hosting:** The database runs on Supabase's cloud servers rather than locally, offering superior scalability and API integration.

### **Data Layer: SQLAlchemy ORM**
To interact with the database efficiently, we use **SQLAlchemy**, a Python Object-Relational Mapping (ORM) library. This acts as an abstraction layer:
- **Python Classes:** Database tables are defined as Python classes mapping directly to the DB.
- **Readability & Security:** It improves maintainability and prevents SQL injection by translating Python expressions into SQL commands.
- **`database.py` Breakdown:**
  - `Sessionmaker`: Creates new sessions for requests.
  - `get_db()`: Manages session lifecycle for each request.
  - `create_engine`: Uses the Supabase URL to connect to the database.
  - `declarative_base()`: Maps Python classes to PostgreSQL tables.

---

## 📂 Innovation: Grammar vs. Vocabulary Modules

Most apps pick basic words and cycle them to teach grammar. Without auxiliary book support, users lack the choice to learn conversational vocabulary.
**Tenjin'ya's Solution:** We separated the logic into two distinct modules:
1. **Grammar Module:** Focuses on particles, verb endings, and sentence structure.
2. **Vocabulary Module:** Allows users to learn words outside the grammar scope.
Users can learn specific vocabulary for each chapter and then apply those connections more efficiently within the grammar section. This dual-pathway ensures you have the necessary "tools" (words) before you try to build the "house" (sentences).

---

## 🚀 Getting Started

### **Startup**
The database schema is initialized automatically via `Base.metadata.create_all(bind=engine)`, creating tables if they do not exist.
To run the server locally:
```bash
.venv\Scripts\python.exe -m uvicorn main:app --port 8000 --reload
```

---

## 📚 References & Research

Our improvements were driven by observations of modern language trends—such as the massive rise in Chinese and Japanese speakers in 2025—and studies on effective acquisition:

- **Kukulska-Hulme, A., & Shield, L. (2008).** *An overview of mobile assisted language learning.* ReCALL Journal.s
- **Deterding, S., Dixon, D., Khaled, R., & Nacke, L. (2011).** *From Game Design Elements to Gamefulness: Defining “Gamification”.*
- **Vesselinov, R., & Grego, J. (2012).** *Duolingo Effectiveness Study.*

*“Evolution and justification through confidence and a well-crafted aesthetic: Tenjin'ya helps people achieve the results they wanted by solving the problems inherent in outdated platforms.”*

---

## 🗄️ Database Restructuring (March 2025)

The database has been restructured for better scalability and separation of concerns.

### What Changed

| Before | After |
|--------|-------|
| `users` table held avatar, banner, achievements, and progress | `users` simplified to core account data only |
| No dedicated profile storage | **New `user_profiles` table** — avatar, banner, equipped achievements |
| No photo upload tracking | **New `user_photos` table** — uploaded images with type and timestamp |
| Chapters had a `level` text field and `image_url` | **New `proficiencies` table** (N5→N1) — chapters reference `proficiency_id` |
| Tests had rigid `option_a/b/c/d` columns | Tests use flexible `options` JSON + `test_type` field |

### New Schema Hierarchy

```
Proficiency (N5, N4, N3, N2, N1)
  └── Chapter (grammar / vocabulary / culture)
        └── Exercise (quiz, course, examination, interactive)
              └── Test (multiple_choice, sentence_builder, matching, text_input, fill_blank, true_false)
```

### Tables Overview

| Table | Purpose |
|-------|---------|
| `users` | Core account: email, name, password, nickname, current_level |
| `user_profiles` | Avatar URL, banner URL, 3 equipped achievement slots |
| `user_photos` | Tracks uploaded photos (type: avatar/banner/gallery) |
| `user_items` | Inventory of owned items (achievements, banners) |
| `status_learning` | Per-module progress (grammar chapter/exercise, vocabulary chapter/exercise) |
| `proficiencies` | JLPT levels: N5 (Beginner) → N1 (Advanced) |
| `chapters` | Grouped under proficiency, categorised as grammar/vocabulary/culture |
| `exercises` | Inside chapters, with exercise_type and XP points |
| `tests` | Individual questions with flexible JSON options, test_type determines UI |
| `achievements` | Collectible items with name, description, image |

---

## 🎮 Exercise System Architecture (Planned)

The exercise runner will support Duolingo-style interactive question types for grammar exercises.

### Supported Test Types

| Type | Description |
|------|-------------|
| `multiple_choice` | Pick the correct answer from 4 options |
| `sentence_builder` | Arrange word blocks into the correct sentence |
| `matching` | Match pairs (Japanese ↔ English) |
| `text_input` | Type the answer freely |
| `fill_blank` | Complete a sentence with the missing word |
| `true_false` | True or false statement |

### Implementation Structure

```
features/exercises/
├── routes.py              — /exercise/{id} unified endpoint
├── renderer.py            — one render function per test_type
└── templates/
    └── exercise_runner.py — lesson page with progress bar and results
```

Each `Test` row in the database has a `test_type` that tells the frontend which renderer to use, and an `options` JSON column with type-specific data. Adding a new exercise type only requires adding a new render function and registering it.
