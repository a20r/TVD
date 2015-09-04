
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import tvd
import matplotlib.pyplot as plt


def tvd_example():
    m = tvd.read_pgm("imgs/strongly_connected.pgm")
    G = tvd.topo_decomp(m)
    mg = tvd.partition(G, 4)
    tvd.draw_multigraph(mg)
    plt.axis("off")
    plt.imshow(m)


if __name__ == "__main__":
    tvd_example()
    plt.show()
