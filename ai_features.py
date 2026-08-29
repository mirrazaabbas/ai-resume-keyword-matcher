"""Optional cross-platform AI explanation for deterministic resume-match results."""
from __future__ import annotations

import json

import app
from ai_platform import AIClient


def explain_match(resume: str, job: str, client: AIClient) -> dict[str, object]:
    if not resume.strip() or not job.strip():
        raise ValueError("Resume and job description must both contain text.")
    result = app.match_resume(resume, job)
    system = (
        "You are a truthful resume coach. Explain the deterministic keyword-match result. Never "
        "recommend adding skills, credentials, achievements, or experience the candidate does not have."
    )
    user = json.dumps(
        {
            "match_result": result,
            "resume": resume,
            "job_description": job,
        },
        ensure_ascii=False,
    )
    return {**result, "ai_explanation": client.generate(system, user)}
