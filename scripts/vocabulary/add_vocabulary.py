import re

with open('d:/JapaneseApp/features/grammar/routes.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Grab the python string literal corresponding to course_grammar
matches = re.search(r'@router\.get\("/course/grammar".*?def course_grammar\(\):\s*return r"""(.*?)"""', text, re.DOTALL)
grammar_html = matches.group(1) if matches else ''

# Replace grammar with vocabulary where necessary
vocab_html = grammar_html.replace('Grammar', 'Vocabulary').replace('grammar', 'vocabulary')

vocab_route = '\n@router.get("/course/vocabulary", response_class=HTMLResponse)\nasync def course_vocabulary():\n    return r"""' + vocab_html + '"""\n'

if 'def course_vocabulary' not in text:
    with open('d:/JapaneseApp/features/grammar/routes.py', 'a', encoding='utf-8') as f:
        f.write('\n\n# ─────────────────────────────────────────────────────────\n#  VOCABULARY PAGE\n# ─────────────────────────────────────────────────────────\n')
        f.write(vocab_route)
    print('Vocabulary page added')
