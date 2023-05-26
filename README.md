# Polysearch

This library provides a collection of state space search algorithms designed to solve problems defined by the `StateSpaceProblem` interface. The library includes both blind and informed search algorithms, making it versatile for various problem-solving scenarios.

## Installation
You can install this software using pip:
```
pip install -U polysearch
```
You can install the latest version of the code directly from GitHub:
```
pip install -U git+https://github.com/chaseburton/polysearch@main
```

## Important Links
- Source code: https://github.com/chaseburton/polysearch
- Documentation: http://polysearch.readthedocs.org

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

## Example
```python
# algorithms
from polysearch.algorithms import *

from polysearch.algorithms import a_star_search
from polysearch.algorithms import best_first_search
from polysearch.algorithms import branch_and_bound_search
from polysearch.algorithms import breadth_first_search
from polysearch.algorithms import depth_first_search
from polysearch.algorithms import hill_climbing_search
from polysearch.algorithms import iterative_deepening_search
from polysearch.algorithms import uniform_cost_search

# existing problems
from polysearch.problems import *

from polysearch.problems.maze import MazeProblem
from polysearch.problems.missionaries_and_cannibals import MissionariesAndCannibalsProblem
from polysearch.problems.n_queens import NQueensProblem

# example problem
from your_problem import YourProblem

problem = YourProblem()
solution = a_star_search(problem, heuristic=your_heuristic_function)