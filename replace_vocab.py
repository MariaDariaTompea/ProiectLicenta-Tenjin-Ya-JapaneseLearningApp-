import re

with open('d:/JapaneseApp/features/grammar/routes.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Grab everything from the vocabulary route to the end or next decorator
matches = re.finditer(r'@router\.get\("/course/vocabulary".*?(?=@router|$)', text, flags=re.DOTALL)
new_text = text
for match in matches:
    block = match.group(0)
    new_block = block.replace('/api/grammar', '/api/vocabulary').replace('/course/grammar', '/course/vocabulary')
    new_text = new_text.replace(block, new_block)

print("Writing file, length matches =", new_text != text)

with open('d:/JapaneseApp/features/grammar/routes.py', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Done")
