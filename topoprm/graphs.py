
import re
import point
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import scipy.spatial as spatial


def get(grid, i, j):
    h = grid.info.height
    return grid.data[h * i + j]


def read_pgm(filename, byteorder='>'):
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    return np.frombuffer(
        buffer, dtype='u1' if int(maxval) < 256 else byteorder + 'u2',
        count=int(width) * int(height), offset=len(header))\
        .reshape((int(height), int(width)))


def nn_prm(N, k, grid):
    h, w = grid.shape
    xs = np.random.uniform(low=0, high=w - 1, size=N)
    ys = np.random.uniform(low=0, high=h - 1, size=N)
    data = zip(xs, ys)
    return nn_prm_given_points(N, k, grid, data)


def nn_prm_given_points(N, k, grid, data):
    G = nx.Graph()
    tree = spatial.KDTree(data)
    for i, vec in enumerate(data):
        x = vec[0]
        y = vec[1]
        if grid[y, x] > 0:
            G.add_node(i, position=point.Point(x, y))
            ds, inds = tree.query(vec, k=k)
            for d, j in zip(ds, inds):
                if grid[int(data[j][1]), int(data[j][0])] > 0:
                    p2 = point.Point(data[j][0], data[j][1])
                    if not crow_collision(grid, G.node[i]["position"], p2):
                        G.add_edge(i, j, distance=d)
    return G


def topo_prm(N, k, grid):
    G = nn_prm(N, k, grid)
    H = nx.Graph()
    S0 = [G.nodes()[0]]
    already_seen_0 = set()
    counter = 0
    while len(S0) > 0:
        i = S0.pop()
        print i
        already_seen_0.add(i)
        S1 = [G.neighbors(i)[0]]
        already_seen_1 = set()
        while len(S1) > 0:
            j = S1.pop()
            imd = G.node[j]["position"]
            for k in G.neighbors(j):
                cur = G.node[i]["position"]
                nxt = G.node[k]["position"]
                if crow_collision(grid, cur, nxt):
                    if not j in already_seen_0:
                        H.add_node(i, position=cur)
                        H.add_node(j, position=imd)
                        H.add_edge(i, j)
                        S0.append(j)
                        already_seen_0.add(j)
                else:
                    if not k in already_seen_1:
                        S1.append(k)
                        already_seen_1.add(k)
    return H


def crow_path(p, q):
    path = list()
    uv = (q - p).to_unit_vector()
    inter = p.copy()
    while q.dist_to(inter) > 1:
        inter = inter + uv
        path.append(inter.intify())
    return path


def crow_collision(grid, p, q):
    path = crow_path(p, q)
    for i in path:
        if grid[i.get_y(), i.get_x()] == 0:
            return True
    return False


def draw(G):
    positions = dict()
    for node_id in G.nodes():
        positions[node_id] = G.node[node_id]['position'].to_list_2d()
    nx.draw_networkx_edges(G, positions)
    nx.draw_networkx_nodes(G, positions, node_size=30)


if __name__ == "__main__":
    m = read_pgm("imgs/bars.pgm")
    G = topo_prm(100, 10, m)
    # G = nn_prm(100, 10, m)
    draw(G)
    plt.imshow(m)
    plt.show()
