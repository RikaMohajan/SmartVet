import sqlite3

conn = sqlite3.connect("database/smartvet.db")
cursor = conn.cursor()

diseases = [

("Cow","Lumpy Skin Disease","Skin Lesion, Fever","A viral disease causing skin nodules and fever.","Isolate the animal and contact a veterinarian."),

("Cow","Milk Fever","Loss of Appetite, Weakness","A metabolic disease due to low calcium.","Provide calcium treatment immediately."),

("Cow","Anthrax","Fever, Weakness","A serious bacterial disease.","Do not touch the carcass. Inform livestock authority."),

("Cow","Mastitis","Swollen Udder, Fever","Udder infection affecting milk production.","Keep udder clean and seek veterinary treatment."),

("Cow","Black Quarter","Fever, Lameness","A bacterial disease affecting muscles.","Immediate veterinary treatment required.")

]

cursor.executemany("""
INSERT INTO diseases
(animal,disease_name,symptom,description,treatment)
VALUES(?,?,?,?,?)
""", diseases)

conn.commit()
conn.close()

print("More Cow diseases added successfully!")