from interfaces.state_space_problem import StateSpaceProblem
import heapq
import time

def uniform_cost_search(problem: StateSpaceProblem, statistics=False):
    start_time = time.time()
    visited = set()
    priority_queue = [(0, problem.initial_state(), [])]
    inferences = 0

    while priority_queue:
        path_cost, state, path = heapq.heappop(priority_queue)
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
                cost = path_cost + problem.cost(state, successor)
                heapq.heappush(priority_queue, (cost, successor, path + [state]))

    if statistics:
        elapsed_time = time.time() - start_time
        return None, {'time': elapsed_time, 'inferences': inferences}
    else:
        return None
