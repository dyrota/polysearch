# from polysearch.algorithms import (
#     # branch_and_bound,
#     # breadth_first,
#     depth_first,
#     # iterative_deepening,
#     # uniform_cost
# )

# from .polysearch.algorithms.best_first import best_first_search

from polysearch.problems import (
    MazeProblem,
    MissionariesAndCannibalsProblem,
    NQueensProblem
)

# from .polysearch.interfaces.state_space_problem import StateSpaceProblem

# from polysearch.problems.maze import MazeProblem
from polysearch.algorithms.depth_first import depth_first_search

# Initialize the example problems
maze_data = [
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 1, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 1, 0, 1, 1, 0, 0]
]

initial_state = (0, 0)
goal_state = (7, 7)
number_of_queens = 8

maze_problem = MazeProblem(maze_data, initial_state, goal_state)
missionaries_and_cannibals_problem = MissionariesAndCannibalsProblem()
n_queens_problem = NQueensProblem(number_of_queens)

# Define a list of algorithms to run on each problem
algorithms = [
    # branch_and_bound.branch_and_bound_search,
    # breadth_first.breadth_first_search,
    depth_first_search,
    # iterative_deepening.iterative_deepening_search,
    # uniform_cost.uniform_cost_search
]

# Define a list of example problems
problems = [
    ("Maze", maze_problem),
    ("Missionaries and Cannibals", missionaries_and_cannibals_problem),
    ("N-Queens", n_queens_problem)
]

# result = depth_first.depth_first_search(maze_problem, statistics=True)
# for _ in result:
#     print(_)

# Run each algorithm on each problem (without using any heuristics) and display the results and statisitcs
for problem_name, problem in problems:
    print(f"Running algorithms on {problem_name} problem:")
    for algorithm in algorithms:
        try:
            result = algorithm(problem, statistics=True)
            print(f"{algorithm.__name__}: {result}")
        except NotImplementedError:
            print(f"{algorithm.__name__}: Not implemented for this problem")
    print("\n")
