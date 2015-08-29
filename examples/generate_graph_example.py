
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import tvd
import matplotlib.pyplot as plt


def tvd_example():
    m = tvd.read_pgm("imgs/strongly_connected.pgm")
    td = tvd.TVD(m)
    # initial = tvd.Point(30, 30)
    # goal = tvd.Point(500, 10)
    # sp = td.shortest_path(initial, goal)
    tvd.draw_paths_graph(td.get_graph())
    tvd.partition(td.get_graph(), 2)
    # tvd.draw_path(sp)
    plt.axis("off")
    plt.imshow(m)


if __name__ == "__main__":
    tvd_example()
    plt.show()
