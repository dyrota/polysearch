from interfaces.state_space_problem import StateSpaceProblem
from data_structures import PriorityQueue
import time

def a_star_search(problem: StateSpaceProblem, heuristic=None, statistics=False):
    """
    A* search algorithm.

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
    priority_queue.push((heuristic(initial_state), 0, initial_state, []))
    inferences = 0

    while not priority_queue.is_empty():
        heuristic_value, accumulated_cost, state, path = priority_queue.pop()
        path_cost = accumulated_cost + heuristic_value
        inferences += 1

        if problem.goal_check(state):
            elapsed_time = time.time() - start_time
            full_path = path + [state]
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
                current_cost = problem.cost(state, successor)
                new_accumulated_cost = accumulated_cost + current_cost
                new_heuristic_value = heuristic(successor)
                priority_queue.push((new_heuristic_value, new_accumulated_cost, successor, path + [state]))

    if statistics:
        elapsed_time = time.time() - start_time
        return None, {'time': elapsed_time, 'inferences': inferences}
    else:
        return None
