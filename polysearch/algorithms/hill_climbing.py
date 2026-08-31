from ..interfaces.state_space_problem import StateSpaceProblem
import time

def hill_climbing_search(problem: StateSpaceProblem, heuristic=None, random_restart=False, num_restarts=10, statistics=False, on_step=None):
    """
    Hill climbing search algorithm.

    :param problem: An object representing the problem to be solved, which
                    must be inherited from the StateSpaceProblem interface.
    :param heuristic: An optional heuristic function that takes a state as input
                        and returns an estimated cost to reach the goal. Default is none.
    :param random_restart: If True, retry from a fresh start state when the climb stalls on a
                           local optimum, keeping the best attempt. Requires the problem to define
                           a random_state() method returning a start state; without one every
                           restart begins from initial_state() and simply repeats the same
                           deterministic climb, so restarts gain nothing (unless the problem is
                           nondeterministic in some other way, e.g. a shuffled operators()).
                           Default is False.
    :param num_restarts: The number of restart attempts to perform, including the first. Default is 10.
    :param statistics: An optional function to return the 'time' and 'inferences'. Default is false.
                       'time' and 'inferences' are totals across every attempt, since that is the
                       work actually performed; 'cost' describes the winning attempt.
                       Hill climbing is not complete: when no attempt reaches a goal the result is
                       {'path': None} (or None without statistics), the same as every other
                       algorithm here. The partial climb is visible through on_step, which is the
                       right channel for it -- a stalled path is a trace, not a solution.
    :param on_step: Optional callback invoked with a dict for each expand/generate/reject/goal/mark
                    event, for live tracing or visualization. Default is none (no-op). Every event
                    is stamped with 'restart_index' since hill climbing has no shared frontier and
                    each restart attempt is otherwise indistinguishable in the trace.
    :return: A tuple containing the solution.
    """
    if heuristic is None:
        heuristic = lambda state: 0

    def hill_climbing(restart_index=0, start_state=None):
        start_time = time.time()
        current_state = problem.initial_state() if start_state is None else start_state
        visited = set()
        path = [current_state]
        inferences = 0

        while not problem.goal_check(current_state):
            visited.add(current_state)

            if on_step:
                on_step({'type': 'expand', 'state': current_state, 'h': heuristic(current_state), 'restart_index': restart_index})

            best_successor = None
            best_heuristic = float('inf')

            for operator in problem.operators():
                successor = problem.apply_operator(operator, current_state)
                if successor is not None:
                    heuristic_value = heuristic(successor)
                    if on_step:
                        on_step({'type': 'generate', 'from_state': current_state, 'to_state': successor, 'operator_name': getattr(operator, '__name__', None), 'h': heuristic_value, 'restart_index': restart_index})
                    if heuristic_value < best_heuristic:
                        best_successor = successor
                        best_heuristic = heuristic_value
                elif on_step:
                    on_step({'type': 'reject', 'from_state': current_state, 'to_state': successor, 'reason': 'invalid', 'restart_index': restart_index})

            inferences += 1

            if best_successor is None or best_heuristic >= heuristic(current_state):
                if on_step:
                    on_step({'type': 'mark', 'kind': 'stuck', 'state': current_state, 'restart_index': restart_index})
                break

            current_state = best_successor
            path.append(current_state)

        if on_step and problem.goal_check(current_state):
            on_step({'type': 'goal', 'state': current_state, 'path_length': len(path), 'restart_index': restart_index})

        elapsed_time = time.time() - start_time
        path_cost = sum(problem.cost(path[i], path[i + 1]) for i in range(len(path) - 1))
        # Whether this climb actually ARRIVED, as opposed to stalling on a local
        # optimum. The loop exits on both, so the path alone cannot tell them
        # apart, and treating a stalled climb's partial path as a solution is
        # exactly the mistake this return value exists to prevent.
        reached_goal = problem.goal_check(current_state)

        # Always return raw values; outer function handles statistics wrapping
        return path, visited, elapsed_time, inferences, path_cost, reached_goal

    best_solution = None
    best_visited = None
    best_cost = float("inf")
    best_found = False
    have_attempt = False
    total_inferences = 0
    total_elapsed = 0.0

    # Restarting only means something if it can start somewhere new, which
    # requires the problem's cooperation: StateSpaceProblem has no notion of a
    # random state, so every restart began from initial_state() and re-ran the
    # identical deterministic climb. Asking for 10 restarts did the same search
    # 10 times. A problem can now opt in by defining random_state(); it is
    # duck-typed rather than added to the ABC so existing problems keep working
    # untouched. The first attempt always starts from initial_state() so a
    # single-attempt search stays predictable.
    random_state_fn = getattr(problem, 'random_state', None)
    attempts = num_restarts if random_restart else 1

    for i in range(attempts):
        if random_restart and on_step:
            on_step({'type': 'mark', 'kind': 'restart-begin', 'restart_index': i})

        start_state = random_state_fn() if (i > 0 and callable(random_state_fn)) else None
        path, vis, elapsed, inf, cost, found = hill_climbing(restart_index=i, start_state=start_state)

        total_inferences += inf
        total_elapsed += elapsed

        if random_restart and on_step:
            on_step({'type': 'mark', 'kind': 'restart-end', 'restart_index': i, 'cost': cost, 'goal_reached': found})

        # An attempt that reached the goal always beats one that did not.
        # Comparing on cost alone inverted this: a climb that stalled
        # immediately has a partial path of cost 0, which beat every genuine
        # solution, so random_restart reliably selected the WORST attempt.
        if not have_attempt:
            take = True
        elif found != best_found:
            take = found
        else:
            take = cost < best_cost
        if take:
            best_solution, best_visited, best_cost, best_found = path, vis, cost, found
            have_attempt = True

    if statistics:
        # Totals across every attempt, not just the winning one: with restarts
        # the algorithm really did perform all of that work, and reporting only
        # the best attempt's cost understated it by up to num_restarts times.
        return (
            {'path': best_solution if best_found else None},
            {'visited': best_visited},
            {
                'time': total_elapsed,
                'inferences': total_inferences,
                'cost': int(best_cost) if best_found else None,
            },
        )
    else:
        return best_solution if best_found else None