import tempfile
import unittest
from pathlib import Path

import app


class ResumeMatcherTests(unittest.TestCase):
    def test_match_resume(self):
        result = app.match_resume(
            "Python automation prompt engineering APIs",
            "Need Python, APIs, automation and data analysis skills",
        )
        self.assertGreater(result["score"], 0)
        self.assertIn("python", result["matched"])

    def test_empty_job(self):
        result = app.match_resume("Python", "")
        self.assertEqual(result["score"], 0.0)
        self.assertEqual(result["matched"], [])

    def test_read_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resume.txt"
            path.write_text("Python AI automation", encoding="utf-8")
            self.assertIn("Python", app.read_file(path))
            with self.assertRaises(ValueError):
                app.read_file(Path(tmp) / "missing.txt")


if __name__ == "__main__":
    unittest.main()
