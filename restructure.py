import os
import shutil

base_dir = r"d:\JapaneseApp"

def mkdir(path):
    os.makedirs(os.path.join(base_dir, path), exist_ok=True)

# 1. DELETE DUPLICATE FOLDER
dup_dir = os.path.join(base_dir, "JapaneseApp")
if os.path.exists(dup_dir):
    shutil.rmtree(dup_dir)

# 2. CREATE NEW DIRECTORIES
new_dirs = [
    "core",
    "features/customization/static",
    "features/customization/templates",
    "features/grammar/templates",
    "features/user/templates",
    "features/japanese/templates",
    "features/japanese/static"
]
for d in new_dirs:
    mkdir(d)

# 3. STATIC FILES
static_folders = ["customisableprofile", "icons", "images", "textures", "videos"]
for folder in static_folders:
    src = os.path.join(base_dir, folder)
    dst = os.path.join(base_dir, "features", "customization", "static", folder)
    if os.path.exists(src):
        shutil.move(src, dst)

other_static = ["katakana_assets", "audio"]
for folder in other_static:
    src = os.path.join(base_dir, folder)
    if os.path.exists(src):
        dst = os.path.join(base_dir, "features", "japanese", "static", folder)
        shutil.move(src, dst)

# 4. MOVE FILES TO RESPECTIVE DIRECTORIES
moves = {
    # database
    "database.py": "core/database.py",

    # customization
    "routes/profile_routes.py": "features/customization/routes.py",
    "models/achievement.py": "features/customization/models.py",
    "templates/profile_templates.py": "features/customization/templates/profile.py",
    "templates/achievements_templates.py": "features/customization/templates/achievements.py",

    # user
    "routes/auth_routes.py": "features/user/routes.py",
    "models/user.py": "features/user/models.py",
    "templates/auth_templates.py": "features/user/templates/auth.py",

    # grammar
    "routes/course_routes.py": "features/grammar/routes.py",
    "models/exercises.py": "features/grammar/models.py",

    # japanese
    "routes/japanese_routes.py": "features/japanese/routes.py",
    "models/japanese.py": "features/japanese/models.py",
    "templates/hiragana_templates.py": "features/japanese/templates/hiragana.py",
    "templates/katakana_templates.py": "features/japanese/templates/katakana.py",
}

for src_path, dst_path in moves.items():
    s = os.path.join(base_dir, src_path)
    d = os.path.join(base_dir, dst_path)
    # create the parent directory of dst just in case
    os.makedirs(os.path.dirname(d), exist_ok=True)
    if os.path.exists(s):
        shutil.move(s, d)

# 5. CREATE __init__.py files
init_dirs = [
    "core",
    "features",
    "features/customization", "features/customization/templates",
    "features/user", "features/user/templates",
    "features/grammar", 
    "features/japanese", "features/japanese/templates"
]
for d in init_dirs:
    with open(os.path.join(base_dir, d, "__init__.py"), "w") as f:
        f.write("")

# Delete old models, routes, templates folders
for folder in ["models", "routes", "templates"]:
    fp = os.path.join(base_dir, folder)
    if os.path.exists(fp):
        shutil.rmtree(fp)

print("done")
