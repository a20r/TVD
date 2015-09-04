
import sklearn.cluster as cluster
import networkx as nx
import numpy as np
import geometry


def affinity_matrix(G):
    dists = nx.floyd_warshall_numpy(G, weight="distance")
    maxes = np.amax(dists, axis=0)
    return maxes - dists


def determine_labels(G, n_parts):
    sc = cluster.SpectralClustering(
        n_clusters=n_parts, affinity="precomputed")
    af = affinity_matrix(G)
    labels = sc.fit_predict(af)
    return labels


def develop_multigraph(G, n_parts):
    labels = determine_labels(G, n_parts)
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
            dist = geometry.path_length(data["path"])
            MG.add_edge(p_sg, q_sg, path=data["path"], distance=dist)
    return MG


def split_path(path, length, ratio=0.5):
    dist = 0
    for i in xrange(0, len(path) - 1):
        dist += path[i].dist_to(path[i + 1])
        diff = ratio * length - dist
        if diff <= 0:
            return path[:i], path[i - 1:]


def partition(G, n_parts):
    mg = develop_multigraph(G, n_parts)
    seen = set()
    for g, h, data in mg.edges_iter(data=True):
        path = data["path"]
        dist = data["distance"]
        edge_set = frozenset([path[0], path[-1]])
        if not edge_set in seen:
            left, right = split_path(path, dist)
            leftr, rightr = list(reversed(left)), list(reversed(right))
            g.add_edge(left[0], left[-1], path=left, distance=0.5 * dist)
            g.add_edge(left[-1], left[0], path=leftr, distance=0.5 * dist)
            h.add_edge(right[0], right[-1], path=right, distance=0.5 * dist)
            h.add_edge(right[-1], right[0], path=rightr, distance=0.5 * dist)
            seen.add(edge_set)
    return mg
