from abc import ABC, abstractmethod

class StateSpaceProblem(ABC):
    """
    StateSpaceProblem is an interface for state space search problems.
    """

    @abstractmethod
    def initial_state(self):
        """
        Returns the initial state of the problem.
        """
        pass

    @abstractmethod
    def goal_check(self, state):
        """
        Checks if the given state is a goal state. Allows for problems with multiple or unknown goal states.

        :param state: The state to check.
        :return: True if the state is a goal state, False otherwise.
        """
        pass

    @abstractmethod
    def operators(self):
        """
        Returns the list of operators applicable to the problem.

        :return: The list of operators.
        """
        pass

    @abstractmethod
    def apply_operator(self, operator, state):
        """
        Applies the given operator to the state and returns the resulting state.

        :param operator: The operator to apply.
        :param state: The state to apply the operator to.
        :return: The resulting state after applying the operator.
        """
        pass

    @abstractmethod
    def cost(self, state1, state2):
        """
        Returns the cost of transitioning from state1 to state2.

        :param state1: The starting state.
        :param state2: The ending state.
        :return: The cost of the transition.
        """
        pass

    @abstractmethod
    def solution(self, state):
        """
        Returns the solution for the problem given the goal state.

        :param state: The goal state.
        :return: The solution for the problem.
        """
        pass
