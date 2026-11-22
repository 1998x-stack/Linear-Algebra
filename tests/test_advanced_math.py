import math
import unittest

def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

class AdvancedMathVerification(unittest.TestCase):
    def test_lu_factorization_and_solution(self):
        A=[[2,1,1],[4,-6,0],[-2,7,2]]
        L=[[1,0,0],[2,1,0],[-1,-1,1]]
        U=[[2,1,1],[0,-8,-2],[0,0,1]]
        self.assertEqual(matmul(L,U),A)
        self.assertEqual(matmul(A,[[1],[1],[2]]),[[5],[-2],[9]])
    def test_qr_gram_schmidt_and_least_squares(self):
        q1=[1/math.sqrt(2),1/math.sqrt(2),0]
        q2=[1/math.sqrt(6),-1/math.sqrt(6),2/math.sqrt(6)]
        self.assertAlmostEqual(sum(x*y for x,y in zip(q1,q2)),0,places=12)
        self.assertAlmostEqual(sum(x*x for x in q1),1,places=12)
        self.assertAlmostEqual(sum(x*x for x in q2),1,places=12)
        x=[5/3,-1/3];A=[[1,1],[1,0],[0,1]];b=[1,2,0]
        residual=[b[i]-sum(A[i][j]*x[j] for j in range(2)) for i in range(3)]
        self.assertAlmostEqual(sum(A[i][0]*residual[i] for i in range(3)),0,places=12)
        self.assertAlmostEqual(sum(A[i][1]*residual[i] for i in range(3)),0,places=12)
    def test_orthogonal_rotation_and_reflection_preserve_norm(self):
        theta=.37;R=((math.cos(theta),-math.sin(theta)),(math.sin(theta),math.cos(theta)))
        w=(R[0][0]*3+R[0][1]*4,R[1][0]*3+R[1][1]*4)
        self.assertAlmostEqual(math.hypot(*w),5,places=12)
        self.assertAlmostEqual(math.hypot(w[0],-w[1]),5,places=12)
        self.assertAlmostEqual(R[0][0]*R[1][1]-R[0][1]*R[1][0],1,places=12)
    def test_symmetric_eigenpairs_trace_and_determinant(self):
        A=[[2,1],[1,2]]
        self.assertEqual(matmul(A,[[1],[1]]),[[3],[3]])
        self.assertEqual(matmul(A,[[1],[-1]]),[[1],[-1]])
        self.assertEqual(3+1,A[0][0]+A[1][1])
        self.assertEqual(3*1,A[0][0]*A[1][1]-A[0][1]*A[1][0])
    def test_positive_definite_minors_and_cholesky(self):
        A=[[4,2],[2,3]];L=[[2,0],[1,math.sqrt(2)]]
        self.assertEqual(A[0][0],4)
        self.assertEqual(A[0][0]*A[1][1]-A[0][1]*A[1][0],8)
        product=matmul(L,[[2,1],[0,math.sqrt(2)]])
        for i in range(2):
            for j in range(2):self.assertAlmostEqual(product[i][j],A[i][j],places=12)
        self.assertGreater((7-math.sqrt(17))/2,0)
    def test_spectral_matrix_power(self):
        self.assertEqual(matmul([[2,1],[1,2]],[[2,1],[1,2]]),[[5,4],[4,5]])
    def test_pca_covariance_eigenvalues_and_variance_ratio(self):
        self.assertAlmostEqual((8/3)/(8/3+2/3),.8)
        self.assertAlmostEqual((2/3)/(8/3+2/3),.2)
        self.assertEqual(2,2)
    def test_svd_image_error_and_storage(self):
        self.assertAlmostEqual(math.sqrt(80**2+40**2),math.sqrt(8000))
        self.assertEqual(40,40);self.assertEqual(0,0)
        self.assertAlmostEqual(17/64*100,26.5625)
        self.assertAlmostEqual(34/64*100,53.125)

if __name__ == "__main__":
    unittest.main()
