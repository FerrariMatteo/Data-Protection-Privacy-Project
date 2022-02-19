import networkx as nx
import numpy as np
from itertools import combinations


def checkRequirements(G, k, l):
    # for every node
    for v in G.nodes():
        neighbors = list(G.neighbors(v))

        # any subset of cardinality |S| <= l of neighbors
        subsets = []
        for i in range(1, l + 1):
            subsets += combinations(neighbors, i)

        # there are at least k distinct vertices
        for s in subsets:
            count = 0

            for i in G.nodes():
                # print(list(sorted(G.neighbors(i))))
                if set(s).issubset(set(G.neighbors(i))):
                    count += 1

            if count < k:
                # print(f'Constraint not verified at node {v})')
                # print(f'Subset {s} has only count={count}')
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

    if len(V) < 1:
        return None

    # TODO: currently assuming that |V| >= 1
    com = set(G.neighbors(V[0]))

    for v in V[1:]:
        com.intersection_update(set(G.neighbors(v)))

    return list(com)


def distNeighbors(distances, v, dist):
    """
    Parameters:
    distances : dictionary containing for each node the dict with the distances from all other nodes.
    v : index of the node we are using as our starting point.
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

    # used to access the costs matrix if node names are not integers in [0, n-1]
    # TODO: is there another way to do this?
    node_index_mapping = {n: i for n, i in zip(G2.nodes(), range(n))}

    if l == 1:
        while flag == 1 and dist < n - 1:
            flag = 0
            for curr_node in G.nodes():
                if G2.degree[curr_node] < k:
                    # connect the current node to all neighbors at distance dist + 1
                    neighbors = distNeighbors(node_dist, curr_node, dist + 1)
                    for v in neighbors:
                        G2.add_edge(curr_node, v)

                        # decrease the cost of the edges
                        # keeping in mind that the matrix is symmetric
                        vi = node_index_mapping[curr_node]
                        vj = node_index_mapping[v]
                        costs[vi][vj] -= 1
                        costs[vj][vi] -= 1

                    flag = 1

            dist += 1

    else:
        while flag == 1 and dist < n:
            flag = 0

            for curr_node in G.nodes():
                neighbors = list(G.neighbors(curr_node))

                if len(commonNeighbors(G2, neighbors)) < k:
                    # connect all vertices in neighbors to some vertices in
                    # V' = G.neighbors(i, dist) in G2 with minimum number of new edges
                    eligible_vertices = distNeighbors(node_dist, curr_node, dist)
                    involved_edges = set()

                    for dest in eligible_vertices:
                        for v in neighbors:
                            if v == dest and dist == 1:   # do not add self loop
                                continue

                            if not G2.has_edge(v, dest):
                                G2.add_edge(v, dest)

                            involved_edges = involved_edges.union({frozenset((v, dest))})      

                        if len(commonNeighbors(G2, neighbors)) >= k:    # condition is satisfied, no more edges are required
                            break

                    # decrease the cost of the involved edges
                    for e in involved_edges:
                        elems = list(e)
                        i = node_index_mapping[elems[0]]
                        j = node_index_mapping[elems[1]]
                        costs[i][j] -= 1
                        costs[j][i] -= 1

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

    v_i = e[0]
    v_j = e[1]

    for ni in G.neighbors(v_i):
        shared_neighbors = set(G.neighbors(ni)).intersection(set(G2.neighbors(v_j)))
        
        for i in range(1, min(l, len(shared_neighbors)) + 1):
            c = combinations(shared_neighbors, i)

            for curr in c:
                if v_i in curr:
                    # this is a valid subset, check if is has at least k common neighbors
                    if len(commonNeighbors(Gp, curr)) < k:
                        return False

    for nj in G.neighbors(v_j):
        shared_neighbors = set(G.neighbors(nj)).intersection(set(G2.neighbors(v_i)))

        for i in range(1, min(l, len(shared_neighbors)) + 1):
            c = combinations(shared_neighbors, i)

            for curr in c:
                if v_i in curr:
                    if len(commonNeighbors(Gp, curr)) < k:
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
    node_index_mapping = {n: i for n, i in zip(G2.nodes(), range(G2.order()))}
    new_edges = sorted(new_edges, key=lambda x: int(costs[node_index_mapping[x[0]]][node_index_mapping[x[1]]]), reverse=True)

    for e in new_edges:
        if l == 1:
            if Gp.degree(e[0]) > k and Gp.degree(e[1]) > k:
                Gp.remove_edge(*e)
                # print('Removing edge: ', e)

        else: # typo in the paper?
            Gp.remove_edge(*e)

            if isSafe(G, G2, Gp, e, k, l):
                G2.remove_edge(*e)
                # print('Removing edge: ', e)
            else:
                Gp.add_edge(*e)

    return Gp