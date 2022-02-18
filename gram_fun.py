import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations


def checkRequirements(G, k, l):
    for v in G.nodes():
        neighbors = list(G.neighbors(v))

        subsets = []
        for i in range(1, l + 1):
            subsets += combinations(neighbors, i)


        for s in subsets:
            count = 0

            for i in G.nodes():
                if set(s).issubset(set(G.neighbors(i))):
                    count += 1

                    if count >= k:
                        break

            if count < k:
                return False

        return True
            

def commonNeighbors(G, V):
    """
    Parameters:
    G : the graph.
    V : set of vertices (a list).

    Returns :
    com : the set of common neighbors of all vertices of V in G.
    """

    # TODO: currently assuming that |V| >= 1
    com = set(G.neighbors(V[0]))

    for v in V[1:]:
        com.intersection_update(set(G.neighbors(v)))

    return list(com)


def distNeighbors(distances, v, dist):
    """
    Parameters:
    distances : dictionary containing for each node the dict with the distances from all other nodes.
    v : the node we are using as our starting point.
    dist : the distance we are interested in.

    Returns:
    The neighbors at distance dist of node v.
    """

    return [n for n in distances[v] if distances[v][n] == dist]


def addEdges(G, k, l, n):
    """
    Parameters:
    G : the graph.
    k, l : privacy parameters.
    n : graph order.

    Returns:
    G2 : augmented graph.
    costs : costs matrix.
    """

    G2 = G.copy()
    costs = np.full((n, n), n)
    flag = 1
    dist = 1

    # precompute the distances between nodes, need only to lookup during execution
    # TODO: is this the most efficient approach? gets pretty big for large n
    node_dist = dict(nx.all_pairs_shortest_path_length(G))

    if l == 1:
        while flag == 1 and dist < n - 1:
            flag = 0
            for i in range(n):
                if G2.degree[i] < k:
                    # connect the current node to all neighbors at distance dist + 1
                    neighbors = distNeighbors(node_dist, i, dist + 1)
                    for v in neighbors:
                        G2.add_edge(i, v)

                        # decrease the cost of the edges
                        # keeping in mind that the matrix is symmetric
                        costs[i][v] -= 1
                        costs[v][i] -= 1

                    flag = 1

            dist += 1

    else:
        while flag == 1 and dist < n:
            flag = 0

            for i in range(n):
                neighbors = list(G.neighbors(i))

                if len(commonNeighbors(G2, neighbors)) < k:
                    # connect all vertices in neighbors to some vertices in
                    # V' = G.neighbors(i, dist) in G2 with minimum number of new edges
                    eligible_vertices = distNeighbors(node_dist, i, dist)

                    for dest in eligible_vertices:
                        if len(commonNeighbors(G2, neighbors)) >= k:    # condition is satisfied, no more edges are required
                            break

                        for v in neighbors:
                            if v == dest:   # do not add self loop
                                continue

                            G2.add_edge(v, dest)
                            costs[v][dest] -= 1
                            costs[dest][v] -= 1

                    flag = 1

            dist += 1

    return G2, costs

def isSafe(G, G2, Gp, e, k, l):
    """
    Parameters:
    G : original graph.
    G2 : augmented graph.
    Gp : modified graph.
    e : candidate edge to be removed.
    k, l : privacy parameters.

    Returns:
    safe : safety flag.
    """

    for v in G.neighbors(e[0]):
        shared_neighbors = set(G.neighbors(v)).intersection(G2.neighbors(e[1]))

        subsets = []
        for i in range(1, min(l, len(shared_neighbors) + 1)):
            c = combinations(shared_neighbors, i)
            subsets += list(filter(lambda x: e[0] in x, c))

        for s in subsets:
            if len(commonNeighbors(Gp, s)) < k:
                return False

    for v in G.neighbors(e[1]):
        shared_neighbors = set(G.neighbors(v)).intersection(G2.neighbors(e[0]))
       
        subsets = []
        for i in range(1, min(l, len(shared_neighbors) + 1)):
            c = combinations(shared_neighbors, i)
            subsets += list(filter(lambda x: e[1] in x, c))

        for s in subsets:
            if len(commonNeighbors(Gp, s)) < k:
                return False

    return True


def removeEdges(G, G2, costs, k, l):
    """
    Parameters:
    G : the original graph.
    G2 : the augmented graph.
    costs : costs matrix.
    k, l : privacy parameters.

    Returns :
    Gp : the protected graph
    """

    Gp = G2.copy()

    # for each "new" edge, in decreasing order of costs
    new_edges = G2.edges - G.edges  # TODO: EdgeView supports set operations, check where we can use them in previous impl.
    new_edges = sorted(new_edges, key=lambda x: costs[x[0]][x[1]], reverse=True)

    for e in new_edges:
        if l == 1:
            if Gp.degree(e[0]) > k and Gp.degree(e[1]) > k:
                Gp.remove_edge(e)

        else: # typo in the paper?
            Gp.update(edges=G2.edges - [e])

            if isSafe(G, G2, Gp, e, k, l):
                G2.update(edges=Gp.edges)
            else:
                Gp.add_edge(e)

    return Gp


            


# not a great choice for the generator, as all nodes will have the same degree
# graph_order = 10
# k = 2
# l = 2
# G = nx.generators.connected_watts_strogatz_graph(graph_order, 4, 0.35, seed=1)

# print(f'G satisfies k={k}, l={l}: {checkRequirements(G, k, l)}')

# nx.draw(G, with_labels=True)
# plt.show()


# G2, costs = addEdges(G, k, l, graph_order)

# print(f'G2 satisfies k={k}, l={l}: {checkRequirements(G2, k, l)}')

# nx.draw(G2, with_labels=True)
# plt.show()

# Gp = removeEdges(G, G2, costs, k, l)

# print(f'Gp satisfies k={k}, l={l}: {checkRequirements(Gp, k, l)}')

# nx.draw(Gp, with_labels=True)
# plt.show()

