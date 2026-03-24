from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
from utils import calculate_similarity_dl, extract_skills
import PyPDF2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    return text


@app.post("/match")
async def match_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_text = extract_text_from_pdf(resume.file)

    #TF - IDF score
    dl_score = calculate_similarity_dl(resume_text , job_description)

    # Weighted Skill Extraction
    jd_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    total_weight = sum(jd_skills.values())
    matched_weight = sum(
        weight for skill, weight in jd_skills.items()
        if skill in resume_skills
    )

    if total_weight > 0:
        skill_score = (matched_weight / total_weight) * 100
    else:
        skill_score = 0

    # Hybrid score
    final_score = (0.6 * skill_score) + (0.4 * dl_score)

    matching = list(set(jd_skills.keys()).intersection(resume_skills.keys()))
    missing = list(set(jd_skills.keys()).difference(resume_skills.keys()))

    return {
        "dl_score": round(dl_score, 2),
        "skill_score": round(skill_score, 2),
        "final_hybrid_score": round(final_score, 2),
        "matching_skills": matching,
        "missing_skills": missing
    }


    