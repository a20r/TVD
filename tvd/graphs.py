
import re
import point
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import scipy.spatial as spatial


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


def is_grid_boundary(i, j, grid):
    r = [-1, 0, 1]
    if grid[i][j] > 0:
        return False
    for di in r:
        for dj in r:
            if grid[i + di][j + dj] > 0:
                return True
    return False


def is_line_inside(xs, ys, grid, b_dist):
    xs = map(int, xs)
    ys = map(int, ys)
    p = point.Point(xs[0], ys[0])
    q = point.Point(xs[1], ys[1])
    p_in = grid[p.y, p.x]
    q_in = grid[q.y, q.x]
    tc_p = too_close(p, b_dist, grid)
    tc_q = too_close(q, b_dist, grid)
    return p_in or q_in or tc_p or tc_q


def too_close(p, rad, grid):
    r = xrange(-rad, rad + 1)
    try:
        for dj in r:
            if grid[p.y + rad, p.x + dj]:
                return True
        for dj in r:
            if grid[p.y - rad, p.x + dj]:
                return True
        for di in r:
            if grid[p.y + di, p.x + rad]:
                return True
        for di in r:
            if grid[p.y + di, p.x - rad]:
                return True
    except IndexError:
        return True
    return False


def crow_path(p, q):
    path = list()
    uv = (q - p).to_unit_vector()
    inter = p.copy()
    while q.dist_to(inter) > 1:
        inter = inter + uv
        if not inter.intify() in path:
            path.append(inter.intify())
    return path


def crow_collision(grid, p, q):
    path = crow_path(p, q)
    for i in path:
        if grid[i.get_y(), i.get_x()]:
            return True
    return False


def fill_border(grid):
    c_grid = np.copy(grid)
    for i in xrange(0, grid.shape[1]):
        c_grid[0, i] = True
        c_grid[grid.shape[0] - 1, i] = True

    for j in xrange(0, grid.shape[0]):
        c_grid[j, 0] = True
        c_grid[j, grid.shape[1] - 1] = True
    return c_grid


def boundary_points(grid):
    ps = list()
    for i in xrange(1, grid.shape[0] - 1):
        for j in xrange(1, grid.shape[1] - 1):
            if is_grid_boundary(i, j, grid):
                ps.append(np.array([j, i]))
    return np.array(ps)


def critical_nodes(G):
    cn = list()
    for n in G.nodes():
        nn = len(G.neighbors(n))
        if nn == 1 or nn > 2:
            cn.append(n)
    return cn


def redundant_path(p, q, path):
    if len(path) == 0:
        return crow_path(p, q)
    else:
        start = path[0]
        end = path[-1]
        if p.dist_to(start) < p.dist_to(end):
            return crow_path(p, start) + path + crow_path(end, q)
        else:
            return crow_path(p, end) + path + crow_path(start, q)


def neighbourhood_reduction(G, k):
    # TODO
    return G


def topo_decomp(grid, b_dist=4, n_size=1):
    rg = redundant_graph(grid, b_dist)
    cns = critical_nodes(rg)
    cns_set = set(cns)
    G = nx.Graph()
    for cn in cns:
        for nbr in rg.neighbors(cn):
            path = list()
            already_seen = set()
            already_seen.add(cn)
            to_search = [nbr]
            while len(to_search) > 0:
                node = to_search.pop()
                already_seen.add(node)
                if node in cns_set:
                    path = redundant_path(cn, node, path)
                    G.add_node(cn, position=cn)
                    G.add_node(node, position=node)
                    G.add_edge(cn, node, path=path)
                    G.add_edge(node, cn, path=list(reversed(path)))
                    path = list()
                else:
                    path.append(node)
                    for inner_nbr in rg.neighbors(node):
                        if not inner_nbr in already_seen:
                            to_search.append(inner_nbr)
    return neighbourhood_reduction(G, n_size)


def redundant_graph(grid, b_dist):
    grid = fill_border(grid == 0)
    points = boundary_points(grid)
    vor = spatial.Voronoi(points)
    G = nx.Graph()
    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            xs = vor.vertices[simplex, 0]
            ys = vor.vertices[simplex, 1]
            if not is_line_inside(xs, ys, grid, b_dist):
                p = point.Point(xs[0], ys[0])
                q = point.Point(xs[1], ys[1])
                G.add_node(p, position=p)
                G.add_node(q, position=q)
                G.add_edge(p, q)
    return G


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
