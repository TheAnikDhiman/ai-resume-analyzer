from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from utils.extractor import extract_text
from utils.skill_detector import detect_skills, SKILL_LIST
from utils.scorer import calculate_ats_score
from utils.suggestions import generate_suggestions
from utils.section_checker import check_sections
from utils.jd_matcher import match_jd
import io
from fastapi.responses import StreamingResponse
from utils.report_generator import generate_report

app = FastAPI()

# Allow React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "AI Resume Analyzer API is running"}


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    jd_text: str = Form("")
):
    # Read uploaded file into memory
    contents = await file.read()
    file_like = io.BytesIO(contents)

    # Extract text
    extracted_text = extract_text(file_like)
    if not extracted_text:
        return {"error": "Could not extract text from PDF"}

    # Core analysis
    detected_skills, missing_skills = detect_skills(extracted_text)
    ats_score = calculate_ats_score(detected_skills, len(SKILL_LIST))
    suggestions = generate_suggestions(ats_score, missing_skills)
    found_sections, missing_sections = check_sections(extracted_text)

    # JD matching (only if JD provided)
    jd_data = None
    if jd_text.strip():
        jd_matched, jd_missing, jd_score = match_jd(
            extracted_text, jd_text, SKILL_LIST
        )
        jd_data = {
            "score": jd_score,
            "matched": jd_matched,
            "missing": jd_missing
        }

    return {
        "ats_score": ats_score,
        "detected_skills": detected_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "found_sections": found_sections,
        "missing_sections": missing_sections,
        "jd_match": jd_data
    }
@app.post("/download-report")
async def download_report(
    file: UploadFile = File(...),
    jd_text: str = Form("")
):
    contents = await file.read()
    file_like = io.BytesIO(contents)
    extracted_text = extract_text(file_like)

    if not extracted_text:
        return {"error": "Could not extract text"}

    detected_skills, missing_skills = detect_skills(extracted_text)
    ats_score = calculate_ats_score(detected_skills, len(SKILL_LIST))
    suggestions = generate_suggestions(ats_score, missing_skills)
    found_sections, missing_sections = check_sections(extracted_text)

    jd_match = None
    if jd_text.strip():
        jd_matched, jd_missing, jd_score = match_jd(extracted_text, jd_text, SKILL_LIST)
        jd_match = {"score": jd_score, "matched": jd_matched, "missing": jd_missing}

    pdf_buffer = generate_report(
        file.filename, ats_score, detected_skills,
        missing_skills, suggestions,
        found_sections, missing_sections, jd_match
    )

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=ATS_Report_{file.filename}"}
    )