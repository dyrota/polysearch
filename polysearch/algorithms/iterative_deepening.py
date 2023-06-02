from ..interfaces.state_space_problem import StateSpaceProblem
import time

def iterative_deepening_search(problem: StateSpaceProblem, max_depth=None, statistics=False):
    """
    Iterative deepening search algorithm.

    :param problem: An object representing the problem to be solved, which
                    must be inherited from the StateSpaceProblem interface.
    :param max_depth: The maximum depth to explore in the search tree. If None (default),
                      the algorithm will continue until a solution is found or the entire tree is explored.
    :param statistics: An optional boolean flag to return the 'time', 'inferences', and 'path_cost' along with the solution.
                       Default is False.
    :return: A tuple containing the solution, total path cost of the solution, and optionally the statistics
    """
    def depth_limited_search(state, depth, path, visited):
        if state in visited or depth == 0:
            return None, visited

        visited.add(state)

        if problem.goal_check(state):
            return path + [state], visited

        best_solution = None
        best_visited = visited

        for operator in problem.operators():
            successor_state = problem.apply_operator(operator, state)
            if successor_state is not None and successor_state not in visited:
                solution, visited_in_successor = depth_limited_search(successor_state, depth - 1, path + [state], visited)
                if solution is not None:
                    best_solution = solution
                    best_visited = visited_in_successor

        return best_solution, best_visited

    start_time = time.time()
    inferences = 0

    if max_depth is None:
        depth = 1
        while True:
            solution, visited = depth_limited_search(problem.initial_state(), depth, [], set())
            inferences += 1

            if solution is not None:
                elapsed_time = time.time() - start_time
                if statistics:
                    path_cost = sum(problem.cost(solution[i], solution[i + 1]) for i in range(len(solution) - 1))
                    return {'path': solution}, {'visited': visited}, {'time': elapsed_time, 'inferences': inferences, 'cost': int(path_cost)}
                else:
                    return solution

            depth += 1
    else:
        solution, visited = depth_limited_search(problem.initial_state(), max_depth, [], set())
        elapsed_time = time.time() - start_time
        if solution is not None:
            if statistics:
                path_cost = sum(problem.cost(solution[i], solution[i + 1]) for i in range(len(solution) - 1))
                return {'path': solution}, {'visited': visited}, {'time': elapsed_time, 'inferences': inferences, 'cost': int(path_cost)}
            else:
                return solution
        else:
            return None
