
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import tvd
import matplotlib.pyplot as plt


def tvd_example():
    m = tvd.read_pgm("imgs/strongly_connected.pgm")
    # m = tvd.read_pgm("imgs/Grelha4.pgm")
    # m = tvd.read_pgm("imgs/Maze.pgm")
    td = tvd.TVD(m)
    labels = tvd.partition(td.get_graph(), 4)
    tvd.draw_paths_graph(td.get_graph(), draw_nodes=False)
    tvd.draw_clusters(td.get_graph(), labels)
    plt.axis("off")
    plt.imshow(m)


if __name__ == "__main__":
    tvd_example()
    plt.show()
