import re
from sklearn.feature_extraction.text import TfidfVectorizer
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

# 🎯 Skill weights
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
    "rest": 1,
    "git": 1,
    "feature engineering": 2,
    "model evaluation": 2
}

# 🔧 Normalize text (for consistency)
def normalize_text(text):
    text = text.lower()

    for phrase, replacement in SYNONYMS.items():
        if phrase in text:
            text = text.replace(phrase, replacement)

    return text

# 📌 TF-IDF similarity (old method)
def calculate_similarity(resume_text, jd_text):
    documents = [resume_text, jd_text]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return round(float(similarity[0][0]) * 100, 2)

# 🚀 Deep Learning similarity (NEW)
def calculate_similarity_dl(resume_text, jd_text):

    resume_text = normalize_text(resume_text)
    jd_text = normalize_text(jd_text)

    resume_embedding = model.encode(resume_text)
    jd_embedding = model.encode(jd_text)

    similarity = cosine_similarity(
        [resume_embedding], [jd_embedding]
    )[0][0]

    return round(float(similarity) * 100, 2)

# 🧠 Extract keywords (basic)
def extract_keywords(text):
    words = text.lower().split()
    cleaned = [word.strip(",.()") for word in words]
    return set(cleaned)

# 🎯 Extract skills using regex + weights
def extract_skills(text):
    text = normalize_text(text)
    found_skills = {}

    for skill, weight in SKILLS.items():
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills[skill] = weight

    return found_skills