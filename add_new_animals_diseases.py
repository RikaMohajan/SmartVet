import sqlite3

conn = sqlite3.connect("database/smartvet.db")
cursor = conn.cursor()

diseases = [

("Dog","Canine Distemper","Fever, Cough, Diarrhea","A serious viral disease affecting multiple organs.","Isolate the dog and seek veterinary treatment immediately."),
("Dog","Parvovirus","Diarrhea, Loss of Appetite, Fever","A highly contagious viral intestinal disease.","Keep hydrated and consult a vet urgently, especially in puppies."),
("Dog","Kennel Cough","Cough, Fever","A contagious respiratory infection.","Rest, isolate from other dogs, consult a vet if it persists."),
("Dog","Mange","Skin Lesion","A skin disease caused by mites.","Keep skin clean and consult a vet for medicated treatment."),

("Cat","Feline Distemper","Fever, Diarrhea, Loss of Appetite","A serious viral disease common in unvaccinated cats.","Isolate and seek veterinary treatment immediately."),
("Cat","Feline Flu","Cough, Fever, Difficulty Breathing","A common viral respiratory infection in cats.","Keep warm, ensure hydration, consult a vet."),
("Cat","Ringworm","Skin Lesion","A fungal infection affecting skin and fur.","Isolate from other pets and apply vet-prescribed treatment."),

("Pigeon","Paramyxovirus","Diarrhea, Loss of Appetite","A viral disease affecting the nervous and digestive system.","Isolate affected birds and consult a vet."),
("Pigeon","Pigeon Pox","Skin Lesion, Fever","A viral disease causing skin lesions.","Isolate infected birds, keep loft clean and dry."),
("Pigeon","Respiratory Infection","Cough, Difficulty Breathing","A common bacterial or viral respiratory illness.","Improve ventilation and consult a vet for treatment."),

("Fish","Fin Rot","Skin Lesion","A bacterial infection affecting fins and skin.","Improve water quality and use appropriate treatment."),
("Fish","Ich (White Spot Disease)","Skin Lesion, Loss of Appetite","A common parasitic infection in fish.","Raise water temperature gradually and treat water with medication."),
("Fish","Dropsy","Loss of Appetite","A bacterial infection causing swelling.","Isolate affected fish and improve water conditions."),

("Rabbit","Myxomatosis","Skin Lesion, Fever","A serious viral disease spread by insects.","Isolate immediately and consult a vet; often fatal if untreated."),
("Rabbit","Rabbit Hemorrhagic Disease","Loss of Appetite, Fever","A highly contagious and often fatal viral disease.","Isolate and seek urgent veterinary care."),
("Rabbit","Snuffles","Cough, Difficulty Breathing","A common respiratory infection in rabbits.","Keep housing clean and dry, consult a vet for antibiotics.")

]

cursor.executemany("""
INSERT INTO diseases
(animal,disease_name,symptom,description,treatment)
VALUES(?,?,?,?,?)
""", diseases)

conn.commit()
conn.close()

print("New animal diseases added successfully!")
