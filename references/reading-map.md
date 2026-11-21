# Reading map and cross-check sources

This repository is an independently written course. The sources below anchor the topic order and mathematical conventions; they are not copied article text or diagram sources.

## Main course spine: MIT 18.06

Gilbert Strang's [MIT OCW 18.06SC Linear Algebra (Fall 2011)](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/) is the primary syllabus cross-check. Its first unit develops (Ax=b), elimination, column space and nullspace, independence, basis, dimension, and the four fundamental subspaces. Its second unit develops orthogonality, projection, least squares, determinants, and eigenvalues. The older [Spring 2010 18.06 lecture index](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/video_galleries/video-lectures/) includes LU, Gram–Schmidt, diagonalization, Markov matrices, and further topics.

## Conceptual and proof-oriented reading

- Jim Hefferon, [Linear Algebra](https://hefferon.net/linearalgebra/): a free first-course textbook. Use for definitions, theorem statements, proof structure, exercises, and computational examples.
- Gilbert Strang, [Lecture Notes for Linear Algebra](https://www-math.mit.edu/~gs/LectureNotes/): useful for linear combinations, dot products, matrix-vector products, column/row spaces, independence, factorizations, and SVD.
- 3Blue1Brown, [Linear Algebra topic collection](https://www.3blue1brown.com/topics/linear-algebra): a visual pedagogy reference for vectors, span, transformations, determinants, null spaces, dot products, eigenvectors, and abstract vector spaces. The diagrams in this repository are original and must not imitate or reuse its assets.

## Math on the web

- NIST Digital Library of Mathematical Functions, [About MathML](https://dlmf.nist.gov/help/mathml): MathML is a standard representation of mathematical content; MathML Core is designed for browsers.
- MDN, [MathML](https://developer.mozilla.org/en-US/docs/Web/MathML): browser-facing MathML Core reference and compatibility information.

## Module-to-source crosswalk

| Module | MIT 18.06 themes | Independent verification focus |
|---|---|---|
| 01 Vectors and linear combinations | Geometry of linear equations; linear combinations; column space | Coordinates, closure, span and independence examples |
| 02 Matrices and linear transformations | Matrix-vector multiplication; matrix multiplication; change of basis | Columns are images of basis vectors; composition order |
| 03 Linear systems and elimination | Elimination; LU; solving (Ax=b); RREF | Row operations preserve solution set; consistency and rank |
| 04 Vector spaces, rank and dimension | Vector spaces; nullspace; basis and dimension; four subspaces | Rank–nullity and orthogonal complement dimensions |
| 05 Determinants | Determinant properties; cofactor formulas; volume | Signed area, row-operation effects, invertibility |
| 06 Eigenvalues and eigenvectors | Eigenvalues; diagonalization; powers of (A) | Characteristic polynomial and direct eigenvector substitution |
| 07 Orthogonality and least squares | Orthogonal subspaces; projection; least squares; Gram–Schmidt | Normal equations, residual orthogonality, direct residual check |
| 08 SVD and low-rank approximation | Singular values and vectors; image compression | (A^TA), orthonormal factors, rank-(k) approximation |

## Citation and scope policy

- Cite the course or textbook for the topic's standard mathematical framework, not as proof that the independent examples appear in that source.
- Worked examples are explicitly labeled as constructed examples.
- No empirical performance claims are made in this course. Any numerical output is calculated from the displayed matrix or data.
- If a convention differs across sources (for example, row-vectors versus column-vectors in a data matrix), state the convention at the point of use.
