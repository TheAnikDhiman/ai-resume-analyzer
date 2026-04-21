def generate_suggestions(ats_score, missing_skills):
    """Returns rule-based suggestions based on ATS score."""
    suggestions = []

    # Score-based suggestions
    if ats_score < 40:
        suggestions.append("⚠️ Your ATS score is low. Add more technical skills to your resume.")
        suggestions.append("📌 Focus on adding high-demand skills like Python, SQL, or JavaScript.")
    elif 40 <= ats_score <= 70:
        suggestions.append("📈 Decent score! Improve keyword coverage to rank higher in ATS filters.")
        suggestions.append(f"🔍 Consider adding some of these missing skills: {', '.join(missing_skills[:4])}")
    else:
        suggestions.append("🌟 Great ATS score! Your resume is well-optimized for keyword matching.")

    # General suggestions — always shown
    suggestions.append("📊 Add quantified achievements (e.g. 'Improved performance by 30%').")
    suggestions.append("📝 Use standard section headings: Experience, Education, Skills, Projects.")

    return suggestions