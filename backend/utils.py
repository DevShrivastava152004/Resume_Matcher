import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# 🔥 Load model once (important for performance)
model = SentenceTransformer('all-MiniLM-L6-v2')

# 🔁 Synonyms normalization
SYNONYMS = {
    "convolutional neural network": "cnn",
    "convolutional neural networks": "cnn",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "natural language processing": "nlp",
    "tfidf": "tf-idf",
    "support vector machine": "svm",
    "support vector machines": "svm"
}
SYNONYMS.update({
    "convolutional neural networks": "cnn",
    "convolutional neural network": "cnn",
    "anti-spoofing": "anti spoofing",
    "liveliness detection": "liveness detection",
    "image processing": "computer vision"
})

# 🎯 Skill weights
SKILLS = {
    # Programming
    "python": 2,
    "java": 2,
    "c++": 2,

    # Core ML/DL
    "machine learning": 3,
    "deep learning": 3,
    "tensorflow": 3,
    "pytorch": 3,
    "scikit-learn": 2,
    "xgboost": 2,
    "svm": 2,

    # Computer Vision (CRITICAL FOR YOUR USE CASE)
    "computer vision": 3,
    "image recognition": 3,
    "object detection": 3,
    "face recognition": 3,
    "cnn": 3,
    "opencv": 3,

    # Special CV techniques
    "liveness detection": 2,
    "anti spoofing": 2,

    # NLP / Transformers
    "nlp": 2,
    "transformer": 2,
    "transformers": 2,

    # Data
    "pandas": 1,
    "numpy": 1,
    "sql": 2,

    # Backend / Tools
    "rest": 1,
    "api": 1,
    "git": 1,
    "docker": 2,

    # Concepts
    "feature engineering": 2,
    "model evaluation": 2
}


# 🔧 Normalize text
def normalize_text(text):
    text = text.lower()
    for phrase, replacement in SYNONYMS.items():
        text = text.replace(phrase, replacement)
    return text


# ==============================
# 🚀 CHUNKED ENCODING
# ==============================

def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        if i + chunk_size >= len(words):
            break

    return chunks if chunks else [text]


def encode_text_chunked(text):
    chunks = chunk_text(text)
    embeddings = model.encode(chunks)
    return np.mean(embeddings, axis=0)


# ======================================
# 🚀 SECTION-AWARE DL SIMILARITY
# ======================================

def extract_sections(text):
    text = text.lower()

    sections = {
        "skills": "",
        "experience": "",
        "projects": "",
        "education": "",
        "other": ""
    }

    current_section = "other"

    for line in text.split("\n"):
        line = line.strip()

        if "skill" in line:
            current_section = "skills"
        elif "experience" in line:
            current_section = "experience"
        elif "project" in line:
            current_section = "projects"
        elif "education" in line:
            current_section = "education"

        sections[current_section] += " " + line

    return sections


def calculate_similarity_sectional(resume_text, jd_text):
    resume_text = normalize_text(resume_text)
    jd_text = normalize_text(jd_text)

    resume_sections = extract_sections(resume_text)
    jd_embedding = encode_text_chunked(jd_text)

    weights = {
        "skills": 0.4,
        "experience": 0.3,
        "projects": 0.2,
        "education": 0.1,
        "other": 0.05
    }

    total_score = 0

    for section, content in resume_sections.items():
        if content.strip():
            section_embedding = encode_text_chunked(content)

            sim = cosine_similarity(
                [section_embedding], [jd_embedding]
            )[0][0]

            total_score += sim * weights.get(section, 0)

    return round(total_score * 100, 2)


# ======================================
# 🚀 ADVANCED SKILL EXTRACTION
# ======================================

def extract_skills_advanced(text):
    text = normalize_text(text)
    found_skills = {}

    for skill, weight in SKILLS.items():
        pattern = r"\b" + re.escape(skill) + r"\b"
        matches = re.findall(pattern, text)

        if matches:
            freq = len(matches)
            score = weight * (1 + 0.2 * freq)
            found_skills[skill] = score

    return found_skills