from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import re

from ai_engine.embedder import embed_texts
from ai_engine.retriever import semantic_match
from ai_engine.reasoner import generate_recommendations
from utils.skill_extractor import extract_skills_from_text  # NEW: skill extraction

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# -----------------------------
# Helpers
# -----------------------------

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.lower()

def normalize_text(text: str) -> str:
    """
    Normalize text WITHOUT destroying newlines.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9+.#\n ]", " ", text)
    text = re.sub(r"[ \t]+", " ", text)  # preserve \n
    return text.strip()

def split_into_sentences(text: str) -> list[str]:
    """
    Split text into meaningful JD / resume chunks.
    Handles periods and newlines correctly.
    """
    raw_chunks = re.split(r"[.\n]", text)
    cleaned = []
    for chunk in raw_chunks:
        c = chunk.strip()
        if len(c) >= 15:
            cleaned.append(c)
    return cleaned

# -----------------------------
# API Endpoint
# -----------------------------

@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files or "jd" not in request.form:
        return jsonify({"error": "Resume file and JD are required"}), 400

    resume_file = request.files["resume"]
    jd_text_raw = request.form["jd"]

    resume_text = normalize_text(extract_text_from_pdf(resume_file))
    jd_text = normalize_text(jd_text_raw)

    resume_chunks = split_into_sentences(resume_text)
    jd_chunks = split_into_sentences(jd_text)

    if not resume_chunks or not jd_chunks:
        return jsonify({
            "match_score": 0,
            "derived_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": ["Insufficient content for meaningful analysis."]
        })

    # -----------------------------
    # Semantic Embeddings
    # -----------------------------
    resume_embeddings = embed_texts(resume_chunks)
    jd_embeddings = embed_texts(jd_chunks)

    similarity_scores = semantic_match(jd_embeddings, resume_embeddings)

    # ---- CALIBRATED THRESHOLD ----
    THRESHOLD = 0.45

    matched_idx = [i for i, s in enumerate(similarity_scores) if s >= THRESHOLD]
    missing_idx = [i for i, s in enumerate(similarity_scores) if s < THRESHOLD]

    matched_requirements = [jd_chunks[i] for i in matched_idx]
    missing_requirements = [jd_chunks[i] for i in missing_idx]

    match_score = round((len(matched_requirements) / len(jd_chunks)) * 100, 1)

    # -----------------------------
    # Derived Skills Extraction
    # -----------------------------
    derived_skills = extract_skills_from_text(resume_text)

    # -----------------------------
    # Mandatory Skill Handling
    # -----------------------------
    mandatory_skills = [skill for skill in jd_chunks if "mandatory" in skill.lower()]
    for skill in mandatory_skills:
        if skill.lower() not in resume_text:
            missing_requirements.append(skill)

    # -----------------------------
    # AI Recommendations
    # -----------------------------
    suggestions = generate_recommendations(
        missing_requirements,
        max_new_tokens=120
    )

    return jsonify({
        "match_score": match_score,
        "derived_skills": derived_skills[:20],
        "matched_skills": matched_requirements[:15],
        "missing_skills": missing_requirements[:15],
        "suggestions": suggestions
    })

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
