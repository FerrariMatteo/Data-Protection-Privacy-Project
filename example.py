import networkx as nx
import matplotlib.pyplot as plt
from gram_fun import *

G = nx.Graph()

G.add_nodes_from(list(range(1,13)))
G.add_edges_from([
    (1,2),(1,6),(1,4),(1,5),
    (2,6),
    (3,5), (3,12), (3,7),
    (4,6), (4, 10), (4, 9), (4, 5),
    (5,6), (5,10), (5,9), (5,11),
    (6,9), (6,10),
    (7,8), (7,11),
    (8, 11),
    (9, 10),
    (11, 12)
])

nx.draw(G, with_labels=True)
plt.show()

k = 3
l = 2

n = G.order()

print(f'Satisfies k={k}, l={l}: {checkRequirements(G, k, l)}')

G2, costs = addEdges(G, k, l, n)

print(f'G2 satisfies k={k}, l={l}: {checkRequirements(G2, k, l)}')

nx.draw(G2, with_labels=True)
plt.show()

Gp = removeEdges(G, G2, costs, k, l)

print(f'Gp satisfies k={k}, l={l}: {checkRequirements(Gp, k, l)}')

nx.draw(Gp, with_labels=True)
plt.show()
