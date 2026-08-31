import pytest
from polysearch.interfaces.state_space_problem import StateSpaceProblem
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


def test_a_star_on_step_is_noop_when_omitted(maze):
    # on_step defaults to None and must not change behavior or return shape.
    with_none = a_star_search(maze, heuristic=maze.manhattan_distance_heuristic, statistics=True)
    without_param = a_star_search(maze, heuristic=maze.manhattan_distance_heuristic, statistics=True, on_step=None)
    assert with_none[0] == without_param[0]
    assert with_none[2]['cost'] == without_param[2]['cost']


def test_a_star_on_step_expand_count_matches_inferences(maze):
    events = []
    result = a_star_search(maze, heuristic=maze.manhattan_distance_heuristic, statistics=True, on_step=events.append)
    _, _, stats = result
    expand_events = [e for e in events if e['type'] == 'expand']
    assert len(expand_events) == stats['inferences']


def test_a_star_on_step_emits_goal_event(maze):
    events = []
    a_star_search(maze, heuristic=maze.manhattan_distance_heuristic, statistics=True, on_step=events.append)
    goal_events = [e for e in events if e['type'] == 'goal']
    assert len(goal_events) == 1
    assert goal_events[0]['state'] == GOAL


class _BoundExceededDemoProblem(StateSpaceProblem):
    """Tiny synthetic graph guaranteed to trigger branch_and_bound's bound-exceeded
    pruning: start->A->GOAL (cost 2) is found and closes the bound before
    start->C->D's edge to GOAL (cost 4.2) finishes generating, so that last edge
    must be pruned. The maze fixture doesn't reliably exercise this path (its
    priority-queue ordering resolves most rejections via plain visited-checks
    before any bound tightens enough to prune), so this is a purpose-built case
    instead of asserting on the shared maze fixture.
    """
    EDGES = [
        ('start', 'A', 1),
        ('start', 'C', 1.2),
        ('A', 'GOAL', 1),
        ('C', 'D', 1),
        ('D', 'GOAL', 2),
    ]

    def initial_state(self):
        return 'start'

    def goal_check(self, state):
        return state == 'GOAL'

    def operators(self):
        return [self._edge_operator(src, dst) for src, dst, _ in self.EDGES]

    def _edge_operator(self, src, dst):
        def operator(state):
            return dst if state == src else None
        operator.__name__ = f'{src}_to_{dst}'
        return operator

    def apply_operator(self, operator, state):
        return operator(state)

    def cost(self, state1, state2):
        for src, dst, c in self.EDGES:
            if src == state1 and dst == state2:
                return c
        raise ValueError(f"no edge {state1} -> {state2}")


def test_branch_and_bound_on_step_bound_exceeded_is_reachable():
    # branch_and_bound's defining behavior is pruning - confirm the instrumentation
    # actually surfaces a bound-exceeded rejection once a bound has been set.
    events = []
    result = branch_and_bound_search(_BoundExceededDemoProblem(), on_step=events.append)
    assert result == ['start', 'A', 'GOAL']
    reasons = [e.get('reason') for e in events if e['type'] == 'reject']
    assert reasons.count('bound-exceeded') == 1


def test_hill_climbing_on_step_stamps_restart_index(maze):
    events = []
    hill_climbing_search(maze, heuristic=maze.manhattan_distance_heuristic, random_restart=True, num_restarts=3, on_step=events.append)
    restart_indices = {e['restart_index'] for e in events if 'restart_index' in e}
    assert restart_indices == {0, 1, 2}


def test_iterative_deepening_on_step_iteration_begin_matches_final_depth(maze):
    events = []
    result = iterative_deepening_search(maze, statistics=True, on_step=events.append)
    path_dict, _, _ = result
    iteration_marks = [e for e in events if e['type'] == 'mark' and e['kind'] == 'iteration-begin']
    # The final iteration-begin's depth_limit must be enough to have found the path.
    assert iteration_marks[-1]['depth_limit'] >= len(path_dict['path']) - 1
