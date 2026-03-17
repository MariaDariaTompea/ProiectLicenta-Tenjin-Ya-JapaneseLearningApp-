# JapaneseApp

## Overview
JapaneseApp is a comprehensive web application designed to help users learn Japanese language and culture interactively. Built with FastAPI, SQLAlchemy, and PostgreSQL, it offers a variety of exercises, achievements, customizable profiles, and multimedia resources (audio, images, videos) to enhance the learning experience.

---

## Basic Concept
The app provides:
- **Language Learning:** Hiragana, Katakana, and Japanese vocabulary exercises.
- **User Profiles:** Customizable avatars, settings, unlockable achievements and banners.
- **Courses:** Structured learning paths for Japanese language and culture.
- **Achievements:** Track progress and unlock rewards.
- **Multimedia:** Audio, images, and videos for immersive learning.
- **Authentication:** Secure user login and profile management.

---

## Main Files & Structure

### Root Directory
- `database.py`: Sets up the SQLAlchemy engine, session, and base for database models. Connects to PostgreSQL.
- `main.py`: FastAPI app entrypoint. Mounts static files, includes routers, and starts the server.

### JapaneseApp/
- `database.py`: Duplicate of root, used for internal imports.
- `main.py`: Main FastAPI app logic.
- `routes/`: Contains route files for different app features.
  - `auth_routes.py`: Authentication endpoints (login, register).
  - `profile_routes.py`: User profile management.
  - `course_routes.py`: Course and learning path endpoints.
  - `japanese_routes.py`: Japanese language exercises and content.
  - `__init__.py`: Combines all routers for inclusion in the app.
- `models/`: SQLAlchemy models for database tables.
  - `achievement.py`: Achievement model.
  - `exercises.py`: Exercise model.
  - `japanese.py`: Japanese language model.
  - `user.py`: User model.
  - `__init__.py`: Model package initializer.
- `templates/`: Template files for rendering responses.
  - `achievements_templates.py`: Achievement-related templates.
  - `auth_templates.py`: Authentication templates.
  - `hiragana_templates.py`: Hiragana learning templates.
  - `katakana_templates.py`: Katakana learning templates.
  - `profile_templates.py`: Profile templates.
  - `__init__.py`: Template package initializer.
- `audio/`, `images/`, `icons/`, `textures/`, `videos/`: Static directories for multimedia assets.
- `katakana_assets/`: Additional multimedia for Katakana learning.
- `customisableprofile/`: Avatars, settings, achievements, banners for user customization.

---

## Key Technologies
- **FastAPI:** Web framework for building APIs.
- **SQLAlchemy:** ORM for database models and queries.
- **PostgreSQL:** Database backend.
- **Uvicorn:** ASGI server for running FastAPI.
- **psycopg2-binary:** PostgreSQL driver.

---

## How It Works
1. **User Authentication:** Users register and log in. Profiles are created and managed.
2. **Learning Modules:** Users access courses, exercises, and multimedia content.
3. **Progress Tracking:** Achievements and progress are tracked in the database.
4. **Customization:** Users unlock avatars, banners, and achievements.
5. **Static Files:** Multimedia assets are served for interactive learning.

---

## App Startup
- The app is started via `main.py` or with Uvicorn:
  ```bash
  python JapaneseApp/main.py
  # or
  uvicorn JapaneseApp.main:app --reload
  ```
- Static files are mounted for easy access.
- Routers are included for modular API endpoints.

---

## Database
- Connection string is set in `database.py`.
- Models define tables for users, achievements, exercises, etc.
- Uses SQLAlchemy ORM for queries and migrations.

---

## Customization & Achievements
- Users can customize their profile with avatars, banners, and unlockable achievements.
- Achievements are tracked and displayed.

---

## Multimedia
- Audio, images, and videos are used for immersive learning.
- Katakana and Hiragana assets are separated for focused study.

---

## Templates
- Templates render responses for achievements, authentication, hiragana, katakana, and profiles.

---

## Routes
- `/auth`: Authentication endpoints.
- `/profile`: Profile management.
- `/course`: Course and learning path endpoints.
- `/japanese`: Japanese language exercises.
- `/images`, `/audio`, `/icons`, `/textures`, `/videos`: Static file endpoints.

---

## Extending the App
- Add new models in `models/`.
- Add new routes in `routes/`.
- Add new templates in `templates/`.
- Add new static assets in their respective directories.

---

## Troubleshooting
- Ensure all dependencies are installed: `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`.
- Check database connection string in `database.py`.
- Run the app with Uvicorn for live reload and debugging.
- Static files must exist in their directories to avoid errors.

---

## License & Credits
- Open source project for educational purposes.
- Built with FastAPI, SQLAlchemy, and PostgreSQL.

---

## Contact
For questions or contributions, open an issue or contact the maintainer.
