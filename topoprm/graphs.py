
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


def is_line_inside(xs, ys, grid):
    xs = map(int, xs)
    ys = map(int, ys)
    p = point.Point(xs[0], ys[0])
    q = point.Point(xs[1], ys[1])
    p_in = grid[p.y, p.x] == 0
    q_in = grid[q.y, q.x] == 0
    return p_in or q_in


def boundary_points(grid):
    ps = list()
    for i in xrange(1, grid.shape[0] - 1):
        for j in xrange(1, grid.shape[1] - 1):
            if is_grid_boundary(i, j, grid):
                ps.append(np.array([j, i]))

    for i in xrange(0, grid.shape[0]):
        ps.append([0, i])
        ps.append([grid.shape[1] - 1, i])

    for j in xrange(0, grid.shape[1]):
        ps.append([j, 0])
        ps.append([j, grid.shape[0] - 1])
    return np.array(ps)


def topo_vor(grid):
    points = boundary_points(grid)
    vor = spatial.Voronoi(points)
    G = nx.Graph()
    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            xs = vor.vertices[simplex, 0]
            ys = vor.vertices[simplex, 1]
            if not is_line_inside(xs, ys, grid):
                p = point.Point(xs[0], ys[0])
                q = point.Point(xs[1], ys[1])
                G.add_node(p, position=p)
                G.add_node(q, position=q)
                G.add_edge(p, q)
    return G


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
