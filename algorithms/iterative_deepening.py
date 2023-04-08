from interfaces.state_space_problem import StateSpaceProblem
import time

def iterative_deepening_search(problem: StateSpaceProblem, max_depth=None, statistics=False):
    """
    Iterative deepening search algorithm.

    :param problem: An object representing the problem to be solved, which
                    must inherit from the StateSpaceProblem interface.
    :param max_depth: The maximum depth to explore in the search tree. If None (default),
                      the algorithm will continue until a solution is found or the entire tree is explored.
    :param statistics: An optional boolean flag to return the 'time', 'inferences', and 'path_cost' along with the solution.
                       Default is False.
    :return: A tuple containing the solution, total path cost of the solution, and optionally the statistics
    """
    def depth_limited_search(state, depth, path, visited):
        if state in visited or depth == 0:
            return None, None

        visited.add(state)

        if problem.goal_check(state):
            return path + [state], None

        best_solution = None

        for operator in problem.operators():
            successor_state = problem.apply_operator(operator, state)
            if successor_state is not None and successor_state not in visited:
                solution, _ = depth_limited_search(successor_state, depth - 1, path + [state], visited)
                if solution is not None:
                    best_solution = solution

        return best_solution, None

    start_time = time.time()
    inferences = 0

    if max_depth is None:
        depth = 1
        while True:
            solution, _ = depth_limited_search(problem.initial_state(), depth, [], set())
            inferences += 1

            if solution is not None:
                elapsed_time = time.time() - start_time
                path_cost = sum(problem.cost(solution[i], solution[i + 1]) for i in range(len(solution) - 1))
                if statistics:
                    return solution, {'time': elapsed_time, 'inferences': inferences, 'cost': int(path_cost)}
                else:
                    return solution

            depth += 1
    else:
        solution, _ = depth_limited_search(problem.initial_state(), max_depth, [], set())
        elapsed_time = time.time() - start_time
        if solution is not None:
            path_cost = sum(problem.cost(solution[i], solution[i + 1]) for i in range(len(solution) - 1))
        else:
            path_cost = None
        if statistics:
            return solution, {'time': elapsed_time, 'inferences': inferences, 'cost': int(path_cost) if path_cost is not None else None}
        else:
            return solution
