from fastapi import FastAPI, UploadFile, File, Form
from utils import calculate_similarity, extract_keywords
import PyPDF2

app = FastAPI()

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
    score = calculate_similarity(resume_text, job_description)

    jd_keywords = extract_keywords(job_description)
    resume_keywords = extract_keywords(resume_text)

    matching = list(jd_keywords.intersection(resume_keywords))
    missing = list(jd_keywords.difference(resume_keywords))

    return {
        "match_score": score,
        "matching_skills": matching[:10],
        "missing_skills": missing[:10]
    }
