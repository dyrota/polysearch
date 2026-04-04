"""
Demo script: run all 8 algorithms on the Maze problem and print a summary.
"""
from polysearch.problems.maze import MazeProblem
from polysearch.algorithms.breadth_first import breadth_first_search
from polysearch.algorithms.depth_first import depth_first_search
from polysearch.algorithms.uniform_cost import uniform_cost_search
from polysearch.algorithms.iterative_deepening import iterative_deepening_search
from polysearch.algorithms.branch_and_bound import branch_and_bound_search
from polysearch.algorithms.best_first import best_first_search
from polysearch.algorithms.a_star import a_star_search
from polysearch.algorithms.hill_climbing import hill_climbing_search

MAZE = [
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 1, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 1, 0, 1, 1, 0, 0],
]

maze = MazeProblem(MAZE, start=(0, 0), goal=(7, 7))

algorithms = [
    ("BFS",            lambda: breadth_first_search(maze, statistics=True)),
    ("DFS",            lambda: depth_first_search(maze, statistics=True)),
    ("UCS",            lambda: uniform_cost_search(maze, statistics=True)),
    ("IDS",            lambda: iterative_deepening_search(maze, statistics=True)),
    ("Branch & Bound", lambda: branch_and_bound_search(maze, statistics=True)),
    ("Best-First",     lambda: best_first_search(maze, heuristic=maze.manhattan_distance_heuristic, statistics=True)),
    ("A*",             lambda: a_star_search(maze, heuristic=maze.manhattan_distance_heuristic, statistics=True)),
    ("Hill Climbing",  lambda: hill_climbing_search(maze, heuristic=maze.manhattan_distance_heuristic, statistics=True)),
]

print(f"{'Algorithm':<16} {'Path Length':>12} {'Visited':>10} {'Cost':>8}")
print("-" * 50)

for name, run in algorithms:
    path_dict, visited_dict, stats = run()
    path = path_dict['path']
    path_len = len(path) if path else 0
    visited_count = len(visited_dict['visited'])
    cost = stats.get('cost', 'N/A')
    print(f"{name:<16} {path_len:>12} {visited_count:>10} {str(cost):>8}")
