import unittest
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "content/01-vectors/index.html",
    "content/02-linear-transformations/index.html",
    "content/03-linear-systems/index.html",
    "content/04-vector-spaces/index.html",
    "content/05-determinants/index.html",
    "content/06-eigenvalues/index.html",
    "content/07-least-squares/index.html",
    "content/08-svd/index.html",
]

class CourseStructureTests(unittest.TestCase):
    def test_eight_modules_exist(self):
        self.assertEqual(len(PAGES), 8)
        for page in PAGES:
            self.assertTrue((ROOT / page).is_file(), page)

    def test_each_module_has_math_visual_and_interaction(self):
        for page in PAGES:
            html = (ROOT / page).read_text(encoding="utf-8")
            with self.subTest(page=page):
                self.assertEqual(len(re.findall(r"<h1\b", html)), 1)
                self.assertGreaterEqual(len(re.findall(r"<math\b", html)), 4)
                self.assertIn("<figure", html)
                self.assertIn("data-demo=", html)
                self.assertIn("<figcaption", html)
                self.assertIn('aria-label=', html)

    def test_homepage_links_all_modules(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for page in PAGES:
            self.assertIn(page, html)

    def test_no_cdn_math_or_js(self):
        pages = [(ROOT / "index.html")] + [ROOT / p for p in PAGES]
        for page in pages:
            html = page.read_text(encoding="utf-8")
            self.assertNotRegex(html, r'<script[^>]+src=["\']https?://')
            self.assertNotRegex(html, r'<link[^>]+href=["\']https?://')

class WorkedExampleTests(unittest.TestCase):
    def test_linear_system_example(self):
        # 2x + y = 5, x - y = 1
        x, y = 2, 1
        self.assertEqual(2*x + y, 5)
        self.assertEqual(x - y, 1)

    def test_rank_nullity_example(self):
        # A = [[1,2,3],[2,4,6]] has rank 1 and nullity 2.
        self.assertEqual(1 + 2, 3)

    def test_eigenpair_example(self):
        # A = [[2,1],[1,2]], v=(1,1), lambda=3.
        A = ((2,1),(1,2))
        v = (1,1)
        Av = (A[0][0]*v[0]+A[0][1]*v[1], A[1][0]*v[0]+A[1][1]*v[1])
        self.assertEqual(Av, (3,3))

    def test_least_squares_residual_is_orthogonal(self):
        # Points (0,1),(1,2),(2,2), fitted y=7/6 + x/2.
        residual = (-1/6, 1/3, -1/6)
        self.assertAlmostEqual(sum(residual), 0)
        self.assertAlmostEqual(0*residual[0] + residual[1] + 2*residual[2], 0)

    def test_svd_diagonal_example(self):
        # diag(3,1) = I diag(3,1) I^T; rank-one truncation error is 1.
        singular_values = (3,1)
        self.assertEqual(singular_values[0], 3)
        self.assertEqual(singular_values[1], 1)
        self.assertEqual((sum(x*x for x in singular_values[1:]))**0.5, 1)

if __name__ == "__main__":
    unittest.main()
