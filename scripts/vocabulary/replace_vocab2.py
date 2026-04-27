import re

with open('d:/JapaneseApp/features/grammar/routes.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Grab the grammar html string
match = re.search(r'@router\.get\("/course/grammar", response_class=HTMLResponse\)\nasync def course_grammar\(\):\n    return r"""(.*?)"""\n', text, re.DOTALL)
if match:
    grammar_html = match.group(1)
    
    # Replace grammar text with vocabulary
    vocab_html = grammar_html.replace('Grammar', 'Vocabulary').replace('grammar', 'vocabulary')
    vocab_html = vocab_html.replace('/api/grammar', '/api/vocabulary')
    vocab_html = vocab_html.replace('/course/grammar', '/course/vocabulary')
    
    # Grab the existing vocabulary function
    old_vocab_match = re.search(r'@router\.get\("/course/vocabulary", response_class=HTMLResponse\)\nasync def course_vocabulary\(\):\n    return """(.*?)"""\n', text, re.DOTALL)
    
    if old_vocab_match:
        old_block = old_vocab_match.group(0)
        new_block = f'@router.get("/course/vocabulary", response_class=HTMLResponse)\nasync def course_vocabulary():\n    return r"""{vocab_html}"""\n'
        
        new_text = text.replace(old_block, new_block)
        with open('d:/JapaneseApp/features/grammar/routes.py', 'w', encoding='utf-8') as f:
            f.write(new_text)
        print("Vocabulary page fully replaced and implemented.")
    else:
        print("Couldn't find the old vocabulary route.")
else:
    print("Couldn't find grammar HTML")

