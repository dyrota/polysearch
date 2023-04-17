from interfaces.state_space_problem import StateSpaceProblem
from data_structures.stack import Stack
import time

def depth_first_search(problem: StateSpaceProblem, statistics=False):
    """
    Depth first search algorithm.

    :param problem: An object representing the problem to be solved, which
                    must inherit from the StateSpaceProblem interface.
    :param statistics: An optional function to return the 'time' and 'inferences'. Default is false.
    :return: A tuple containing the solution.
    """
    start_time = time.time()
    visited = set()
    stack = Stack()
    stack.push((problem.initial_state(), []))
    inferences = 0

    while not stack.is_empty():
        state, path = stack.pop()
        inferences += 1

        if problem.goal_check(state):
            elapsed_time = time.time() - start_time
            full_path = path + [state]
            path_cost = sum(problem.cost(full_path[i], full_path[i + 1]) for i in range(len(full_path) - 1))
            if statistics:
                return full_path, {'time': elapsed_time, 'inferences': inferences, 'cost': int(path_cost)}
            else:
                return full_path

        if state in visited:
            continue

        visited.add(state)

        for operator in problem.operators():
            successor = problem.apply_operator(operator, state)
            if successor is not None and successor not in visited:
                stack.push((successor, path + [state]))

    if statistics:
        elapsed_time = time.time() - start_time
        return None, {'time': elapsed_time, 'inferences': inferences}
    else:
        return None