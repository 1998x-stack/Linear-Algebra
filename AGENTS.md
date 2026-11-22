# Agent instructions

## Authority and scope

This repository is a Chinese undergraduate linear-algebra teaching site. Use the [Olah-style-posts](https://github.com/1998x-stack/Olah-style-posts) workflow as a methodological reference, not as a source to copy. The goal is a mathematically correct, independently written course with visual explanations.

## Mandatory article workflow

1. **Define the question.** Begin with a misconception, concrete problem, or geometric tension.
2. **Plan the learning path.** Use the order: concrete example → visual model → definition → equation → derivation → worked example → limits/counterexample → synthesis.
3. **Check the mathematics first.** State dimensions, assumptions, domains, and notation. Verify each worked example by substitution or an independent route.
4. **Draw to explain a claim.** Each SVG needs a question, a meaningful caption, `title`, `desc`, `viewBox`, and legible labels. Arrows and axes must agree with the mathematics.
5. **Typeset equations semantically.** Use MathML Core for substantive expressions. Every `math` has an accurate `aria-label`; display math sits in a keyboard-focusable horizontal scroll region. Never nest MathML inside SVG.
6. **Make interaction optional.** The static page must remain mathematically complete if JavaScript is disabled. Controls must update a visible mathematical state and have accessible labels.
7. **Cross-check.** Use at least two of: symbolic derivation, direct substitution, dimension/rank check, geometric interpretation, independent numerical computation, counterexample.
8. **Maintain the verification ledger.** Keep `references/verification-matrix.md` aligned with worked examples; update exact computations when article examples change.
9. **Cite learning sources.** Cite MIT 18.06 / Hefferon / other primary educational sources where appropriate. Do not imply a source contains an original illustration or proof that was independently created here.
10. **Validate before publishing.** Run `python3 scripts/validate_site.py`, `python3 -m unittest discover -s tests -v`, and (after installing `requirements-dev.txt` plus Chromium) `python3 scripts/browser_smoke.py`. Review screenshots before claiming visual QA.

## Content standards

- Distinguish definitions, theorems, intuition, worked examples, and numerical experiments.
- Do not treat a diagram as a proof; state the algebraic reason as well.
- Explain why a formula is true and when it applies, not only how to calculate it.
- Distinguish square/invertible matrices from rectangular matrices; distinguish eigenvalues from singular values.
- Keep matrix dimensions explicit for products and transformations.
- For least squares, distinguish an exact solution from a minimizer of residual norm.
- For SVD, state singular values are nonnegative and ordered; do not imply every matrix is diagonalizable.
- Avoid unsupported claims about applications or historical attribution.
- Do not copy text, diagrams, code, or branded design assets from Colah, 3Blue1Brown, MIT, or textbook sources.

## Repository structure

- `index.html`: course homepage and learning route.
- `content/NN-topic/index.html`: standalone article.
- `assets/diagrams/`: standalone, original SVG diagrams.
- `assets/css/site.css`, `assets/js/site.js`: shared site system and progressive enhancement.
- `references/reading-map.md`: source map.
- `scripts/validate_site.py`, `tests/`: repeatable checks.

## Release gate

A successful static check is not the same as browser QA. Report each check as passed, failed, or not verified. Do not claim GitHub Pages is live until the Actions deployment succeeds and the workflow confirms its environment URL.


## Second-batch content and verification rules

- The course now has sixteen numbered modules. Keep the progression coherent: LU → QR → orthogonal matrices → symmetric matrices → positive definiteness → spectral theorem → PCA → SVD image compression.
- Every new module must contain eight substantial sections, at least eight original SVG figures, at least eight accessible MathML display equations, one meaningful interactive experiment, and one self-check.
- Each module directory must include an evidence.json ledger. Separate theorem/course references from calculations independently derived for the worked example; use verified only for claims checked against the cited source and derived for calculations reproduced in the verification matrix.
- Every figure must have a useful Chinese alt description in the HTML and a title plus desc in the SVG. Avoid generic decorative figures; each diagram must explain a specific step, geometry, comparison, or data structure.
- Cross-check numerical examples independently: multiply factors back, substitute solutions, verify orthogonality, check dimensions, compute determinant/eigenvalue signs, and report residuals where relevant.
- Keep the Matrix Computation Lab explicitly educational and bounded to 2×2/3×3 matrices. Do not describe its Jacobi/Gram–Schmidt implementations as production-grade replacements for LAPACK, NumPy, or SciPy.
- When changing an example, update its article, evidence.json, references/verification-matrix.md, Python regression tests, and browser interaction expectation in the same change.
- Before release run scripts/validate_site.py, unittest discovery, and scripts/browser_smoke.py after installing Chromium. Inspect desktop and mobile screenshots, not just test exit codes.
