import sqlite3

conn = sqlite3.connect("database/smartvet.db")
cursor = conn.cursor()

diseases = [

(
    "Goat",
    "PPR",
    "Fever, Cough, Diarrhea",
    "A highly contagious viral disease of goats.",
    "Isolate the goat and contact a veterinarian immediately."
),

(
    "Goat",
    "Pneumonia",
    "Cough, Fever",
    "Respiratory infection affecting goats.",
    "Keep the goat warm and seek veterinary treatment."
),

(
    "Goat",
    "Coccidiosis",
    "Diarrhea, Weight Loss",
    "A parasitic intestinal disease.",
    "Provide clean water and appropriate medication."
),

(
    "Goat",
    "Foot Rot",
    "Lameness",
    "A bacterial infection affecting the feet.",
    "Clean the hoof and consult a veterinarian."
),

(
    "Goat",
    "Orf",
    "Skin Lesion",
    "A contagious viral skin disease.",
    "Separate infected goats and maintain hygiene."
)

]

cursor.executemany("""
INSERT INTO diseases
(animal, disease_name, symptom, description, treatment)
VALUES (?, ?, ?, ?, ?)
""", diseases)

conn.commit()
conn.close()

print("Goat diseases added successfully!")