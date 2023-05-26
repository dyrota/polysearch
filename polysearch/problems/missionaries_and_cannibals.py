from interfaces.state_space_problem import StateSpaceProblem

class MissionariesAndCannibalsProblem(StateSpaceProblem):
    def __init__(self):
        self._initial_state = (3, 3, 1) # Privately defines representation "missionaries, cannibals, boat_position"
        self._goal_state = (0, 0, 0)

    def initial_state(self):
        return self._initial_state

    def goal_check(self, state):
        return state == self._goal_state

    def operators(self):
        return [self.move_1m, self.move_1c, self.move_2m, self.move_2c, self.move_1m_1c]

    def apply_operator(self, operator, state):
        new_state = operator(state)
        if self.is_valid_state(new_state):
            return new_state
        return None

    def cost(self, state1, state2):
        return 1

    def solution(self, state):
        return state

    def move_1m(self, state):
        missionaries, cannibals, boat_position = state
        if boat_position == 1:
            return missionaries - 1, cannibals, 0
        else:
            return missionaries + 1, cannibals, 1

    def move_1c(self, state):
        missionaries, cannibals, boat_position = state
        if boat_position == 1:
            return missionaries, cannibals - 1, 0
        else:
            return missionaries, cannibals + 1, 1

    def move_2m(self, state):
        missionaries, cannibals, boat_position = state
        if boat_position == 1:
            return missionaries - 2, cannibals, 0
        else:
            return missionaries + 2, cannibals, 1

    def move_2c(self, state):
        missionaries, cannibals, boat_position = state
        if boat_position == 1:
            return missionaries, cannibals - 2, 0
        else:
            return missionaries, cannibals + 2, 1

    def move_1m_1c(self, state):
        missionaries, cannibals, boat_position = state
        if boat_position == 1:
            return missionaries - 1, cannibals - 1, 0
        else:
            return missionaries + 1, cannibals + 1, 1

    def is_valid_state(self, state):
        missionaries, cannibals, _ = state

        if not (0 <= missionaries <= 3 and 0 <= cannibals <= 3):
            return False

        if missionaries != 0 and missionaries < cannibals:
            return False

        if missionaries != 3 and (3 - missionaries) < (3 - cannibals):
            return False

        return True

    def trips_heuristic(self, state):
        missionaries, cannibals, boat_position = state

        if boat_position == 0:
            missionaries += 1
            cannibals += 1

        total_people = missionaries + cannibals

        trips = (total_people + 1) // 2 - 1 # Estimates the number of boat trips needed
        return trips
