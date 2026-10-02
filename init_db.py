import sqlite3

conn = sqlite3.connect("database/smartvet.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS diseases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal TEXT,
    disease_name TEXT,
    symptom TEXT,
    description TEXT,
    treatment TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")