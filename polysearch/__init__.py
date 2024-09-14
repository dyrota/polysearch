from . import algorithms
from . import problems
from . import interfaces
from . import data_structures

# You might also want to import specific functions for easier access
from .algorithms import (
    a_star_search,
    best_first_search,
    branch_and_bound_search,
    breadth_first_search,
    depth_first_search,
    hill_climbing_search,
    iterative_deepening_search,
    uniform_cost_search
)

from .problems import MazeProblem, MissionariesAndCannibalsProblem, NQueensProblem