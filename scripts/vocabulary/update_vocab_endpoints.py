import re

with open('d:/JapaneseApp/features/grammar/routes.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure we don't accidentally update the grammar endpoints
def update_vocabulary_block(match):
    block = match.group(0)
    block = re.sub(r'/api/grammar', '/api/vocabulary', block)
    block = re.sub(r'/course/grammar', '/course/vocabulary', block)
    return block

# Find the vocabulary route definition and update only that part
updated_text = re.sub(
    r'@router\.get\("/course/vocabulary".*?def course_vocabulary\(\).*?return r"""(.*?)"""',
    update_vocabulary_block,
    text,
    flags=re.DOTALL
)

if updated_text != text:
    with open('d:/JapaneseApp/features/grammar/routes.py', 'w', encoding='utf-8') as f:
        f.write(updated_text)
    print("Updated Vocabulary specific endpoints")
