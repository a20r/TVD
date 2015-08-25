
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import topoprm
import matplotlib.pyplot as plt


def topo_prm_sanity_test():
    m = topoprm.read_pgm("imgs/bars.pgm")
    H, G = topoprm.topo_prm(100, 5, m)
    plt.subplot(2, 1, 1)
    topoprm.draw(H)
    plt.imshow(m)
    plt.subplot(2, 1, 2)
    topoprm.draw(G)
    plt.imshow(m)


def topo_vor_sanity_test():
    # m = topoprm.read_pgm("imgs/strongly_connected.pgm")
    m = topoprm.read_pgm("imgs/bars.pgm")
    G = topoprm.topo_decomp(m)
    topoprm.draw_path_graph(G)
    # topoprm.draw_topo_graph(G)
    plt.imshow(m)


if __name__ == "__main__":
    topo_vor_sanity_test()
    plt.show()
