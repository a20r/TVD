
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import matplotlib.cm as cm
import matplotlib.animation as animation


def draw_node(p, color):
    plt.plot(p.x, p.y, color)


def draw_topo_graph(G):
    positions = dict()
    for node in G.nodes():
        positions[node] = node.to_list_2d()
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


def draw_path(path, **kwargs):
    xs = list()
    ys = list()
    for r in path:
        xs.append(r.x)
        ys.append(r.y)
    plt.plot(xs, ys, **kwargs)


def draw_path_graph(G, draw_nodes=True):
    for i, (p, q, data) in enumerate(G.edges_iter(data=True)):
        if draw_nodes:
            plt.plot(p.x, p.y, "go")
            plt.plot(q.x, q.y, "go")
        xs = list()
        ys = list()
        for r in data["path"]:
            xs.append(r.x)
            ys.append(r.y)
        plt.plot(xs, ys, color="k")


def draw_multigraph(G):
    colors = cm.jet(np.linspace(0, 1, len(G.nodes()) + 1))
    for i, sg in enumerate(G.nodes()):
        xs = list()
        ys = list()
        for _, _, data in sg.edges_iter(data=True):
            draw_path(data["path"], color=colors[i])
        for node in sg.nodes():
            xs.append(node.x)
            ys.append(node.y)
        plt.scatter(xs, ys, color=colors[i])


def play_simulation(mg, ecs, delay=0.1):
    # draw_multigraph(mg)
    vel = 10
    def data_gen():
        for i, ec in enumerate(ecs):
            for u, v in ec:
                for path in mg.nodes()[i].get_edge_data(u, v).values():
                    for p in path["path"]:
                        yield p
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_ylim(0, 500)
    ax.set_xlim(0, 500)
    ax.grid()
    xdata, ydata = [], []
    def run(data):
        # update the data
        p = data
        print p
        xdata.append(p.x)
        ydata.append(p.y)
        xmin, xmax = ax.get_xlim()

        # if t >= xmax:
        #     ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
        line.set_data(xdata, ydata)
        return line,

    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=10,
        repeat=False)
    plt.show()
    return ani
