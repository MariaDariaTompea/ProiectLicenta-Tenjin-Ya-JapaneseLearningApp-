import sqlite3

# Check backup
try:
    conn = sqlite3.connect('japanese_app_backup.db')
    c = conn.cursor()
    for t in ['hiraganacharacters', 'katakanacharacters']:
        try:
            c.execute(f"SELECT COUNT(*) FROM {t}")
            count = c.fetchone()[0]
            print(f"BACKUP - {t}: {count} rows")
            if count > 0:
                c.execute(f"SELECT * FROM {t} LIMIT 3")
                for row in c.fetchall():
                    print(f"  {row}")
        except Exception as e:
            print(f"BACKUP - {t}: {e}")
    conn.close()
except:
    print("No backup DB found")

# Check what columns exist
conn = sqlite3.connect('japanese_app.db')
c = conn.cursor()
for t in ['hiraganacharacters', 'katakanacharacters']:
    c.execute(f"PRAGMA table_info({t})")
    cols = c.fetchall()
    print(f"\n{t} columns: {[col[1] for col in cols]}")
conn.close()
