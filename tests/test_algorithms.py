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


# --- iterative deepening: max_depth is a ceiling, not the search depth -------

# An OPEN grid, deliberately: the walled MAZE fixture is constrained enough
# that depth-limited DFS stumbles onto the optimal path anyway, so it cannot
# distinguish a real deepening from a single deep DFS. With room to wander, the
# difference is stark -- this grid returned a 41-step path where the optimum is
# 15.
OPEN_GRID = [[0] * 8 for _ in range(8)]


def test_iterative_deepening_bounded_returns_shallowest_path():
    # A generous max_depth must not change WHICH solution is returned: the
    # deepening still starts at 0, so the first solution found is the
    # shallowest one, matching the unbounded search exactly.
    problem = MazeProblem(OPEN_GRID, (0, 0), (7, 7))
    bounded = iterative_deepening_search(problem, max_depth=60, statistics=True)
    unbounded = iterative_deepening_search(MazeProblem(OPEN_GRID, (0, 0), (7, 7)), statistics=True)
    assert bounded[0]['path'] == unbounded[0]['path']


def test_iterative_deepening_bounded_matches_bfs_optimal_length():
    # BFS is optimal on a unit-cost graph, so iterative deepening must agree
    # with it on path length. Previously this returned 41 against BFS's 15.
    ids = iterative_deepening_search(MazeProblem(OPEN_GRID, (0, 0), (7, 7)), max_depth=60, statistics=True)
    bfs = breadth_first_search(MazeProblem(OPEN_GRID, (0, 0), (7, 7)), statistics=True)
    assert len(ids[0]['path']) == len(bfs[0]['path'])


def test_iterative_deepening_reports_real_inference_count(maze):
    # The bounded branch never incremented its counter, so this was always 0 --
    # which made iterative deepening look free next to every other algorithm.
    result = iterative_deepening_search(maze, max_depth=60, statistics=True)
    assert result[2]['inferences'] > 0


def test_iterative_deepening_inferences_match_expand_events(maze):
    events = []
    result = iterative_deepening_search(maze, max_depth=60, statistics=True, on_step=events.append)
    expands = [e for e in events if e['type'] == 'expand']
    assert result[2]['inferences'] == len(expands)


def test_iterative_deepening_iterates_through_every_depth(maze):
    events = []
    iterative_deepening_search(maze, max_depth=60, statistics=True, on_step=events.append)
    depths = [e['depth_limit'] for e in events if e['type'] == 'mark' and e['kind'] == 'iteration-begin']
    # Consecutive from 0, i.e. it actually deepens rather than jumping to the cap.
    assert depths == list(range(len(depths)))


def test_iterative_deepening_unreachable_depth_returns_standard_shape(maze):
    # Too shallow to reach the goal. Previously a bare None even with
    # statistics=True, unlike every other algorithm in the package.
    result = iterative_deepening_search(maze, max_depth=2, statistics=True)
    assert result is not None
    path_dict, visited_dict, stats = result
    assert path_dict['path'] is None
    assert isinstance(visited_dict['visited'], set)
    assert stats['inferences'] > 0


def test_iterative_deepening_unreachable_depth_without_statistics(maze):
    assert iterative_deepening_search(maze, max_depth=2) is None


def test_iterative_deepening_depth_zero_checks_only_the_start():
    # A limit of 0 means "expand the root and stop", so it finds a solution
    # only when the start state is already a goal.
    start_is_goal = MazeProblem(MAZE, START, START)
    assert iterative_deepening_search(start_is_goal, max_depth=0) == [START]
    assert iterative_deepening_search(MazeProblem(MAZE, START, GOAL), max_depth=0) is None


# --- hill climbing: stalling is failure, and restarts must help not hurt ----

