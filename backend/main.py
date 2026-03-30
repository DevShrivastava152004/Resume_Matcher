from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
from utils import calculate_similarity_sectional, extract_skills_advanced
import PyPDF2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 📄 Extract text from PDF
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

    # 🚀 SECTION-AWARE DL SCORE
    dl_score = calculate_similarity_sectional(resume_text, job_description)

    # 🎯 ADVANCED SKILL EXTRACTION
    jd_skills = extract_skills_advanced(job_description)
    resume_skills = extract_skills_advanced(resume_text)

    # 🧪 DEBUG (IMPORTANT – remove later)
    print("\n========== DEBUG ==========")
    print("JD TEXT:", job_description[:300])  # first 300 chars
    print("RESUME TEXT:", resume_text[:300])
    print("JD SKILLS:", jd_skills)
    print("RESUME SKILLS:", resume_skills)
    print("===========================\n")

    total_weight = sum(jd_skills.values())

    matched_weight = sum(
        weight for skill, weight in jd_skills.items()
        if skill in resume_skills
    )

    # 🛑 Prevent divide by zero + detect empty JD skills
    if total_weight == 0:
        skill_score = 0
        print("⚠️ WARNING: No skills detected in JD")
    else:
        skill_score = (matched_weight / total_weight) * 100

    # 🔥 HYBRID SCORE
    final_score = (0.6 * skill_score) + (0.4 * dl_score)

    matching = list(set(jd_skills.keys()).intersection(resume_skills.keys()))
    missing = list(set(jd_skills.keys()).difference(resume_skills.keys()))

    # 🚀 PRIORITY MISSING SKILLS
    high_priority_missing = sorted(
        missing,
        key=lambda skill: jd_skills.get(skill, 0),
        reverse=True
    )[:5]

    return {
        "dl_score": round(dl_score, 2),
        "skill_score": round(skill_score, 2),
        "final_hybrid_score": round(final_score, 2),
        "matching_skills": matching,
        "missing_skills": missing,
        "high_priority_missing": high_priority_missing,
        "debug": {
            "jd_skills_count": len(jd_skills),
            "resume_skills_count": len(resume_skills)
        }
    }