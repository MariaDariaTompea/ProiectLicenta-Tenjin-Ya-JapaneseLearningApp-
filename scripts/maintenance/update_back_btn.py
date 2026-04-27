import re

def update_back_btn(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    new_btn = '<a class="back-btn" href="/welcome" title="Back to Menu"><svg viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg></a>'

    # Try matching <a ... class="back-btn" ... > ... </a>
    updated_text = re.sub(
        r'<a[^>]*class=["\']?back-btn["\']?[^>]*>.*?</a>',
        new_btn,
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    if updated_text != text:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_text)
        print('Updated ' + filepath)

update_back_btn('d:/JapaneseApp/features/customization/templates/achievements.py')
update_back_btn('d:/JapaneseApp/features/customization/templates/profile.py')
update_back_btn('d:/JapaneseApp/features/grammar/routes.py')
