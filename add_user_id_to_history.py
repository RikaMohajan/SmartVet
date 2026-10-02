import sqlite3

conn = sqlite3.connect("database/smartvet.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE history ADD COLUMN user_id INTEGER")
    print("user_id column added successfully!")
except sqlite3.OperationalError as e:
    print("Info:", e)

conn.commit()
conn.close()
