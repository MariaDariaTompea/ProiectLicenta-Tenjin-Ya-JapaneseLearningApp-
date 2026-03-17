# Tenjin'ya (天神屋) — Innovative Japanese Language Learning

Tenjin'ya is an advanced language learning application designed to provide a comprehensive and immersive path to Japanese fluency. By focusing on the foundational elements of the language—starting with its unique writing systems—and integrating cultural context, Tenjin'ya bridges the gap between mechanical memorization and true linguistic comprehension.

---

## 🎨 Concept & Philosophy

Through testing and analysis of existing platforms like Duolingo, HelloTalk, and Shinobi, Tenjin'ya identifies and addresses three critical limitations in modern language learning apps:

### 1. Writing System Mastery (Hiragana, Katakana, Kanji)
Most apps skip the arduous task of teaching characters, forcing learners to jump directly into vocabulary using Latin transliterations (Romaji). Tenjin'ya prioritizes **Character Mastery**. It provides dedicated modules to visualize, practice, and recognize Hiragana, Katakana, and Kanji before moving to advanced grammar. We believe that a strong foundation in the writing system is essential for efficient long-term acquisition.

### 2. Achievement-Based Motivation vs. Toxic Competition
Many apps use "streaks" and competitive leaderboards that eventually pressure users to "cheat" the system for points rather than focusing on learning. 
Tenjin'ya introduces a **Personal Achievement System**. Instead of competing against others, users unlock unique achievements by completing missions and mastering chapters at their own pace. This maintains high engagement through personal growth rather than stressful comparison.

### 3. Cultural Context & Nuance
Language does not exist in a vacuum. Most apps neglect the cultural nuances that dictate how Japanese is actually spoken—such as honorifics and social hierarchy. Tenjin'ya includes **Interactive Cultural Learning Modules** that explain the "why" behind expressions, helping learners communicate appropriately in real-world Japanese society.

---

## 🏗️ Technical Architecture

### **The Backend: FastAPI & Uvicorn**
Tenjin'ya is powered by **FastAPI**, a modern, high-performance Python web framework. 
- **Asynchronous Processing:** Built on the **ASGI** standard, FastAPI handles multiple requests concurrently, ensuring a snappy user experience.
- **Automatic Documentation:** Provides interactive API docs (Swagger/OpenAPI) at `/docs` for seamless testing.
- **Uvicorn:** A lightning-fast ASGI server that hosts the application and handles communication between the app and the web.

### **Database Strategy: Supabase & PostgreSQL**
Rather than a local file, Tenjin'ya utilizes a cloud-hosted **PostgreSQL** database managed by **Supabase**.
- **PostgreSQL:** An industry-standard relational database (RDBMS) known for its reliability, concurrency control, and support for complex data types.
- **Cloud Hosting:** By using Supabase, the data is accessible, secure, and independent of local hardware.

### **Data Layer: SQLAlchemy ORM**
The application uses **SQLAlchemy** as an Object-Relational Mapping (ORM) layer.
- **Abstraction:** Database tables are defined as Python classes, allowing us to perform operations using clean Python code instead of raw SQL.
- **Security:** Built-in protection against SQL injection and improved maintainability.

---

## 📂 Project Structure (Feature-Based)

The codebase follows a modular **Feature-Based Architecture**, making it easy to extend for new languages or modules:

- **`core/`**: Central application logic, database connection handling (`database.py`), and foundational settings.
- **`features/`**:
  - **`grammar/`**: Routes and logic for the curriculum, including the horizontal "Belt" navigation system.
  - **`customization/`**: User profile management, avatar uploads, and achievement tracking.
- **`static/`**: Centralized storage for multimedia assets including:
  - `/images` & `/textures`: High-quality UI elements and backgrounds.
  - `/audio`: Native pronunciation guides.
  - `/videos`: Character stroke animations (e.g., the running fox transitions).

---

## 🚀 Getting Started

### **Prerequisites**
- Python 3.12+
- Virtual environment (`.venv`)

### **Execution**
To start the application locally:
```bash
# Activate your environment
.venv\Scripts\activate

# Run the server
python -m uvicorn main:app --port 8000 --reload
```
The app will be available at `http://127.0.0.1:8000`.

---

## 📚 References

The development of Tenjin'ya was informed by key research in Mobile Assisted Language Learning (MALL) and Gamification:

- **Kukulska-Hulme, A., & Shield, L. (2008).** *An overview of mobile assisted language learning: From content delivery to supported collaboration and interaction.* ReCALL Journal.
- **Deterding, S., Dixon, D., Khaled, R., & Nacke, L. (2011).** *From Game Design Elements to Gamefulness: Defining “Gamification”.* Proceedings of the 15th International Academic MindTrek Conference.
- **Vesselinov, R., & Grego, J. (2012).** *Duolingo Effectiveness Study.* City University of New York.

---

*“Evolution and justification through well-crafted aesthetics — Tenjin'ya is about helping people achieve the linguistic results they actually want.”*
