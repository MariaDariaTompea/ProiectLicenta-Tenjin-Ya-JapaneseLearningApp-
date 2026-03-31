import sqlite3

def add_pdf_url_column():
    conn = sqlite3.connect("japanese_app.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE chapters ADD COLUMN pdf_url TEXT DEFAULT ''")
        conn.commit()
        print("Successfully added pdf_url column to chapters table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Column pdf_url already exists.")
        else:
            print(f"OperationalError: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_pdf_url_column()
