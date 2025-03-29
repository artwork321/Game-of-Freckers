# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part A: Single Player Freckers
from queue import PriorityQueue
from .core import CellState, Coord, Direction, MoveAction
from .utils import render_board
from .ai_utils import *

def search(
    board: dict[Coord, CellState]
) -> list[MoveAction] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `CellState` instances which can be one of
            `CellState.RED`, `CellState.BLUE`, or `CellState.LILY_PAD`.
    
    Returns:
        A list of "move actions" as MoveAction instances, or `None` if no
        solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    print(render_board(board, ansi=True))

    # Do some impressive AI stuff here to find the solution...
    # ...
    # ... (your solution goes here!)
    # ...

    init_node = Node(State(board, None), None, None, 0, [], 1, 1, 1)
    priority_queue = PriorityQueue()
    priority_queue.put(init_node)

    DIR_ACTIONS = [Direction.Down, Direction.Right, Direction.Left, Direction.DownLeft, Direction.DownRight]
    
    while True:
        if priority_queue == []:
            # no more possible states
            return None

        next_node = priority_queue.get()

        if (goal_test(next_node)):
            return get_path(next_node)

        for dir in DIR_ACTIONS:
            new_node = apply_action(dir, next_node)

            if (new_node is not None):
                next_node.add_children(new_node)
                priority_queue.put(new_node)


    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    return [
        MoveAction(Coord(0, 5), [Direction.Down]),
        MoveAction(Coord(1, 5), [Direction.DownLeft]),
        MoveAction(Coord(3, 3), [Direction.Left]),
        MoveAction(Coord(3, 2), [Direction.Down, Direction.Right]),
        MoveAction(Coord(5, 4), [Direction.Down]),
        MoveAction(Coord(6, 4), [Direction.Down]),
    ]
