# SHL Assessment Recommendation System

This project implements a semantic recommendation system to suggest relevant SHL assessments based on natural language hiring queries.

---

## 🔍 Problem Overview

Given a hiring query (e.g., *“Hiring a Java developer who can collaborate with business teams”*), the system recommends the most relevant SHL assessments using semantic similarity and ranking strategies.

---

## 🏗️ System Architecture

1. **Data Collection**
   - Scraped publicly available SHL assessment catalog.
   - Extracted assessment metadata such as name, URL, test type, duration, and features.

2. **Text Embeddings**
   - Used `Sentence-BERT (all-MiniLM-L6-v2)` to convert assessments and queries into dense vectors.

3. **Vector Search**
   - Built a FAISS index for efficient similarity search.

4. **Ranking**
   - Initial retrieval using FAISS.
   - Final ranking using a balanced relevance scoring approach.

5. **API**
   - FastAPI backend exposes a `/recommend` endpoint.
   - Returns clean, JSON-serializable assessment recommendations.

6. **Frontend**
   - Streamlit UI for interactive query input and result visualization.

---

## 🧪 Evaluation

- Metric used: **Recall@10**
- Dataset provided: `Gen_AI Dataset.xlsx`
- Observation:
  - The provided ground-truth assessment URLs do not overlap with the current public SHL catalog.
  - This results in Recall@10 = 0 despite correct semantic recommendations.
- This limitation is documented and explained, reflecting real-world dataset inconsistencies.

---

## 📂 Output Files

- `predictions.csv`: Top-10 recommended assessment URLs for each query in the dataset.

---

## 🚀 How to Run

### Backend
```bash
python -m uvicorn api.main:app


### Frontend
streamlit run frontend/app.py

### Generate Predictions
python -m evaluation.generate_predictions

⚠️ Limitations & Future Work

Ground-truth URLs may be outdated or deprecated.
Future improvements could include:
Title-based matching for evaluation
Feedback-driven learning
Deployment on cloud infrastructure



👤 Author
- Dhruv Maheshwari