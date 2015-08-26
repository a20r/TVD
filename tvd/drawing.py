
import matplotlib.pyplot as plt
import networkx as nx


def draw_topo_graph(G):
    positions = dict()
    for node_id in G.nodes():
        positions[node_id] = G.node[node_id]['position'].to_list_2d()
    nx.draw_networkx_edges(G, positions)
    nx.draw_networkx_nodes(G, positions, node_size=30)


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


def draw_path(path):
    xs = list()
    ys = list()
    for r in path:
        xs.append(r.x)
        ys.append(r.y)
    plt.plot(xs, ys, "y")


def draw_paths_graph(G):
    for p, q, data in G.edges_iter(data=True):
        plt.plot(p.x, p.y, "go")
        plt.plot(q.x, q.y, "go")
        xs = list()
        ys = list()
        path = data["paths"][0]
        for path in data["paths"]:
            for r in path:
                xs.append(r.x)
                ys.append(r.y)
        plt.plot(xs, ys, "k")
