from interfaces.state_space_problem import StateSpaceProblem
from data_structures.priority_queue import PriorityQueue
import time

def best_first_search(problem: StateSpaceProblem, heuristic=None, statistics=False):
    """
    Best first search algorithm.

    :param problem: An object representing the problem to be solved, which
                    must inherit from the StateSpaceProblem interface.
    :param heuristic: An optional heuristic function that takes a state as input
                        and returns an estimated cost to reach the goal.
    :param statistics: An optional function to return the 'time', 'inferences', and 'cost'. Default is false.
    :return: A tuple containing the solution.
    """
    if heuristic is None:
        heuristic = lambda state: 0

    start_time = time.time()
    visited = set()
    priority_queue = PriorityQueue()
    initial_state = problem.initial_state()
    priority_queue.push((initial_state, []), heuristic(initial_state))
    inferences = 0

    while not priority_queue.is_empty():
        # _ = heuristic_value
        _, (state, path) = priority_queue.pop()
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
                priority_queue.push((successor, path + [state]), heuristic(successor))

    if statistics:
        elapsed_time = time.time() - start_time
        return None, {'time': elapsed_time, 'inferences': inferences}
    else:
        return None
