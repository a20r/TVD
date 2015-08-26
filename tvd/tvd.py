
import geometry
import networkx as nx
import point
import scipy.spatial as spatial


class TVD(object):

    def __init__(self, grid, b_dist=1, n_size=1, auto=True):
        self.grid = grid
        self.auto = auto
        if auto:
            self.generate_graph(b_dist=b_dist, n_size=n_size)
        else:
            self.G = None
            self.rg = None
            self.vor = None
            self.tree = None

    def generate_graph(self, b_dist=1, n_size=1):
        self.b_dist = b_dist
        self.n_size = n_size
        self.G, self.rG, self.vor = geometry.topo_decomp(
            self.grid, b_dist=b_dist, n_size=n_size)
        ps = point.to_np_array(self.vor.nodes())
        self.tree = spatial.KDTree(ps)
        return self

    def shortest_path(self, initial, goal):
        i_out = self.grid[initial.y, initial.x] == 0
        g_out = self.grid[goal.y, goal.x] == 0
        if i_out or g_out:
            return list()
        ds, inds = self.tree.query(initial.to_np_array_2d(), k=1)
        v_i = self.vor.nodes()[inds]
        ds, inds = self.tree.query(goal.to_np_array_2d(), k=1)
        v_g = self.vor.nodes()[inds]
        s_path = nx.shortest_path(self.vor, source=v_i, target=v_g)
        return geometry.redundant_path(initial, goal, s_path)

    def update_grid(self, i, j, val):
        self.grid[j][i] = val
        return self

    def set_grid(self, grid):
        self.grid = grid
        return self

    def get_graph(self):
        return self.G

    def get_redundant_graph(self):
        return self.rG

    def get_voronoi_graph(self):
        return self.vor
