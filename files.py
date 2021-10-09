"""
This module create all the files that required in the project and calculate the Jaccard measure
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#this method creates the data.txt file, which will contain the generated data from Random Data Points Generation
def file_data(observations, ideal_cluster, n):
    file_data = open("data.txt", "w")
    for j in range(n-1):
        array_for_txt = np.array(observations[j])
        np.savetxt(file_data, array_for_txt, fmt="%0.8f", newline=",")
        file_data.write(str(ideal_cluster[j]))
        file_data.write("\n")
    array_for_txt = np.array(observations[n-1])
    np.savetxt(file_data, array_for_txt, fmt="%0.8f", newline=",")
    file_data.write(str(ideal_cluster[n-1]))
    file_data.close()

#this method creates the clusters.txt file, will contain the computed clusters from both algorithms
def file_clusters(results_normalized_spectral ,results_k_means , k ):
    file_clusters = open("clusters.txt", "w")
    file_clusters.write(str(k))
    file_clusters.write('\n')

    for i in range(k):
        array_for_txt = np.array(np.where(results_normalized_spectral == i))
        if array_for_txt.size != 0:
            np.savetxt(file_clusters, array_for_txt, delimiter=',', fmt="%i")

    for i in range(k-1):
        array_for_txt = np.array(np.where(results_k_means == i))
        if array_for_txt.size != 0:
            np.savetxt(file_clusters, array_for_txt, delimiter=',', fmt="%i")

    array_for_txt = np.where(results_k_means == k-1)
    len_array = len(array_for_txt[0])
    for j in array_for_txt[0]:
        file_clusters.write("%i" % j)
        len_array -= 1
        if len_array != 0:
            file_clusters.write(",")
    file_clusters.close()


# this method calculates the jaccard measure for each clustering algorithm
def jaccard_measure(ideal_cluster, results, n):
    sum_for_denominator = 0
    sum_for_nominator = 0
    for i in range(n):
        for j in range(i + 1, n):
            if results[i] == results[j] and ideal_cluster[i] == ideal_cluster[j]:
                sum_for_nominator += 1
            if results[i] == results[j] or ideal_cluster[i] == ideal_cluster[j]:
                sum_for_denominator += 1
    if sum_for_denominator==0: # we choose to handle the case of the denominator is zero to return that the accard measure = 1
        jacard_dist =1
    else:
        jacard_dist = sum_for_nominator / sum_for_denominator
    return jacard_dist

# this method creates the clusters.pdf file,
# which contains the visualization and information on the clusters that have been calculated.
def visualization_clusters(observations ,jacard_k_mean ,jacard_normalized_spectral, d,n ,k , K, results_normalized_spectral, results_k_means ):

    f = plt.figure()
    spectra_data_frame = pd.DataFrame(observations)
    spectra_data_frame.insert(d, "cluster", results_normalized_spectral)
    kmeans_data_frame = pd.DataFrame(observations)
    kmeans_data_frame.insert(d, "cluster", results_k_means)

    x = spectra_data_frame.iloc[:, 0]
    y = spectra_data_frame.iloc[:, 1]
    i = kmeans_data_frame.iloc[:, 0]
    j = kmeans_data_frame.iloc[:, 1]

    if d == 3:
        z = spectra_data_frame.iloc[:, 2]
        h = kmeans_data_frame.iloc[:, 2]

    if d == 3:
        ax = f.add_subplot(121, projection='3d')
        plt.title("Normalized Spectral Clustering")
        ax.scatter(x, y, z, c=spectra_data_frame['cluster'], cmap='tab20b')
        ay = f.add_subplot(122, projection='3d')
        plt.title("kmeans")
        ay.scatter(i, j, h, c=kmeans_data_frame['cluster'], cmap='tab20b')
    else:
        ax = f.add_subplot(121)
        ax.scatter(x, y, c=spectra_data_frame['cluster'], cmap='tab20b')
        plt.title("Normalized Spectral Clustering")
        ay = f.add_subplot(122)
        plt.title("kmeans")
        ay.scatter(i, j, c=kmeans_data_frame['cluster'], cmap='tab20b')

    info = "Data was generated from the values:" + "\n" + "n=" + str(n) + ", k=" + str(
        K) + "\n" + "The k that was used for both algorithms was " + str(
        k) + "\n" + "The Jaccard measure for Spectral Clustering: " + "{:.2f}".format(
        jacard_normalized_spectral) + "\n" + "The Jaccard measure for K-means: " + "{:.2f}".format(jacard_k_mean)

    plt.figtext(0.5, 0.01, info, ha='center', fontsize=14, va='top', fontstyle='normal')
    plt.savefig("clusters.pdf", bbox_inches='tight', dpi=100)
    plt.tight_layout()
