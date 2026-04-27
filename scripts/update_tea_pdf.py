import sqlite3
conn = sqlite3.connect("japanese_app.db")
cursor = conn.cursor()
cursor.execute("UPDATE chapters SET pdf_url = 'culturedocs/read1.pdf' WHERE title = 'Traditional Tea Ceremony'")
conn.commit()
conn.close()
print("Updated 'Traditional Tea Ceremony' to use 'culturedocs/read1.pdf'")
