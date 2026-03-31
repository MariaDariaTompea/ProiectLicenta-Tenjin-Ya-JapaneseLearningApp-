import sqlite3
conn = sqlite3.connect("japanese_app.db")
cursor = conn.cursor()
cursor.execute("SELECT id, title, category, pdf_url FROM chapters")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
