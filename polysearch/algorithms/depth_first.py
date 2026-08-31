from ..interfaces.state_space_problem import StateSpaceProblem
from ..data_structures.stack import Stack
import time

def depth_first_search(problem: StateSpaceProblem, statistics=False, on_step=None):
    """
    Depth first search algorithm.

    :param problem: An object representing the problem to be solved, which
                    must be inherited from the StateSpaceProblem interface.
    :param statistics: An optional function to return the 'time' and 'inferences'. Default is false.
    :param on_step: Optional callback invoked with a dict for each expand/generate/reject/goal
                    event, for live tracing or visualization. Default is none (no-op).
    :return: A tuple containing the solution.
    """
    start_time = time.time()
    visited = set()
    stack = Stack()
    stack.push((problem.initial_state(), []))
    inferences = 0
    frontier_size = 1

    while not stack.is_empty():
        state, path = stack.pop()
        inferences += 1
        frontier_size -= 1

        if on_step:
            on_step({'type': 'expand', 'state': state, 'frontier_size': frontier_size, 'inferences': inferences})

        if problem.goal_check(state):
            elapsed_time = time.time() - start_time
            full_path = path + [state]
            path_cost = sum(problem.cost(full_path[i], full_path[i + 1]) for i in range(len(full_path) - 1))
            if on_step:
                on_step({'type': 'goal', 'state': state, 'path_length': len(full_path), 'cost': int(path_cost)})
            if statistics:
                return {'path': full_path}, {'visited': visited}, {'time': elapsed_time, 'inferences': inferences, 'cost': int(path_cost)}
            else:
                return full_path

        if state in visited:
            continue

        visited.add(state)

        for operator in problem.operators():
            successor = problem.apply_operator(operator, state)
            if successor is not None and successor not in visited:
                if on_step:
                    on_step({'type': 'generate', 'from_state': state, 'to_state': successor, 'operator_name': getattr(operator, '__name__', None)})
                stack.push((successor, path + [state]))
                frontier_size += 1
            elif on_step:
                on_step({'type': 'reject', 'from_state': state, 'to_state': successor, 'reason': 'invalid' if successor is None else 'visited'})

    if statistics:
        elapsed_time = time.time() - start_time
        return {'path': None}, {'visited': visited}, {'time': elapsed_time, 'inferences': inferences}
    else:
        return None