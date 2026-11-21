# Mathematical verification matrix

This ledger records the independent checks behind the worked examples in the eight articles. The examples are constructed for teaching; the checks below are reproducible calculations, not empirical claims.

## 01 · Vectors and linear combinations

Let $u=(1,2)$, $v=(2,1)$, and target $w=(0,3)$.

- Coefficients: $w=2u-v$.
- Direct coordinate check: $2(1,2)-(2,1)=(0,3)$.
- Independence check: $\det\begin{pmatrix}1&2\\2&1\end{pmatrix}=1-4=-3\ne0$.
- Consequence: $u,v$ form a basis of $\mathbb R^2$; the representation is unique.

## 02 · Matrices and linear transformations

For $A=\begin{pmatrix}2&1\\1&1\end{pmatrix}$:

- $Ae_1=(2,1)$ and $Ae_2=(1,1)$, matching the columns.
- For $x=(x_1,x_2)$, $Ax=x_1(2,1)+x_2(1,1)=(2x_1+x_2,x_1+x_2)$.
- With shear $S=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ and quarter-turn $R=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$, $SR=\begin{pmatrix}1&-1\\1&0\end{pmatrix}$, while $RS=\begin{pmatrix}0&-1\\1&1\end{pmatrix}$.
- Consequence: composition order matters; $SR\ne RS$.

## 03 · Linear systems and elimination

For $x+y=3$, $x-y=1$:

- Row operation $R_2\leftarrow R_2-R_1$ gives $0x-2y=-2$.
- Hence $y=1$, then $x=2$.
- Direct substitution: $2+1=3$, $2-1=1$.
- Inconsistent counterexample: $x+y=2$, $2x+2y=5$ reduces to $0=1$.
- Infinite-solution counterexample: $x+y=2$, $2x+2y=4$ has one independent equation and one free variable.

## 04 · Vector spaces, rank and dimension

Let $A=\begin{pmatrix}1&2&3\\2&4&6\end{pmatrix}$.

- The second row is twice the first, so $\operatorname{rank}(A)=1$.
- $Ax=0$ reduces to $x+2y+3z=0$, with basis $(-2,1,0)$, $(-3,0,1)$; nullity $=2$.
- Rank–nullity: $1+2=3$, equal to the number of columns.
- Row-space orthogonality: $(1,2,3)\cdot(-2,1,0)=0$ and $(1,2,3)\cdot(-3,0,1)=0$.
- Left-nullspace check: $(-2,1)^TA=(0,0,0)$.

## 05 · Determinants

For $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$:

- $\det(A)=1\cdot4-2\cdot3=-2$.
- The transformed unit square has area $|\det(A)|=2$, and the negative sign records orientation reversal.
- The columns $(1,3)$, $(2,4)$ are independent because the determinant is nonzero.
- Singular counterexample: $\begin{pmatrix}2&4\\1&2\end{pmatrix}$ has determinant zero and dependent columns.

## 06 · Eigenvalues and eigenvectors

For $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$:

- Characteristic polynomial: $(2-\lambda)^2-1=(\lambda-1)(\lambda-3)$.
- Eigenpairs: $A(1,1)=3(1,1)$, $A(1,-1)=1(1,-1)$.
- Trace check: $3+1=4=\operatorname{tr}(A)$.
- Determinant check: $3\cdot1=3=\det(A)$.
- Diagonalization: $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$, $D=\operatorname{diag}(3,1)$, and $A=PDP^{-1}$.
- Non-diagonalizable counterexample: $\begin{pmatrix}1&1\\0&1\end{pmatrix}$ has only one independent eigenvector.

## 07 · Orthogonal projection and least squares

For observations $(0,1),(1,2),(2,2)$ and design matrix $A=\begin{pmatrix}1&0\\1&1\\1&2\end{pmatrix}$:

- $A^TA=\begin{pmatrix}3&3\\3&5\end{pmatrix}$, $A^Tb=(5,6)^T$.
- Solving the normal equations gives $c=7/6$, $m=1/2$.
- Residual $r=b-A\hat{x}=(-1/6,1/3,-1/6)^T$.
- Orthogonality check: $A^Tr=(0,0)^T$.
- Projection check: for $a=(1,1)$, $b=(2,0)$, $\operatorname{proj}_a b=(1,1)$ and residual $(1,-1)\cdot(1,1)=0$.

## 08 · Singular value decomposition

For $A=\operatorname{diag}(3,1)$:

- One valid SVD is $U=I$, $\Sigma=\operatorname{diag}(3,1)$, $V=I$.
- The unit circle maps to an ellipse with semi-axes 3 and 1.
- Truncating to rank 1 gives $A_1=\operatorname{diag}(3,0)$.
- Frobenius error: $\|A-A_1\|_F=\sqrt{1^2}=1$.
- Retaining both singular directions gives exact reconstruction and zero error.

## What these checks do and do not establish

- Direct substitution verifies the displayed solutions and eigenpairs.
- Rank–nullity and orthogonality checks verify the stated subspace dimensions and relationships.
- Determinant and singular-value calculations verify the specific geometric scale examples.
- These examples do not replace proofs of the general theorems; the articles state the relevant hypotheses and connect each worked example to the general result.
