def calculate_match(resume_skills, jd_skills):
    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    score = round((len(matched) / len(jd_skills)) * 100, 2) if jd_skills else 0

    return score, matched, missing
