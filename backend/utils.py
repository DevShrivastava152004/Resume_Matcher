import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# 🔥 Load model safely
try:
    model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
except Exception as e:
    print("Model loading failed:", e)
    model = None

# 🔁 Synonyms
SYNONYMS = {
    "convolutional neural network": "cnn",
    "convolutional neural networks": "cnn",
    "sklearn": "scikit-learn",
    "natural language processing": "nlp",
    "tfidf": "tf-idf",
    "support vector machine": "svm",
    "support vector machines": "svm",
    "github": "git",
    "sentiment analysis": "nlp",
    "rest api": "rest",
    "apis": "rest"
}

# 🎯 Skills
SKILLS = {
    "python": 2,
    "machine learning": 3,
    "deep learning": 3,
    "tensorflow": 3,
    "pytorch": 3,
    "cnn": 3,
    "opencv": 2,
    "nlp": 2,
    "tf-idf": 2,
    "scikit-learn": 2,
    "xgboost": 2,
    "svm": 2,
    "pandas": 1,
    "numpy": 1,
    "sql": 1,
    "rest": 2,
    "git": 1,
    "feature engineering": 2,
    "model evaluation": 2
}

# 🔧 Normalize text
def normalize_text(text):
    text = text.lower()
    for k, v in SYNONYMS.items():
        text = text.replace(k, v)
    return text

# 🧹 Clean text
def clean_text(text):
    text = normalize_text(text)
    text = re.sub(r'\s+', ' ', text)
    return text

# 🧩 Chunking
def chunk_text(text, size=300):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

# 🚀 Encode text
def encode_text(text):
    if model is None:
        return None

    text = clean_text(text)
    chunks = chunk_text(text)

    embeddings = model.encode(chunks)
    return np.mean(embeddings, axis=0)

# 🚀 FINAL DL similarity (NO section logic)
def calculate_similarity_dl(resume_text, jd_text):
    if model is None:
        return 0

    resume_embedding = encode_text(resume_text)
    jd_embedding = encode_text(jd_text)

    similarity = cosine_similarity(
        [resume_embedding], [jd_embedding]
    )[0][0]

    return round(float(similarity) * 100, 2)

# 🎯 Skill extraction (improved)
def extract_skills_advanced(text):
    text = normalize_text(text)
    found = {}

    for skill, weight in SKILLS.items():
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found[skill] = weight

    # fallback for GitHub
    if "github" in text:
        found["git"] = 1

    return found