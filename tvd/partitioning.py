
import sklearn.cluster as cluster
import networkx as nx
import numpy as np
import geometry
import postman


def determine_labels(G, n_parts):
    sc = cluster.AgglomerativeClustering(
        n_clusters=n_parts, linkage="ward")
    dists = nx.floyd_warshall_numpy(G, weight="distance")
    labels = sc.fit_predict(dists)
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
    for i in xrange(len(path) - 1):
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
            half_dist = 0.5 * dist
            g.add_edge(left[0], left[-1], path=left, distance=half_dist)
            g.add_edge(left[-1], left[0], path=leftr, distance=half_dist)
            h.add_edge(right[0], right[-1], path=right, distance=half_dist)
            h.add_edge(right[-1], right[0], path=rightr, distance=half_dist)
            seen.add(edge_set)
    return mg


def weighted_topo_graph(G):
    H = nx.Graph()
    for i, j, data in G.edges_iter(data=True):
        H.add_edge(i, j, distance=data["distance"], weight=data["distance"])
    return H


def node_orderings(MG):
    ps = list()
    for g in MG.nodes():
        tg = weighted_topo_graph(g)
        _, pth = postman.single_chinese_postman_path(tg)
        ps.append(pth)
    return ps


def tours(MG):
    nos = node_orderings(MG)
    paths = list()
    for g, no in zip(MG.nodes(), nos):
        path = list()
        for i in xrange(len(no) - 1):
            path.extend(g[no[i]][no[i + 1]][0]["path"])
        paths.append(path)
    return paths
