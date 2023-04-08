from interfaces.state_space_problem import StateSpaceProblem
import time

def hill_climbing_search(problem: StateSpaceProblem, heuristic=None, random_restart=False, num_restarts=10, statistics=False):
    """
    Hill climbing search algorithm.

    :param problem: An object representing the problem to be solved, which
                    must inherit from the StateSpaceProblem interface.
    :param heuristic: An optional heuristic function that takes a state as input
                      and returns an estimated cost to reach the goal.
    :param random_restart: If True, perform random restarts in case the algorithm
                           gets stuck in a local minimum. Default is False.
    :param num_restarts: The number of random restarts to perform. Default is 10.
    :param statistics: An optional function to return the 'time' and 'inferences'. Default is false.
    :return: A tuple containing the solution.
    """
    if heuristic is None:
        heuristic = lambda state: 0

    def hill_climbing():
        start_time = time.time()
        current_state = problem.initial_state()
        path = [current_state]
        inferences = 0

        while not problem.goal_check(current_state):
            best_successor = None
            best_heuristic = float('inf')

            for operator in problem.operators():
                successor = problem.apply_operator(operator, current_state)
                if successor is not None:
                    heuristic_value = heuristic(successor)
                    if heuristic_value < best_heuristic:
                        best_successor = successor
                        best_heuristic = heuristic_value

            inferences += 1

            if best_successor is None or best_heuristic >= heuristic(current_state):
                break

            current_state = best_successor
            path.append(current_state)

        elapsed_time = time.time() - start_time
        if statistics:
            return path, {'time': elapsed_time, 'inferences': inferences}
        else:
            return path

    best_solution = None
    best_cost = float("inf")

    if random_restart:
        for _ in range(num_restarts):
            solution, stats = hill_climbing()
            cost = sum(problem.cost(solution[i], solution[i + 1]) for i in range(len(solution) - 1))
            if cost < best_cost:
                best_solution, best_cost = solution, cost
                if statistics:
                    best_stats = stats
    else:
        best_solution, best_stats = hill_climbing()
        best_cost = sum(problem.cost(best_solution[i], best_solution[i + 1]) for i in range(len(best_solution) - 1))

    if statistics:
        return best_solution, best_stats
    else:
        return best_solution
