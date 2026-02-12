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
