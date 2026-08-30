# AI Resume Keyword Matcher

[![CI](https://github.com/mirrazaabbas/ai-resume-keyword-matcher/actions/workflows/ci.yml/badge.svg)](https://github.com/mirrazaabbas/ai-resume-keyword-matcher/actions/workflows/ci.yml)

A truth-preserving Python resume/job-description analysis tool. It keeps the original lightweight keyword CLI while adding structured ATS-style scoring for skills, keywords, multi-word phrases, missing requirements, and machine-readable reporting.

## Implemented features

### Lightweight matcher

- Resume/job text tokenization
- Stopword filtering
- Keyword frequency ranking
- Match percentage
- Matched and missing keyword lists
- UTF-8/file validation
- CLI workflow

### Structured ATS analysis

`ats.py` adds:

- Separate skill and keyword scores
- Weighted ATS-style overall score
- Hard-skill detection
- Soft-skill detection
- Multi-word skill/phrase detection
- Matched skill reporting
- Missing skill reporting
- Matched/missing keyword reporting
- JSON output helper
- Escaped standalone HTML report helper
- Explicit truthfulness rule for missing skills

The analyzer does **not** tell users to claim skills they do not have. Missing items are presented as review gaps and may only be added when genuinely supported by experience.

## Run the original CLI

```bash
python app.py sample_resume.txt sample_job.txt
```

## Run structured ATS analysis

```python
from pathlib import Path
import ats

resume = Path("sample_resume.txt").read_text(encoding="utf-8")
job = Path("sample_job.txt").read_text(encoding="utf-8")

result = ats.analyze(resume, job)
print(ats.to_json(result))
```

The result includes:

```text
ats_score
skill_score
keyword_score
matched_skills
missing_skills
matched_keywords
missing_keywords
truth_rule
```

## Quality checks

```bash
python -m pip install -r requirements-dev.txt
ruff check .
coverage run -m unittest discover -s tests -v
coverage report --fail-under=80
```

CI runs on Python 3.10–3.12 and covers both the original matcher and the structured ATS module.

## Dependency maintenance

Dependabot is configured for weekly Python and GitHub Actions dependency updates.

## Current scope

This project demonstrates transparent deterministic resume/JD matching. The ATS score is an explainable portfolio heuristic, **not** a claim to reproduce the proprietary ranking algorithm of every commercial applicant tracking system. Semantic embeddings, PDF/DOCX extraction, resume rewriting, and production recruitment-platform integrations remain separate extensions.

## Skills demonstrated

Python · ATS-style Analysis · Text Processing · Skill Extraction · Keyword Scoring · Multi-word Phrase Matching · JSON · HTML Reporting · Validation · Testing · CI/CD
