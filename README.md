# State Space Search Algorithm Library

This library provides a collection of state space search algorithms designed to solve problems defined by the `StateSpaceProblem` interface. The library includes both blind and informed search algorithms, making it versatile for various problem-solving scenarios.

## Structure

The library is structured as a package containing several search algorithms. Each algorithm utilizes a standard interface, allowing users to easily switch between algorithms when solving a problem. To demonstrate the usage of these algorithms, three example problems are provided, which can be run using `blind_search.py` and `informed_search.py`.

## Algorithms

The library includes the following algorithms:

1. A Star Search (A*)
2. Best-First Search (BestFS)
3. Branch And Bound (B&B)
4. Breadth-First Search (BFS)
5. Depth-First Search (DFS)
6. Hill Climbing (HC)
7. Iterative Deepening (ID)
8. Uniform Cost Search (UCS)

## Usage

To use the library, first, create a class for your problem that inherits from the `StateSpaceProblem` interface. This interface requires you to define the following methods:

- `initial_state()`: Returns the initial state of the problem.
- `goal_check(state)`: Checks if the given state is a goal state. Allows for problems with multiple or unknown goal states.
- `operators()`: Returns the list of operators applicable to the problem.
- `apply_operator(operator, state)`: Applies the given operator to the state and returns the resulting state.
- `cost(state1, state2)`: Returns the cost of transitioning from state1 to state2.
- `solution(state)`: Returns the solution for the problem given the goal state.

After defining your problem, you can use any of the algorithms from the library by importing the desired algorithm and passing your problem instance to it. If needed, you can also provide a heuristic function for informed search algorithms like Best-First Search and A* Search.

```python
# algorithms
from state_space_search.algorithms.a_star import a_star_search
from state_space_search.algorithms.best_first import best_first_search
from state_space_search.algorithms.branch_and_bound import branch_and_bound_search
from state_space_search.algorithms.breadth_first import breadth_first_search
from state_space_search.algorithms.depth_first import depth_first_search
from state_space_search.algorithms.hill_climbing import hill_climbing_search
from state_space_search.algorithms.iterative_deepening import iterative_deepening_search
from state_space_search.algorithms.uniform_cost import uniform_cost_search

# existing problems
from state_space_search.problems.maze import MazeProblem
from state_space_search.problems.missionaries_and_cannibals import MissionariesAndCannibalsProblem
from state_space_search.problems.n_queens import NQueensProblem

# example problem
from your_problem import YourProblem

problem = YourProblem()
solution = a_star_search(problem, heuristic=my_heuristic_function)