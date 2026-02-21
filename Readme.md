# 📄 AI Resume Analyzer

A Streamlit web app that analyzes resumes for ATS (Applicant Tracking System) compatibility.

## 🚀 Features
- Upload resume as PDF
- Extracts text automatically
- Detects technical skills
- Calculates ATS score
- Provides improvement suggestions

## ⚙️ Setup

Install dependencies:
pip install -r requirements.txt


## ▶️ Run

streamlit run app.py


## 🛠️ Built With
- Python
- Streamlit
- pdfplumber
```

---

Save it. Your final folder should now look like:
```
ai_resume_analyzer/
├── app.py
├── requirements.txt
├── README.md
└── utils/
    ├── __init__.py
    ├── extractor.py
    ├── skill_detector.py
    ├── scorer.py
    └── suggestions.py