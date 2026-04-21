# Predefined skill list — expand later if needed
SKILL_LIST = [
    "Python", "Java", "C++", "SQL", "Machine Learning", "Deep Learning",
    "Data Science", "React", "Flutter", "HTML", "CSS", "JavaScript",
    "AWS", "Docker", "Git", "FastAPI"
]

def detect_skills(text):
    """Detects present and missing skills from resume text."""
    text_lower = text.lower()
    
    detected = []
    missing = []

    for skill in SKILL_LIST:
        if skill.lower() in text_lower:
            detected.append(skill)
        else:
            missing.append(skill)

    return detected, missing