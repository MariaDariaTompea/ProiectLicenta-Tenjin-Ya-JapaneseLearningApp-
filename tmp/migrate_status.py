import sqlite3

def migrate():
    conn = sqlite3.connect('japanese_app.db')
    cursor = conn.cursor()
    columns_to_add = [
        ("status_learning", "status_chapter_culture", "INTEGER", "1"),
        ("status_learning", "status_exercise_culture", "INTEGER", "1"),
    ]
    for table, col, col_type, default_val in columns_to_add:
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type} DEFAULT {default_val};")
            print(f"Added {col} to {table}.")
        except sqlite3.OperationalError as e:
            print(f"Error for {col}: {e}")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
