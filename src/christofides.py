"""
File: christofides.py
Author: Frederico D. S. Baker - fredericobaker@dcc.ufmg.br
Date: December 5, 2023

Implementation of the Christofides algorithm for the Traveling Salesman Problem (TSP).
This script constructs a graph from a distance matrix, finds a minimum spanning tree (MST),
creates a matching for odd degree nodes, and forms an Eulerian circuit to approximate a solution
to the TSP.

Dependencies: networkx
"""

import networkx as nx

from src.utils import *

def christofides(matrix):
    n = len(matrix)

    # Creates graph from matrix
    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=matrix[i][j])
    
    # Finds the minimum spanning tree
    mst = nx.minimum_spanning_tree(G, algorithm="prim")

    # Create a subgraph with odd degree nodes in the MST
    odd_degree_nodes = [v for v, d in mst.degree() if d % 2 != 0]
    odd_subgraph = G.subgraph(odd_degree_nodes)

    # Find a minimum weight matching
    matching = nx.algorithms.matching.min_weight_matching(odd_subgraph)

    # Add edges from matching to the MST
    mst = nx.MultiGraph(mst)
    mst.add_edges_from(matching)

    # # Find an Eulerian circuit in the combined graph
    eulerian_circuit = list(nx.eulerian_circuit(mst))

    # Convert the Eulerian circuit to a Hamiltonian circuit by skipping visited nodes
    visited = set()
    path = [eulerian_circuit[0][0]]
    for u, v in eulerian_circuit:
        if v not in visited:
            path.append(v)
            visited.add(v)

    # Returns to the starting point
    path.append(path[0])

    # Gets the cost of the found path
    cost = sum(matrix[path[i]][path[i + 1]] for i in range(len(path) - 1))

    return path, cost