
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import tvd
import matplotlib.pyplot as plt


def topo_vor_sanity_test():
    # m = tvd.read_pgm("imgs/gates.pgm")
    m = tvd.read_pgm("imgs/strongly_connected.pgm")
    # m = tvd.read_pgm("imgs/bars.pgm")
    # G = tvd.topo_decomp_with_redundancy(m, 1)
    G = tvd.topo_decomp(m)
    # tvd.draw_path_graph(G)
    tvd.draw_paths_graph(G)
    # tvd.draw_topo_graph(G)
    plt.axis("off")
    plt.imshow(m)


if __name__ == "__main__":
    topo_vor_sanity_test()
    plt.show()
