from __future__ import annotations

import unittest
from unittest.mock import patch

import ai_features
import ai_platform


class FakeClient:
    def generate(self, system: str, user: str) -> str:
        self.system = system
        self.user = user
        return "Use only truthful skills already supported by the resume."


class AiFeatureTests(unittest.TestCase):
    def test_resume_ai_explanation(self) -> None:
        client = FakeClient()
        result = ai_features.explain_match(
            "Python automation and APIs",
            "Need Python APIs automation and data analysis",
            client,
        )
        self.assertGreater(result["score"], 0)
        self.assertIn("truthful", result["ai_explanation"])
        self.assertIn("job_description", client.user)

    def test_provider_response_shapes(self) -> None:
        cases = [
            ("openai", {"choices": [{"message": {"content": "openai ok"}}]}, "openai ok"),
            ("anthropic", {"content": [{"text": "claude ok"}]}, "claude ok"),
            (
                "gemini",
                {"candidates": [{"content": {"parts": [{"text": "gemini ok"}]}}]},
                "gemini ok",
            ),
        ]
        for provider, payload, expected in cases:
            client = ai_platform.HTTPAIClient(
                ai_platform.AIConfig(provider, "key", "model", "https://example.test")
            )
            with patch.object(client, "_post", return_value=payload):
                self.assertEqual(client.generate("system", "user"), expected)


if __name__ == "__main__":
    unittest.main()
