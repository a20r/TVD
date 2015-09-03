
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
    mg = tvd.partition(td.get_graph(), 4)
    tvd.draw_multi_graph(mg)
    plt.axis("off")
    plt.imshow(m)


if __name__ == "__main__":
    tvd_example()
    plt.show()
