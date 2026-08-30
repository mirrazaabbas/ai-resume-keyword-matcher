import unittest

import ats


class AtsTests(unittest.TestCase):
    def test_analyze_scores_supported_skills(self):
        result = ats.analyze(
            "Python automation customer service Excel",
            "Need Python automation data analysis customer service and Excel",
        )
        self.assertGreater(result["ats_score"], 0)
        self.assertIn("python", result["matched_skills"])
        self.assertIn("data analysis", result["missing_skills"])

    def test_truth_rule_is_explicit(self):
        result = ats.analyze("Python", "Python SQL")
        self.assertIn("genuinely supported", result["truth_rule"])

    def test_output_formats(self):
        result = ats.analyze("Python", "Python SQL")
        self.assertIn('"ats_score"', ats.to_json(result))
        self.assertIn("ATS Score", ats.to_html(result))

    def test_empty_input_is_rejected(self):
        with self.assertRaises(ValueError):
            ats.analyze("", "Python")


if __name__ == "__main__":
    unittest.main()
