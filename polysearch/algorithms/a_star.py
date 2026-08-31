from ..interfaces.state_space_problem import StateSpaceProblem
from ..data_structures.priority_queue import PriorityQueue
import time

def a_star_search(problem: StateSpaceProblem, heuristic=None, statistics=False, on_step=None):
    """
    A* search algorithm.

    :param problem: An object representing the problem to be solved, which
                    must be inherited from the StateSpaceProblem interface.
    :param heuristic: An optional heuristic function that takes a state as input
                        and returns an estimated cost to reach the goal. Default is none.
    :param statistics: An optional function to return the 'time', 'inferences', and 'cost'. Default is false.
    :param on_step: Optional callback invoked with a dict for each expand/generate/reject/goal
                    event, for live tracing or visualization. Default is none (no-op).
    :return: A tuple containing the solution.
    """
    if heuristic is None:
        heuristic = lambda state: 0

    start_time = time.time()
    visited = set()
    priority_queue = PriorityQueue()
    initial_state = problem.initial_state()
    priority_queue.push((initial_state, [], 0), heuristic(initial_state))
    inferences = 0
    frontier_size = 1

    while not priority_queue.is_empty():
        # _ = accumulated_cost + heuristic value
        _, (state, path, accumulated_cost) = priority_queue.pop()
        inferences += 1
        frontier_size -= 1

        if on_step:
            h = heuristic(state)
            on_step({'type': 'expand', 'state': state, 'g': accumulated_cost, 'h': h, 'f': accumulated_cost + h, 'frontier_size': frontier_size, 'inferences': inferences})

        if problem.goal_check(state):
            elapsed_time = time.time() - start_time
            full_path = path + [state]
            if on_step:
                on_step({'type': 'goal', 'state': state, 'path_length': len(full_path), 'cost': int(accumulated_cost)})
            if statistics:
                return {'path': full_path}, {'visited': visited}, {'time': elapsed_time, 'inferences': inferences, 'cost': int(accumulated_cost)}
            else:
                return full_path

        if state in visited:
            continue

        visited.add(state)

        for operator in problem.operators():
            successor = problem.apply_operator(operator, state)
            if successor is not None and successor not in visited:
                current_cost = problem.cost(state, successor)
                new_accumulated_cost = accumulated_cost + current_cost
                new_heuristic_value = heuristic(successor)
                if on_step:
                    on_step({'type': 'generate', 'from_state': state, 'to_state': successor, 'operator_name': getattr(operator, '__name__', None), 'g': new_accumulated_cost, 'h': new_heuristic_value})
                priority_queue.push((successor, path + [state], new_accumulated_cost), new_accumulated_cost + new_heuristic_value)
                frontier_size += 1
            elif on_step:
                on_step({'type': 'reject', 'from_state': state, 'to_state': successor, 'reason': 'invalid' if successor is None else 'visited'})

    if statistics:
        elapsed_time = time.time() - start_time
        return {'path': None}, {'visited': visited}, {'time': elapsed_time, 'inferences': inferences}
    else:
        return None
