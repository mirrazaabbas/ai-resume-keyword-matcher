# AI Resume Keyword Matcher

[![CI](https://github.com/mirrazaabbas/ai-resume-keyword-matcher/actions/workflows/ci.yml/badge.svg)](https://github.com/mirrazaabbas/ai-resume-keyword-matcher/actions/workflows/ci.yml)
[![Security](https://github.com/mirrazaabbas/ai-resume-keyword-matcher/actions/workflows/security.yml/badge.svg)](https://github.com/mirrazaabbas/ai-resume-keyword-matcher/actions/workflows/security.yml)

A transparent, truth-preserving resume/job-description analysis tool. It combines explainable ATS-style skill and keyword scoring with structured job-requirement extraction, resume-section checks, lexical similarity, optional PDF/DOCX ingestion, JSON output and a safe standalone HTML report.

## What it analyzes

- required vs preferred skills from structured job descriptions
- hard, soft and multi-word skills
- matched and missing required skills
- keyword overlap and lexical cosine similarity
- stated experience-year requirements
- education terms appearing in the JD
- presence of summary, experience, skills, education, certifications and projects sections
- truthful recommendations that never instruct a candidate to invent unsupported experience

## Supported documents

TXT and Markdown work with the base install. PDF and DOCX are available through the optional `documents` extra using `pypdf` and `python-docx`.

```bash
python -m pip install ".[documents]"
```

## CLI

```bash
resume-ats resume.pdf job-description.docx --format json --json report.json --html report.html
```

Source checkout:

```bash
python app.py sample_resume.txt sample_job.txt --html report.html
```

## Scoring boundary

The score is an **explainable portfolio heuristic**. It is not presented as the proprietary algorithm of Workday, Greenhouse, Lever, Taleo or any other commercial ATS. The tool surfaces gaps for review; a missing skill should only be added to a resume when it is genuinely supported by the candidate's experience.

## Engineering evidence

- installable Python package and `resume-ats` CLI
- Python 3.10–3.12 CI
- branch-coverage quality gate
- wheel build/install smoke test
- safe HTML escaping
- CodeQL static analysis
- dependency audit and CycloneDX SBOM generation
- weekly Dependabot maintenance

## Quality checks

```bash
python -m pip install -r requirements-dev.txt ".[documents]" build
ruff check .
coverage run -m unittest discover -s tests -v
coverage report --fail-under=80
python -m build
```

## Skills demonstrated

Python · ATS-style Analysis · NLP · Job Requirement Extraction · Document Parsing · PDF · DOCX · Skill Matching · Lexical Similarity · Truth-preserving Recommendations · JSON · HTML Reporting · Packaging · Testing · CI/CD · CodeQL · SBOM
