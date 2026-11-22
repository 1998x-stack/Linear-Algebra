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


## 09 · LU decomposition

For
\[
A=\begin{pmatrix}2&1&1\\4&-6&0\\-2&7&2\end{pmatrix},\quad
L=\begin{pmatrix}1&0&0\\2&1&0\\-1&-1&1\end{pmatrix},\quad
U=\begin{pmatrix}2&1&1\\0&-8&-2\\0&0&1\end{pmatrix}.
\]
- Row 2 of LU is 2U₁+U₂=(4,−6,0); row 3 is −U₁−U₂+U₃=(−2,7,2). Thus LU=A exactly.
- For b=(5,−2,9)ᵀ, forward substitution gives y=(5,−12,2)ᵀ; back substitution gives x=(1,1,2)ᵀ.
- Direct substitution: Ax=(5,−2,9)ᵀ=b.
- This example has nonzero pivots 2, −8, 1; it does not demonstrate the need for pivoting. The separate pivoting example is a structural counterexample.

## 10 · QR and least squares

Let a₁=(1,1,0)ᵀ, a₂=(1,0,1)ᵀ, and A=[a₁ a₂].
- q₁=(1,1,0)ᵀ/√2.
- u₂=a₂−(q₁ᵀa₂)q₁=(1/2,−1/2,1)ᵀ, with ‖u₂‖=√6/2.
- q₂=(1,−1,2)ᵀ/√6, so q₁ᵀq₂=0 and both columns have unit norm.
- R=QᵀA=[[√2,1/√2],[0,√6/2]], and multiplication verifies QR=A.
- For b=(1,2,0)ᵀ, least squares gives x=(5/3,−1/3)ᵀ. Residual r=(-1/3,1/3,1/3)ᵀ and Aᵀr=(0,0)ᵀ.

## 11 · Orthogonal matrices

- For planar rotation R(θ)=[[cosθ,−sinθ],[sinθ,cosθ]], RᵀR=I and det R=1.
- Reflection F=diag(1,−1) satisfies FᵀF=I and det F=−1.
- For v=(3,4)ᵀ, ‖v‖=5; both Rv and FRv have norm 5.
- A 3×2 matrix with orthonormal columns satisfies QᵀQ=I₂, while QQᵀ has rank 2 and is a projection, not I₃.

## 12 · Symmetric matrices

For A=[[2,1],[1,2]]:
- Characteristic polynomial (2−λ)²−1=(λ−1)(λ−3), so eigenvalues are 3 and 1.
- Eigenvectors (1,1)ᵀ and (1,−1)ᵀ have dot product 0.
- Trace check: 3+1=4=tr(A); determinant check: 3·1=3=det(A).
- Counterexample: B=[[1,1],[0,2]] has eigenvectors (1,0)ᵀ and (1,1)ᵀ, whose dot product is 1.

## 13 · Positive definiteness

For A=[[4,2],[2,3]]:
- Leading principal minors are Δ₁=4>0 and Δ₂=det(A)=12−4=8>0; Sylvester confirms positive definiteness.
- Completing the square: xᵀAx=4x²+4xy+3y²=4(x+y/2)²+2y².
- Cholesky factor L=[[2,0],[1,√2]] satisfies LLᵀ=A.
- Eigenvalues solve λ²−7λ+8=0: (7±√17)/2, both positive.
- For A(c)=[[4,c],[c,3]], det(A)=12−c²; positive definiteness requires |c|<√12.

## 14 · Spectral theorem

For A=[[2,1],[1,2]]:
- Orthonormal eigenvectors are columns of Q=(1/√2)[[1,1],[1,−1]], with Λ=diag(3,1).
- Multiplication verifies QΛQᵀ=A and QᵀQ=I.
- A²=[[5,4],[4,5]], consistent with Q diag(9,1) Qᵀ.
- The real planar rotation [[0,−1],[1,0]] has eigenvalues ±i, so it has no real eigenbasis and is not real orthogonally diagonalizable.

## 15 · Principal component analysis

Use four centered observations {2u₁,−2u₁,u₂,−u₂}, where u₁=(√3/2,1/2)ᵀ and u₂=(−1/2,√3/2)ᵀ are orthonormal.
- Sample covariance is C=(8u₁u₁ᵀ+2u₂u₂ᵀ)/3.
- Eigenvalues are 8/3 and 2/3; explained-variance ratios are 80% and 20%.
- Keeping only PC1 leaves squared Frobenius reconstruction error 2; keeping both components leaves error 0.
- The example is synthetic and exact; it is not a benchmark result from a real dataset.

## 16 · SVD image approximation

Construct an 8×8 Sylvester Hadamard matrix H and A=(1/8)H diag(1184,80,40,0,0,0,0,0)Hᵀ.
- Since H/√8 is orthogonal, this is an exact SVD with singular values 1184, 80, 40, 0, …, 0.
- Pixel values are 148+10hᵢ₁hⱼ₁+5hᵢ₂hⱼ₂, so all 64 values lie between 133 and 163.
- Rank-1 Frobenius error is √(80²+40²)=√8000≈89.44; rank-2 error is 40; rank-3 error is 0.
- Low-rank storage is k(8+8+1)=17k values versus 64 raw entries: 26.6%, 53.1%, and 79.7% for k=1,2,3, excluding encoding overhead.
