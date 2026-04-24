SKILL_LIST = [
    # Languages
    "Python", "Java", "C++", "C", "JavaScript", "TypeScript",
    "SQL", "R", "Go", "Kotlin", "Swift",

    # Web & Frameworks
    "React", "Angular", "Vue", "HTML", "CSS",
    "FastAPI", "Flask", "Django", "Node.js", "Express",

    # Mobile
    "Flutter", "React Native",

    # Data / AI / ML
    "Machine Learning", "Deep Learning", "Data Science",
    "NLP", "Computer Vision", "TensorFlow", "PyTorch",
    "Pandas", "NumPy", "Scikit-learn", "Matplotlib",

    # DevOps / Cloud
    "AWS", "Azure", "GCP", "Docker", "Kubernetes",
    "Git", "Linux", "CI/CD",

    # Databases
    "MongoDB", "PostgreSQL", "MySQL", "Firebase",
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