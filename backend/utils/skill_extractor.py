# backend/utils/skill_extractor.py

import re

# -----------------------------
# DOMAIN SKILLS (expandable)
# -----------------------------

TECH_SKILLS = [
    "HTML", "CSS", "JavaScript", "React", "Angular", "Vue", "Node.js", "Express", "TypeScript",
    "Python", "Django", "Flask", "FastAPI", "Java", "Spring", "C++", "C#", "SQL", "MongoDB",
    "PostgreSQL", "MySQL", "Git", "Docker", "Kubernetes", "REST", "GraphQL", "Redux",
    "UI", "UX", "Web Development", "Frontend", "Backend", "Full Stack"
]

AI_SKILLS = [
    "AI", "ML", "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing",
    "Computer Vision", "TensorFlow", "PyTorch", "Keras", "HuggingFace", "Transformers",
    "LangChain", "Stable Diffusion", "Diffusers", "OpenAI", "Reinforcement Learning",
    "Generative AI", "Data Science", "Data Analysis", "Scikit-learn", "Pandas", "NumPy"
]

NON_TECH_SKILLS = [
    "Leadership", "Communication", "Collaboration", "Teamwork", "Project Management",
    "Agile", "Scrum", "Critical Thinking", "Problem Solving", "Time Management",
    "Customer Service", "Sales", "Marketing", "Business Strategy", "Finance", "Analytics"
]

# Merge all into a single common list for extraction
COMMON_SKILLS = TECH_SKILLS + AI_SKILLS + NON_TECH_SKILLS

# Normalize skill names (React.js → React, PyTorch → PyTorch)
SKILL_NORMALIZATION = {
    "react.js": "React",
    "vue.js": "Vue",
    "nodejs": "Node.js",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "keras": "Keras",
    "nlp": "NLP",
    "ai": "AI",
    "ml": "ML",
    "c++": "C++",
    "c#": "C#"
}

# -----------------------------
# Skill Extraction Function
# -----------------------------

def extract_skills_from_text(text: str) -> list[str]:
    """
    Extract skills from resume text based on predefined domain skills.
    - Handles duplicates, variations, and common skill aliases.
    - Returns a clean, sorted list.
    """
    if not text:
        return []

    text = text.lower()
    found_skills = set()

    for skill in COMMON_SKILLS:
        skill_lower = skill.lower()
        # exact match or word boundary to avoid partial matches
        if re.search(rf"\b{re.escape(skill_lower)}\b", text):
            # normalize if mapping exists
            normalized = SKILL_NORMALIZATION.get(skill_lower, skill)
            found_skills.add(normalized)

    # Return sorted list for consistency
    return sorted(found_skills)
