import tempfile
import unittest
from pathlib import Path

from analysis import analyze_resume_job
from documents import read_document
from reporting import to_html
from requirements import parse_job_requirements
from semantic import embedding_similarity, lexical_similarity


class FakeEmbedder:
    def embed(self, texts):
        return [[1.0, 0.0], [1.0, 0.0]]


class AdvancedResumeTests(unittest.TestCase):
    def test_requirement_and_structured_analysis(self):
        job = """Requirements:\n- Python\n- customer service\n- 3+ years experience\nPreferred:\n- prompt engineering\nResponsibilities:\n- Support customers"""
        resume = """Summary\nOperations professional\nExperience\nPython customer service\nSkills\nPython\nEducation\nBBA\nCertifications\nGoogle AI"""
        requirements = parse_job_requirements(job)
        self.assertEqual(requirements["minimum_experience_years"], 3)
        result = analyze_resume_job(resume, job)
        self.assertIn("python", result["matched_required_skills"])
        self.assertGreater(result["overall_match_score"], 0)
        self.assertIn("transparent heuristic", result["accuracy_note"])

    def test_similarity_and_html_escape(self):
        self.assertGreater(lexical_similarity("python automation", "python systems"), 0)
        self.assertEqual(embedding_similarity("a", "b", FakeEmbedder()), 1.0)
        result = analyze_resume_job("Skills\nPython", "Requirements:\nPython")
        result["truthful_recommendations"].append("<script>alert(1)</script>")
        rendered = to_html(result)
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_txt_document_reader(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resume.txt"
            path.write_text("Python automation", encoding="utf-8")
            self.assertEqual(read_document(path), "Python automation")
            bad = Path(tmp) / "resume.exe"
            bad.write_text("x", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_document(bad)


if __name__ == "__main__":
    unittest.main()
