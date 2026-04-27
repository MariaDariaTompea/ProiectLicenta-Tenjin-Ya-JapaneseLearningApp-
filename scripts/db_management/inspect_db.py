import sqlite3

def check_db():
    conn = sqlite3.connect("japanese_app.db")
    cursor = conn.cursor()
    
    print("--- User Items ---")
    cursor.execute("SELECT * FROM user_items")
    items = cursor.fetchall()
    for row in items:
        print(row)
        
    print("\n--- Users ---")
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for row in users:
        print(row)
    
    print("\n--- Status Learning ---")
    cursor.execute("SELECT * FROM status_learning")
    status = cursor.fetchall()
    for row in status:
        print(row)
    
    conn.close()

if __name__ == "__main__":
    check_db()
