
import sklearn.cluster as cluster
import networkx as nx
import numpy as np


def get_affinity_function(G):
    dists = nx.floyd_warshall(G, weight="distance")
    max_dist = max(dists.values())

    def affinity(i, j):
        p = G.nodes()[i]
        q = G.nodes()[j]
        return max_dist - dists[p][q]

    return affinity


def partition(G, n_parts):
    af = get_affinity_function(G)
    sc = cluster.SpectralClustering(
        n_clusters=n_parts, affinity=af)
    print sc.fit(range(len(G.nodes())))
