import unittest

import networkx as nx

from gram.gram_fun import *


class TestURVemail(unittest.TestCase):

    def setUp(self):
        self.G = nx.readwrite.edgelist.read_edgelist('test/graphs/urvemail')
        self.n = self.G.order()

    def testk1l1(self):
        k = 1
        l = 1
        G2, costs = addEdges(self.G, k, l, self.n)
        Gp = removeEdges(self.G, G2, costs, k, l)
        self.assertTrue(checkRequirements(Gp, k, l))


if __name__ == '__main__':
    unittest.main()
