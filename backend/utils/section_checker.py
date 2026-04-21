# Standard resume sections to look for
REQUIRED_SECTIONS = ["education", "experience", "skills", "projects"]

def check_sections(text):
    """Checks if resume has standard section headings."""
    text_lower = text.lower()
    
    found = []
    missing = []
    
    for section in REQUIRED_SECTIONS:
        if section in text_lower:
            found.append(section.title())
        else:
            missing.append(section.title())
    
    return found, missing