from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
from utils import calculate_similarity_dl, extract_skills_advanced
import PyPDF2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourresumematchersite.netlify.app","*"],  # change later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📄 Extract text
def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


@app.post("/match")
async def match_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_text = extract_text_from_pdf(resume.file)

    # 🚀 DL similarity
    dl_score = calculate_similarity_dl(resume_text, job_description)

    # 🎯 Skills
    jd_skills = extract_skills_advanced(job_description)
    resume_skills = extract_skills_advanced(resume_text)

    total_weight = sum(jd_skills.values())

    matched_weight = sum(
        weight for skill, weight in jd_skills.items()
        if skill in resume_skills
    )

    skill_score = (matched_weight / total_weight) * 100 if total_weight > 0 else 0

    # 🔥 Hybrid score
    final_score = (0.5 * skill_score) + (0.5 * dl_score)

    matching = list(set(jd_skills.keys()).intersection(resume_skills.keys()))

    missing = sorted(
        list(set(jd_skills.keys()).difference(resume_skills.keys())),
        key=lambda x: jd_skills.get(x, 0),
        reverse=True
    )

    high_priority_missing = missing[:5]

    return {
        "dl_score": round(dl_score, 2),
        "skill_score": round(skill_score, 2),
        "final_hybrid_score": round(final_score, 2),
        "matching_skills": matching,
        "missing_skills": missing,
        "high_priority_missing": high_priority_missing
    }