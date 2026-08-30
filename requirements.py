"""Structured job-description requirement extraction."""
from __future__ import annotations

import re
from typing import Any

from ats import extract_skills

HEADING_ALIASES = {
    "required": {"required", "requirements", "must have", "qualifications"},
    "preferred": {"preferred", "nice to have", "desired", "bonus"},
    "responsibilities": {"responsibilities", "what you will do", "duties"},
}
DEGREE_TERMS = (
    "bachelor",
    "bachelors",
    "bachelor's",
    "master",
    "masters",
    "master's",
    "degree",
    "bba",
    "mba",
    "b.tech",
    "btech",
)


def parse_job_requirements(text: str) -> dict[str, Any]:
    if not text.strip():
        raise ValueError("job description cannot be empty")
    sections = _sections(text)
    required_text = sections.get("required", text)
    preferred_text = sections.get("preferred", "")
    responsibilities_text = sections.get("responsibilities", "")
    years = [
        int(value)
        for value in re.findall(r"\b(\d{1,2})\+?\s*(?:years?|yrs?)\b", text.lower())
    ]
    education = sorted({term for term in DEGREE_TERMS if term in text.lower()})
    return {
        "required_skills": sorted(extract_skills(required_text)),
        "preferred_skills": sorted(extract_skills(preferred_text)),
        "minimum_experience_years": min(years) if years else None,
        "education_terms": education,
        "responsibilities": _bullet_lines(responsibilities_text),
    }


def _sections(text: str) -> dict[str, str]:
    lines = text.splitlines()
    result: dict[str, list[str]] = {}
    current: str | None = None
    for raw in lines:
        stripped = raw.strip()
        normalized = stripped.lower().rstrip(":")
        matched = next(
            (
                canonical
                for canonical, aliases in HEADING_ALIASES.items()
                if normalized in aliases
            ),
            None,
        )
        if matched:
            current = matched
            result.setdefault(current, [])
            continue
        if current is not None:
            result[current].append(raw)
    return {key: "\n".join(value).strip() for key, value in result.items()}


def _bullet_lines(text: str) -> list[str]:
    items = []
    for line in text.splitlines():
        value = re.sub(r"^\s*[-*•]\s*", "", line).strip()
        if value:
            items.append(value)
    return items
