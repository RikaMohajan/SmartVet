import sqlite3

conn = sqlite3.connect("database/smartvet.db")
cursor = conn.cursor()

diseases = [

(
    "Chicken",
    "Newcastle Disease",
    "Fever, Cough, Difficulty Breathing",
    "A highly contagious viral disease affecting chickens.",
    "Isolate infected birds and consult a veterinarian."
),

(
    "Chicken",
    "Avian Influenza",
    "Fever, Cough",
    "A serious viral disease affecting poultry.",
    "Report immediately and isolate infected birds."
),

(
    "Chicken",
    "Coccidiosis",
    "Diarrhea, Loss of Appetite",
    "A parasitic disease affecting the intestine.",
    "Provide anticoccidial medicine and clean drinking water."
),

(
    "Chicken",
    "Fowl Pox",
    "Skin Lesion, Fever",
    "A viral disease causing lesions on skin and mouth.",
    "Separate infected birds and vaccinate healthy birds."
),

(
    "Chicken",
    "Infectious Bronchitis",
    "Cough, Difficulty Breathing",
    "A contagious respiratory disease.",
    "Improve ventilation and seek veterinary advice."
)

]

cursor.executemany("""
INSERT INTO diseases
(animal, disease_name, symptom, description, treatment)
VALUES (?, ?, ?, ?, ?)
""", diseases)

conn.commit()
conn.close()

print("Chicken diseases added successfully!")