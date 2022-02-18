from gram_fun import *
import matplotlib.pyplot as plt

# not a great choice for the generator, as all nodes will have the same degree
graph_order = 100
k = 5
l = 2
G = nx.generators.connected_watts_strogatz_graph(graph_order, 3, 0.35)

print(f'G satisfies k={k}, l={l}: {checkRequirements(G, k, l)}')

# nx.draw(G, with_labels=True)
# plt.show()

G2, costs = addEdges(G, k, l, graph_order)

print(f'G2 satisfies k={k}, l={l}: {checkRequirements(G2, k, l)}')

# nx.draw(G2, with_labels=True)
# plt.show()

Gp = removeEdges(G, G2, costs, k, l)

print(f'Gp satisfies k={k}, l={l}: {checkRequirements(Gp, k, l)}')

# nx.draw(Gp, with_labels=True)
# plt.show()