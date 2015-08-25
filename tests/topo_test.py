
import os
import sys

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
    m = topoprm.read_pgm("imgs/bars.pgm")
    G = topoprm.topo_vor(m)
    topoprm.draw(G)
    plt.imshow(m)


if __name__ == "__main__":
    topo_vor_sanity_test()
    plt.show()
