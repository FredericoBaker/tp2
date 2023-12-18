"""
File: twice_around_the_tree.py
Author: Frederico D. S. Baker - fredericobaker@dcc.ufmg.br
Date: December 5, 2023

Implementation of the 'Twice Around the Tree' algorithm for the Traveling Salesman Problem (TSP).
Creates a minimum spanning tree (MST) from a distance matrix, performs a preorder traversal
to form a path, and calculates the total path cost.

Dependencies: networkx
"""

import networkx as nx

from src.utils import *

def twice_around_the_tree(matrix):
    n = len(matrix)

    # Creates graph from matrix
    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=matrix[i][j])
    
    # Finds the minimum spanning tree
    mst = nx.minimum_spanning_tree(G, algorithm="prim")

    # Makes a preorder traversal in mst
    path = list(nx.dfs_preorder_nodes(mst, 0))

    # Returns to the starting point
    path.append(path[0])

    # Gets the cost of the found path
    cost = sum(matrix[path[i]][path[i + 1]] for i in range(len(path) - 1))

    return path, cost