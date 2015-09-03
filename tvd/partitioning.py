
import sklearn.cluster as cluster
import networkx as nx
import numpy as np


def affinity_matrix(G):
    dists = nx.floyd_warshall_numpy(G, weight="distance")
    maxes = np.amax(dists, axis=0)
    return maxes - dists


def partition(G, n_parts):
    sc = cluster.SpectralClustering(
        n_clusters=n_parts, affinity="precomputed")
    af = affinity_matrix(G)
    labels = sc.fit_predict(af)
    return labels
