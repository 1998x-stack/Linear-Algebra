import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = sorted((ROOT / "content").glob("[0-9][0-9]-*/index.html"))

class CourseContentTests(unittest.TestCase):
    def test_sixteen_modules_exist(self):
        self.assertEqual(len(ARTICLES), 16)
        for path in ARTICLES:
            with self.subTest(path=path):
                self.assertTrue(path.exists())
                self.assertTrue(path.parent.name[:2].isdigit())
    def test_each_article_has_eight_figures_math_and_a_demo(self):
        for path in ARTICLES:
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertGreaterEqual(source.count("<figure>"), 8)
                self.assertGreaterEqual(source.count("<math "), 8)
                self.assertIn("data-demo=", source)
                self.assertEqual(source.count("<h1>"), 1)
    def test_each_module_has_evidence_ledger(self):
        for path in ARTICLES:
            evidence_path = path.parent / "evidence.json"
            with self.subTest(path=evidence_path):
                data = json.loads(evidence_path.read_text(encoding="utf-8"))
                self.assertEqual(data["module"], path.parent.name[:2])
                self.assertGreaterEqual(len(data["evidence"]), 3)
    def test_every_article_figure_points_to_a_real_svg(self):
        for path in ARTICLES:
            source = path.read_text(encoding="utf-8")
            refs = re.findall(r'<img[^>]+src="([^"]+\.svg)"', source)
            with self.subTest(path=path):
                self.assertGreaterEqual(len(refs), 8)
                for ref in refs:
                    self.assertTrue((path.parent / ref).resolve().exists(), ref)
    def test_homepage_and_lab_are_present(self):
        home=(ROOT/"index.html").read_text(encoding="utf-8")
        lab=(ROOT/"lab/index.html").read_text(encoding="utf-8")
        self.assertIn("content/16-image-compression/index.html",home)
        self.assertIn("lab/index.html",home)
        self.assertIn('id="run-lab"',lab)
        self.assertIn('id="matrix-input"',lab)

if __name__ == "__main__":
    unittest.main()
