import streamlit as st
from utils.extractor import extract_text
from utils.skill_detector import detect_skills, SKILL_LIST
from utils.scorer import calculate_ats_score
from utils.suggestions import generate_suggestions
from utils.jd_matcher import match_jd
import plotly.graph_objects as go
from utils.section_checker import check_sections

def score_gauge(score, title):
    color = "#ef4444" if score < 40 else "#f59e0b" if score < 70 else "#10b981"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": title, "font": {"size": 14}},
        number={"suffix": "%", "font": {"size": 28}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 40],  "color": "#1f2535"},
                {"range": [40, 70], "color": "#1a2040"},
                {"range": [70, 100],"color": "#1a2d30"},
            ],
        }
    ))
    fig.update_layout(height=220, margin=dict(t=40, b=0, l=20, r=20),
                      paper_bgcolor="rgba(0,0,0,0)", font_color="#e8ecf5")
    return fig
# --- Page Config ---
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get an ATS compatibility score instantly.")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")

    # Debug toggle
    extracted_text = extract_text(uploaded_file)
    if st.checkbox("Show extracted text (debug)"):
        st.text_area("Extracted Text", extracted_text, height=200)

    # --- Analyze Button ---
    # --- Job Description Input ---
st.subheader("📋 Job Description (Optional)")
jd_text = st.text_area(
    "Paste the Job Description here for targeted analysis",
    height=150,
    placeholder="e.g. We are looking for a Python developer with experience in SQL, Docker, AWS..."
)

if st.button("🔍 Analyze Resume"):
    if extracted_text:
        detected_skills, missing_skills = detect_skills(extracted_text)
        ats_score = calculate_ats_score(detected_skills, len(SKILL_LIST))
        suggestions = generate_suggestions(ats_score, missing_skills)

        # --- Section Checker ---
        found_sections, missing_sections = check_sections(extracted_text)

        st.markdown("#### 🗂️ Resume Section Checker")
        col1, col2 = st.columns(2)
        with col1:
            st.success("✅ Sections Found")
            for s in found_sections:
                st.write(f"• {s}")
        with col2:
            if missing_sections:
                st.warning("⚠️ Sections Missing")
                for s in missing_sections:
                    st.write(f"• {s}")
            else:
                st.success("🎉 All sections present!")

        st.divider()
        st.subheader("📊 Results")

        # --- JD Match (only if JD was provided) ---
        if jd_text.strip():
            jd_matched, jd_missing, jd_score = match_jd(extracted_text, jd_text, SKILL_LIST)

            st.markdown("#### 🎯 Job Description Match")
            st.plotly_chart(score_gauge(jd_score, "JD Match Score"), use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.success("✅ Matched from JD")
                for skill in jd_matched:
                    st.write(f"• {skill}")
            with col2:
                st.error("❌ Missing from JD")
                for skill in jd_missing:
                    st.write(f"• {skill}")

            st.divider()

        # --- General ATS Score ---
        st.markdown("#### 📈 Overall ATS Score")
        st.plotly_chart(score_gauge(ats_score, "Overall ATS Score"), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.success("✅ Detected Skills")
            for skill in detected_skills:
                st.write(f"• {skill}")
        with col2:
            st.error("❌ Missing Skills")
            for skill in missing_skills:
                st.write(f"• {skill}")

        st.divider()

        st.subheader("💡 Suggestions")
        for tip in suggestions:
            st.write(tip)
    else:
        st.error("❌ Could not extract text. Try a different PDF.")
else:
    st.info("Please upload a PDF file to begin.")