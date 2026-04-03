# 🚀 AI Resume – Job Description Matcher

An AI-powered web application that evaluates how well a candidate’s resume aligns with a job description using a **hybrid AI scoring system**.

This system combines **Deep Learning-based semantic similarity (Sentence Transformers)** with **weighted skill-based matching** to generate an accurate and interpretable compatibility score.

---

## 🌐 Live Demo

Frontend: https://yourresumematchersite.netlify.app/

Backend API Docs:  
https://resume-matcher-lizq.onrender.com/docs

---

## 🚀 Features

- 📄 Resume PDF text extraction
- 🧠 Deep Learning semantic similarity using Sentence Transformers (MiniLM)
- 🎯 Weighted skill-based matching system
- 🔁 Synonym normalization (e.g., CNN ↔ Convolutional Neural Networks)
- 🛡️ Regex-based boundary-safe skill detection (avoids false positives like “rest” in “interest”)
- 📊 Hybrid scoring system (DL + Skills)
- ⚡ FastAPI backend with real-time processing
- 💻 Clean frontend UI with dynamic result display
- 📌 Highlights missing and high-priority skills

---

## 🧠 Scoring Methodology

The system computes three metrics:

### 1️⃣ Deep Learning Score  
Uses transformer-based embeddings to calculate semantic similarity between resume and job description.

### 2️⃣ Skill Score  
Calculates weighted overlap of domain-relevant skills extracted from both resume and job description.

### 3️⃣ Final Hybrid Score  

Final Score = (0.5 × Skill Score) + (0.5 × DL Score)

This hybrid approach ensures both **context understanding** and **skill precision**.

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Sentence Transformers (BERT-based model)
- Scikit-learn
- PyPDF2

### Frontend
- HTML
- CSS
- JavaScript

---

## 🔍 Engineering Highlights

- Implemented **transformer-based semantic similarity** for contextual understanding
- Designed **weighted skill extraction system** for domain-aware scoring
- Built **synonym normalization pipeline** to improve matching accuracy
- Applied **regex-based word boundary detection** to eliminate false positives
- Developed **hybrid scoring logic combining DL + rule-based methods**
- Integrated full **frontend ↔ backend communication pipeline**
- Solved real-world deployment challenges (CORS, Render + Netlify integration)

---

## 📊 Example Output

Final Score: 77%  
DL Score: 71%  
Skill Score: 83%  

Matching Skills:  
Python, Deep Learning, TensorFlow, OpenCV  

Missing Skills:  
Model Evaluation, Git  

High Priority Missing:  
Model Evaluation, Git  

---

## 📂 Project Structure

resume-matcher/  
│  
├── backend/  
│   ├── main.py  
│   ├── utils.py  
│   ├── requirements.txt  
│  
├── frontend/  
│   ├── index.html  
│   ├── style.css  
│   ├── script.js  
│  
└── README.md  

---

## 🎯 Future Enhancements

- 🤖 AI-based resume improvement suggestions
- 🧠 GPT-powered resume rewriting
- 📄 Downloadable PDF analysis report
- 📊 Recruiter dashboard with analytics
- 🧩 Skill categorization (Core vs Secondary)
- 🔍 ATS optimization insights

---

## 📌 Status

✅ MVP Complete – Fully functional AI resume analysis system  
🚀 Deployed with frontend (Netlify) and backend (Render)  
💡 Ready for real-world usage and further scaling

---

## 👨‍💻 Author

Dev Shrivastava