class _LocalOptimumProblem(StateSpaceProblem):
    """A 1-D landscape on 0..10 with the goal at 10 and a deep well at 3.

    Climbing from 0 walks into the well and stalls there, never reaching the
    goal. Starting anywhere at 5 or above climbs cleanly to 10. That split is
    what makes restart behavior observable: one start fails, another succeeds.
    """

    def __init__(self, start=0, restart_states=None):
        self._start = start
        self._restart_states = list(restart_states or [])
        self.random_state_calls = 0

    def initial_state(self):
        return self._start

    def goal_check(self, state):
        return state == 10

    def operators(self):
        return [lambda s: s - 1, lambda s: s + 1]

    def apply_operator(self, operator, state):
        nxt = operator(state)
        return nxt if 0 <= nxt <= 10 else None

    def cost(self, state1, state2):
        return 1

    def heuristic(self, state):
        # The well at 3 is more attractive than the goal, so a climb that
        # reaches it can never leave.
        return -100 if state == 3 else abs(10 - state)

    def random_state(self):
        state = self._restart_states[self.random_state_calls % len(self._restart_states)]
        self.random_state_calls += 1
        return state


def test_hill_climbing_stall_is_reported_as_failure():
    # The climb stalls in the well at 3 and never reaches 10. Returning that
    # partial path made a failed search look like a solved one.
    problem = _LocalOptimumProblem()
    assert hill_climbing_search(problem, heuristic=problem.heuristic) is None


def test_hill_climbing_stall_with_statistics_matches_package_shape():
    problem = _LocalOptimumProblem()
    path_dict, visited_dict, stats = hill_climbing_search(problem, heuristic=problem.heuristic, statistics=True)
    assert path_dict['path'] is None
    assert stats['cost'] is None
    assert isinstance(visited_dict['visited'], set)


def test_hill_climbing_success_still_returns_its_path():
    problem = _LocalOptimumProblem(start=5)
    path = hill_climbing_search(problem, heuristic=problem.heuristic)
    assert path is not None
    assert path[0] == 5 and path[-1] == 10


def test_hill_climbing_restart_prefers_a_solution_over_a_stall():
    # Attempt 0 starts at 0, stalls in the well with a partial path of cost 3.
    # Attempt 1 restarts at 5 and reaches the goal with cost 5. Selecting on
    # cost alone chose the cheaper STALL, so random_restart reliably returned
    # the worst attempt; a solution must always win.
    problem = _LocalOptimumProblem(restart_states=[5])
    path = hill_climbing_search(problem, heuristic=problem.heuristic, random_restart=True, num_restarts=2)
    assert path is not None
    assert path[-1] == 10


def test_hill_climbing_restart_uses_random_state():
    # Without a random_state() the restarts all began from initial_state() and
    # re-ran the identical deterministic climb.
    problem = _LocalOptimumProblem(restart_states=[5, 6, 7])
    hill_climbing_search(problem, heuristic=problem.heuristic, random_restart=True, num_restarts=4)
    # First attempt uses initial_state(), the other three ask for a start.
    assert problem.random_state_calls == 3


def test_hill_climbing_restart_starts_are_actually_different():
    problem = _LocalOptimumProblem(restart_states=[5, 6, 7])
    events = []
    hill_climbing_search(
        problem, heuristic=problem.heuristic, random_restart=True, num_restarts=4, on_step=events.append
    )
    first_expand = {}
    for e in events:
        if e['type'] == 'expand':
            first_expand.setdefault(e['restart_index'], e['state'])
    assert len(set(first_expand.values())) > 1


def test_hill_climbing_restart_totals_cover_every_attempt():
    problem = _LocalOptimumProblem(restart_states=[5])
    single = hill_climbing_search(_LocalOptimumProblem(start=5), heuristic=problem.heuristic, statistics=True)
    multi = hill_climbing_search(problem, heuristic=problem.heuristic, random_restart=True, num_restarts=2, statistics=True)
    # Two attempts really were performed, so the reported work must exceed one.
    assert multi[2]['inferences'] > single[2]['inferences']


def test_hill_climbing_restart_reports_goal_reached_per_attempt():
    problem = _LocalOptimumProblem(restart_states=[5])
    events = []
    hill_climbing_search(
        problem, heuristic=problem.heuristic, random_restart=True, num_restarts=2, on_step=events.append
    )
    ends = [e for e in events if e['type'] == 'mark' and e['kind'] == 'restart-end']
    assert [e['goal_reached'] for e in ends] == [False, True]
