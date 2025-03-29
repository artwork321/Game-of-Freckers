from .core import Coord, CellState, BOARD_N, MoveAction, Direction
from .utils import render_board

# Node: contain state, parent, action, depth, children, h(n), f(n), min (f(n))
class Node:
    def __init__(self, state, parent, action : MoveAction, depth, children, hn, fn, min_fn):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.children = children
        self.hn = hn  
        self.fn = fn  
        self.min_fn = min_fn  # minimum fn so far

    
    def add_children(self, child_node):
        self.children.append(child_node)

    def __str__(self) -> str:
        return render_board(self.state.board, ansi=True)
            



# State: contain red frog position, board = dict[Coord, CellState]
class State:
    def __init__(self, board: dict[Coord, CellState], frog_coord: Coord):
        self.board = board

        if (frog_coord is None):
            for (coord, value) in board.items():
                if value == CellState.RED:
                    self.frog_coord = coord
                    break
        else:
            self.frog_coord = frog_coord



# get path: loop from the node to the parent

# apply action, check if action is valid
def apply_action(direction : Direction, node):

    current_state = node.state
    new_state = State(node.state.board.copy(), node.state.frog_coord)

    try: 
        new_coord = current_state.frog_coord + direction
    except ValueError as e:
        return None
    
    # Update state for valid move
    if (new_coord in current_state.board and current_state.board[new_coord] == CellState.BLUE): # Jump scenario
        try:
            new_coord = new_coord + direction
        except ValueError:
            return None  # Invalid jump move

    print(new_coord)
    if (new_coord in current_state.board and current_state.board[new_coord] == CellState.LILY_PAD): # Valid lily pad
        
        new_state.frog_coord = new_coord
        new_state.board[new_state.frog_coord] = CellState.RED # Move Red frog to new cell
        new_state.board.pop(current_state.frog_coord)

        hn = fn = min_fn = 1
        new_node = Node(new_state, node, MoveAction(current_state.frog_coord, direction), node.depth+1, None, hn, fn, min_fn)

        return new_node
    else:
        return None

    

# goal test