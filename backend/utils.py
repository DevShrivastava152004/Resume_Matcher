SYNONYMS = {
    "convolutional neural network": "cnn",
    "convolutional neural networks": "cnn",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "natural language processing": "nlp",
    "tfidf" : "tf-idf",
    "support vector machine": "svm",
    "support vector machines": "svm"
}

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


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_text, jd_text):
    documents = [resume_text, jd_text]
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    return round(float(similarity[0][0]) * 100, 2)

def extract_keywords(text):

    words = text.lower().split()
    cleaned = [word.strip(",.()") for word in words]
    return set(cleaned)

def extract_skills(text):
    text = normalize_text(text)
    found_skills = {}

    for skill, weight  in SKILLS.items():
        if skill in text:
            found_skills[skill] = weight


    return found_skills

def normalize_text(text):
    text = text.lower()

    for phrase, replacement in SYNONYMS.items():
        if phrase in text:
            text = text.replace(phrase, replacement)


    return text

