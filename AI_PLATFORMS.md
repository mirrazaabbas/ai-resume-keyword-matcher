# AI platform compatibility

The resume matcher always computes its keyword score locally. An optional AI explanation layer uses the shared `AIClient` interface and supports OpenAI/OpenAI-compatible APIs, Anthropic Claude, and Google Gemini.

## Offline verification

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python app.py sample_resume.txt sample_job.txt
```

No API key is required for these checks.

## Provider selection

```bash
# OpenAI or OpenAI-compatible
export AI_PROVIDER=openai
export AI_API_KEY="YOUR_KEY"
export AI_MODEL="YOUR_CHAT_MODEL"
# Optional: export AI_BASE_URL="https://provider.example/v1"
```

```bash
# Anthropic Claude
export AI_PROVIDER=anthropic
export AI_API_KEY="YOUR_KEY"
export AI_MODEL="YOUR_CLAUDE_MODEL"
```

```bash
# Google Gemini
export AI_PROVIDER=gemini
export AI_API_KEY="YOUR_KEY"
export AI_MODEL="YOUR_GEMINI_MODEL"
```

## Run the optional AI explanation

```bash
python - <<'PY'
from pathlib import Path
from ai_features import explain_match
from ai_platform import create_ai_client
from app import read_file

resume = read_file(Path("sample_resume.txt"))
job = read_file(Path("sample_job.txt"))
result = explain_match(resume, job, create_ai_client())
print(result["score"])
print(result["ai_explanation"])
PY
```

The AI layer is instructed to explain the deterministic match honestly and not invent experience, skills, credentials, or achievements.
