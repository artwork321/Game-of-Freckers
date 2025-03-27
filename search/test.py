import heapq
import typing

class FrogGame:
    def __init__(self, board: typing.List[typing.List[str]]):
        """
        Initialize the game board and find the initial red frog position
        
        :param board: 2D list representing the game board
        """
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.start = self._find_red_frog()
        self.goal_row = self.rows - 1
        self.blue_frog_positions = self._find_blue_frogs()

    def _find_red_frog(self) -> typing.Tuple[int, int]:
        """
        Find the initial position of the red frog
        
        :return: Coordinates of the red frog
        """
        for x in range(self.rows):
            for y in range(self.cols):
                if self.board[x][y] == 'R':
                    return (x, y)
        raise ValueError("No red frog found on the board")

    def _find_blue_frogs(self) -> typing.List[typing.Tuple[int, int]]:
        """
        Find all blue frog positions on the board
        
        :return: List of blue frog coordinates
        """
        blue_frogs = []
        for x in range(self.rows):
            for y in range(self.cols):
                if self.board[x][y] == 'B':
                    blue_frogs.append((x, y))
        return blue_frogs

    def heuristic(self, current_position: typing.Tuple[int, int]) -> float:
        """
        Calculate heuristic value for A* search
        
        :param current_position: Current position of the red frog
        :return: Estimated cost to reach the goal
        """
        # Calculate direct distance to goal
        distance_to_goal = self.goal_row - current_position[0]
        
        # Penalty for blue frogs blocking the path
        blue_frog_rows = len(set(pos[0] for pos in self.blue_frog_positions 
                                 if pos[0] > current_position[0]))
        blue_frog_penalty = min(blue_frog_rows * 2 - 1, 6)
        
        # Check for disconnected jumps
        def is_jumps_disconnected():
            # Check the 5 forward directions for potential jumps
            jump_directions = [(1, 0), (0, 1), (0, -1), (1, 1), (1, -1)]
            
            for dx, dy in jump_directions:
                mid_x = current_position[0] + dx
                mid_y = current_position[1] + dy
                jump_x = current_position[0] + 2 * dx
                jump_y = current_position[1] + 2 * dy

                if (mid_y >= 0 and mid_y < 8 and mid_x >= 0 and mid_x < 8 and self.board[mid_x][mid_y] != "B"):
                    continue
                jump_x = current_position[0] + dx
                jump_y = current_position[1] + dy
                
                # Check if the jump position is in front of another blue frog
                if (
                    0 <= jump_x < self.rows and 
                    0 <= jump_y < self.cols
                ):
                    for blue_pos in self.blue_frog_positions:
                        if jump_x > blue_pos[0]:
                            return True
            return False
        
        # Combine components of the heuristic
        disconnected_jump_penalty = 1 if is_jumps_disconnected() else 0
        
        # Final heuristic calculation
        h_value = (
            distance_to_goal - 
            blue_frog_penalty + 
            disconnected_jump_penalty
        )
        
        return max(h_value, 0)  # Ensure non-negative heuristic

    def a_star(self) -> typing.Optional[typing.List[typing.Tuple[int, int]]]:
        """
        Perform A* search to find path to goal row
        
        :return: Path to goal or None if no path exists
        """
        open_list = []
        heapq.heappush(open_list, (0, self.start))
        
        came_from = {}
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start)}
        explored_tiles = set()

        while open_list:
            current_priority, current = heapq.heappop(open_list)
            explored_tiles.add(current)
            
            # Goal reached
            if current[0] == self.goal_row:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(self.start)
                return path[::-1]
            
            # Possible move directions
            directions = [(1, -1), (1, 0), (1, 1)]
            
            for dx, dy in directions:
                # Regular move
                nx, ny = current[0] + dx, current[1] + dy
                if (0 <= nx < self.rows and 0 <= ny < self.cols and 
                    self.board[nx][ny] == '*'):
                    self._process_neighbor(current, (nx, ny), g_score, f_score, 
                                           came_from, open_list)
                
                # Jump move
                jump_x, jump_y = current[0] + 2 * dx, current[1] + 2 * dy
                mid_x, mid_y = current[0] + dx, current[1] + dy
                
                if (0 <= jump_x < self.rows and 0 <= jump_y < self.cols and
                    self.board[mid_x][mid_y] == 'B' and 
                    self.board[jump_x][jump_y] == '*'):
                    self._process_neighbor(current, (jump_x, jump_y), g_score, 
                                           f_score, came_from, open_list)

        return None

    def _process_neighbor(self, current, neighbor, g_score, f_score, 
                           came_from, open_list):
        """
        Process a neighboring tile for A* search
        
        :param current: Current position
        :param neighbor: Neighboring position to process
        :param g_score: Cost from start dict
        :param f_score: Total estimated cost dict
        :param came_from: Path tracking dict
        :param open_list: Priority queue for search
        """
        tentative_g_score = g_score[current] + 1
        
        if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = tentative_g_score + self.heuristic(neighbor)
            heapq.heappush(open_list, (f_score[neighbor], neighbor))

def main():
    # Example board
    board = [
        ['*', '*', '*', '*', '.', 'R', '*', '*'], 
        ['.', '*', '.', '.', '.', '*', '.', '*'], 
        ['.', '*', '.', '*', 'B', '*', '*', '*'], 
        ['.', '.', '*', '*', 'B', '.', 'B', '.'], 
        ['.', '.', 'B', '.', '.', '.', '*', '*'], 
        ['.', '.', '*', 'B', '*', '.', '*', '*'], 
        ['*', '*', '*', '.', '*', '.', '.', '.'], 
        ['*', '.', 'B', '*', '*', '*', '.', '.']
    ]

    # Create game instance and solve
    game = FrogGame(board)
    path = game.a_star()
    
    # Print results
    print("Initial Board:")
    for row in board:
        print(" ".join(row))
    
    print("\nPath:", path)
    
    # Visualize path on board
    if path:
        board_copy = [row.copy() for row in board]
        for x, y in path[1:]:  # Skip start position
            board_copy[x][y] = 'X'
        
        print("\nPath on Board:")
        for row in board_copy:
            print(" ".join(row))

if __name__ == "__main__":
    main()