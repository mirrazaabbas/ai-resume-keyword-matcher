"""CLI and compatibility helpers for transparent resume/job analysis."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from analysis import analyze_resume_job
from documents import read_document
from reporting import to_html

STOPWORDS = {"the","and","a","an","to","of","in","for","with","on","is","are","as","at","be","by","or","from","that","this","we","you","your","our","will","have","has","using","use"}


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9+#.-]*", text.lower())
    return [word for word in words if word not in STOPWORDS and len(word) > 1]


def keyword_counts(text: str) -> Counter[str]:
    return Counter(tokenize(text))


def match_resume(resume: str, job: str) -> dict[str, object]:
    """Legacy lightweight overlap score retained for API compatibility."""
    resume_words = set(tokenize(resume))
    important = [word for word, _ in keyword_counts(job).most_common(30)]
    matched = [word for word in important if word in resume_words]
    missing = [word for word in important if word not in resume_words]
    score = round((len(matched) / len(important)) * 100, 1) if important else 0.0
    return {"score": score, "matched": matched, "missing": missing}


def read_file(path: Path) -> str:
    """Backward-compatible document reader; now supports TXT/MD/PDF/DOCX."""
    return read_document(path)


def analyze_files(resume_path: Path, job_path: Path) -> dict[str, Any]:
    return analyze_resume_job(read_document(resume_path), read_document(job_path))


def _text_report(result: dict[str, Any]) -> str:
    lines = [
        f"Overall match score: {result['overall_match_score']}%",
        f"Required-skill score: {result['required_skill_score']}%",
        f"Lexical similarity: {result['lexical_similarity_score']}%",
        "",
        "Matched required skills: " + (", ".join(result["matched_required_skills"]) or "None detected"),
        "Missing required skills to verify: " + (", ".join(result["missing_required_skills"]) or "None detected"),
        "",
        "Truth-preserving recommendations:",
    ]
    recommendations = result["truthful_recommendations"]
    lines.extend(f"- {item}" for item in recommendations)
    lines.extend(["", str(result["accuracy_note"])])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="resume-ats",
        description="Analyze a resume against a job description with transparent ATS-style heuristics.",
    )
    parser.add_argument("resume", type=Path, help="Resume: TXT, MD, PDF or DOCX")
    parser.add_argument("job_description", type=Path, help="Job description: TXT, MD, PDF or DOCX")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--json", dest="json_path", type=Path, help="Write structured JSON report")
    parser.add_argument("--html", dest="html_path", type=Path, help="Write standalone HTML report")
    args = parser.parse_args()
    try:
        result = analyze_files(args.resume, args.job_description)
    except (ValueError, RuntimeError) as exc:
        parser.error(str(exc))

    rendered_json = json.dumps(result, indent=2, sort_keys=True)
    if args.json_path:
        args.json_path.write_text(rendered_json + "\n", encoding="utf-8")
    if args.html_path:
        args.html_path.write_text(to_html(result), encoding="utf-8")
    print(rendered_json if args.format == "json" else _text_report(result))


if __name__ == "__main__":
    main()
