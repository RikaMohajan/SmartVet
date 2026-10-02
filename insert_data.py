import sqlite3

conn = sqlite3.connect("database/smartvet.db")
cursor = conn.cursor()

diseases = [

    (
        "Cow",
        "Foot and Mouth Disease",
        "Fever, Saliva Dropping",
        "A highly contagious viral disease affecting cattle.",
        "Isolate the animal and contact a veterinarian immediately."
    ),

    (
        "Cow",
        "Pneumonia",
        "Cough, Fever",
        "Respiratory infection affecting the lungs.",
        "Keep the animal warm and seek veterinary care."
    ),

    (
        "Cow",
        "Bloat",
        "Loss of Appetite",
        "Gas accumulation in the stomach.",
        "Avoid grazing and contact a veterinarian."
    )

]

cursor.executemany("""
INSERT INTO diseases
(animal, disease_name, symptom, description, treatment)
VALUES (?, ?, ?, ?, ?)
""", diseases)

conn.commit()
conn.close()

print("Disease data inserted successfully!")