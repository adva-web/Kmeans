"""
This module handle the first step in 'kmeans' algorithm and generates the first k centroids as describes in homework 2
"""

import numpy as np
import mykmeanssp  as km


#clalculate the probeblity of each xi to be the candidate centroid
def calculate_prob(listofdist, N):
    temp_list = np.zeros(N)
    summ = np.sum(listofdist)
    if summ==0: # in case of division by zero, we choose to raise an error
        print("Error, division by zero when calculate probability in kmeans algorithm")
        exit(1)
    for i in range(N):
        temp_list[i] = listofdist[i] / summ
    return temp_list


def k_means(observations ,k,n , x):
    """
          input: Observations ,k , n = number of Observations , x = d  the dimension of the Observations
          output:   output is a list of clusters , that each cluster puts in the belong index of observations
      """

    N=n
    K = k
    d = x
    MAX_ITER = 300
    centroids = np.zeros((K, d), np.float32)

    # starting step 1
    np.random.seed(0)
    temp_lst = np.arange(N)
    i=np.random.choice(temp_lst, 1)
    index = i[0]
    centroids[0]=observations[index]
    list_of_dists = np.full(N, np.inf, dtype=np.float32)
    j=1
    while j <= K-1:
        list_of_dists = np.minimum(list_of_dists, np.sum(np.power(centroids[j - 1] - observations, 2), axis=1))
        listofprob  = calculate_prob(list_of_dists, N)
        temp_lst =  np.arange(N)
        c=np.random.choice(temp_lst, 1, p=listofprob)
        counter = c[0]
        centroids[j] = observations[counter]
        j += 1

    centroids_list = centroids.tolist()
    observations_list = observations.tolist()
    output = km.get_main(K, N, d, MAX_ITER, observations_list, centroids_list)

    return output




