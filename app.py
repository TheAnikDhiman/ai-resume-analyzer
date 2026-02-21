import streamlit as st
from utils.extractor import extract_text
from utils.skill_detector import detect_skills, SKILL_LIST
from utils.scorer import calculate_ats_score
from utils.suggestions import generate_suggestions

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
    if st.button("🔍 Analyze Resume"):
        if extracted_text:
            detected_skills, missing_skills = detect_skills(extracted_text)
            ats_score = calculate_ats_score(detected_skills, len(SKILL_LIST))
            suggestions = generate_suggestions(ats_score, missing_skills)

            st.divider()

            # --- Results Section ---
            st.subheader("📊 Results")
            st.metric(label="ATS Score", value=f"{ats_score}%")

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