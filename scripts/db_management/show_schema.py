import sqlite3

conn = sqlite3.connect("japanese_app.db")
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print("=" * 50)
print("  NEW DATABASE SCHEMA")
print("=" * 50)

for (table_name,) in tables:
    print(f"\n--- {table_name} ---")
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    for col in columns:
        col_id, name, col_type, notnull, default, pk = col
        flags = []
        if pk:
            flags.append("PK")
        if notnull:
            flags.append("NOT NULL")
        if default is not None:
            flags.append(f"default={default}")
        flag_str = f"  [{', '.join(flags)}]" if flags else ""
        print(f"  {name:30s} {col_type:10s}{flag_str}")

conn.close()
