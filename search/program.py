# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part A: Single Player Freckers
from .stable_pq import StablePriorityQueue
from .core import CellState, Coord, Direction, MoveAction
from .utils import render_board
from .ai_utils import *
import time
import resource 

DIR_ACTIONS = [Direction.Down, Direction.Right, Direction.Left, Direction.DownLeft, Direction.DownRight]

def search(
    board: dict[Coord, CellState]
) -> list[MoveAction] | None:
    """
    Solve the search problem discussed in the Part A specification.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `CellState` instances which can be one of
            `CellState.RED`, `CellState.BLUE`, or `CellState.LILY_PAD`.

    Returns:
        A list of "move actions" as MoveAction instances, or `None` if no
        solution is possible.
    """
    print(render_board(board, ansi=True))

    node_count = 0 
    time_start = time.perf_counter()

    State.get_target_pos(board)
    init_node = Node(State(board, None), None, None)
    priority_queue = StablePriorityQueue()
    queuing_fn(priority_queue, init_node)

    while True:
        if priority_queue.empty():
            time_elapsed = (time.perf_counter() - time_start)
            memMb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0/1024.0
            print ("%5.5f secs %5.5f MByte" % (time_elapsed,memMb))
            print(f"Total nodes expanded: {node_count}")
            return None

        next_node = priority_queue.get()

        if next_node.goal_test():
            time_elapsed = (time.perf_counter() - time_start)
            memMb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0/1024.0
            print ("%5.5f secs %5.5f MByte" % (time_elapsed,memMb))
            print(f"Total nodes expanded: {node_count}")
            return next_node.get_path(display=False)

        for dir in DIR_ACTIONS:
            new_node = next_node.apply_action(dir)

            if new_node is not None:
                queuing_fn(priority_queue, new_node)
                node_count += 1

def queuing_fn(queue: StablePriorityQueue, node: Node) -> None:
    if node.est_total_cost is not None:
        queue.put(node)