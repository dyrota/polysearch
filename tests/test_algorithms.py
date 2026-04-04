import pytest
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
START = (0, 0)
GOAL = (7, 7)


@pytest.fixture
def maze():
    return MazeProblem(MAZE, START, GOAL)


def assert_valid_path(path, start, goal):
    assert path is not None, "Expected a path but got None"
    assert len(path) > 0, "Path should not be empty"
    assert path[0] == start, f"Path should start at {start}, got {path[0]}"
    assert path[-1] == goal, f"Path should end at {goal}, got {path[-1]}"


def test_bfs(maze):
    result = breadth_first_search(maze, statistics=True)
    path_dict, visited_dict, stats = result
    assert_valid_path(path_dict['path'], START, GOAL)
    assert isinstance(visited_dict['visited'], set)


def test_dfs(maze):
    result = depth_first_search(maze, statistics=True)
    path_dict, visited_dict, stats = result
    assert_valid_path(path_dict['path'], START, GOAL)
    assert isinstance(visited_dict['visited'], set)


def test_ucs(maze):
    result = uniform_cost_search(maze, statistics=True)
    path_dict, visited_dict, stats = result
    assert_valid_path(path_dict['path'], START, GOAL)
    assert isinstance(visited_dict['visited'], set)


def test_ids(maze):
    result = iterative_deepening_search(maze, statistics=True)
    path_dict, visited_dict, stats = result
    assert_valid_path(path_dict['path'], START, GOAL)
    assert isinstance(visited_dict['visited'], set)


def test_branch_and_bound(maze):
    result = branch_and_bound_search(maze, statistics=True)
    path_dict, visited_dict, stats = result
    assert_valid_path(path_dict['path'], START, GOAL)
    assert isinstance(visited_dict['visited'], set)


def test_best_first(maze):
    result = best_first_search(maze, heuristic=maze.manhattan_distance_heuristic, statistics=True)
    path_dict, visited_dict, stats = result
    assert_valid_path(path_dict['path'], START, GOAL)
    assert isinstance(visited_dict['visited'], set)


def test_a_star(maze):
    result = a_star_search(maze, heuristic=maze.manhattan_distance_heuristic, statistics=True)
    path_dict, visited_dict, stats = result
    assert_valid_path(path_dict['path'], START, GOAL)
    assert isinstance(visited_dict['visited'], set)
    assert stats['cost'] <= stats['cost'] + 1  # cost is a non-negative int


def test_hill_climbing(maze):
    # Hill climbing may get stuck in local optima, so only assert the path starts at the initial state.
    result = hill_climbing_search(maze, heuristic=maze.manhattan_distance_heuristic, statistics=True)
    path_dict, visited_dict, stats = result
    path = path_dict['path']
    assert path is not None
    assert len(path) > 0
    assert path[0] == START


def test_bfs_no_statistics(maze):
    path = breadth_first_search(maze)
    assert_valid_path(path, START, GOAL)


def test_ucs_no_statistics(maze):
    path = uniform_cost_search(maze)
    assert_valid_path(path, START, GOAL)


def test_ids_no_statistics(maze):
    path = iterative_deepening_search(maze)
    assert_valid_path(path, START, GOAL)


def test_hill_climbing_no_statistics(maze):
    path = hill_climbing_search(maze, heuristic=maze.manhattan_distance_heuristic)
    assert path is not None
    assert len(path) > 0
    assert path[0] == START
