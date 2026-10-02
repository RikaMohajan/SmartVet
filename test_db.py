import sqlite3

# Database-এর সাথে সংযোগ
conn = sqlite3.connect("database/smartvet.db")
cursor = conn.cursor()

# সব Disease বের করো
cursor.execute("SELECT * FROM diseases")

rows = cursor.fetchall()

# Terminal-এ দেখাও
for row in rows:
    print(row)

conn.close()