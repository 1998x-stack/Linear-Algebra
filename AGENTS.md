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
8. **Maintain the verification ledger.** Keep `references/verification-matrix.md` aligned with worked examples; update exact computations when article examples change.\n9. **Cite learning sources.** Cite MIT 18.06 / Hefferon / other primary educational sources where appropriate. Do not imply a source contains an original illustration or proof that was independently created here.
10. **Validate before publishing.** Run `python3 scripts/validate_site.py` and `python3 -m unittest discover -s tests -v`. Review the actual rendered page at desktop and mobile widths before claiming browser QA.

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

A successful static check is not the same as browser QA. Report each check as passed, failed, or not verified. Do not claim GitHub Pages is live until the Actions deployment succeeds and the public URL is opened successfully.
