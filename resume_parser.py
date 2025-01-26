import re
import fitz
import streamlit as st
import spacy
import csv
import nltk

nltk.download('punkt')

nlp = spacy.load('en_core_web_sm')

def load_keywords(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return set(row[0] for row in reader)

def extract_name(doc):
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            names = ent.text.split()
            if len(names) >= 2 and names[0].istitle() and names[1].istitle():
                return names[0], ' '.join(names[1:])
    return "", ""


def extract_email(doc):
    matcher = spacy.matcher.Matcher(nlp.vocab)
    email_pattern = [{'LIKE_EMAIL': True}]
    matcher.add('EMAIL', [email_pattern])

    matches = matcher(doc)
    for match_id, start, end in matches:
        if match_id == nlp.vocab.strings['EMAIL']:
            return doc[start:end].text
    return ""


def extract_contact_number_from_resume(doc):
    contact_number = None
    text = doc.text  # Extract text from SpaCy doc object
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()
    return contact_number


def extract_education_from_resume(doc):
    universities = []

    doc = nlp(doc)

    for entity in doc.ents:
        if entity.label_ == "ORG" and ("university" in entity.text.lower() or "college" in entity.text.lower() or "institute" in entity.text.lower()):
            universities.append(entity.text)

    return universities


def csv_skills(doc):
    skills_keywords = load_keywords('data/newSkills.csv')
    skills = set()

    for keyword in skills_keywords:
        if keyword.lower() in doc.text.lower():
            skills.add(keyword)

    return skills


nlp_skills = spacy.load('Model/skills')  

def extract_skills_from_ner(doc):
    non_skill_labels = {'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL', 'EMAIL'}
    
    skills = set()
    for ent in nlp_skills(doc.text).ents:
        if ent.label_ == 'SKILL':
            if ent.label_ not in non_skill_labels and not ent.text.isdigit():
                skill_text = ''.join(filter(str.isalpha, ent.text))
                if skill_text:
                    skills.add(skill_text)
    return skills


def is_valid_skill(skill_text):
    return len(skill_text) > 1 and not any(char.isdigit() for char in skill_text)


def extract_skills(doc):
    skills_csv = csv_skills(doc)
    skills_ner = extract_skills_from_ner(doc)
    
    filtered_skills_csv = {skill for skill in skills_csv if is_valid_skill(skill)}
    filtered_skills_ner = {skill for skill in skills_ner if is_valid_skill(skill)}
    
    combined_skills = filtered_skills_csv.union(filtered_skills_ner)  
    
    return list(combined_skills)  


def extract_experience(doc):
    verbs = [token.text for token in doc if token.pos_ == 'VERB']

    senior_keywords = ['lead', 'manage', 'direct', 'oversee', 'supervise', 'orchestrate', 'govern']
    mid_senior_keywords = ['develop', 'design', 'analyze', 'implement', 'coordinate', 'execute', 'strategize']
    mid_junior_keywords = ['assist', 'support', 'collaborate', 'participate', 'aid', 'facilitate', 'contribute']
    
    if any(keyword in verbs for keyword in senior_keywords):
        level_of_experience = "Senior"
    elif any(keyword in verbs for keyword in mid_senior_keywords):
        level_of_experience = "Mid-Senior"
    elif any(keyword in verbs for keyword in mid_junior_keywords):
        level_of_experience = "Mid-Junior"
    else:
        level_of_experience = "Entry Level"


    return {
        'level_of_experience': level_of_experience,
    }



def extract_resume_info_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    return nlp(text)



def extract_resume_info(doc):
    first_lines = '\n'.join(doc.text.splitlines()[:10])
    first_name, last_name = extract_name(doc)
    email = extract_email(doc)
    skills = extract_skills(doc)
    experience = extract_experience(doc)

    return {'first_name': first_name, 'last_name': last_name, 'email': email, 'skills': skills, 'experience': experience}



def parse_resume(file):

    pdf_text = extract_resume_info_from_pdf(file)
    resume_info = extract_resume_info(pdf_text)
    education_info = extract_education_from_resume(pdf_text)
    experience_info = extract_experience(pdf_text)
    
    first_name = resume_info['first_name']
    last_name = resume_info['last_name']
    email = resume_info['email']
    skills = resume_info['skills']
    contact_number = extract_contact_number_from_resume(pdf_text)
    level_of_experience = experience_info['level_of_experience']

    return {

        "details": {
            "email": email,
            "full_name": f"{first_name} {last_name}",
            "skills": skills,
            "phone_number": contact_number,
            "education": education_info,
        },
        "experience_level": level_of_experience,
    }