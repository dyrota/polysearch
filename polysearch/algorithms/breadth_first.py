from ..interfaces.state_space_problem import StateSpaceProblem
from ..data_structures.queue import Queue
import time

def breadth_first_search(problem: StateSpaceProblem, statistics=False):
    """
    Breadth-first search algorithm.

    :param problem: An object representing the problem to be solved, which
                    must be inherited from the StateSpaceProblem interface.
    :param statistics: An optional function to return the 'time' and 'inferences'. Default is false.
    :return: A tuple containing the solution.
    """
    start_time = time.time()
    visited = set()
    queue = Queue()
    queue.enqueue((problem.initial_state(), []))
    inferences = 0

    while not queue.is_empty():
        state, path = queue.dequeue()
        inferences += 1

        if problem.goal_check(state):
            elapsed_time = time.time() - start_time
            full_path = path + [state]
            path_cost = sum(problem.cost(full_path[i], full_path[i + 1]) for i in range(len(full_path) - 1))
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
                queue.enqueue((successor, path + [state]))

    if statistics:
        elapsed_time = time.time() - start_time
        return {'path': None}, {'visited': visited}, {'time': elapsed_time, 'inferences': inferences}
    else:
        return None