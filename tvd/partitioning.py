
import sklearn.cluster as cluster
import networkx as nx
import numpy as np
import geometry


def affinity_matrix(G):
    dists = nx.floyd_warshall_numpy(G, weight="distance")
    maxes = np.amax(dists, axis=0)
    return maxes - dists


def partition(G, n_parts):
    sc = cluster.SpectralClustering(
        n_clusters=n_parts, affinity="precomputed")
    af = affinity_matrix(G)
    labels = sc.fit_predict(af)
    ld = dict()
    node_clusters = [list() for _ in xrange(max(labels) + 1)]
    subgraphs = list()
    MG = nx.MultiDiGraph()
    for i, label in enumerate(labels):
        node_clusters[label].append(G.nodes()[i])
        ld[G.nodes()[i]] = label
    for nc in node_clusters:
        subgraphs.append(G.subgraph(nc))
    for p, q, data in G.edges_iter(data=True):
        if not ld[p] == ld[q]:
            p_sg = subgraphs[ld[p]]
            q_sg = subgraphs[ld[q]]
            for path in data["paths"]:
                dist = geometry.path_length(path)
                MG.add_edge(p_sg, q_sg, path=path, distance=dist)
    return MG
