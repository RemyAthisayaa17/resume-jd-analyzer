from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber, re

app = Flask(__name__)
CORS(app)

def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for p in pdf.pages:
            if p.extract_text():
                text += p.extract_text() + " "
    return text.lower()

def normalize(t):
    t = re.sub(r"[^a-z0-9+.# ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def keywords(t):
    return set(normalize(t).split())

def score_message(score):
    if score >= 80:
        return "Strong alignment with role expectations."
    if score >= 60:
        return "Moderate alignment with core requirements."
    if score >= 40:
        return "Partial alignment. Targeted improvements recommended."
    return "Low alignment. Significant gaps detected."

@app.route("/analyze", methods=["POST"])
def analyze():
    resume = request.files.get("resume")
    jd = request.form.get("jd")

    resume_words = keywords(extract_text(resume))
    jd_words = keywords(jd)

    matched = resume_words & jd_words
    missing = jd_words - resume_words

    score = round((len(matched) / len(jd_words)) * 100, 1) if jd_words else 0

    suggestions = [
        f"{s.capitalize()} is required but not clearly reflected. "
        f"Adding a focused project or explicit mention would improve alignment."
        for s in list(missing)[:5]
    ] or ["Profile demonstrates strong alignment. Focus on clarity and depth."]

    return jsonify({
        "match_score": score,
        "score_message": score_message(score),
        "matched_skills": list(matched)[:12],
        "missing_skills": list(missing)[:12],
        "suggestions": suggestions
    })

if __name__ == "__main__":
    app.run(debug=True)
