import spacy
from spacy.training.example import Example
import csv
import random

def train_model(output_dir="Model/skills", iterations=20):
    nlp = spacy.blank("en") 

    ner = nlp.add_pipe("ner", name="ner", last=True)
    ner.add_label("SKILL")  

    TRAIN_DATA = []
    count = 0
    with open('data/newSkills.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            skill_text = row[0].strip()  
            if skill_text:  
                doc = nlp.make_doc(skill_text)
                entities = [(0, len(skill_text), "SKILL")]
                TRAIN_DATA.append((doc, {"entities": entities}))
        count += 1
        print("Loaded", count, "skills from CSV")

    nlp.begin_training()

    for itn in range(iterations):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            example = Example.from_dict(text, annotations)
            nlp.update([example], drop=0.5, losses=losses)

        print("Iteration:", itn+1, "Loss:", losses)

    nlp.to_disk(output_dir)
    print("Trained model saved to:", output_dir)
    return nlp

trained_model = train_model()