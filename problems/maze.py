from interfaces.state_space_problem import StateSpaceProblem
import math # Needed for the Euclidean heuristic

class MazeProblem(StateSpaceProblem):
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.rows = len(maze)
        self.cols = len(maze[0])

    def initial_state(self):
        return self.start

    def goal_check(self, state):
        return state == self.goal

    def operators(self):
        return [self.move_up, self.move_down, self.move_left, self.move_right]

    def apply_operator(self, operator, state):
        return operator(state)

    def cost(self, state1, state2):
        return 1

    def solution(self, state):
        return state

    def move_up(self, state):
        row, col = state
        new_row, new_col = row - 1, col
        if 0 <= new_row < self.rows and self.maze[new_row][new_col] == 0:
            return new_row, new_col
        return None

    def move_down(self, state):
        row, col = state
        new_row, new_col = row + 1, col
        if 0 <= new_row < self.rows and self.maze[new_row][new_col] == 0:
            return new_row, new_col
        return None

    def move_left(self, state):
        row, col = state
        new_row, new_col = row, col - 1
        if 0 <= new_col < self.cols and self.maze[new_row][new_col] == 0:
            return new_row, new_col
        return None

    def move_right(self, state):
        row, col = state
        new_row, new_col = row, col + 1
        if 0 <= new_col < self.cols and self.maze[new_row][new_col] == 0:
            return new_row, new_col
        return None
    
    def manhattan_distance_heuristic(self, state):
        current_row, current_col = state
        goal_row, goal_col = self.goal
        return abs(current_row - goal_row) + abs(current_col - goal_col)

    def euclidean_distance_heuristic(self, state):
            current_row, current_col = state
            goal_row, goal_col = self.goal
            return math.sqrt((current_row - goal_row)**2 + (current_col - goal_col)**2)