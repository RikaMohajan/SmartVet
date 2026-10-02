import sqlite3

conn = sqlite3.connect("database/smartvet.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    animal TEXT,

    symptoms TEXT,

    disease TEXT,

    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()
conn.close()

print("History table created successfully!")