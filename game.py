from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import numpy as np
from typing import Optional, Tuple
from constants import GRID_SIZE, CELL_SIZE, GAP_SIZE, WIDTH, HEIGHT, BACKGROUND_COLOR, TEXT_COLOR, CELL_COLOR

class Game:
    def __init__(self) -> None:
        """
        Initialize the game with a score, move counter, and starting grid configuration.
        """
        self.score = 0
        self.moves = 0
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.grid[GRID_SIZE-1, GRID_SIZE-1] = 2
        self.resetgame()
    
    def score_function(self, grid: np.ndarray) -> int:
        """
        Calculate the score based on the highest tile and the number of empty cells.
        
        Args:
            grid (np.ndarray): The current game grid.
        
        Returns:
            int: The calculated score.
        """
        empty_cells = np.sum(grid == 0)  # Count empty tiles
        max_tile = np.max(grid)  # Highest tile
        return max_tile + empty_cells * 10  # Reward empty spaces

    def resetgame(self) -> None:
        """
        Reset the game by clearing the grid, resetting the score and move counter.
        """
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.grid[GRID_SIZE-1, GRID_SIZE-1] = 2
        self.moves = 0
        self.score = 0

    def get_tile_spawn_probabilities(self, grid: np.ndarray) -> list[tuple[int, float]]:
        """
        Get the probabilities of spawning different tile values.
        
        Args:
            grid (np.ndarray): The current game grid.
        
        Returns:
            list[tuple[int, float]]: A list of tuples containing tile values and their spawn probabilities.
        """
        return [(2, 0.9), (4, 0.1)]

    def add_tile(self) -> None:
        """
        Add a new tile (2 or 4) to a random empty cell based on predefined probabilities.
        """
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r, c] == 0]
        
        if empty_cells:
            r, c = empty_cells[np.random.randint(len(empty_cells))]
            
            # Get the tile spawn probabilities based on the current score
            tile_probabilities = self.get_tile_spawn_probabilities(self.grid)
            
            # Choose a random number between 0 and 1 and use it to select a tile based on probabilities
            rand = np.random.random()
            cumulative_prob = 0.0
            
            for tile_value, probability in tile_probabilities:
                cumulative_prob += probability
                if rand < cumulative_prob:
                    self.grid[r, c] = tile_value
                    break

    def slide_and_merge(self, row: list[int]) -> np.ndarray:
        """
        Perform the slide and merge operation on a single row.
        
        Args:
            row (list[int]): A list representing a row of the grid.
        
        Returns:
            np.ndarray: The processed row after sliding and merging.
        """

        # Convert the row to a NumPy array
        row = np.array(row, dtype=np.int16)
        
        # Remove zeros by using boolean indexing
        non_zero = row[row != 0]
        
        # Initialize an empty list to store the merged row
        new_row = []
        i = 0
        
        while i < len(non_zero):
            if i < len(non_zero) - 1 and non_zero[i] == non_zero[i + 1]:
                # Merge the tiles and append to new_row
                new_row.append(non_zero[i] * 2)
                i += 2  # Skip the next tile since it's merged
            else:
                # Otherwise just append the current tile
                new_row.append(non_zero[i])
                i += 1

        # Return the new row filled with zeros to match GRID_SIZE
        return np.pad(new_row, (0, len(row) - len(new_row)), mode='constant').astype(np.int16)

    def move(self, direction: str) -> None:
        """
        Move tiles in the given direction, merge tiles where possible, and add a new tile.
        
        Args:
            direction (str): The direction of the move ('left', 'right', 'up', 'down').
        """
        old_grid = self.grid.copy()
        rotations = {"left": 0, "up": 1, "right": 2, "down": 3}
        
        if direction in rotations:
            self.grid = np.rot90(self.grid, rotations[direction])  # Rotate to "left"
            self.grid = np.array([self.slide_and_merge(row) for row in self.grid])
            self.grid = np.rot90(self.grid, -rotations[direction])  # Rotate back

        if not np.array_equal(old_grid, self.grid):
            self.moves += 1
            self.score = self.score_function(self.grid)
            self.add_tile()

        if self.game_over():
            print("Game Over! Resetting the game.")
            self.resetgame()  # Reset the game if no moves are available
    
    def game_over(self) -> bool:
        """
        Check if the game is over, meaning no moves are left.
        
        Returns:
            bool: True if no moves are possible, otherwise False.
        """

        # Check for empty cells
        if np.any(self.grid == 0):
            return False
        
        # Check for adjacent tiles that can merge
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if r < GRID_SIZE - 1 and self.grid[r, c] == self.grid[r + 1, c]:
                    return False
                if c < GRID_SIZE - 1 and self.grid[r, c] == self.grid[r, c + 1]:
                    return False
        return True

