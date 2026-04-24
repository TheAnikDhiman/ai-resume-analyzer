from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os
import platform
import os
import platform

def _register_fonts():
    if platform.system() == "Windows":
        font_dir = "C:/Windows/Fonts/"
        font_map = {
            "DV":   "arial.ttf",
            "DV-B": "arialbd.ttf",
            "DV-I": "ariali.ttf",
        }
    else:
        font_dir = "/usr/share/fonts/truetype/dejavu/"
        font_map = {
            "DV":   "DejaVuSans.ttf",
            "DV-B": "DejaVuSans-Bold.ttf",
            "DV-I": "DejaVuSans-Oblique.ttf",
        }
    for alias, filename in font_map.items():
        path = os.path.join(font_dir, filename)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(alias, path))

_register_fonts()

BLUE  = colors.HexColor("#1d4ed8")
DARK  = colors.HexColor("#111827")
GRAY  = colors.HexColor("#4b5563")
GREEN = colors.HexColor("#16a34a")
RED   = colors.HexColor("#dc2626")
AMBER = colors.HexColor("#d97706")

def generate_report(filename, ats_score, detected_skills,
                    missing_skills, suggestions,
                    found_sections, missing_sections, jd_match=None):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=18*mm, leftMargin=18*mm,
                            topMargin=16*mm, bottomMargin=16*mm)

    S = lambda name, **kw: ParagraphStyle(name, **kw)
    title_s   = S("t",  fontName="DV-B", fontSize=22, textColor=BLUE,  alignment=TA_CENTER, spaceAfter=4)
    sub_s     = S("s",  fontName="DV-I", fontSize=10, textColor=GRAY,  alignment=TA_CENTER, spaceAfter=2)
    sec_s     = S("sc", fontName="DV-B", fontSize=11, textColor=BLUE,  spaceBefore=14, spaceAfter=4)
    body_s    = S("b",  fontName="DV",   fontSize=9,  textColor=DARK,  spaceAfter=3,   leading=14)
    score_s   = S("sc2",fontName="DV-B", fontSize=32, textColor=BLUE,  alignment=TA_CENTER, spaceAfter=4)
    label_s   = S("l",  fontName="DV",   fontSize=9,  textColor=GRAY,  alignment=TA_CENTER, spaceAfter=8)
    bullet_s  = S("bu", fontName="DV",   fontSize=9,  textColor=DARK,  spaceAfter=3,
                  leftIndent=14, firstLineIndent=-10, leading=14)

    def HR(): return HRFlowable(width="100%", thickness=0.6,
                                color=colors.HexColor("#d1d5db"), spaceAfter=4)
    def BLUEHR(): return HRFlowable(width="100%", thickness=1.0,
                                    color=BLUE, spaceAfter=6)
    def bullet(text, color=DARK):
        return Paragraph("\u2022  " + text,
                         ParagraphStyle("bx", parent=bullet_s, textColor=color))

    score_color = GREEN if ats_score >= 70 else AMBER if ats_score >= 40 else RED
    score_label = "Strong" if ats_score >= 70 else "Moderate" if ats_score >= 40 else "Needs Work"

    story = []

    # Header
    story.append(Paragraph("AI Resume Analyzer", title_s))
    story.append(Paragraph("ATS Score Report", sub_s))
    story.append(Paragraph(f"File: {filename}", sub_s))
    story.append(BLUEHR())

    # ATS Score
    story.append(Paragraph("OVERALL ATS SCORE", sec_s))
    story.append(Paragraph(f"{ats_score}%",
                 ParagraphStyle("sc3", parent=score_s, textColor=score_color)))
    story.append(Paragraph(score_label,
                 ParagraphStyle("sl", parent=label_s, textColor=score_color)))

    # JD Score
    if jd_match:
        story.append(Paragraph("JD MATCH SCORE", sec_s))
        jd_color = GREEN if jd_match['score'] >= 70 else AMBER if jd_match['score'] >= 40 else RED
        story.append(Paragraph(f"{jd_match['score']}%",
                     ParagraphStyle("jds", parent=score_s, textColor=jd_color)))
        story.append(HR())

    # Detected Skills
    story.append(Paragraph("DETECTED SKILLS", sec_s))
    story.append(BLUEHR())
    for skill in detected_skills:
        story.append(bullet(skill, GREEN))

    # Missing Skills
    story.append(Paragraph("MISSING SKILLS", sec_s))
    story.append(BLUEHR())
    for skill in missing_skills:
        story.append(bullet(skill, RED))

    # Section Checker
    story.append(Paragraph("RESUME SECTION CHECKER", sec_s))
    story.append(BLUEHR())
    for s in found_sections:
        story.append(bullet(f"{s} — Found", GREEN))
    for s in missing_sections:
        story.append(bullet(f"{s} — Missing", RED))

    # Suggestions
    story.append(Paragraph("SUGGESTIONS", sec_s))
    story.append(BLUEHR())
    for tip in suggestions:
        # strip emoji for PDF
        clean = tip.encode('ascii', 'ignore').decode()
        story.append(bullet(clean.strip(), AMBER))

    # Footer
    story.append(Spacer(1, 12))
    story.append(HR())
    story.append(Paragraph("Generated by AI Resume Analyzer · BCA Final Year Project",
                 ParagraphStyle("ft", parent=sub_s, fontSize=8)))

    doc.build(story)
    buffer.seek(0)
    return buffer