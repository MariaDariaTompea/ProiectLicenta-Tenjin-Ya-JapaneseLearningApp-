import sqlite3

def add_column():
    conn = sqlite3.connect('japanese_app.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE chapters ADD COLUMN image_url TEXT DEFAULT '';")
        conn.commit()
        print("Column 'image_url' added successfully.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Column 'image_url' already exists.")
        else:
            print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_column()
