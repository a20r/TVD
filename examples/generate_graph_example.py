
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import tvd
import matplotlib.pyplot as plt
import networkx as nx


def tvd_example():
    m = tvd.read_pgm("imgs/strongly_connected.pgm")
    G, rg, vor = tvd.topo_decomp(m, all_graphs=True)
    mg = tvd.partition(G, 4)
    tvd.draw_multigraph(mg, plt)
    # ecs = tvd.tours(mg)
    # tvd.play_simulation(mg, ecs, m)
    plt.tight_layout()
    plt.imshow(m == 0, cmap="Greys")
    plt.axis("off")


def all_plots(img_name, name):
    m = tvd.read_pgm(img_name)
    G, rg, wl, vor = tvd.topo_decomp(m, all_graphs=True)
    tvd.draw_topo_graph(vor)
    plt.imshow(m < 100, cmap="Greys")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("../ICRA16-TVD/figs/" + name + "_vor.pdf")
    plt.show()

    tvd.draw_path_graph(wl)
    plt.imshow(m < 100, cmap="Greys")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("../ICRA16-TVD/figs/" + name + "_leaves.pdf")
    plt.show()

    tvd.draw_path_graph(rg)
    plt.imshow(m < 100, cmap="Greys")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("../ICRA16-TVD/figs/" + name + "_rTVD.pdf")
    plt.show()

    tvd.draw_path_graph(G)
    plt.imshow(m < 100, cmap="Greys")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("../ICRA16-TVD/figs/" + name + "_TVD.pdf")
    plt.show()


if __name__ == "__main__":
    # tvd_example()
    # all_plots("imgs/strongly_connected.pgm", "strongly_connected")
    all_plots("imgs/bars.pgm", "bars")
    # all_plots("imgs/Grelha4.pgm", "Grelha4")
