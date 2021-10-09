"""
This module runs the Normalized Spectral Clustering Algorithm, as described.
"""
import math
import numpy as np

def cal_norm(x_i, x_j):
    """
        input: two rows vectors- x_i and x_j, shape 1xn
        output: the calculated Euclidean norm
    """
    dist = x_i - x_j
    return np.linalg.norm(dist)

def set_weighted_matrix(observations , n):
    """
    input: Observations(=the rows of the matrix A), int n
    output: the matrix W - shape nXn, holds the weights of all pairs
    """
    W = np.zeros([n,n] , dtype=np.float32)
    for i in range(n) :
        for j in range(i+1,n):
            W[i][j] = cal_norm(observations[i], observations[j])/(-2)
            W[j][i] = W[i][j]
    # in the description we defined the diagonal of W as zeros - wii == 0
    # and because we are using np.exp for all the matrix we need to subtract the identity matrix to get what is required
    W = np.exp(W) - np.identity(n)
    return W

def set_diagonal_degree_matrix(W_matrix, n):
    """
        input: W_matrix - shape nXn, and int n
        output: the matrix E = D^-0.5, as described in the algorithm
       """
    E =np.zeros([n,n] , dtype=np.float32)
    res = np.sqrt(W_matrix.sum(axis=1))
    if res.any()==0: # in case of division by zero, we choose to raise an error
        print("Error, division by zero in calculation of the diagonal matrix ^ (-0.5)")
        exit(1)
    rows_sum = 1/res
    np.fill_diagonal(E , rows_sum)
    return E

def multiply_matrix(E, W):
    """
        input: the matrices E and W - shape nxn
        output: the matrix ExWxE, which is the multiplication of the matrices
    """
    return E@W@E


def gram_schmidt_algorithm(L ,n):
    """
          input: the matrix L - nXn shape
          output: the matrices Q(an orthogonal matrix) and R(an upper triangular matrix)
      """
    R = np.zeros([n, n], dtype=np.float32)
    Q = np.zeros([n, n], dtype=np.float32)
    U = np.copy(L)
    for i in range(n):
        R[i,i] = np.linalg.norm(U[:,i])
        if (R[i,i])!=0:
            Q[:,i] = U[:,i] / (R[i,i])
        # we initialise R to matrix of zeros , we choose to take care  of the case when Rii = 0 by leaving the component equle to zero
        R[i][i+1:n]=np.transpose(Q[:,i])@U[:,i+1:n]
        temp=(R[i][:,np.newaxis]*Q[:,i])
        U[:,i+1:n]=U[:,i+1:n]-temp.transpose()[:,i+1:n]

    return (Q,R)


def qr_iteration_algorithm(L,n):

    """
         input: the matrix L - nXn shape
         output: the matrices A_eigenvalue(whose diagonal elements approach the eigenvalues of A) and Q_eigenvector(whose columns approach
         the eigenvectors of A
     """
    epsilon = 0.0001
    A_eigenvalue = np.copy(L)
    Q_eigenvector = np.identity(n)
    for i in range(n):
        Q , R = gram_schmidt_algorithm(A_eigenvalue,n)
        A_eigenvalue = R@Q
        G = np.abs(Q_eigenvector) - np.abs(Q_eigenvector@Q)
        if np.all(np.abs(G)<=epsilon):
            return(A_eigenvalue , Q_eigenvector)

        Q_eigenvector = Q_eigenvector@Q


    return (A_eigenvalue, Q_eigenvector)


def set_eigengap_heuristic(A_eigenvalue, Q_eigenvector , n , boolean, k):
    """
        input: the matrix A_eigenvalue, the matrix Q_eigenvector, int n, boolean bool, int k
        output: the matrix U - shape nXk, which holds the first k eigenvectors of the matrix Q,
        and int k-the number of clusters that will be used if Random==True, calculated according to the algorithm
    """
    eigenvalue= np.diagonal(A_eigenvalue)
    sorted_indexes = np.argsort(eigenvalue)
    eigenvalue = np.sort(eigenvalue)
    Q_eigenvector_t = Q_eigenvector.transpose()
    U = Q_eigenvector_t[sorted_indexes]
    U = U.transpose()
    if boolean:
        dist = np.abs(np.diff(eigenvalue))
        dist = dist[:math.ceil(n / 2)]
        k = np.argmax(dist) + 1
    else:
        k=k
    U = U[:, :k]
    return (k , U)


def set_renormalizing(U):
    """
        input: the matrix U - nXk shape
        output: the matrix T - nXk shape, as described in The Normalized Spectral Clustering Algorithm
    """
    row = U.shape[0]
    res = (np.linalg.norm(U, axis=-1).transpose()).reshape(row, 1)
    if res.any() == 0: # in case of division by zero, we choose to raise an error
        print("error, division by zero in the calculation of T matrix")
        exit(1)
    T = U / res

    return T


def normalized_spectral_clustering(Observations, n,  boolean, k):
    """
        input: Observations(=the rows of the matrix A), int n,  boolean bool, int k
        output: T- a list of K inner lists, each inner list will contain the indices of the observations that assigned to the cluster,
        and int k- the number of clusters that will be used if Random==True, calculated according to the algorithm
    """
    W = set_weighted_matrix(Observations, n)
    E = set_diagonal_degree_matrix(W ,n)
    L = multiply_matrix(E,W) # calculates E@W@E
    # we choose to add the identity matrix to L norm matrix as recommend on the course forum
    L_norm = np.identity(n) - L + np.identity(n)
    A_eigenvalue,Q_eigenvector= qr_iteration_algorithm(L_norm,n)
    k , U=set_eigengap_heuristic(A_eigenvalue, Q_eigenvector ,n, boolean, k)
    T = set_renormalizing(U)
    return (T,k)










