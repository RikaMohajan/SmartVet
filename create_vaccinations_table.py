import sqlite3

conn = sqlite3.connect("database/smartvet.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS vaccinations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        animal TEXT NOT NULL,
        animal_name TEXT,
        vaccine_name TEXT NOT NULL,
        given_date TEXT NOT NULL,
        next_date TEXT
    )
''')

conn.commit()
conn.close()

print("Vaccinations table created successfully!")
