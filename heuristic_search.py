from algorithms import (
    a_star,
    best_first,
    hill_climbing,
)

from problems import (
    MazeProblem,
    MissionariesAndCannibalsProblem,
    NQueensProblem
)

from interfaces.state_space_problem import StateSpaceProblem

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
    a_star.a_star_search,
    best_first.best_first_search,
    hill_climbing.hill_climbing_search,
]

# Define a list of example problems
problems = [
    ("Maze", maze_problem),
    ("Missionaries and Cannibals", missionaries_and_cannibals_problem),
    ("N-Queens", n_queens_problem)
]

print("Running algorithms on MazeProblem problem using Manhattan heuristic:")
for algorithm in algorithms:
    try:
        result = algorithm(maze_problem, maze_problem.manhattan_distance_heuristic, statistics=True)
        print(f"{algorithm.__name__}: {result}")
    except NotImplementedError:
        print(f"{algorithm.__name__}: Not implemented for this problem")
print("\n")

print("Running algorithms on MazeProblem problem using Euclidean heuristic:")
for algorithm in algorithms:
    try:
        result = algorithm(maze_problem, maze_problem.euclidean_distance_heuristic, statistics=True)
        print(f"{algorithm.__name__}: {result}")
    except NotImplementedError:
        print(f"{algorithm.__name__}: Not implemented for this problem")
print("\n")

print("Running algorithms on Missionaries and Cannibals problem using attacking queen pairs heuristic:")
for algorithm in algorithms:
    try:
        result = algorithm(missionaries_and_cannibals_problem, missionaries_and_cannibals_problem.trips_heuristic, statistics=True)
        print(f"{algorithm.__name__}: {result}")
    except NotImplementedError:
        print(f"{algorithm.__name__}: Not implemented for this problem")
print("\n")

print("Running algorithms on N-Queens problem using attacking queen pairs heuristic:")
for algorithm in algorithms:
    try:
        result = algorithm(n_queens_problem, n_queens_problem.attacking_queen_pairs_heuristic, statistics=True)
        print(f"{algorithm.__name__}: {result}")
    except NotImplementedError:
        print(f"{algorithm.__name__}: Not implemented for this problem")
print("\n")

print("Hill Climbing | Maze, Missionaries & Cannibals, Random Restarts")
result = hill_climbing.hill_climbing_search(problem=missionaries_and_cannibals_problem, heuristic=missionaries_and_cannibals_problem.trips_heuristic, random_restart=True, num_restarts=100, statistics=True)
print(result)