import sqlite3

def check_chapters_schema():
    conn = sqlite3.connect("japanese_app.db")
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(chapters)")
    columns = cursor.fetchall()
    print("--- Chapters Table Schema ---")
    for col in columns:
        print(col)
        
    conn.close()

if __name__ == "__main__":
    check_chapters_schema()
