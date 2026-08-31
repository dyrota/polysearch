from ..interfaces.state_space_problem import StateSpaceProblem
import time

def iterative_deepening_search(problem: StateSpaceProblem, max_depth=None, statistics=False, on_step=None):
    """
    Iterative deepening search algorithm.

    :param problem: An object representing the problem to be solved, which
                    must be inherited from the StateSpaceProblem interface.
    :param max_depth: A CEILING on the deepening, not the depth to search at. The search always
                      iterates depth = 0, 1, 2, ... and returns the shallowest solution it finds;
                      max_depth simply stops it from going deeper than that. If None (default),
                      the deepening is unbounded and continues until a solution is found.
                      Note: None is genuinely unbounded (no recursion cap) - callers driving this from
                      a UI/live context should always pass an explicit max_depth to avoid a runaway search.
    :param statistics: An optional boolean flag to return the 'time', 'inferences', and 'path_cost' along with the solution.
                       Default is False. 'inferences' counts every node expansion across every
                       iteration, including the shallow nodes this algorithm deliberately re-expands
                       at each new depth - that repetition is the real cost of iterative deepening.
                       When no solution is found within max_depth, the return shape is the same
                       ({'path': None}, {'visited': ...}, {...}) as every other algorithm here.
    :param on_step: Optional callback invoked with a dict for each expand/generate/reject/goal/mark
                    event, for live tracing or visualization. Default is none (no-op). Every event is
                    stamped with 'depth_limit' (the current outer iteration's depth cap) since that's
                    the axis this algorithm actually varies along.
    :return: A tuple containing the solution, total path cost of the solution, and optionally the statistics
    """
    node_count = 0

    def depth_limited_search(state, remaining_depth, path, path_set, visited, depth_limit):
        nonlocal node_count
        # Cycle detection uses path_set (current branch only), not the shared visited set.
        # visited accumulates all nodes touched across branches for statistics tracking.
        if state in path_set:
            if on_step:
                on_step({'type': 'reject', 'from_state': path[-1] if path else None, 'to_state': state, 'reason': 'visited', 'depth_limit': depth_limit})
            return None, visited

        visited.add(state)
        node_count += 1

        if on_step:
            on_step({'type': 'expand', 'state': state, 'depth': depth_limit - remaining_depth, 'depth_limit': depth_limit, 'inferences': node_count})

        if problem.goal_check(state):
            if on_step:
                on_step({'type': 'goal', 'state': state, 'path_length': len(path) + 1, 'depth_limit': depth_limit})
            return path + [state], visited

        if remaining_depth == 0:
            if on_step:
                on_step({'type': 'mark', 'kind': 'cutoff', 'state': state, 'depth_limit': depth_limit})
            return None, visited

        new_path = path + [state]
        new_path_set = path_set | {state}

        for operator in problem.operators():
            successor_state = problem.apply_operator(operator, state)
            if successor_state is not None:
                if on_step:
                    on_step({'type': 'generate', 'from_state': state, 'to_state': successor_state, 'operator_name': getattr(operator, '__name__', None), 'depth_limit': depth_limit})
                solution, visited = depth_limited_search(successor_state, remaining_depth - 1, new_path, new_path_set, visited, depth_limit)
                if solution is not None:
                    return solution, visited
            elif on_step:
                on_step({'type': 'reject', 'from_state': state, 'to_state': successor_state, 'reason': 'invalid', 'depth_limit': depth_limit})

        return None, visited

    start_time = time.time()
    visited = set()

    # max_depth is a CAP on how deep the deepening is allowed to go, not the
    # single depth to search at. Both branches iterate; the only difference is
    # whether there is a ceiling. Running one depth-limited search directly at
    # max_depth is plain depth-limited DFS, not iterative deepening: it returns
    # whichever solution DFS happens to reach first rather than the shallowest
    # one, and on an open 8x8 maze that meant a 41-step path where the optimum
    # is 15.
    depth = 0
    while max_depth is None or depth <= max_depth:
        if on_step:
            on_step({'type': 'mark', 'kind': 'iteration-begin', 'depth_limit': depth})
        solution, visited = depth_limited_search(problem.initial_state(), depth, [], set(), set(), depth)

        if solution is not None:
            elapsed_time = time.time() - start_time
            if statistics:
                path_cost = sum(problem.cost(solution[i], solution[i + 1]) for i in range(len(solution) - 1))
                # node_count, not a count of outer iterations: re-expanding the
                # shallow nodes at every depth is the real, and genuinely
                # higher, cost of iterative deepening, and reporting the
                # iteration count instead made it look dramatically cheaper
                # than the other algorithms in any side-by-side comparison.
                return {'path': solution}, {'visited': visited}, {'time': elapsed_time, 'inferences': node_count, 'cost': int(path_cost)}
            else:
                return solution

        depth += 1

    # Exhausted max_depth without finding a solution. Returns the same shape as
    # every other algorithm in this package rather than a bare None, which
    # forced callers to special-case this one function.
    elapsed_time = time.time() - start_time
    if statistics:
        return {'path': None}, {'visited': visited}, {'time': elapsed_time, 'inferences': node_count}
    return None
