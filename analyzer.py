import PyPDF2
import re
from transformers import pipeline

print("Loading AI model...")
nlp = pipeline("text-generation", model="gpt2")

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Extract skills
def extract_skills(text):
    skills_list = ['Python', 'Java', 'C++', 'Machine Learning', 'AI', 'SQL', 'HTML', 'CSS', 'JavaScript']
    found = [skill for skill in skills_list if re.search(skill, text, re.IGNORECASE)]
    return found

# Score resume
def score_resume(text, skills):
    score = 0

    # Skills (40 points)
    score += min(len(skills) * 10, 40)

    # Education & Experience (30 points)
    if re.search(r'B\.?Tech|M\.?Tech|BE|Bachelor|Master', text, re.IGNORECASE):
        score += 15
    if re.search(r'Internship|Experience|Worked at', text, re.IGNORECASE):
        score += 15

    # Extra keywords (30 points)
    for kw in ["Project", "Certification", "Achievement"]:
        if re.search(kw, text, re.IGNORECASE):
            score += 10

    return min(score, 100)

# ---- REPLACE THIS FUNCTION WITH THE NEW VERSION ----
def analyze_resume(text):
    skills = extract_skills(text)
    score = score_resume(text, skills)

    all_skills = ['Python', 'Java', 'C++', 'Machine Learning', 'AI', 'SQL', 'HTML', 'CSS', 'JavaScript']
    missing_skills = [s for s in all_skills if s not in skills]

    # Generate suggestions based on score and missing skills
    suggestions = []
    if score < 70:
        suggestions.append("Add more relevant projects or internships to boost your score.")
    if "Machine Learning" not in skills:
        suggestions.append("Include Machine Learning or Data Science skills if applicable.")
    if "SQL" not in skills:
        suggestions.append("Mention database skills like SQL to strengthen your resume.")
    if not re.search(r'Certification', text, re.IGNORECASE):
        suggestions.append("List certifications (e.g., Java, Python, or Cloud) to stand out.")

    return {
        "skills": skills,
        "missing_skills": missing_skills,
        "score": score,
        "suggestions": suggestions if suggestions else ["Your resume looks strong. Keep it concise and professional."]
    }


