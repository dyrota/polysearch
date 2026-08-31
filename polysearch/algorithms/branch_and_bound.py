from ..interfaces.state_space_problem import StateSpaceProblem
from ..data_structures.priority_queue import PriorityQueue
import time

def branch_and_bound_search(problem: StateSpaceProblem, statistics=False, on_step=None):
    """
    Branch and Bound search algorithm.

    :param problem: An object representing the problem to be solved, which
                    must be inherited from the StateSpaceProblem interface.
    :param statistics: An optional function to return the 'time', 'inferences', and 'cost'. Default is false.
    :param on_step: Optional callback invoked with a dict for each expand/generate/reject/goal-candidate
                    event, for live tracing or visualization. Default is none (no-op). Note: 'reject' events
                    with reason='bound-exceeded' are the defining behavior of this algorithm (pruning
                    successors that can't beat the current best) and are emitted specifically for that.
    :return: A tuple containing the solution.
    """
    start_time = time.time()
    visited = set()
    priority_queue = PriorityQueue()
    initial_state = problem.initial_state()
    priority_queue.push((initial_state, []), 0)
    inferences = 0
    frontier_size = 1
    best_solution = None
    best_cost = float("inf")

    while not priority_queue.is_empty():
        accumulated_cost, (state, path) = priority_queue.pop()
        inferences += 1
        frontier_size -= 1

        if on_step:
            on_step({'type': 'expand', 'state': state, 'g': accumulated_cost, 'frontier_size': frontier_size, 'inferences': inferences})

        if problem.goal_check(state):
            improved = accumulated_cost < best_cost
            if on_step:
                on_step({'type': 'goal-candidate', 'state': state, 'cost': accumulated_cost, 'improved': improved})
            if improved:
                best_solution = path + [state]
                best_cost = accumulated_cost
                continue

        if state in visited:
            continue

        visited.add(state)

        for operator in problem.operators():
            successor = problem.apply_operator(operator, state)
            if successor is not None and successor not in visited:
                current_cost = problem.cost(state, successor)
                new_accumulated_cost = accumulated_cost + current_cost
                if new_accumulated_cost < best_cost:
                    if on_step:
                        on_step({'type': 'generate', 'from_state': state, 'to_state': successor, 'operator_name': getattr(operator, '__name__', None), 'g': new_accumulated_cost})
                    priority_queue.push((successor, path + [state]), new_accumulated_cost)
                    frontier_size += 1
                elif on_step:
                    on_step({'type': 'reject', 'from_state': state, 'to_state': successor, 'reason': 'bound-exceeded'})
            elif on_step:
                on_step({'type': 'reject', 'from_state': state, 'to_state': successor, 'reason': 'invalid' if successor is None else 'visited'})

    elapsed_time = time.time() - start_time
    full_path = best_solution
    if statistics:
        return {'path': full_path}, {'visited': visited}, {'time': elapsed_time, 'inferences': inferences, 'cost': best_cost} # Cost can be inf
    else:
        return full_path