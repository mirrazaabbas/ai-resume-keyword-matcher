"""Structured, truth-preserving ATS-style analysis."""
from __future__ import annotations

import re
from typing import Any

import ats
from requirements import parse_job_requirements
from semantic import lexical_similarity

SECTION_ALIASES = {
    "summary": ("summary", "profile", "professional summary"),
    "experience": ("experience", "work experience", "employment"),
    "skills": ("skills", "technical skills", "core skills"),
    "education": ("education", "academic"),
    "certifications": ("certifications", "certificates"),
    "projects": ("projects", "project experience"),
}


def section_presence(resume: str) -> dict[str, bool]:
    lines = [re.sub(r"[^a-z ]", "", line.lower()).strip() for line in resume.splitlines()]
    return {
        section: any(line in aliases for line in lines)
        for section, aliases in SECTION_ALIASES.items()
    }


def analyze_resume_job(resume: str, job: str) -> dict[str, Any]:
    base = ats.analyze(resume, job)
    requirements = parse_job_requirements(job)
    sections = section_presence(resume)
    required = set(requirements["required_skills"])
    present = ats.extract_skills(resume)
    matched_required = sorted(required & present)
    missing_required = sorted(required - present)
    required_score = len(matched_required) / len(required) if required else 1.0
    structure_score = sum(sections.values()) / len(sections)
    similarity = lexical_similarity(resume, job)
    overall = round(
        0.50 * (float(base["ats_score"]) / 100)
        + 0.25 * required_score
        + 0.15 * similarity
        + 0.10 * structure_score,
        4,
    )
    suggestions = [
        f"Verify whether '{skill}' is genuinely supported by your experience before adding it."
        for skill in missing_required
    ]
    missing_sections = [name for name, present_value in sections.items() if not present_value]
    if missing_sections:
        suggestions.append(
            "Consider clearly labeled sections where truthful and relevant: "
            + ", ".join(missing_sections)
            + "."
        )
    return {
        "overall_match_score": round(overall * 100, 1),
        "ats": base,
        "requirements": requirements,
        "required_skill_score": round(required_score * 100, 1),
        "lexical_similarity_score": round(similarity * 100, 1),
        "section_presence": sections,
        "section_structure_score": round(structure_score * 100, 1),
        "matched_required_skills": matched_required,
        "missing_required_skills": missing_required,
        "truthful_recommendations": suggestions,
        "accuracy_note": (
            "This is a transparent heuristic and optional embedding interface, not a claim to "
            "replicate a proprietary ATS ranking algorithm."
        ),
    }
