
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import matplotlib.cm as cm


def draw_node(p, color):
    plt.plot(p.x, p.y, color)


def draw_topo_graph(G):
    positions = dict()
    for node_id in G.nodes():
        positions[node_id] = G.node[node_id]['position'].to_list_2d()
    nx.draw_networkx_edges(G, positions)
    nx.draw_networkx_nodes(G, positions, node_size=30)


def draw_clusters(G, labels, **kwargs):
    colors = cm.jet(np.linspace(0, 1, max(labels) + 1))
    xs = list()
    ys = list()
    cs = list()
    for i, l in enumerate(labels):
        xs.append(G.nodes()[i].x)
        ys.append(G.nodes()[i].y)
        cs.append(colors[l])
    plt.scatter(xs, ys, color=cs, s=50,
                edgecolors="k", **kwargs)


def draw_path_graph(G):
    for p, q, data in G.edges_iter(data=True):
        plt.plot(p.x, p.y, "go")
        plt.plot(q.x, q.y, "go")
        xs = list()
        ys = list()
        for r in data["path"]:
            xs.append(r.x)
            ys.append(r.y)
        plt.plot(xs, ys, "k")


def draw_path(path, **kwargs):
    xs = list()
    ys = list()
    for r in path:
        xs.append(r.x)
        ys.append(r.y)
    plt.plot(xs, ys, **kwargs)


def draw_paths_graph(G, draw_nodes=True):
    for i, (p, q, data) in enumerate(G.edges_iter(data=True)):
        if draw_nodes:
            plt.plot(p.x, p.y, "go")
            plt.plot(q.x, q.y, "go")
        xs = list()
        ys = list()
        for path in data["paths"]:
            for r in path:
                xs.append(r.x)
                ys.append(r.y)
        plt.plot(xs, ys, color="k")


def draw_multi_graph(G):
    colors = cm.jet(np.linspace(0, 1, len(G.nodes()) + 1))
    for i, sg in enumerate(G.nodes()):
        draw_paths_graph(sg, draw_nodes=False)
        xs = list()
        ys = list()
        for node in sg.nodes():
            xs.append(node.x)
            ys.append(node.y)
        plt.scatter(xs, ys, color=colors[i])
    for _, _, data in G.edges_iter(data=True):
        draw_path(data["path"], color="k")