class AI:
    """
    AI class implementing Minimax and heuristic-based decision-making for the 2048 game.
    The AI selects the best move to maximize score and survival using evaluation functions.
    """
    
    def __init__(self, game: "Game2048"):
        """
        Initializes the AI with a reference to the game instance and predefined move directions.

        Args:
            game (Game2048): The 2048 game instance.
        """
        self.game = game
        self.perfectsnake = np.array((
            [2, 2**2, 2**3, 2**4], 
            [2**8, 2**7, 2**6, 2**5], 
            [2**9, 2**10, 2**11, 2**12], 
            [2**16, 2**15, 2**14, 2**13]
        ))
        self.directions = {0: "left", 1: "up", 2: "right", 3: "down"}
        self.directions_list = ["left", "up", "right", "down"]

    def random_move(self) -> None:
        """Performs a random move by selecting a direction at random."""
        self.game.move(self.directions[np.random.randint(0,4)])

    def calc_move(self, grid: np.ndarray) -> None:
        """Calculates and executes the best move using the Minimax algorithm with a given depth."""
        best_dir = self.find_best_move(grid, depth=4)
        self.game.move(best_dir)

    def evaluate(self, grid: np.ndarray) -> float:
        """
        Heuristic evaluation function that assigns a score to a given grid state.
        
        The evaluation considers:
        - Smoothness: Penalizes rough transitions between adjacent tiles.
        - Tile arrangement: Rewards a snake-like structure for better merging potential.
        - Empty spaces: Rewards having more empty cells.
        - Merge potential: Encourages tiles that can merge.
        - Max tile placement: Penalizes if the highest tile is not in the bottom row.
        - Row sorting: Rewards if the last row is sorted in descending order.
        
        Returns:
            float: The computed heuristic score for the given grid state.
        """
        smoothness_score = -np.sum(np.abs(np.diff(grid)))  # Penalize rough transitions
        perfection = np.sum(self.perfectsnake * grid)  # Reward snake-like structure
        
        empty_cells = np.sum(grid == 0)  # Count empty spaces
        empty_score = np.square(empty_cells)  # Reward more empty tiles (small step)

        merge_score = np.sum(grid[:, :-1] == grid[:, 1:]) + np.sum(grid[:-1, :] == grid[1:, :])  
        merge_bonus = merge_score * np.max(grid)  # Weight merges more when larger numbers are involved

        # Find the max and second max tile values
        unique_values = np.sort(np.unique(grid))
        max_tile = unique_values[0]
        second_max_tile = unique_values[1] if len(unique_values) > 1 else 0

        bottom_row = grid[-1, :]  # Last row of the grid

        # Penalty if max tile is not in the bottom row
        penalty_max = -np.square(max_tile) if max_tile not in bottom_row else 0

        # Penalty if second max tile is not in the bottom row
        penalty_second_max = -np.square(second_max_tile) if second_max_tile not in bottom_row else 0

        if np.all(bottom_row[:-1] >= bottom_row[1:]):  # Checks if sorted in descending order
            sorted_bonus = np.sum(bottom_row) * 0.2  # Small reward
        else:
            sorted_bonus = 0

        return max(perfection + smoothness_score + empty_score + merge_bonus + penalty_max + penalty_second_max + sorted_bonus, 0)  # Slightly boost the heuristic
    
    def simulate_move(self, grid: np.ndarray, move: str) -> Optional[np.ndarray]:
        """
        Simulates a move without modifying the actual game state.
        
        This method applies the given move, slides and merges the tiles, 
        and returns the resulting grid.
        
        Args:
            grid (np.ndarray): The current game grid.
            move (str): The direction of the move ('left', 'up', 'right', 'down').
        
        Returns:
            np.ndarray or None: The new grid if the move is valid; otherwise, None.
        """
        temp_grid = grid.copy()
        rotations = {"left": 0, "up": 1, "right": 2, "down": 3}
        
        if move in rotations:
            temp_grid = np.rot90(temp_grid, rotations[move])
            temp_grid = np.array([self.game.slide_and_merge(row) for row in temp_grid])
            temp_grid = np.rot90(temp_grid, -rotations[move])

        if not np.array_equal(temp_grid, grid):
            return temp_grid
        return None
    
    def minimax(self, grid: np.ndarray, depth: int, maximizing_player: bool = False, alpha: float = -np.inf, beta: float = np.inf) -> float:
        """
        Minimax algorithm with alpha-beta pruning to determine the best move.
        
        If maximizing, it simulates the player's move; if minimizing, it considers random tile spawns.
        
        Args:
            grid (np.ndarray): The current game grid.
            depth (int): The search depth.
            maximizing_player (bool): True if evaluating player moves, False if evaluating AI-generated tiles.
            alpha (float): Alpha value for pruning.
            beta (float): Beta value for pruning.
        
        Returns:
            float: The evaluated score of the grid state.
        """

        if depth == 0:
            return self.evaluate(grid)
        
        if maximizing_player:
            max_evaluation = -np.inf
            for dir in self.directions.values():
                new_grid = self.simulate_move(grid, dir)
                if new_grid is not None:
                    evaluation = self.minimax(grid=new_grid, depth=depth-1, maximizing_player=False, alpha=alpha, beta=beta)
                    max_evaluation = max(max_evaluation, evaluation)
                    alpha = max(alpha, max_evaluation)
                    if beta <= alpha:
                        break
            return max_evaluation
        else:
            empty_cells = np.argwhere(grid == 0)
            if empty_cells.size == 0:
                return self.evaluate(grid)
            
            total_evaluation = 0
            tile_probabilities = self.game.get_tile_spawn_probabilities(grid=grid)
            for r, c in empty_cells:
                for tile_value, probability in tile_probabilities:
                    new_grid = grid.copy()
                    new_grid[r, c] = tile_value
                    single_eval = self.minimax(new_grid, depth - 1, True)
                    total_evaluation += probability * single_eval
                    beta = min(beta, single_eval)
                    if beta<= alpha:
                        break
            return total_evaluation / len(empty_cells)

    def find_best_move_mult(self, grid: np.ndarray, depth: int = 3) -> str:
        """
        Finds the best move using Minimax with multiprocessing.
        
        Each move is evaluated in parallel using multiple processes to speed up decision-making.
        
        Args:
            grid (np.ndarray): The current game grid.
            depth (int): The search depth for Minimax.
        
        Returns:
            str: The best move direction ('left', 'up', 'right', 'down').
        """

        best_score = -np.inf
        best_move = None
        pool = Pool(4) # 4 directions

        dirs = []

        for dir in self.directions_list:
            new_grid = self.simulate_move(grid, dir)
            if new_grid is not None:
                dirs.append((dir, new_grid))
            
        # Use multiprocessing to evaluate moves in parallel
        results = pool.starmap(self.minimax_worker, [(new_grid, depth - 1) for _, new_grid in dirs])
        pool.close()
        pool.join()

        # Find the best move based on Minimax results
        for i, (dir, _) in enumerate(dirs):
            score = results[i]
            if score > best_score:
                best_score = score
                best_move = dir

        return best_move

    def find_best_move_mult_thread(self, depth: int = 3, threads: int = 4) -> str:
        """
        Finds the best move using Minimax with multithreading.

        This method evaluates potential moves using Minimax in parallel threads.
        
        Args:
            depth (int): The search depth for Minimax.
            threads (int): Number of threads to use for evaluation.
        
        Returns:
            str: The best move direction.
        """
        best_score = -np.inf
        best_move: Optional[str] = None
        possible_moves: list[Tuple[str, np.ndarray]] = []

        # Generate valid move simulations
        for direction in self.directions_list:
            new_grid = self.simulate_move(self.game.grid, direction)
            if new_grid is not None:
                possible_moves.append((direction, new_grid))

        # Define the function for evaluating a move
        def minimax_sub_func(direction_and_grid: Tuple[str, np.ndarray]) -> Tuple[str, float]:
            direction, grid = direction_and_grid
            return direction, self.minimax(grid, depth - 1, False)

        # Execute minimax evaluations in parallel using threading
        with ThreadPool(threads) as threads:
            results = list(threads.map(minimax_sub_func, possible_moves))

        # Find the move with the highest score
        for direction, score in results:
            if score > best_score:
                best_score = score
                best_move = direction

        return best_move if best_move is not None else "left"  # Default to "left" if no valid move is found
    

    def find_best_move(self, grid: np.ndarray, depth: int = 3) -> str:
        """
        Finds the best move by running Minimax for all possible moves.
        
        Args:
            grid (np.ndarray): The current game grid.
            depth (int): The search depth for Minimax.
        
        Returns:
            str: The best move direction.
        """

        best_score = -np.inf
        best_move = None
        for dir in self.directions_list:
            new_grid = self.simulate_move(grid, dir)
            if new_grid is not None:
                score = self.minimax(new_grid, depth - 1, False)
                if score > best_score:
                    best_score = score
                    best_move = dir

        return best_move