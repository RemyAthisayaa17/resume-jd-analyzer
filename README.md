# Resume JD Analyzer ✨ (Gen AI)

Analyze resumes against job descriptions with AI-powered insights.
This project evaluates candidate skills, identifies gaps, generates strategic recommendations, and extracts derived skills — all while maintaining a clean, domain-friendly interface.

---

## 🚀 Features

* **Alignment Score**: Percentage match between candidate resume and job description.
* **Derived Skills**: Extract skills directly from resumes for a clean skill overview.
* **Competency Breakdown**: Highlights matched competencies and critical gaps.
* **Strategic Recommendations**: Provides actionable insights for skill improvement.
* **Domain-Aware**: Works across tech, AI, and non-tech fields.
* **Preserves Flow & UI**: Maintains smooth and intuitive user experience.
* **PDF Resume Support**: Upload PDFs directly for analysis.
* **Real-Time Frontend**: Instant results using React frontend and Flask backend.

---

## 💻 Tech Stack

* **Frontend**: React, modern JSX, responsive UI
* **Backend**: Flask, Python
* **PDF Parsing**: pdfplumber
* **AI Layer**: Semantic matching, derived skill extraction, recommendations
* **Hosting Ready**: Compatible for Vercel, Netlify (frontend) + Render, Railway (backend)
* **Data Handling**: JSON-based storage, modular architecture

---

## 📂 Project Structure

```
resume-jd-analyzer/
├─ backend/
│  ├─ app.py               # Main Flask API
│  ├─ ai_engine/           # AI modules (embedder, retriever, reasoner)
│  ├─ utils/               # Helper functions (PDF, skill extraction)
│  └─ requirements.txt
├─ frontend/
│  ├─ src/
│  │  └─ App.jsx           # Main React component
│  └─ index.html
└─ README.md
```

---

## ⚡ Quick Start (Local)

1. **Clone repo**

```bash
git clone https://github.com/RemyAthisayaa17/resume-jd-analyzer.git
cd resume-jd-analyzer
```

2. **Backend Setup**

```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python app.py
```

3. **Frontend Setup**

```bash
cd frontend
npm install
npm run dev
```

4. Open browser at [http://localhost:5173](http://localhost:5173) and test!

---

## 📈 Usage

* Upload your PDF resume.
* Paste or type the Job Description.
* Click **Generate Strategic Insights**.
* View **Alignment Score**, **Derived Skills**, **Competency Breakdown**, and **Recommendations** instantly.

---

## 🎯 Notes

* AI analysis is **domain-aware** (tech, AI, non-tech).
* Handles **PDF parsing, semantic matching, and skill derivation**.
* Fully **Gen AI ready** for future integration or improvements.

---

## 📝 Contribution

* Fork the repo
* Create a branch (`git checkout -b feature-name`)
* Commit changes (`git commit -m 'Add feature'`)
* Push to branch (`git push origin feature-name`)
* Open a Pull Request

---

## 📧 Contact

Remy Athisayaa

[GitHub](https://github.com/RemyAthisayaa17)
