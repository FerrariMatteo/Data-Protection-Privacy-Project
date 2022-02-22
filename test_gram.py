from itertools import product
import timeit

import networkx as nx

from gram_fun import *


def testGram(name, G, k, l):

    print(f'Testing {name} graph with k={k} and l={l}... ')

    n = G.order()

    # Compute initial metrics
    start_m = G.number_of_edges()
    start_APL = nx.average_shortest_path_length(G)
    start_ACC = sum(nx.clustering(G).values()) / len(G)
    start_ABC = sum(nx.betweenness_centrality(G).values()) / len(G)
    start_time = timeit.default_timer()

    # Execute algorithm
    G2, costs = addEdges(G, k, l, n)
    Gp = removeEdges(G, G2, costs, k, l)

    # Compute final metrics
    end_m = Gp.number_of_edges()
    end_APL = nx.average_shortest_path_length(Gp)
    end_ACC = sum(nx.clustering(Gp).values()) / len(Gp)
    end_ABC = sum(nx.betweenness_centrality(Gp).values()) / len(Gp)
    end_time = timeit.default_timer()

    try:

        # Metrics
        print(f'\tΔm:        {end_m - start_m}')
        print(f'\tabs(ΔAPL): {abs(end_APL - start_APL):.4f}')
        print(f'\tabs(ΔACC): {abs(end_ACC - start_ACC):.4f}')
        print(f'\tabs(ΔABC): {abs(end_ABC - start_ABC):.4f}')
        print(f'\tRun time:  {(end_time - start_time):.2f} seconds')

        # Check if it (k, l)-anonymous
        print('\tResulting graph is ', end='')
        if not checkRequirements(Gp, k, l):
            print('not ', end='')
        print('(k, l)-anonymous\n')
    except KeyError as e:
        print()
        raise e
    except Exception as e:
        print('ERROR', '\n', e)


def runAllTests():
    edgelists = [
        'jazz',
        'karate',
        'urvemail',
        'uspowergrid',
    ]
    graphs = [nx.read_edgelist(f'graphs/{el}') for el in edgelists]
    kvals = [3, 4, 5, 10]
    lvals = [1, 2]

    for (name, G), k, l in product(zip(edgelists, graphs), kvals, lvals):
        testGram(name, G, k, l)


if __name__ == '__main__':
    runAllTests()
