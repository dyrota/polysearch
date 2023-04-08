# from collections import deque
from interfaces.state_space_problem import StateSpaceProblem
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
    stack = [(problem.initial_state(), [])]
    inferences = 0

    while stack:
        state, path = stack.pop()
        inferences += 1

        if problem.goal_check(state):
            elapsed_time = time.time() - start_time
            if statistics:
                return path + [state], {'time': elapsed_time, 'inferences': inferences}
            else:
                return path + [state]

        if state in visited:
            continue

        visited.add(state)

        for operator in problem.operators():
            successor = problem.apply_operator(operator, state)
            if successor is not None and successor not in visited:
                stack.append((successor, path + [state]))

    if statistics:
        elapsed_time = time.time() - start_time
        return None, {'time': elapsed_time, 'inferences': inferences}
    else:
        return None