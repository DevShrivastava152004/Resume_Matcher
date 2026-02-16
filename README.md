# AI Resume – Job Description Matcher

An AI-powered web application that evaluates how well a candidate’s resume aligns with a given job description using a hybrid AI scoring approach.

This system combines semantic similarity (TF-IDF) with weighted skill-based matching to generate an interpretable and robust compatibility score.

---

## 🚀 Features

- Resume PDF text extraction
- TF-IDF based semantic similarity scoring
- Weighted skill-based matching
- Synonym normalization (e.g., CNN ↔ Convolutional Neural Networks)
- Regex-based boundary-safe skill detection (prevents false positives like “rest” inside “interest”)
- Hybrid scoring system
- FastAPI backend
- Clean frontend UI with real-time scoring display

---

## 🧠 Scoring Methodology

The system computes three metrics:

### 1️⃣ TF-IDF Score  
Measures textual similarity between resume and job description using vector space modeling.

### 2️⃣ Skill Score  
Calculates weighted overlap of predefined domain-relevant skills.

### 3️⃣ Final Hybrid Score  

Final Score = (0.6 × Skill Score) + (0.4 × TF-IDF Score)

This hybrid approach improves precision while maintaining semantic awareness.

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Scikit-learn
- PyPDF2

### Frontend
- HTML
- CSS
- JavaScript

---


---

## 🔍 Engineering Highlights

- Implemented synonym normalization to improve skill recall
- Added regex-based word-boundary matching to eliminate substring false positives
- Designed weighted skill dictionary for domain-aware scoring
- Integrated end-to-end frontend and backend communication
- Enabled CORS for seamless local development

---

## 🎯 Future Enhancements

- Embedding-based semantic similarity (BERT / Sentence Transformers)
- Skill categorization (Core vs Secondary)
- Resume improvement suggestions
- Cloud deployment
- Recruiter dashboard

---

## 📌 Status

MVP Complete – End-to-end functional AI resume matching web application.


## 📂 Project Structure

