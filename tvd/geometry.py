
import point
import numpy as np
import networkx as nx
import scipy.spatial as spatial


def is_grid_boundary(i, j, grid):
    r = [-1, 0, 1]
    if grid[i][j] > 0:
        return False
    for di in r:
        for dj in r:
            if grid[i + di][j + dj] > 0:
                return True
    return False


def is_inside(p, grid):
    in_x = p.x > 0 and p.x < grid.shape[1]
    in_y = p.y > 0 and p.y < grid.shape[0]
    return in_x and in_y


def is_line_inside(xs, ys, grid, b_dist):
    xs = map(int, xs)
    ys = map(int, ys)
    p = point.Point(xs[0], ys[0])
    q = point.Point(xs[1], ys[1])
    if is_inside(p, grid) and is_inside(q, grid):
        p_in = grid[p.y, p.x]
        q_in = grid[q.y, q.x]
        tc_p = too_close(p, b_dist, grid)
        tc_q = too_close(q, b_dist, grid)
        return p_in or q_in or tc_p or tc_q
    else:
        return False


def too_close_xs(p, rad, grid, r):
    for dj in r:
        if grid[p.y + rad, p.x + dj]:
            return True
    for dj in r:
        if grid[p.y - rad, p.x + dj]:
            return True
    return False


def too_close_ys(p, rad, grid, r):
    for di in r:
        if grid[p.y + di, p.x + rad]:
            return True
    for di in r:
        if grid[p.y + di, p.x - rad]:
            return True
    return False


def too_close(p, rad, grid):
    r = xrange(-rad, rad + 1)
    try:
        tcx = too_close_xs(p, rad, grid, r)
        tcy = too_close_ys(p, rad, grid, r)
        return tcx or tcy
    except IndexError:
        return True


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
    return G


def remove_close_nodes(G, grid, b_dist):
    H = G.copy()
    for n in G.nodes():
        if n in H.nodes():
            is_leaf = len(G.neighbors(n)) == 1
            if is_leaf and too_close(n, b_dist + 1, grid):
                H.remove_node(n)
    return H


def path_length(path):
    length = 0.0
    for i in xrange(len(path) - 1):
        length += path[i].dist_to(path[i + 1])
    return length


def topo_decomp_with_redundancy(grid, b_dist):
    rg = redundant_graph(grid, b_dist)
    cns = critical_nodes(rg)
    cns_set = set(cns)
    G = nx.DiGraph()
    for cn in cns:
        for nbr in rg.neighbors(cn):
            path = [cn]
            already_seen = set()
            already_seen.add(cn)
            to_search = [nbr]
            while len(to_search) > 0:
                node = to_search.pop()
                already_seen.add(node)
                path.append(node)
                if node in cns_set:
                    path = redundant_path(cn, node, path)
                    G.add_node(cn, position=cn)
                    G.add_edge(cn, node, path=path)
                    break
                else:
                    for inner_nbr in rg.neighbors(node):
                        if not inner_nbr in already_seen:
                            to_search.append(inner_nbr)
    H = remove_close_nodes(G, grid, b_dist)
    return H, rg


def topo_decomp(grid, b_dist=1, n_size=1):
    rg, vor = topo_decomp_with_redundancy(grid, b_dist)
    cns = critical_nodes(rg)
    cns_set = set(cns)
    G = nx.DiGraph()
    for cn in cns:
        for nbr in rg.neighbors(cn):
            path = list()
            already_seen = set()
            already_seen.add(cn)
            to_search = [(cn, nbr)]
            while len(to_search) > 0:
                parent, node = to_search.pop()
                already_seen.add(node)
                path += rg[parent][node]["path"]
                if node in cns_set:
                    G.add_node(cn, position=cn)
                    if not G.has_edge(cn, node):
                        G.add_edge(cn, node, paths=list())
                    G[cn][node]["paths"].append(path)
                    G[cn][node]["distance"] = path_length(path)
                    break
                else:
                    for inner_nbr in rg.neighbors(node):
                        if not inner_nbr in already_seen:
                            to_search.append((node, inner_nbr))
    return neighbourhood_reduction(G, n_size), rg, vor


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
