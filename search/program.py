# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part A: Single Player Freckers
from .stable_pq import StablePriorityQueue
from .core import CellState, Coord, Direction, MoveAction
from .utils import render_board
from .ai_utils import *

DIR_ACTIONS = [Direction.Down, Direction.Right, Direction.Left, Direction.DownLeft, Direction.DownRight]

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
    init_node = Node(State(board, None), None, None, [])
    priority_queue = StablePriorityQueue()
    queuing_fn_BestFS(priority_queue, init_node)
    # queuing_fn_BreadthFS(priority_queue, init_node)

    while True:
        if priority_queue.empty():
            # no more possible states
            return None

        next_node = priority_queue.get()

        if next_node.goal_test():
            return next_node.get_path(True)

        for dir in DIR_ACTIONS:
            new_node = apply_action(dir, next_node)

            if (new_node is not None):
                # print(new_node)
                # multiple_jumps_node = []

                # if (new_node.is_jump):
                #     multiple_jumps_node = expand_node_jump(new_node)

                next_node.add_children(new_node)
                queuing_fn_BestFS(priority_queue, new_node)
                # queuing_fn_BreadthFS(priority_queue, new_node)

                # for node in multiple_jumps_node:
                #     next_node.add_children(node)
                #     queuing_fn_BreadthFS(priority_queue, node)
                
                # queuing_fn_BreadthFS(priority_queue, new_node)


def expand_node_jump(node, multiple_jumps = []):

    for dir in DIR_ACTIONS:
        new_node = apply_action(dir, node)

        # Only allow multiple jumps
        if (new_node is not None and new_node.is_jump):
            # Merge two nodes
            new_node.action = MoveAction(node.action.coord, node.action.directions + new_node.action.directions)
            new_node.parent = node.parent
            new_node.cost_so_far = node.cost_so_far

            multiple_jumps.append(new_node)
            expand_node_jump(new_node, multiple_jumps)
        
    return multiple_jumps

def queuing_fn_BreadthFS(queue: StablePriorityQueue, node: Node) -> None:
    node.est_total_cost = node.cost_so_far
    queue.put(node)

def queuing_fn_BestFS(queue: StablePriorityQueue, node: Node) -> None:
    if node.est_total_cost is not None:
        queue.put(node)