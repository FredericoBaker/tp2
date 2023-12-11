"""
File: tsp_branch_and_bound.py
Author: Frederico D. S. Baker - fredericobaker@dcc.ufmg.br
Date: December 5, 2023

This script implements the Branch and Bound algorithm to solve the Traveling Salesman Problem (TSP).
It includes a function to calculate the lower bound for a path in the TSP and the main function to solve the TSP.
The algorithm tracks execution time, logs solutions, and performance metrics, and handles execution time limits.

Dependencies: numba, pandas, heapq, time
"""

from numba import njit
import pandas as pd
import heapq
import time

from utils import *

@njit
def bound(matrix, path):
    """
    Calculate the lower bound of a path in the TSP using a given matrix.
    Includes the cost of edges in the path and estimates for remaining vertices.
    """

    n = matrix.shape[0]
    bound = 0
    path_size = len(path)

    # Add cost of edges already in path
    if path_size > 1:
        for i in range(path_size - 1):
            bound += matrix[path[i], path[i + 1]]

    # If path is complete, returns total cost
    if path_size == n:
        return int(np.ceil(bound + matrix[path[-1], path[0]]))

    remain_vertices = np.array([i for i in range(n) if i not in path])

    # For each node not visites, finds the two lowest edges
    for i in remain_vertices:
        remain_except_i = remain_vertices[remain_vertices != i]

        if remain_except_i.size >= 2:
            min_edges = np.partition(matrix[i, remain_except_i], 1)[:2]
            bound += np.sum(min_edges) / 2
        elif remain_except_i.size == 1:
            bound += matrix[i, remain_except_i[0]] / 2

    return int(np.ceil(bound))

def tsp(matrix, priority='optimized', time_limit=30):
    """
    Solves the Traveling Salesman Problem (TSP) using the branch and bound method.
    Tracks execution time and logs solutions and performance metrics.
    
    Args:
    matrix: Distance matrix for TSP.
    priority: Method of prioritizing nodes in the heap ('regular' or 'optimized').
    time_limit: Maximum execution time in minutes.
    
    Returns:
    DataFrame logging solutions and a boolean indicating if the process finished within the time limit.
    """
    n = len(matrix)

    root = Node(level=0, path=[0], cost=0)
    root.bound = bound(matrix, np.array(root.path))
    root.priority = (root.bound / len(root.path))

    heap = []
    heapq.heappush(heap, (root.priority, root))

    best = sum([matrix[i][(i + 1) % n] for i in range(n)])
    solution = []

    leaves_count = 0

    finished = True

    start_time = time.time()

    while heap:
        current_time = time.time()
        if (current_time - start_time) / 60 > time_limit:  # Check if 30 minutes have passed
            finished = False
            break

        _, node = heapq.heappop(heap)

        if node.level == n - 1 and node.cost + matrix[node.path[-1]][0] < best:
            best = node.cost + matrix[node.path[-1]][0]
            solution = node.path + [0]

            leaves_count += 1
            
        elif node.bound < best:

            for i in range(n):
                if i not in node.path:
                    new_level = node.level + 1
                    new_path = node.path + [i]
                    new_cost = node.cost + matrix[node.path[-1]][i]
                    
                    new_node = Node(level=new_level, path=new_path, cost=new_cost)

                    new_node.bound = bound(matrix, np.array(new_path))
                    
                    new_node.priority = (new_node.bound / len(new_node.path)) if priority == 'optimized' else new_node.bound

                    heapq.heappush(heap, (new_node.priority, new_node))
                      
    return solution, best, finished, leaves_count