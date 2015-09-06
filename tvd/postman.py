#!/usr/bin/env python2.7
import networkx as nx

__author__ = 'Ralf Kistner'


def pairs(lst, circular=False):
    i = iter(lst)
    first = prev = item = i.next()
    for item in i:
        yield prev, item
        prev = item
    if circular:
        yield item, first


def graph_components(graph):
    components = list(nx.connected_component_subgraphs(graph))
    components.sort(key=lambda c: c.size(), reverse=True)
    return components


def odd_graph(graph):
    result = nx.Graph()
    odd_nodes = [n for n in graph.nodes() if graph.degree(n) % 2 == 1]
    for u in odd_nodes:
        paths = nx.shortest_path(graph, source=u, weight='weight')
        lengths = nx.shortest_path_length(graph, source=u, weight='weight')
        for v in odd_nodes:
            if u <= v:
                continue
            result.add_edge(u, v, weight=-lengths[v], path=paths[v])

    return result


def edge_sum(graph):
    total = 0
    for u, v, data in graph.edges(data=True):
        total += data['weight']
    return total


def matching_cost(graph, matching):
    # Calculate the cost of the additional edges
    cost = 0
    for u, v in matching.items():
        if v <= u:
            continue
        data = graph[u][v]
        cost += abs(data['weight'])
    return cost


def find_matchings(graph, n=5):
    best_matching = nx.max_weight_matching(graph, True)
    matchings = [best_matching]

    for u, v in best_matching.items():
        if v <= u:
            continue
        smaller_graph = nx.Graph(graph)
        smaller_graph.remove_edge(u, v)
        matching = nx.max_weight_matching(smaller_graph, True)
        if len(matching) > 0:
            matchings.append(matching)

    matching_costs = [(matching_cost(graph, matching), matching)
                      for matching in matchings]
    matching_costs.sort()

    final_matchings = []
    last_cost = None
    for cost, matching in matching_costs:
        if cost == last_cost:
            continue
        last_cost = cost
        final_matchings.append((cost, matching))

    return final_matchings


def build_eulerian_graph(graph, odd, matching):
    eulerian_graph = nx.MultiGraph(graph)
    for u, v in matching.items():
        if v <= u:
            continue
        edge = odd[u][v]
        path = edge['path']
        for p, q in pairs(path):
            eulerian_graph.add_edge(p, q, weight=graph[p][q]['weight'])

    return eulerian_graph


def eulerian_circuit(graph):
    circuit = list(nx.eulerian_circuit(graph))
    nodes = []
    for u, v in circuit:
        nodes.append(u)
    # Close the loop
    nodes.append(circuit[0][0])
    return nodes


def chinese_postman_paths(graph, n=5):
    odd = odd_graph(graph)
    matchings = find_matchings(odd, n)
    paths = []
    for cost, matching in matchings[:n]:
        eulerian_graph = build_eulerian_graph(graph, odd, matching)
        nodes = eulerian_circuit(eulerian_graph)
        paths.append((eulerian_graph, nodes))
    return paths


def single_chinese_postman_path(graph):
    odd = odd_graph(graph)
    matching = nx.max_weight_matching(odd, True)
    eulerian_graph = build_eulerian_graph(graph, odd, matching)
    nodes = eulerian_circuit(eulerian_graph)
    return eulerian_graph, nodes
