# Import subpackages
from polysearch import algorithms
from polysearch import data_structures
from polysearch import interfaces
from polysearch import problems

# Import specific functions and classes for easier access
from polysearch.algorithms import (
    a_star_search,
    best_first_search,
    branch_and_bound_search,
    breadth_first_search,
    depth_first_search,
    hill_climbing_search,
    iterative_deepening_search,
    uniform_cost_search
)

from polysearch.problems import MazeProblem, MissionariesAndCannibalsProblem, NQueensProblem

# You can also import specific data structures if needed
from polysearch.data_structures import PriorityQueue, Queue, Stack

# If you want to make the StateSpaceProblem interface easily accessible
from polysearch.interfaces import StateSpaceProblem