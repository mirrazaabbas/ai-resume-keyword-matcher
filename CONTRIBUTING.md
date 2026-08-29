# Contributing

Contributions should keep the matcher transparent, testable, and careful not to encourage misleading resume claims.

1. Create a focused branch from `main`.
2. Add tests for scoring, tokenization, validation, or CLI behavior changes.
3. Run `ruff check .`, the coverage-gated unit tests, and the sample CLI smoke test.
4. Never commit credentials, private resumes, or personal data.
5. Keep suggestions framed as keywords to review and use only where they truthfully match a candidate's background.
6. In the pull request, explain what changed, why it changed, and how it was tested.
