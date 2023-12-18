# Traveling Salesman Problem: Comparative Study

## Overview
This repository contains a comprehensive study on solving the Traveling Salesman Problem (TSP) using different algorithms. The primary focus is on the Branch and Bound algorithm and two approximate methods: the Christofides algorithm and the Twice Around the Tree (TAT) algorithm. The study evaluates the efficiency, accuracy, and practical applicability of these algorithms.

## Contents
- `data/`: Contains the TSP datasets used in the algorithms' performance comparison.
- `results/`: Includes the output results from the algorithm executions.
- `src/`: Source code for the Branch and Bound, Christofides, and Twice Around the Tree algorithms.
- `analysis.ipynb`: A Jupyter notebook containing the testing code and visualizations of the study's data.
- `paper.pdf`: A detailed report of the study, outlining methodologies, results, and conclusions.

## Key Findings
- **Branch and Bound**: Did not reach optimal solutions within the 30-minute time limit.
- **Christofides Algorithm**: More accurate but with a longer execution time.
- **Twice Around the Tree**: Faster execution but less accurate.

The choice of the algorithm depends on the priority between precision and speed, with Branch and Bound being suitable for cases where an exact solution is crucial.

## Usage
Each script in the repository corresponds to an implementation of the respective algorithm. To run an algorithm, navigate to the script's directory and execute it with an appropriate TSP dataset.

Example:
```bash
python BranchAndBound.py <dataset_path>
```

## Requirements
- Python 3.x
- NetworkX library
- Numba library
- Matplotlib library
- Pandas library

Install the required libraries using:
```bash
pip install networkx numba matplotlib pandas
```

## Acknowledgments
Special thanks to Professor Renato Vimieiro for his guidance and teachings during the semester.
