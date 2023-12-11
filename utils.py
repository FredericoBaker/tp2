"""
File: tsp_utils.py
Author: Frederico D. S. Baker - fredericobaker@dcc.ufmg.br
Date: December 5, 2023

This script provides utility functions and classes for solving the Traveling Salesman Problem (TSP).
It includes a function to calculate Euclidean distances, a function to create a distance matrix from a dataset,
and a Node class used in the branch and bound method for solving the TSP.

Dependencies: numpy, math, csv
"""

import numpy as np
import math
import csv

def calculate_euclidean_distance(x1, y1, x2, y2):
    """
    Calculate the Euclidean distance between two points.
    
    Args:
    x1, y1: Coordinates of the first point.
    x2, y2: Coordinates of the second point.
    
    Returns:
    The Euclidean distance as an integer.
    """
    xd = x1 - x2
    yd = y1 - y2
    return int(round(math.sqrt(xd**2 + yd**2)))

def get_dataset_matrix(dataset):
    """
    Create a distance matrix from a dataset of coordinates.
    
    Args:
    dataset: Name of the dataset file (CSV format).
    
    Returns:
    A numpy matrix representing distances between each pair of nodes.
    """
    path = f'./data/cleaned/{dataset}.csv'

    with open(path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        nodes = list(reader)

    n = len(nodes)
    matrix = np.zeros((n, n))

    # Populate the matrix with distances
    for i in range(n):
        for j in range(n):
            if i != j:
                x1, y1 = int(nodes[i][1]), int(nodes[i][2])
                x2, y2 = int(nodes[j][1]), int(nodes[j][2])
                matrix[i][j] = calculate_euclidean_distance(x1, y1, x2, y2)

    return matrix

class Node:
    """
    A class representing a node in the branch and bound tree for solving TSP.

    Attributes:
    level (int): The level of the node in the tree.
    path (list): The path taken to reach this node.
    cost (int): The total cost of the path.
    bound (int): The lower bound of the total path cost.
    priority (float): The priority of the node for the purpose of the branch and bound algorithm.
    """
    def __init__(self, level=None, path=None, cost=None, bound=None, priority=None):
        self.level = level
        self.path = path
        self.cost = cost
        self.bound = bound
        self.priority = priority

    def __lt__(self, other):
        # Defines the comparison behavior for the priority queue
        return self.priority < other.priority
    
    def __str__(self):
        # String representation of the node
        return str(tuple([self.level, self.path, self.bound]))