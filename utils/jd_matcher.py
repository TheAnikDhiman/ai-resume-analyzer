def match_jd(resume_text, jd_text, skill_list):
    """
    Compares resume against job description.
    Returns JD-specific detected, missing skills and a JD match score.
    """
    jd_lower = jd_text.lower()
    resume_lower = resume_text.lower()

    # Find skills mentioned in the JD
    jd_skills = [skill for skill in skill_list if skill.lower() in jd_lower]

    if not jd_skills:
        return [], [], 0

    # From those JD skills, check which ones resume has
    matched = [skill for skill in jd_skills if skill.lower() in resume_lower]
    missing = [skill for skill in jd_skills if skill.lower() not in resume_lower]

    # Score based on JD skills only
    score = round((len(matched) / len(jd_skills)) * 100)

    return matched, missing, score