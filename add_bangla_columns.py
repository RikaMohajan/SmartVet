import sqlite3

conn = sqlite3.connect("database/smartvet.db")
cursor = conn.cursor()

for col in ["disease_name_bn", "description_bn", "treatment_bn"]:
    try:
        cursor.execute(f"ALTER TABLE diseases ADD COLUMN {col} TEXT")
        print(col, "added")
    except sqlite3.OperationalError as e:
        print(col, "-", e)

conn.commit()
conn.close()
