from os import remove
from gram_fun import *
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from(range(1,12))
G.add_edges_from([
    (1,2),
    (2,3),(2,11),
    (4,5),
    (5,6),(5,11),
    (7,11),
    (8,11),(8,9),
    (9,10),
    (10,11)
])

nx.draw(G, with_labels=True)
plt.show()

k = 2
l = 2

G2, costs = addEdges(G, k, l, G.order())

nx.draw(G2, with_labels=True)
plt.show()

# print('costs matrix:')
# print(costs)
# print(f'G2 satisfies k={k}, l={l}: {checkRequirements(G2, k, l)}')

# Gp = removeEdges(G, G2, costs, k, l)

# nx.draw(Gp, with_labels=True)
# plt.show()

# print(f'Gp satisfies k={k}, l={l}: {checkRequirements(Gp, k, l)}')