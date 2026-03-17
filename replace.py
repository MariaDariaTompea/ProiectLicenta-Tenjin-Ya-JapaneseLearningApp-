import os
import re

base_dir = r"d:\JapaneseApp"

def replace_in_file(filepath, replacements):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements:
        new_content = re.sub(old, new, new_content)

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

replacements = [
    # database
    (r"from core.database import", "from core.database import"),
    
    # models
    (r"from models\.user import", "from features.user.models import"),
    (r"from models\.japanese import", "from features.japanese.models import"),
    (r"from models\.achievement import", "from features.customization.models import"),
    (r"from models\.exercises import", "from features.grammar.models import"),
    
    # templates
    (r"from templates\.auth_templates import", "from features.user.templates.auth import"),
    (r"from templates\.hiragana_templates import", "from features.japanese.templates.hiragana import"),
    (r"from templates\.katakana_templates import", "from features.japanese.templates.katakana import"),
    (r"from templates\.profile_templates import", "from features.customization.templates.profile import"),
    (r"from templates\.achievements_templates import", "from features.customization.templates.achievements import"),
]

# Specifically handling "from features.user.models import User, Achievement..."
# It's better to just manually replace the models/templates imports in each file, as they are a few lines.
