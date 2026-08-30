"""Truth-preserving ATS-style resume analysis."""
from __future__ import annotations

import html
import json
import re
from collections import Counter

STOPWORDS = {"the","and","a","an","to","of","in","for","with","on","is","are","as","at","be","by","or","from","that","this","we","you","your","our","will","have","has","using","use"}
HARD_SKILLS = {"python","sql","excel","docker","git","github","fastapi","rag","automation","crm","kyc","aml","reporting","reconciliation"}
SOFT_SKILLS = {"communication","leadership","coaching","mentoring","collaboration"}
PHRASE_SKILLS = {"google sheets","prompt engineering","ai agents","data analysis","customer service","stakeholder management","team management","process improvement","escalation management","problem solving"}


def tokens(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9+#.-]*", (text or "").lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def extract_skills(text: str) -> set[str]:
    normalized = re.sub(r"\s+", " ", (text or "").lower())
    found = {s for s in PHRASE_SKILLS if re.search(rf"(?<!\w){re.escape(s)}(?!\w)", normalized)}
    words = set(tokens(text))
    found.update((HARD_SKILLS | SOFT_SKILLS) & words)
    return found


def keyword_score(resume: str, job: str, limit: int = 30) -> tuple[float, list[str], list[str]]:
    resume_words = set(tokens(resume))
    important = [word for word, _ in Counter(tokens(job)).most_common(limit)]
    matched = [word for word in important if word in resume_words]
    missing = [word for word in important if word not in resume_words]
    score = len(matched) / len(important) if important else 0.0
    return score, matched, missing


def analyze(resume: str, job: str) -> dict[str, object]:
    if not resume.strip() or not job.strip():
        raise ValueError("Resume and job description must both contain text.")
    job_skills = extract_skills(job)
    resume_skills = extract_skills(resume)
    matched_skills = sorted(job_skills & resume_skills)
    missing_skills = sorted(job_skills - resume_skills)
    skill_score = len(matched_skills) / len(job_skills) if job_skills else 1.0
    kw_score, matched_keywords, missing_keywords = keyword_score(resume, job)
    final = round((0.65 * skill_score + 0.35 * kw_score) * 100, 1)
    return {
        "ats_score": final,
        "skill_score": round(skill_score * 100, 1),
        "keyword_score": round(kw_score * 100, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "truth_rule": "Only add missing skills when they are genuinely supported by your experience.",
    }


def to_json(result: dict[str, object]) -> str:
    return json.dumps(result, indent=2, sort_keys=True)


def to_html(result: dict[str, object]) -> str:
    rows = "".join(f"<li>{html.escape(str(skill))}</li>" for skill in result["missing_skills"])
    return (
        "<!doctype html><meta charset='utf-8'><title>ATS Report</title>"
        f"<h1>ATS Score: {result['ats_score']}%</h1>"
        f"<p>Skill score: {result['skill_score']}% · Keyword score: {result['keyword_score']}%</p>"
        f"<h2>Missing skills to review truthfully</h2><ul>{rows}</ul>"
        f"<p>{html.escape(str(result['truth_rule']))}</p>"
    )
