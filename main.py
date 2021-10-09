"""
This module is the main of the project - its job is to connect all the parts of the project and run all the other files
"""
import argparse
import random
import numpy as np
import spectral_algorithm as project
import kmeans_pp as kmeans
import files as files
from sklearn.datasets import make_blobs

if __name__ == "__main__":
    #reads from the commend line
    parser = argparse.ArgumentParser(description='the argument from cl')
    parser.add_argument("K", type=int, help="K – the number of clusters")
    parser.add_argument("N", type=int, help="N – the number of observations ")
    parser.add_argument('--no-Random', dest='Random' , default=True, action='store_false')

    args = parser.parse_args()
    K = args.K
    N = args.N
    Random = args.Random

    if not Random:
        n = N
        k = K
        #  we choose to raise an error when number of cluster is equal to number of observation (k=n)
        if K <= 0 or N <= 0 or K >= N:
            print("Error, one of the parameters transmitted through command line is invalid")
            exit(1)

    n_max_capacity_3d, k_max_capacity_3d = 400 ,20
    n_max_capacity_2d, k_max_capacity_2d = 420 , 20

    #Random choice of observations and dimensions
    d=random.randint(2,3)
    # If Random == True k, n will choose randomly from the max capacity
    if Random:
        if d == 3:
            n = random.randint(int(n_max_capacity_3d/2) , n_max_capacity_3d)
            k = random.randint(int(k_max_capacity_3d/2) , k_max_capacity_3d)
        else: #d == 2
            n = random.randint((n_max_capacity_2d / 2), n_max_capacity_2d)
            k = random.randint((k_max_capacity_2d / 2), k_max_capacity_2d)
    K = k
    points = make_blobs(n_samples = n ,centers= k ,n_features=d)
    observations = np.array(points[0])
    #The clusters of the observations as set in make_blobs
    ideal_cluster = points[1]

    #Creating file of the selected observations and the original clusters
    files.file_data(observations, ideal_cluster, n)

    #Calculation of matrix T and int k with "normalized spectral" algorithm
    T, k = project.normalized_spectral_clustering(observations, len(observations), Random, k)

    results_normalized_spectral = np.array(kmeans.k_means(T, k, n, T.shape[1]))#T.shape[1]==d
    results_k_means = np.array(kmeans.k_means(observations, k, n, observations.shape[1]))#observations.shape[1]==d

    #Creating file of the dividing the observations into clusters
    files.file_clusters(results_normalized_spectral, results_k_means, k)

    #Calculation of the Jaccard measure of the "normalized spectral" algorithm
    jacard_normalized_spectral = files.jaccard_measure(ideal_cluster ,results_normalized_spectral , n)

    #Calculation of the Jaccard measure of the "kmeans" algorithm
    jacard_k_mean = files.jaccard_measure(ideal_cluster ,results_k_means , n)

    #Creating clusters.pdf that showing the division of the clusters in a graph
    files.visualization_clusters(observations, jacard_k_mean, jacard_normalized_spectral, d, n, k,K,
                           results_normalized_spectral, results_k_means)








