from itertools import product

import networkx as nx

from gram_fun import *


def testGram(name, G, k, l):

    print(f'Testing {name} graph with k={k} and l={l}... ', end='')

    n = G.order()
    G2, costs = addEdges(G, k, l, n)
    Gp = removeEdges(G, G2, costs, k, l)

    try:
        if checkRequirements(Gp, k, l):
            print('OK')
        else:
            print('FAIL')
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
    # kvals = [3, 4, 5, 10]
    # lvals = [1, 2, 3]
    kvals = [3]
    lvals = [1]

    for (name, G), k, l in product(zip(edgelists, graphs), kvals, lvals):
        testGram(name, G, k, l)


if __name__ == '__main__':
    runAllTests()
