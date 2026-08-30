"""Similarity primitives for resume/job matching."""
from __future__ import annotations

import math
from collections import Counter
from typing import Protocol

from ats import tokens


class EmbeddingProvider(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]: ...


def lexical_similarity(resume: str, job: str) -> float:
    """Cosine similarity over normalized term-frequency vectors."""
    left = Counter(tokens(resume))
    right = Counter(tokens(job))
    if not left or not right:
        return 0.0
    dot = sum(value * right.get(term, 0) for term, value in left.items())
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return round(dot / (left_norm * right_norm), 6) if left_norm and right_norm else 0.0


def embedding_similarity(resume: str, job: str, provider: EmbeddingProvider) -> float:
    if not resume.strip() or not job.strip():
        raise ValueError("resume and job text must be non-empty")
    vectors = provider.embed([resume, job])
    if len(vectors) != 2 or not vectors[0] or len(vectors[0]) != len(vectors[1]):
        raise RuntimeError("embedding provider returned invalid vectors")
    dot = sum(a * b for a, b in zip(vectors[0], vectors[1], strict=True))
    a_norm = math.sqrt(sum(value * value for value in vectors[0]))
    b_norm = math.sqrt(sum(value * value for value in vectors[1]))
    if not a_norm or not b_norm:
        return 0.0
    cosine = max(-1.0, min(1.0, dot / (a_norm * b_norm)))
    return round((cosine + 1.0) / 2.0, 6)
