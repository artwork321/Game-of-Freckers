from .core import Vector2, Coord, CellState, BOARD_N, MoveAction, Direction
from .utils import render_board
import numpy as np

BOARD_N = 8
GOAL_ROW = 7
BEST_FS = True # Set to False for Breadth-First Search (baseline)

# Node contains state, parent, action, depth, h(n), f(n)
class Node:
    def __init__(self, state, parent, action: MoveAction, is_jump=False):
        self.state = state
        self.parent = parent
        self.action = action
        self.is_jump = is_jump
        
        if not parent:
            self.cost_so_far = 0
        # Check if this is a part of consecutive jumps
        elif parent.is_jump and is_jump:
            self.action = MoveAction(self.parent.action.coord, self.parent.action.directions + self.action.directions)
            self.cost_so_far = parent.cost_so_far
            self.parent = self.parent.parent
        else: 
            self.cost_so_far = parent.cost_so_far + 1

        self.est_cost_to_goal = self._get_est_cost_to_goal()
        # Check if there are no valid targets
        if self.est_cost_to_goal is None:
            self.est_total_cost = None
        else:  
            self.est_total_cost = self.cost_so_far + self.est_cost_to_goal

    def _get_est_cost_to_goal(self): 
        # Set heuristic to 0 for Breadth-First Search
        if not BEST_FS or self.goal_test():
            return 0

        est_cost_to_goal = None 
        for coord in State.target_coords:
            # Check if the coord is reachable (on a higher row than that of the red frog)
            if coord.r >= self.state.red_frog_coord.r:
                est_distance = self._get_est_distance(coord)
                if est_cost_to_goal is None:
                    est_cost_to_goal = est_distance
                elif est_distance < est_cost_to_goal:
                    est_cost_to_goal = est_distance

        return est_cost_to_goal

    def _get_est_distance(self, target: Coord):
        verti_dist = abs(target.r - self.state.red_frog_coord.r)
        horiz_dist = abs(target.c - self.state.red_frog_coord.c)
        n_diag_moves = min(verti_dist, horiz_dist)

        return verti_dist + horiz_dist - n_diag_moves

    # Evaluate whether the given node satisfies the goal of the problem
    def goal_test(self):
        return self.state.red_frog_coord.r == GOAL_ROW
    
    # Apply action, check if action is valid
    def apply_action(self, direction: Direction):
        current_state = self.state
        new_state = State(self.state.board, self.state.red_frog_coord)
        is_jump = False

        try: 
            new_coord = current_state.red_frog_coord + direction
        except ValueError as e:
            return None
        
        # Update state for valid move
        if (new_coord in current_state.board and current_state.board[new_coord] == CellState.BLUE): # Can jump
            try:
                new_coord = new_coord + direction
                is_jump = True
            except ValueError:
                return None  # Invalid jump move

        if (new_coord in current_state.board and current_state.board[new_coord] == CellState.LILY_PAD): # Valid lily pad
            
            new_state.red_frog_coord = new_coord
            new_state.board[new_state.red_frog_coord] = CellState.RED # Move Red frog to new cell
            new_state.board.pop(current_state.red_frog_coord)

            new_node = Node(new_state, self, MoveAction(current_state.red_frog_coord, direction), is_jump)

            return new_node
        else:
            return None

    #  Return the sequence of actions that generated the given the node
    def get_path(self, display=False):
        path = []
        nodes_along_path = []

        next_node = self
        while next_node.parent:
            nodes_along_path.insert(0, next_node)
            path.insert(0, next_node.action)
            next_node = next_node.parent

        if display:
            for node in nodes_along_path:
                print(node)

        return path

    def __str__(self) -> str:
        return render_board(self.state.board, ansi=True)     


# State contains red frog position, board = dict[Coord, CellState]
class State:
    # Cached coordinates of blue frogs and final-row lily pads
    # for heuristic calculations. These remain constant until
    # the red frog reaches the goal.
    target_coords = []

    def __init__(self, board: dict[Coord, CellState], red_frog_coord: Coord):
        self.board = board.copy()

        if red_frog_coord is None:
            for (coord, cell_state) in board.items():
                if cell_state == CellState.RED:
                    self.red_frog_coord = Coord(coord.r, coord.c)
                    break
        else:
            self.red_frog_coord = Coord(red_frog_coord.r, red_frog_coord.c)

    @classmethod
    def get_target_pos(cls, board: dict[Coord, CellState]):
        if BEST_FS:
            for (coord, cell_state) in board.items():
                if cell_state == CellState.BLUE: 
                    cls.target_coords.append(coord)
                elif coord.r == GOAL_ROW and cell_state == CellState.LILY_PAD:
                    cls.target_coords.append(coord)
