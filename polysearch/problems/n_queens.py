from ..interfaces.state_space_problem import StateSpaceProblem

class NQueensProblem(StateSpaceProblem):
    def __init__(self, n):
        self.n = n
        self._initial_state = ()

    def initial_state(self):
        return self._initial_state

    def goal_check(self, state):
        return len(state) == self.n

    def operators(self):
        return [self.place_queen_in_row(row) for row in range(self.n)]

    def apply_operator(self, operator, state):
        col = len(state)
        if col >= self.n:
            return None

        new_state = list(state)
        new_state.append(operator(state))

        if self.is_valid_position(new_state, col):
            return tuple(new_state)
        return None

    def cost(self, state1, state2):
        return 1

    def place_queen_in_row(self, row):
        def operator(state):
            return row
        return operator

    def is_valid_position(self, state, col):
        for i in range(col):
            if state[i] == state[col] or abs(state[i] - state[col]) == abs(i - col):
                return False
        return True

    def attacking_queen_pairs_heuristic(self, state):
        attacking_pairs = 0
        for i in range(len(state)):
            for j in range(i+1, len(state)):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    attacking_pairs += 1
        return attacking_pairs